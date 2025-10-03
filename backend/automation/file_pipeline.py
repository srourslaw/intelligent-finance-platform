"""
Automatic File Processing Pipeline

Automatically processes files downloaded from email/webhooks through
the extraction and classification pipeline.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


class FilePipeline:
    """
    Automated file processing pipeline.

    Monitors upload directories and automatically processes new files through:
    1. File extraction (PDF, Excel parsing)
    2. AI classification (document type detection)
    3. Transaction extraction
    4. Project assignment
    """

    def __init__(self):
        """Initialize file pipeline."""
        self.email_upload_dir = Path("data/email_uploads")
        self.webhook_upload_dir = Path("data/webhook_uploads")
        self.extraction_dir = Path("data/extractions")
        self.processed_files_log = Path("data/processed_files.json")

        # Create directories
        self.email_upload_dir.mkdir(parents=True, exist_ok=True)
        self.webhook_upload_dir.mkdir(parents=True, exist_ok=True)
        self.extraction_dir.mkdir(parents=True, exist_ok=True)

        # Load processed files log
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self) -> Dict[str, Any]:
        """Load list of already processed files."""
        if self.processed_files_log.exists():
            try:
                with self.processed_files_log.open('r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load processed files log: {e}")
        return {"files": [], "statistics": {"total_processed": 0, "total_errors": 0}}

    def _save_processed_files(self):
        """Save processed files log."""
        try:
            with self.processed_files_log.open('w') as f:
                json.dump(self.processed_files, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save processed files log: {e}")

    def _mark_as_processed(self, file_path: Path, success: bool, error: Optional[str] = None):
        """Mark file as processed."""
        self.processed_files["files"].append({
            "file_path": str(file_path),
            "processed_at": datetime.now().isoformat(),
            "success": success,
            "error": error
        })

        if success:
            self.processed_files["statistics"]["total_processed"] += 1
        else:
            self.processed_files["statistics"]["total_errors"] += 1

        self._save_processed_files()

    def is_processed(self, file_path: Path) -> bool:
        """Check if file has already been processed."""
        file_str = str(file_path)
        return any(f["file_path"] == file_str for f in self.processed_files["files"])

    async def process_file(
        self,
        file_path: Path,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a single file through the pipeline.

        Args:
            file_path: Path to file
            project_id: Optional project ID (detected if not provided)

        Returns:
            Processing result
        """
        logger.info(f"📄 Processing file: {file_path.name}")

        try:
            # Import extraction functions
            from app.services.file_extraction import extract_file_content
            from app.services.ai_classifier import classify_document

            # Step 1: Extract file content
            logger.info(f"  1️⃣  Extracting content...")
            extraction_result = await extract_file_content(str(file_path))

            if extraction_result.get("error"):
                raise Exception(f"Extraction failed: {extraction_result['error']}")

            # Step 2: Classify document
            logger.info(f"  2️⃣  Classifying document...")
            classification = await classify_document(extraction_result)

            # Step 3: Extract transactions (if applicable)
            logger.info(f"  3️⃣  Extracting transactions...")
            transactions = extraction_result.get("transactions", [])

            # Step 4: Determine project ID
            if not project_id:
                # Try to detect from filename or content
                project_id = self._detect_project_id(file_path, extraction_result)

            # Save extraction result
            result = {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "processed_at": datetime.now().isoformat(),
                "project_id": project_id,
                "document_type": classification.get("document_type"),
                "confidence": classification.get("confidence"),
                "transactions": transactions,
                "extracted_data": extraction_result
            }

            # Save to extraction directory
            result_file = self.extraction_dir / f"{file_path.stem}_result.json"
            with result_file.open('w') as f:
                json.dump(result, f, indent=2, default=str)

            logger.info(f"  ✅ Processing complete: {len(transactions)} transactions extracted")

            # Mark as processed
            self._mark_as_processed(file_path, success=True)

            return result

        except Exception as e:
            logger.error(f"  ❌ Processing failed: {e}")
            self._mark_as_processed(file_path, success=False, error=str(e))
            raise

    def _detect_project_id(self, file_path: Path, extraction_result: Dict) -> Optional[str]:
        """Detect project ID from filename or content."""
        import re

        # Check filename
        patterns = [
            r'Project[_\s]+([A-Za-z0-9_\-]+)',
            r'\[([A-Za-z0-9_\-]+)\]',
            r'([A-Z]\d+_\d{4})',  # Q4_2024 pattern
        ]

        filename = file_path.name
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return match.group(1)

        # Check extracted text
        text = extraction_result.get("raw_text", "")
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    async def scan_and_process(self) -> Dict[str, Any]:
        """
        Scan upload directories and process new files.

        Returns:
            Processing statistics
        """
        logger.info("🔍 Scanning for new files...")

        processed_count = 0
        error_count = 0
        results = []

        # Scan email uploads
        for file_path in self.email_upload_dir.glob("*"):
            if file_path.is_file() and not self.is_processed(file_path):
                try:
                    result = await self.process_file(file_path)
                    results.append(result)
                    processed_count += 1
                except Exception as e:
                    logger.error(f"Failed to process {file_path.name}: {e}")
                    error_count += 1

        # Scan webhook uploads
        for file_path in self.webhook_upload_dir.glob("*"):
            if file_path.is_file() and not self.is_processed(file_path):
                try:
                    result = await self.process_file(file_path)
                    results.append(result)
                    processed_count += 1
                except Exception as e:
                    logger.error(f"Failed to process {file_path.name}: {e}")
                    error_count += 1

        logger.info(f"✅ Scan complete: {processed_count} processed, {error_count} errors")

        return {
            "processed": processed_count,
            "errors": error_count,
            "results": results
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.processed_files.get("statistics", {})


# Singleton instance
_pipeline: Optional[FilePipeline] = None


def get_pipeline() -> FilePipeline:
    """Get or create file pipeline singleton."""
    global _pipeline

    if _pipeline is None:
        _pipeline = FilePipeline()

    return _pipeline
