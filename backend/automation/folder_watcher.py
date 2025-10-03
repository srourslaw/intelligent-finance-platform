"""
Folder Monitoring Service

Monitors local/network folders for new files and auto-processes them.
Uses watchdog library for efficient file system event monitoring.
"""
import os
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent
import asyncio
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Global observer instance
_observer: Optional[Observer] = None
_watch_configs: List[Dict[str, Any]] = []


class FileProcessingHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers processing.
    """

    def __init__(self, watch_config: Dict[str, Any]):
        """
        Initialize handler with watch configuration.

        Args:
            watch_config: Configuration dict with:
                - path: Folder to watch
                - project_id: Project ID for auto-assignment
                - patterns: File patterns to watch (e.g., ["*.xlsx", "*.pdf"])
                - recursive: Watch subdirectories
                - process_existing: Process existing files on startup
        """
        super().__init__()
        self.watch_config = watch_config
        self.path = Path(watch_config['path'])
        self.project_id = watch_config.get('project_id')
        self.patterns = watch_config.get('patterns', ['*.xlsx', '*.pdf', '*.csv'])
        self.processed_files = set()  # Track processed files to avoid duplicates
        self.cooldown = 2  # Seconds to wait before processing (avoid partial writes)

        logger.info(f"📂 Initialized watcher for {self.path}")

    def on_created(self, event: FileCreatedEvent):
        """Handle file creation events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Check if file matches patterns
        if not self._matches_pattern(file_path):
            return

        logger.info(f"📄 New file detected: {file_path.name}")

        # Wait for file to finish writing
        time.sleep(self.cooldown)

        # Process file
        self._process_file(file_path)

    def on_modified(self, event: FileModifiedEvent):
        """Handle file modification events (optional)"""
        # Only process modifications if configured
        if not self.watch_config.get('process_modifications', False):
            return

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if not self._matches_pattern(file_path):
            return

        # Avoid processing same file multiple times
        if str(file_path) in self.processed_files:
            return

        logger.info(f"📝 File modified: {file_path.name}")
        time.sleep(self.cooldown)
        self._process_file(file_path)

    def _matches_pattern(self, file_path: Path) -> bool:
        """Check if file matches configured patterns"""
        for pattern in self.patterns:
            if file_path.match(pattern):
                return True
        return False

    def _process_file(self, file_path: Path):
        """
        Process detected file.

        This will trigger the automated file processing pipeline.
        """
        try:
            # Avoid duplicate processing
            if str(file_path) in self.processed_files:
                logger.debug(f"  ⏭️  Already processed: {file_path.name}")
                return

            # Mark as processed
            self.processed_files.add(str(file_path))

            # Import here to avoid circular dependency
            from automation.file_pipeline import get_pipeline

            # Get pipeline
            pipeline = get_pipeline()

            # Process file asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            result = loop.run_until_complete(
                pipeline.process_file(file_path, project_id=self.project_id)
            )

            loop.close()

            if result['status'] == 'success':
                logger.info(f"  ✅ Successfully processed: {file_path.name}")

                # Log to statistics
                self._log_processing_result(file_path, result)
            else:
                logger.error(f"  ❌ Failed to process: {file_path.name} - {result.get('error')}")

        except Exception as e:
            logger.error(f"  ❌ Error processing {file_path.name}: {e}")

    def _log_processing_result(self, file_path: Path, result: Dict[str, Any]):
        """Log processing result to statistics file"""
        stats_dir = Path("data/folder_watch_stats")
        stats_dir.mkdir(parents=True, exist_ok=True)

        stats_file = stats_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        # Load existing stats
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {"processed_files": []}

        # Add new entry
        stats["processed_files"].append({
            "file_name": file_path.name,
            "file_path": str(file_path),
            "project_id": self.project_id,
            "processed_at": datetime.now().isoformat(),
            "result": result
        })

        # Save stats
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)


def start_folder_monitoring(watch_configs: List[Dict[str, Any]]):
    """
    Start monitoring configured folders.

    Args:
        watch_configs: List of watch configurations, each with:
            - path: Folder to watch
            - project_id: Optional project ID for auto-assignment
            - patterns: File patterns to watch
            - recursive: Watch subdirectories
            - process_existing: Process existing files on startup
    """
    global _observer, _watch_configs

    if _observer is not None:
        logger.warning("Folder monitoring already running")
        return

    _observer = Observer()
    _watch_configs = watch_configs

    for config in watch_configs:
        path = Path(config['path'])

        # Create directory if it doesn't exist
        path.mkdir(parents=True, exist_ok=True)

        # Create event handler
        handler = FileProcessingHandler(config)

        # Schedule observer
        _observer.schedule(
            handler,
            str(path),
            recursive=config.get('recursive', False)
        )

        logger.info(f"👀 Watching folder: {path}")
        logger.info(f"   Project: {config.get('project_id', 'Auto-detect')}")
        logger.info(f"   Patterns: {config.get('patterns', ['*.xlsx', '*.pdf', '*.csv'])}")

        # Process existing files if configured
        if config.get('process_existing', False):
            _process_existing_files(handler, path, config.get('recursive', False))

    # Start observer
    _observer.start()
    logger.info("✅ Folder monitoring started")


def _process_existing_files(handler: FileProcessingHandler, path: Path, recursive: bool):
    """Process existing files in watched folder"""
    logger.info(f"📂 Processing existing files in {path}")

    if recursive:
        files = path.rglob('*')
    else:
        files = path.glob('*')

    for file_path in files:
        if file_path.is_file() and handler._matches_pattern(file_path):
            logger.info(f"  📄 Processing existing: {file_path.name}")
            handler._process_file(file_path)


def stop_folder_monitoring():
    """Stop folder monitoring"""
    global _observer

    if _observer is None:
        return

    _observer.stop()
    _observer.join()
    _observer = None

    logger.info("🛑 Folder monitoring stopped")


def get_watch_status() -> Dict[str, Any]:
    """
    Get current folder monitoring status.

    Returns:
        Status dict with running state and configured watches
    """
    return {
        "running": _observer is not None and _observer.is_alive() if _observer else False,
        "watch_configs": _watch_configs
    }


def add_watch_folder(config: Dict[str, Any]):
    """
    Add a new folder to watch (hot reload).

    Args:
        config: Watch configuration
    """
    global _observer, _watch_configs

    if _observer is None or not _observer.is_alive():
        # Start monitoring if not running
        start_folder_monitoring([config])
        return

    # Add to existing observer
    path = Path(config['path'])
    path.mkdir(parents=True, exist_ok=True)

    handler = FileProcessingHandler(config)

    _observer.schedule(
        handler,
        str(path),
        recursive=config.get('recursive', False)
    )

    _watch_configs.append(config)

    logger.info(f"👀 Added watch folder: {path}")

    # Process existing files if configured
    if config.get('process_existing', False):
        _process_existing_files(handler, path, config.get('recursive', False))


def remove_watch_folder(path: str):
    """
    Remove a watched folder.

    Args:
        path: Path to stop watching
    """
    global _watch_configs

    # Find and remove from config
    _watch_configs = [c for c in _watch_configs if c['path'] != path]

    # Note: watchdog doesn't support removing individual watches easily
    # Would need to restart observer with new config
    logger.warning(f"Removed {path} from config. Restart monitoring to apply changes.")


# Default configuration (can be overridden via API or config file)
DEFAULT_WATCH_CONFIGS = [
    {
        "path": "data/monitored_folders/project_001",
        "project_id": "PROJ001",
        "patterns": ["*.xlsx", "*.pdf", "*.csv"],
        "recursive": True,
        "process_existing": False,
        "process_modifications": False
    }
]


def load_watch_configs_from_file(config_file: str = "config/folder_watches.json") -> List[Dict[str, Any]]:
    """
    Load watch configurations from JSON file.

    Args:
        config_file: Path to config file

    Returns:
        List of watch configurations
    """
    config_path = Path(config_file)

    if not config_path.exists():
        logger.info(f"No watch config file found at {config_file}, using defaults")
        return DEFAULT_WATCH_CONFIGS

    try:
        with open(config_path, 'r') as f:
            configs = json.load(f)
        logger.info(f"Loaded {len(configs)} watch configs from {config_file}")
        return configs
    except Exception as e:
        logger.error(f"Error loading watch configs: {e}")
        return DEFAULT_WATCH_CONFIGS


if __name__ == "__main__":
    # Test folder monitoring
    logging.basicConfig(level=logging.INFO)

    print("🔍 Starting folder monitoring test...")

    # Start monitoring
    start_folder_monitoring(DEFAULT_WATCH_CONFIGS)

    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping folder monitoring...")
        stop_folder_monitoring()
