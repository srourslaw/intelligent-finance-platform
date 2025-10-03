"""
Cloud Storage Webhook API Routes

Endpoints for receiving webhooks from cloud storage providers.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, Request, Query, Header
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.auth_utils import get_current_user
from cloud_webhooks.webhook_handler import get_webhook_handler

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class WebhookEvent(BaseModel):
    """Webhook event."""
    timestamp: str
    provider: str
    event_type: str
    data: Dict[str, Any]


class WebhookStatistics(BaseModel):
    """Webhook statistics."""
    total_events: int
    by_provider: Dict[str, int]
    by_event_type: Dict[str, int]


# ============================================================================
# WEBHOOK RECEIVERS (No auth required for external services)
# ============================================================================

@router.post("/dropbox")
async def dropbox_webhook(
    request: Request,
    x_dropbox_signature: Optional[str] = Header(None)
):
    """
    Dropbox webhook receiver.

    Dropbox sends POST requests when files change in monitored folders.

    **Setup**:
    1. Create Dropbox app at https://www.dropbox.com/developers/apps
    2. Add webhook URL: https://your-domain.com/api/webhooks/dropbox
    3. Set DROPBOX_WEBHOOK_SECRET environment variable

    **Flow**:
    1. Dropbox sends notification with list of accounts that have changes
    2. Call Dropbox API /files/list_folder/continue to get actual changes
    3. Download new/modified files
    4. Process through extraction pipeline
    """
    handler = get_webhook_handler()

    # Get raw body for signature verification
    body = await request.body()

    # Parse JSON
    try:
        json_data = await request.json()
    except Exception:
        json_data = {}

    try:
        result = handler.handle_dropbox_webhook(
            signature=x_dropbox_signature or '',
            body=body,
            json_data=json_data
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


@router.post("/google-drive")
async def google_drive_webhook(
    request: Request,
    x_goog_channel_id: Optional[str] = Header(None),
    x_goog_resource_id: Optional[str] = Header(None),
    x_goog_resource_state: Optional[str] = Header(None)
):
    """
    Google Drive push notification receiver.

    Google Drive sends notifications via watch channels.

    **Setup**:
    1. Enable Google Drive API in Google Cloud Console
    2. Create watch channel for specific folder
    3. Set notification URL: https://your-domain.com/api/webhooks/google-drive

    **Resource States**:
    - sync: Initial channel setup
    - add: New file created
    - update: File modified
    - trash: File moved to trash
    - remove: File permanently deleted
    - change: Generic change
    """
    handler = get_webhook_handler()

    headers = dict(request.headers)

    try:
        result = handler.handle_google_drive_webhook(
            channel_id=x_goog_channel_id or '',
            resource_id=x_goog_resource_id or '',
            resource_state=x_goog_resource_state or '',
            headers=headers
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


@router.post("/onedrive")
async def onedrive_webhook(
    request: Request,
    validationToken: Optional[str] = Query(None)
):
    """
    OneDrive/SharePoint webhook receiver.

    OneDrive sends notifications when files change in monitored libraries.

    **Setup**:
    1. Register Microsoft app at https://portal.azure.com
    2. Create subscription for document library
    3. Set notification URL: https://your-domain.com/api/webhooks/onedrive

    **Validation**:
    OneDrive sends validation request with validationToken query parameter.
    Must echo back the token to confirm subscription.

    **Change Types**:
    - created: New file/folder created
    - updated: File/folder modified
    - deleted: File/folder deleted
    """
    handler = get_webhook_handler()

    # Handle validation request
    if validationToken:
        result = handler.verify_onedrive_signature(validationToken)
        if result:
            # Return plain text response with validation token
            return {"validationToken": result}

    # Parse JSON notification
    try:
        json_data = await request.json()
    except Exception:
        json_data = {}

    try:
        result = handler.handle_onedrive_webhook(json_data)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


# ============================================================================
# MANAGEMENT ENDPOINTS (Auth required)
# ============================================================================

@router.get("/events", response_model=List[WebhookEvent])
async def list_webhook_events(
    provider: Optional[str] = Query(None, description="Filter by provider (dropbox, google_drive, onedrive)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of events to return"),
    user: dict = Depends(get_current_user)
):
    """
    List webhook events.

    Returns history of received webhook notifications.
    """
    handler = get_webhook_handler()
    events = handler.get_events(provider=provider, limit=limit)

    return [WebhookEvent(**event) for event in events]


@router.get("/statistics", response_model=WebhookStatistics)
async def get_webhook_statistics(
    user: dict = Depends(get_current_user)
):
    """
    Get webhook statistics.

    Returns:
    - Total events received
    - Events by provider
    - Events by type
    """
    handler = get_webhook_handler()
    stats = handler.get_statistics()

    return WebhookStatistics(**stats)


@router.get("/health")
async def webhook_health():
    """
    Health check for webhook service.
    """
    handler = get_webhook_handler()

    return {
        "status": "healthy",
        "service": "cloud_webhooks",
        "configured_providers": {
            "dropbox": handler.dropbox_secret is not None,
            "google_drive": handler.google_secret is not None,
            "onedrive": handler.onedrive_secret is not None
        }
    }
