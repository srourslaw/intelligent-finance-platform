"""
Application Configuration and Environment Variable Validation

Validates all required environment variables on startup and provides
centralized configuration management.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Config:
    """
    Application configuration with environment variable validation.
    """

    def __init__(self):
        """Initialize configuration and validate environment variables."""
        # Core Settings
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'

        # API Keys
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.jwt_secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')

        # Email Integration
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_imap_server = os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com')
        self.email_imap_port = int(os.getenv('EMAIL_IMAP_PORT', '993'))

        # Cloud Webhooks
        self.dropbox_webhook_secret = os.getenv('DROPBOX_WEBHOOK_SECRET')
        self.google_webhook_secret = os.getenv('GOOGLE_WEBHOOK_SECRET')
        self.onedrive_webhook_secret = os.getenv('ONEDRIVE_WEBHOOK_SECRET')

        # Database (future)
        self.database_url = os.getenv('DATABASE_URL')

        # Redis (future)
        self.redis_url = os.getenv('REDIS_URL')

        # File Storage
        self.upload_dir = Path(os.getenv('UPLOAD_DIR', 'data/uploads'))
        self.extraction_dir = Path(os.getenv('EXTRACTION_DIR', 'data/extractions'))
        self.batch_job_dir = Path(os.getenv('BATCH_JOB_DIR', 'data/batch_jobs'))

        # Ensure directories exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.extraction_dir.mkdir(parents=True, exist_ok=True)
        self.batch_job_dir.mkdir(parents=True, exist_ok=True)

        # Validate configuration
        self._validate()

    def _validate(self):
        """Validate configuration and log warnings for missing optional settings."""
        issues = []
        warnings = []

        # Critical validations (will raise error)
        if not self.anthropic_api_key:
            warnings.append("ANTHROPIC_API_KEY is not set - AI features will not work")

        if self.environment == 'production' and self.jwt_secret_key == 'dev-secret-key-change-in-production':
            issues.append("JWT_SECRET_KEY must be changed in production")

        # Optional feature validations (will log warning)
        if not self.email_address or not self.email_password:
            warnings.append("Email integration not configured (EMAIL_ADDRESS/EMAIL_PASSWORD missing)")

        if not any([self.dropbox_webhook_secret, self.google_webhook_secret, self.onedrive_webhook_secret]):
            warnings.append("No cloud webhook secrets configured (all webhooks disabled)")

        if not self.database_url:
            warnings.append("DATABASE_URL not set - using file-based storage (not recommended for production)")

        if not self.redis_url:
            warnings.append("REDIS_URL not set - caching disabled")

        # Log warnings
        if warnings:
            logger.warning("⚠️  Configuration warnings:")
            for warning in warnings:
                logger.warning(f"  - {warning}")

        # Raise error if critical issues
        if issues:
            logger.error("❌ Critical configuration errors:")
            for issue in issues:
                logger.error(f"  - {issue}")
            raise ValueError("Configuration validation failed. Please check environment variables.")

        # Log success
        logger.info("✅ Configuration validated successfully")
        self._log_status()

    def _log_status(self):
        """Log configuration status."""
        logger.info("Configuration status:")
        logger.info(f"  Environment: {self.environment}")
        logger.info(f"  Debug: {self.debug}")
        logger.info(f"  Anthropic API: {'✅ Configured' if self.anthropic_api_key else '❌ Missing'}")
        logger.info(f"  Email Integration: {'✅ Configured' if self.email_address and self.email_password else '❌ Not configured'}")
        logger.info(f"  Dropbox Webhook: {'✅ Configured' if self.dropbox_webhook_secret else '❌ Not configured'}")
        logger.info(f"  Google Webhook: {'✅ Configured' if self.google_webhook_secret else '❌ Not configured'}")
        logger.info(f"  OneDrive Webhook: {'✅ Configured' if self.onedrive_webhook_secret else '❌ Not configured'}")
        logger.info(f"  Database: {'✅ Configured' if self.database_url else '⚠️  Using file storage'}")
        logger.info(f"  Redis: {'✅ Configured' if self.redis_url else '⚠️  Caching disabled'}")

    def get_status(self) -> Dict[str, Any]:
        """Get configuration status as dictionary."""
        return {
            "environment": self.environment,
            "debug": self.debug,
            "features": {
                "ai": bool(self.anthropic_api_key),
                "email": bool(self.email_address and self.email_password),
                "webhooks": {
                    "dropbox": bool(self.dropbox_webhook_secret),
                    "google_drive": bool(self.google_webhook_secret),
                    "onedrive": bool(self.onedrive_webhook_secret)
                },
                "database": bool(self.database_url),
                "caching": bool(self.redis_url)
            },
            "storage": {
                "upload_dir": str(self.upload_dir),
                "extraction_dir": str(self.extraction_dir),
                "batch_job_dir": str(self.batch_job_dir)
            }
        }


# Singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create configuration singleton."""
    global _config

    if _config is None:
        _config = Config()

    return _config


def validate_config():
    """Validate configuration on startup."""
    try:
        config = get_config()
        logger.info("✅ Application configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"❌ Configuration validation failed: {e}")
        raise
