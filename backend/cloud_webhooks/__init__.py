"""Cloud storage webhook integration for automated file uploads."""

from .webhook_handler import WebhookHandler, get_webhook_handler

__all__ = ['WebhookHandler', 'get_webhook_handler']
