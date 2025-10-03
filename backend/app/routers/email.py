"""
Email Integration API Routes

Endpoints for email-based file uploads and monitoring.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.auth_utils import get_current_user
from email_integration.email_processor import get_email_processor

router = APIRouter(prefix="/api/email", tags=["email"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class EmailConfig(BaseModel):
    """Email configuration."""
    email_address: EmailStr
    imap_server: str = "imap.gmail.com"
    imap_port: int = 993
    watched_folder: str = "INBOX"
    allowed_senders: Optional[List[EmailStr]] = None


class EmailAttachment(BaseModel):
    """Email attachment metadata."""
    filename: str
    saved_as: str
    filepath: str
    size: int
    project_id: Optional[str] = None
    message_id: str
    received_at: str


class EmailStatistics(BaseModel):
    """Email processing statistics."""
    total_processed: int
    total_files: int


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/check", response_model=List[EmailAttachment])
async def check_emails(
    user: dict = Depends(get_current_user)
):
    """
    Check email inbox for new files.

    Connects to the configured email account and:
    1. Searches for unread emails
    2. Downloads attachments (PDF, Excel, images)
    3. Automatically detects project ID from subject/body
    4. Saves files to upload directory

    Returns list of processed attachments.

    **Project ID Detection**:
    - Subject: "Invoice - Project Q4_2024" → Q4_2024
    - Subject: "[Q4_2024] Report" → Q4_2024
    - Body: "Project: Q4_2024" → Q4_2024

    **Supported File Types**:
    - PDF (.pdf)
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    - Images (.png, .jpg, .jpeg)
    """

    processor = get_email_processor()

    if not processor:
        raise HTTPException(
            status_code=503,
            detail="Email integration not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables."
        )

    try:
        attachments = processor.check_emails()

        return [EmailAttachment(**att) for att in attachments]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check emails: {str(e)}"
        )


@router.get("/statistics", response_model=EmailStatistics)
async def get_email_statistics(
    user: dict = Depends(get_current_user)
):
    """
    Get email processing statistics.

    Returns:
    - Total emails processed
    - Total files downloaded
    """

    processor = get_email_processor()

    if not processor:
        raise HTTPException(
            status_code=503,
            detail="Email integration not configured"
        )

    stats = processor.get_statistics()

    return EmailStatistics(**stats)


@router.get("/status")
async def email_integration_status(
    user: dict = Depends(get_current_user)
):
    """
    Check if email integration is configured and operational.

    Returns:
    - configured: Whether email credentials are set
    - email_address: Configured email (if available)
    - imap_server: IMAP server address
    """

    processor = get_email_processor()

    if not processor:
        return {
            "configured": False,
            "email_address": None,
            "imap_server": None,
            "message": "Email integration not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables."
        }

    return {
        "configured": True,
        "email_address": processor.email_address,
        "imap_server": processor.imap_server,
        "watched_folder": processor.watched_folder,
        "message": "Email integration active"
    }


@router.get("/health")
async def email_health():
    """
    Health check for email integration service.
    """

    processor = get_email_processor()

    return {
        "status": "healthy" if processor else "unconfigured",
        "service": "email_integration",
        "configured": processor is not None
    }
