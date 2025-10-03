"""
System Health and Configuration API Routes

Endpoints for system monitoring, health checks, and configuration status.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime
import psutil
import platform

from app.auth_utils import get_current_user
from app.config import get_config

router = APIRouter(prefix="/api/system", tags=["system"])


# ============================================================================
# SYSTEM HEALTH ENDPOINTS
# ============================================================================

@router.get("/health")
async def system_health():
    """
    Comprehensive system health check.

    Returns:
    - Overall system status
    - All service statuses (batch, email, webhooks)
    - System resources (CPU, memory, disk)
    """
    config = get_config()

    # Check all services
    services = {}

    # Batch scheduler
    try:
        from batch.scheduler import get_scheduler
        scheduler = get_scheduler()
        services["batch_scheduler"] = {
            "status": "running" if scheduler.scheduler.running else "stopped",
            "job_count": len(scheduler.list_jobs())
        }
    except Exception as e:
        services["batch_scheduler"] = {"status": "error", "error": str(e)}

    # Email integration
    try:
        from email_integration.email_processor import get_email_processor
        processor = get_email_processor()
        services["email_integration"] = {
            "status": "configured" if processor else "not_configured",
            "statistics": processor.get_statistics() if processor else None
        }
    except Exception as e:
        services["email_integration"] = {"status": "error", "error": str(e)}

    # Cloud webhooks
    try:
        from cloud_webhooks.webhook_handler import get_webhook_handler
        handler = get_webhook_handler()
        services["cloud_webhooks"] = {
            "status": "healthy",
            "statistics": handler.get_statistics()
        }
    except Exception as e:
        services["cloud_webhooks"] = {"status": "error", "error": str(e)}

    # System resources
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        system_resources = {
            "cpu": {
                "percent": cpu_percent,
                "count": psutil.cpu_count()
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            }
        }
    except Exception as e:
        system_resources = {"error": str(e)}

    # Overall status
    all_healthy = all(
        service.get("status") in ["running", "configured", "healthy", "not_configured"]
        for service in services.values()
    )

    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "environment": config.environment,
        "services": services,
        "system_resources": system_resources,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "python_version": platform.python_version()
        }
    }


@router.get("/config")
async def get_configuration(
    user: dict = Depends(get_current_user)
):
    """
    Get application configuration status.

    Returns configuration status without exposing secrets.
    """
    config = get_config()
    return config.get_status()


@router.get("/services")
async def list_services(
    user: dict = Depends(get_current_user)
):
    """
    List all available services and their status.

    Returns:
    - Service name
    - Status (enabled/disabled/configured)
    - Endpoints
    """
    config = get_config()

    services = {
        "batch_processing": {
            "enabled": True,
            "configured": True,
            "endpoints": [
                "/api/batch/jobs",
                "/api/batch/jobs/aggregation",
                "/api/batch/health"
            ]
        },
        "email_integration": {
            "enabled": config.features["email"],
            "configured": config.features["email"],
            "endpoints": [
                "/api/email/check",
                "/api/email/statistics",
                "/api/email/status"
            ]
        },
        "cloud_webhooks": {
            "enabled": any(config.features["webhooks"].values()),
            "configured": any(config.features["webhooks"].values()),
            "providers": config.features["webhooks"],
            "endpoints": [
                "/api/webhooks/dropbox",
                "/api/webhooks/google-drive",
                "/api/webhooks/onedrive",
                "/api/webhooks/events"
            ]
        },
        "file_extraction": {
            "enabled": config.features["ai"],
            "configured": config.features["ai"],
            "endpoints": [
                "/api/extraction/upload",
                "/api/extraction/extract",
                "/api/extraction/classify"
            ]
        },
        "aggregation": {
            "enabled": True,
            "configured": True,
            "endpoints": [
                "/api/aggregation/aggregate",
                "/api/aggregation/validate"
            ]
        },
        "financials": {
            "enabled": config.features["ai"],
            "configured": config.features["ai"],
            "endpoints": [
                "/api/financials/consolidate",
                "/api/financials/balance-sheet",
                "/api/financials/income-statement"
            ]
        }
    }

    return {
        "total_services": len(services),
        "enabled_services": len([s for s in services.values() if s["enabled"]]),
        "services": services
    }


@router.get("/metrics")
async def system_metrics(
    user: dict = Depends(get_current_user)
):
    """
    Get system performance metrics.

    Returns:
    - Request counts (future)
    - Processing times (future)
    - Error rates (future)
    - Resource usage
    """
    # Get resource usage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # Get service metrics
    from batch.scheduler import get_scheduler
    scheduler = get_scheduler()
    jobs = scheduler.list_jobs()

    from email_integration.email_processor import get_email_processor
    email_processor = get_email_processor()
    email_stats = email_processor.get_statistics() if email_processor else {}

    from cloud_webhooks.webhook_handler import get_webhook_handler
    webhook_handler = get_webhook_handler()
    webhook_stats = webhook_handler.get_statistics()

    return {
        "timestamp": datetime.now().isoformat(),
        "resources": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent
        },
        "services": {
            "batch_jobs": {
                "total_jobs": len(jobs),
                "enabled_jobs": len([j for j in jobs if j["enabled"]]),
                "active_jobs": len([j for j in jobs if j["status"] == "running"])
            },
            "email": email_stats,
            "webhooks": webhook_stats
        }
    }


@router.get("/info")
async def system_info():
    """
    Get basic system information (public endpoint).

    Returns application version and basic info without sensitive data.
    """
    return {
        "name": "Intelligent Finance Platform API",
        "version": "1.0.0",
        "status": "running",
        "environment": get_config().environment,
        "timestamp": datetime.now().isoformat()
    }
