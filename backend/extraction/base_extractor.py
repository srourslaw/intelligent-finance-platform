"""
Base extractor interface for all file types.

All extractors (Excel, PDF, CSV, OCR, etc.) inherit from this base class
to ensure consistent API and behavior.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import hashlib
import mimetypes
from datetime import datetime

from schemas.extraction_schema import (
    ExtractionResult,
    FileMetadata,
    FileType,
    DocumentType,
    ExtractedData,
    ExtractionNotes,
    DataQuality,
    ClassificationStats
)


class BaseExtractor(ABC):
    """
    Abstract base class for all file extractors.

    Each extractor must implement the extract() method which returns
    an ExtractionResult containing all extracted financial data.
    """

    def __init__(self):
        self.supported_extensions: List[str] = []
        self.extractor_name: str = "base_extractor"
        self.version: str = "1.0.0"

    @abstractmethod
    def extract(self, file_path: str) -> ExtractionResult:
        """
        Extract financial data from the given file.

        Args:
            file_path: Absolute path to the file to extract

        Returns:
            ExtractionResult with all extracted data and metadata

        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
            Exception: For other extraction errors
        """
        pass

    def detect_file_type(self, file_path: str) -> FileType:
        """Detect the file type based on extension and MIME type."""
        path = Path(file_path)
        extension = path.suffix.lower()
        mime_type, _ = mimetypes.guess_type(file_path)

        # Excel files
        if extension in ['.xlsx', '.xls', '.xlsm', '.xlsb']:
            return FileType.EXCEL

        # PDF files
        elif extension == '.pdf':
            return FileType.PDF

        # CSV files
        elif extension == '.csv':
            return FileType.CSV

        # Image files
        elif extension in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
            return FileType.IMAGE

        # Word files
        elif extension in ['.docx', '.doc']:
            return FileType.WORD

        else:
            return FileType.UNKNOWN

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file for unique identification."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()[:16]  # First 16 chars for shorter ID

    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        return Path(file_path).stat().st_size

    def create_metadata(self, file_path: str, extraction_start: datetime) -> FileMetadata:
        """Create file metadata for extraction result."""
        path = Path(file_path)
        file_id = self.calculate_file_hash(file_path)
        file_type = self.detect_file_type(file_path)
        file_size = self.get_file_size(file_path)

        extraction_end = datetime.utcnow()
        duration = (extraction_end - extraction_start).total_seconds()

        return FileMetadata(
            file_id=file_id,
            original_filename=path.name,
            file_path=str(path.absolute()),
            file_type=file_type,
            file_size_bytes=file_size,
            upload_date=datetime.utcnow(),
            extraction_date=extraction_end,
            processed_by=f"{self.extractor_name}_v{self.version}",
            extraction_duration_seconds=duration,
            confidence_score=0.0,  # Will be updated by classifier
            document_classification=DocumentType.UNKNOWN  # Will be updated by classifier
        )

    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that file exists and is readable.

        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)

        if not path.exists():
            return False, f"File not found: {file_path}"

        if not path.is_file():
            return False, f"Path is not a file: {file_path}"

        if not path.stat().st_size > 0:
            return False, f"File is empty: {file_path}"

        file_type = self.detect_file_type(file_path)
        if file_type == FileType.UNKNOWN:
            return False, f"Unsupported file type: {path.suffix}"

        return True, None

    def create_empty_result(self, file_path: str, error_message: str) -> ExtractionResult:
        """Create an empty extraction result with error."""
        metadata = self.create_metadata(file_path, datetime.utcnow())
        metadata.confidence_score = 0.0

        notes = ExtractionNotes(
            errors=[error_message]
        )

        return ExtractionResult(
            metadata=metadata,
            extracted_data=ExtractedData(),
            extraction_notes=notes,
            data_quality=DataQuality(
                completeness_score=0.0,
                consistency_check="failed"
            ),
            classification_stats=ClassificationStats()
        )

    def extract_with_validation(self, file_path: str) -> ExtractionResult:
        """
        Wrapper around extract() that handles validation and errors.

        This is the method that should be called externally.
        """
        # Validate file
        is_valid, error = self.validate_file(file_path)
        if not is_valid:
            return self.create_empty_result(file_path, error)

        # Attempt extraction
        try:
            extraction_start = datetime.utcnow()
            result = self.extract(file_path)
            return result

        except Exception as e:
            error_msg = f"Extraction failed: {str(e)}"
            return self.create_empty_result(file_path, error_msg)


class ExtractorFactory:
    """
    Factory class to get the appropriate extractor for a file type.

    Usage:
        extractor = ExtractorFactory.get_extractor(file_path)
        result = extractor.extract_with_validation(file_path)
    """

    _extractors: Dict[FileType, BaseExtractor] = {}

    @classmethod
    def register_extractor(cls, file_type: FileType, extractor: BaseExtractor):
        """Register an extractor for a specific file type."""
        cls._extractors[file_type] = extractor

    @classmethod
    def get_extractor(cls, file_path: str) -> Optional[BaseExtractor]:
        """Get the appropriate extractor for the given file."""
        # Detect file type
        path = Path(file_path)
        extension = path.suffix.lower()

        # Determine file type
        if extension in ['.xlsx', '.xls', '.xlsm', '.xlsb']:
            file_type = FileType.EXCEL
        elif extension == '.pdf':
            file_type = FileType.PDF
        elif extension == '.csv':
            file_type = FileType.CSV
        elif extension in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
            file_type = FileType.IMAGE
        elif extension in ['.docx', '.doc']:
            file_type = FileType.WORD
        else:
            return None

        return cls._extractors.get(file_type)

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Get list of all supported file extensions."""
        return [
            '.xlsx', '.xls', '.xlsm', '.xlsb',  # Excel
            '.pdf',  # PDF
            '.csv',  # CSV
            '.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp',  # Images
            '.docx', '.doc'  # Word
        ]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def detect_numbers_in_text(text: str) -> List[float]:
    """Extract all numbers from text string."""
    import re
    # Match currency and numbers
    pattern = r'[$£€¥]?\s*-?\d{1,3}(?:,\d{3})*(?:\.\d{2,})?'
    matches = re.findall(pattern, text)

    numbers = []
    for match in matches:
        # Clean and convert
        cleaned = match.replace('$', '').replace('£', '').replace('€', '').replace('¥', '').replace(',', '').strip()
        try:
            numbers.append(float(cleaned))
        except ValueError:
            continue

    return numbers


def clean_label(label: str) -> str:
    """Clean and normalize a label string."""
    if not label:
        return ""

    # Remove extra whitespace
    cleaned = ' '.join(label.split())

    # Remove common prefixes/suffixes
    cleaned = cleaned.strip(':-•*')

    # Title case
    cleaned = cleaned.title()

    return cleaned


def detect_date_in_text(text: str) -> Optional[str]:
    """
    Detect dates in text and return in YYYY-MM-DD format.

    Handles various formats:
    - 2024-10-03
    - 10/03/2024
    - October 3, 2024
    - 3 Oct 2024
    """
    from dateutil import parser as date_parser

    try:
        parsed_date = date_parser.parse(text, fuzzy=True)
        return parsed_date.strftime('%Y-%m-%d')
    except (ValueError, OverflowError):
        return None
