"""
Folder Monitoring API

Endpoints for configuring and managing local/network folder monitoring.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import json

from app.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/folder-watch",
    tags=["folder-watch"],
    dependencies=[Depends(get_current_user)]
)


class WatchFolderConfig(BaseModel):
    """Configuration for folder watching"""
    path: str
    project_id: Optional[str] = None
    patterns: List[str] = ["*.xlsx", "*.pdf", "*.csv"]
    recursive: bool = True
    process_existing: bool = False
    process_modifications: bool = False


class WatchFolderResponse(BaseModel):
    """Response for folder watch operations"""
    message: str
    status: str


@router.post("/start", response_model=WatchFolderResponse)
async def start_monitoring(user: dict = Depends(get_current_user)):
    """
    Start folder monitoring with configured watches.

    Loads watch configurations from file or uses defaults.
    """
    try:
        from automation.folder_watcher import start_folder_monitoring, load_watch_configs_from_file, get_watch_status

        # Check if already running
        status = get_watch_status()
        if status["running"]:
            return WatchFolderResponse(
                message="Folder monitoring is already running",
                status="already_running"
            )

        # Load configurations
        configs = load_watch_configs_from_file()

        # Start monitoring
        start_folder_monitoring(configs)

        logger.info(f"📂 Folder monitoring started by {user.get('email')}")

        return WatchFolderResponse(
            message=f"Started monitoring {len(configs)} folder(s)",
            status="started"
        )

    except Exception as e:
        logger.error(f"Error starting folder monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop", response_model=WatchFolderResponse)
async def stop_monitoring(user: dict = Depends(get_current_user)):
    """
    Stop folder monitoring.
    """
    try:
        from automation.folder_watcher import stop_folder_monitoring, get_watch_status

        # Check if running
        status = get_watch_status()
        if not status["running"]:
            return WatchFolderResponse(
                message="Folder monitoring is not running",
                status="not_running"
            )

        # Stop monitoring
        stop_folder_monitoring()

        logger.info(f"📂 Folder monitoring stopped by {user.get('email')}")

        return WatchFolderResponse(
            message="Folder monitoring stopped",
            status="stopped"
        )

    except Exception as e:
        logger.error(f"Error stopping folder monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status(user: dict = Depends(get_current_user)):
    """
    Get folder monitoring status.

    Returns:
        - running: Whether monitoring is active
        - watch_configs: List of configured watches
        - statistics: Processing statistics
    """
    try:
        from automation.folder_watcher import get_watch_status

        status = get_watch_status()

        # Load statistics
        stats = _load_statistics()

        return {
            "running": status["running"],
            "watch_configs": status["watch_configs"],
            "statistics": stats
        }

    except Exception as e:
        logger.error(f"Error getting folder monitoring status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add", response_model=WatchFolderResponse)
async def add_watch_folder(
    config: WatchFolderConfig,
    user: dict = Depends(get_current_user)
):
    """
    Add a new folder to watch.

    This will add the folder to the monitoring system and optionally
    process existing files in the folder.
    """
    try:
        from automation.folder_watcher import add_watch_folder

        # Validate path exists or can be created
        path = Path(config.path)

        # Convert Pydantic model to dict
        config_dict = config.model_dump()

        # Add watch
        add_watch_folder(config_dict)

        # Save to config file
        _save_watch_config(config_dict)

        logger.info(f"📂 Added watch folder {config.path} by {user.get('email')}")

        return WatchFolderResponse(
            message=f"Added watch folder: {config.path}",
            status="added"
        )

    except Exception as e:
        logger.error(f"Error adding watch folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/remove/{path:path}")
async def remove_watch_folder(path: str, user: dict = Depends(get_current_user)):
    """
    Remove a watched folder.
    """
    try:
        from automation.folder_watcher import remove_watch_folder

        # Remove watch
        remove_watch_folder(path)

        # Remove from config file
        _remove_from_config(path)

        logger.info(f"📂 Removed watch folder {path} by {user.get('email')}")

        return {
            "message": f"Removed watch folder: {path}",
            "status": "removed",
            "note": "Restart monitoring to apply changes"
        }

    except Exception as e:
        logger.error(f"Error removing watch folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics(user: dict = Depends(get_current_user)):
    """
    Get folder monitoring statistics.

    Returns processing statistics for all watched folders.
    """
    try:
        stats = _load_statistics()
        return {"statistics": stats}

    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _save_watch_config(config: Dict[str, Any]):
    """Save watch config to file"""
    config_file = Path("config/folder_watches.json")
    config_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing configs
    if config_file.exists():
        with open(config_file, 'r') as f:
            configs = json.load(f)
    else:
        configs = []

    # Add new config (avoid duplicates)
    configs = [c for c in configs if c['path'] != config['path']]
    configs.append(config)

    # Save
    with open(config_file, 'w') as f:
        json.dump(configs, f, indent=2)


def _remove_from_config(path: str):
    """Remove watch config from file"""
    config_file = Path("config/folder_watches.json")

    if not config_file.exists():
        return

    # Load configs
    with open(config_file, 'r') as f:
        configs = json.load(f)

    # Remove matching config
    configs = [c for c in configs if c['path'] != path]

    # Save
    with open(config_file, 'w') as f:
        json.dump(configs, f, indent=2)


def _load_statistics() -> Dict[str, Any]:
    """Load folder monitoring statistics"""
    stats_dir = Path("data/folder_watch_stats")

    if not stats_dir.exists():
        return {
            "total_processed": 0,
            "total_errors": 0,
            "by_date": {}
        }

    # Aggregate statistics from all daily files
    total_processed = 0
    total_errors = 0
    by_date = {}

    for stats_file in stats_dir.glob("*.json"):
        try:
            with open(stats_file, 'r') as f:
                daily_stats = json.load(f)

            date = stats_file.stem
            processed_files = daily_stats.get("processed_files", [])

            by_date[date] = {
                "processed": len(processed_files),
                "errors": sum(1 for f in processed_files if f.get('result', {}).get('status') == 'error')
            }

            total_processed += len(processed_files)
            total_errors += by_date[date]["errors"]

        except Exception as e:
            logger.error(f"Error loading stats from {stats_file}: {e}")

    return {
        "total_processed": total_processed,
        "total_errors": total_errors,
        "success_rate": (total_processed - total_errors) / total_processed * 100 if total_processed > 0 else 0,
        "by_date": by_date
    }
