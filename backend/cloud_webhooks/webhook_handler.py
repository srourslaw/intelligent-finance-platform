"""
Cloud Storage Webhook Handler

Handles webhooks from cloud storage providers (Dropbox, Google Drive, OneDrive)
for automated file synchronization.
"""

import os
import json
import hmac
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Webhook handler for cloud storage providers.

    Supports:
    - Dropbox webhooks
    - Google Drive push notifications
    - OneDrive webhooks
    """

    def __init__(self):
        """Initialize webhook handler."""
        self.webhook_dir = Path("data/webhooks")
        self.webhook_dir.mkdir(parents=True, exist_ok=True)

        self.events_file = self.webhook_dir / "webhook_events.json"
        self.events: List[Dict[str, Any]] = self._load_events()

        # Load secrets from environment
        self.dropbox_secret = os.getenv('DROPBOX_WEBHOOK_SECRET')
        self.google_secret = os.getenv('GOOGLE_WEBHOOK_SECRET')
        self.onedrive_secret = os.getenv('ONEDRIVE_WEBHOOK_SECRET')

    def _load_events(self) -> List[Dict[str, Any]]:
        """Load webhook events history."""
        if self.events_file.exists():
            try:
                with self.events_file.open('r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load webhook events: {e}")
        return []

    def _save_events(self):
        """Save webhook events history."""
        try:
            # Keep only last 1000 events
            if len(self.events) > 1000:
                self.events = self.events[-1000:]

            with self.events_file.open('w') as f:
                json.dump(self.events, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save webhook events: {e}")

    def _record_event(self, provider: str, event_type: str, data: Dict[str, Any]):
        """Record webhook event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "event_type": event_type,
            "data": data
        }
        self.events.append(event)
        self._save_events()

    # ========================================================================
    # DROPBOX WEBHOOKS
    # ========================================================================

    def verify_dropbox_signature(self, signature: str, body: bytes) -> bool:
        """
        Verify Dropbox webhook signature.

        Args:
            signature: X-Dropbox-Signature header
            body: Raw request body

        Returns:
            True if signature is valid
        """
        if not self.dropbox_secret:
            logger.warning("Dropbox webhook secret not configured")
            return False

        expected_signature = hmac.new(
            self.dropbox_secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def handle_dropbox_webhook(
        self,
        signature: str,
        body: bytes,
        json_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle Dropbox webhook.

        Dropbox sends list of user IDs with changes.
        We need to call /files/list_folder/continue to get actual changes.

        Args:
            signature: X-Dropbox-Signature header
            body: Raw request body
            json_data: Parsed JSON data

        Returns:
            Response data
        """
        # Verify signature
        if not self.verify_dropbox_signature(signature, body):
            raise ValueError("Invalid Dropbox signature")

        # Extract user accounts with changes
        accounts = json_data.get('list_folder', {}).get('accounts', [])

        logger.info(f"📦 Dropbox webhook: {len(accounts)} account(s) with changes")

        self._record_event('dropbox', 'file_change', {
            'accounts': accounts,
            'account_count': len(accounts)
        })

        return {
            "status": "received",
            "provider": "dropbox",
            "accounts": accounts
        }

    # ========================================================================
    # GOOGLE DRIVE WEBHOOKS
    # ========================================================================

    def handle_google_drive_webhook(
        self,
        channel_id: str,
        resource_id: str,
        resource_state: str,
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Handle Google Drive push notification.

        Google Drive sends notifications via watch channels.

        Args:
            channel_id: X-Goog-Channel-ID header
            resource_id: X-Goog-Resource-ID header
            resource_state: X-Goog-Resource-State header (sync, add, remove, update, trash, untrash, change)
            headers: All request headers

        Returns:
            Response data
        """
        logger.info(f"📁 Google Drive webhook: {resource_state} on channel {channel_id}")

        # Check if notification should be processed
        if resource_state == 'sync':
            # Initial sync notification, acknowledge but don't process
            return {"status": "sync_acknowledged"}

        self._record_event('google_drive', resource_state, {
            'channel_id': channel_id,
            'resource_id': resource_id,
            'resource_state': resource_state
        })

        return {
            "status": "received",
            "provider": "google_drive",
            "channel_id": channel_id,
            "resource_state": resource_state
        }

    # ========================================================================
    # ONEDRIVE WEBHOOKS
    # ========================================================================

    def verify_onedrive_signature(self, validation_token: Optional[str]) -> Optional[str]:
        """
        Verify OneDrive webhook validation.

        OneDrive sends a validation token on subscription creation.

        Args:
            validation_token: validationToken query parameter

        Returns:
            Validation token to echo back (or None)
        """
        if validation_token:
            logger.info(f"✅ OneDrive validation request received")
            return validation_token
        return None

    def handle_onedrive_webhook(
        self,
        json_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle OneDrive webhook notification.

        OneDrive sends notifications about file changes.

        Args:
            json_data: Parsed JSON notification

        Returns:
            Response data
        """
        # Extract notification data
        value = json_data.get('value', [])

        logger.info(f"☁️  OneDrive webhook: {len(value)} notification(s)")

        for notification in value:
            resource = notification.get('resource')
            change_type = notification.get('changeType')

            logger.info(f"  - {change_type}: {resource}")

            self._record_event('onedrive', change_type, {
                'resource': resource,
                'change_type': change_type,
                'subscription_id': notification.get('subscriptionId')
            })

        return {
            "status": "received",
            "provider": "onedrive",
            "notification_count": len(value)
        }

    # ========================================================================
    # GENERIC WEBHOOK HANDLER
    # ========================================================================

    def handle_webhook(
        self,
        provider: str,
        headers: Dict[str, str],
        body: bytes,
        json_data: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Route webhook to appropriate handler.

        Args:
            provider: Cloud provider (dropbox, google_drive, onedrive)
            headers: Request headers
            body: Raw request body
            json_data: Parsed JSON data (if applicable)
            query_params: URL query parameters

        Returns:
            Response data
        """
        if provider == 'dropbox':
            signature = headers.get('X-Dropbox-Signature', '')
            return self.handle_dropbox_webhook(signature, body, json_data or {})

        elif provider == 'google_drive':
            channel_id = headers.get('X-Goog-Channel-ID', '')
            resource_id = headers.get('X-Goog-Resource-ID', '')
            resource_state = headers.get('X-Goog-Resource-State', '')
            return self.handle_google_drive_webhook(channel_id, resource_id, resource_state, headers)

        elif provider == 'onedrive':
            # Check for validation request
            validation_token = query_params.get('validationToken') if query_params else None
            if validation_token:
                return {"validationToken": validation_token}

            return self.handle_onedrive_webhook(json_data or {})

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_events(
        self,
        provider: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get webhook events.

        Args:
            provider: Filter by provider (optional)
            limit: Maximum number of events to return

        Returns:
            List of events
        """
        events = self.events

        if provider:
            events = [e for e in events if e.get('provider') == provider]

        # Return most recent events
        return events[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Get webhook statistics."""
        stats = {
            "total_events": len(self.events),
            "by_provider": {},
            "by_event_type": {}
        }

        for event in self.events:
            provider = event.get('provider', 'unknown')
            event_type = event.get('event_type', 'unknown')

            stats['by_provider'][provider] = stats['by_provider'].get(provider, 0) + 1
            stats['by_event_type'][event_type] = stats['by_event_type'].get(event_type, 0) + 1

        return stats


# Singleton instance
_webhook_handler: Optional[WebhookHandler] = None


def get_webhook_handler() -> WebhookHandler:
    """Get or create webhook handler singleton."""
    global _webhook_handler

    if _webhook_handler is None:
        _webhook_handler = WebhookHandler()

    return _webhook_handler
