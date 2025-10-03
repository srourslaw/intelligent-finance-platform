"""
Email Processing Service

Monitors email inbox for incoming files and automatically processes them.
Supports IMAP email providers (Gmail, Outlook, etc.)
"""

import os
import json
import email
import imaplib
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from email.header import decode_header
import logging

logger = logging.getLogger(__name__)


class EmailProcessor:
    """
    Email processor for automated file uploads.

    Monitors an email inbox and automatically downloads attachments,
    then processes them through the extraction pipeline.
    """

    def __init__(
        self,
        email_address: str,
        password: str,
        imap_server: str,
        imap_port: int = 993,
        watched_folder: str = "INBOX",
        allowed_senders: Optional[List[str]] = None
    ):
        """
        Initialize email processor.

        Args:
            email_address: Email address to monitor
            password: Email password or app-specific password
            imap_server: IMAP server address (e.g., imap.gmail.com)
            imap_port: IMAP port (default 993 for SSL)
            watched_folder: Email folder to monitor (default INBOX)
            allowed_senders: Optional list of allowed sender emails (whitelist)
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.watched_folder = watched_folder
        self.allowed_senders = allowed_senders or []

        self.upload_dir = Path("data/email_uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.upload_dir / "email_metadata.json"
        self.processed_emails: Dict[str, Any] = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata about processed emails."""
        if self.metadata_file.exists():
            try:
                with self.metadata_file.open('r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load email metadata: {e}")
        return {"processed_message_ids": [], "statistics": {"total_processed": 0, "total_files": 0}}

    def _save_metadata(self):
        """Save metadata about processed emails."""
        try:
            with self.metadata_file.open('w') as f:
                json.dump(self.processed_emails, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save email metadata: {e}")

    def connect(self) -> imaplib.IMAP4_SSL:
        """Connect to IMAP server."""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.password)
            logger.info(f"✅ Connected to {self.imap_server} as {self.email_address}")
            return mail
        except Exception as e:
            logger.error(f"❌ Failed to connect to email: {e}")
            raise

    def is_sender_allowed(self, sender: str) -> bool:
        """Check if sender is in whitelist."""
        if not self.allowed_senders:
            return True  # No whitelist = allow all

        sender_lower = sender.lower()
        return any(allowed.lower() in sender_lower for allowed in self.allowed_senders)

    def decode_email_subject(self, subject: str) -> str:
        """Decode email subject handling various encodings."""
        decoded_parts = []
        for part, encoding in decode_header(subject):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or 'utf-8', errors='ignore'))
            else:
                decoded_parts.append(part)
        return ''.join(decoded_parts)

    def extract_project_id(self, subject: str, body: str) -> Optional[str]:
        """
        Extract project ID from email subject or body.

        Looks for patterns like:
        - Subject: "Invoice - Project Q4_2024"
        - Body: "Project: Q4_2024"
        - Subject: "[Q4_2024] Weekly Report"
        """
        import re

        # Check subject first
        patterns = [
            r'Project[:\s]+([A-Za-z0-9_\-]+)',
            r'\[([A-Za-z0-9_\-]+)\]',
            r'Project_([A-Za-z0-9_\-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, subject, re.IGNORECASE)
            if match:
                return match.group(1)

        # Check body
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                return match.group(1)

        # Default project if none found
        return None

    def process_attachments(
        self,
        message_id: str,
        msg: email.message.Message,
        project_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract and save attachments from email message.

        Returns:
            List of attachment metadata
        """
        attachments = []

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if not filename:
                continue

            # Decode filename
            filename = self.decode_email_subject(filename)

            # Filter file types
            allowed_extensions = ['.pdf', '.xlsx', '.xls', '.csv', '.png', '.jpg', '.jpeg']
            if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
                logger.info(f"⏭️  Skipping unsupported file: {filename}")
                continue

            # Save attachment
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            filepath = self.upload_dir / safe_filename

            try:
                with filepath.open('wb') as f:
                    f.write(part.get_payload(decode=True))

                logger.info(f"📎 Saved attachment: {safe_filename}")

                attachments.append({
                    "filename": filename,
                    "saved_as": safe_filename,
                    "filepath": str(filepath),
                    "size": filepath.stat().st_size,
                    "project_id": project_id,
                    "message_id": message_id,
                    "received_at": timestamp
                })

            except Exception as e:
                logger.error(f"❌ Failed to save attachment {filename}: {e}")

        return attachments

    def check_emails(self) -> List[Dict[str, Any]]:
        """
        Check inbox for new emails with attachments.

        Returns:
            List of processed attachments with metadata
        """
        all_attachments = []

        try:
            mail = self.connect()
            mail.select(self.watched_folder)

            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')

            if status != 'OK':
                logger.error("Failed to search emails")
                return []

            email_ids = messages[0].split()
            logger.info(f"📧 Found {len(email_ids)} unread emails")

            for email_id in email_ids:
                try:
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')

                    if status != 'OK':
                        continue

                    # Parse email
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Get message ID
                    message_id = msg.get('Message-ID', f'unknown_{email_id.decode()}')

                    # Skip if already processed
                    if message_id in self.processed_emails.get('processed_message_ids', []):
                        logger.info(f"⏭️  Already processed: {message_id}")
                        continue

                    # Get sender
                    sender = msg.get('From', '')

                    # Check sender whitelist
                    if not self.is_sender_allowed(sender):
                        logger.warning(f"⛔ Blocked sender: {sender}")
                        continue

                    # Get subject
                    subject = self.decode_email_subject(msg.get('Subject', ''))

                    # Get body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                    else:
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

                    # Extract project ID
                    project_id = self.extract_project_id(subject, body)

                    logger.info(f"📨 Processing email: {subject} (from: {sender})")
                    if project_id:
                        logger.info(f"🎯 Detected project: {project_id}")

                    # Process attachments
                    attachments = self.process_attachments(message_id, msg, project_id)

                    if attachments:
                        all_attachments.extend(attachments)

                        # Mark as processed
                        self.processed_emails.setdefault('processed_message_ids', []).append(message_id)
                        self.processed_emails['statistics']['total_processed'] += 1
                        self.processed_emails['statistics']['total_files'] += len(attachments)

                        logger.info(f"✅ Processed {len(attachments)} attachments from email")

                except Exception as e:
                    logger.error(f"❌ Failed to process email {email_id}: {e}")

            mail.close()
            mail.logout()

            # Save metadata
            self._save_metadata()

        except Exception as e:
            logger.error(f"❌ Email check failed: {e}")

        return all_attachments

    def get_statistics(self) -> Dict[str, Any]:
        """Get email processing statistics."""
        return self.processed_emails.get('statistics', {})


# Singleton instance
_email_processor: Optional[EmailProcessor] = None


def get_email_processor(
    email_address: Optional[str] = None,
    password: Optional[str] = None,
    imap_server: Optional[str] = None,
    **kwargs
) -> Optional[EmailProcessor]:
    """
    Get or create email processor singleton.

    If credentials are not provided, reads from environment variables:
    - EMAIL_ADDRESS
    - EMAIL_PASSWORD
    - EMAIL_IMAP_SERVER
    """
    global _email_processor

    if _email_processor is None:
        # Read from environment if not provided
        email_address = email_address or os.getenv('EMAIL_ADDRESS')
        password = password or os.getenv('EMAIL_PASSWORD')
        imap_server = imap_server or os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com')

        if not all([email_address, password]):
            logger.warning("Email integration not configured (missing credentials)")
            return None

        _email_processor = EmailProcessor(
            email_address=email_address,
            password=password,
            imap_server=imap_server,
            **kwargs
        )

    return _email_processor
