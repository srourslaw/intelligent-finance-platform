"""
File extraction API routes.

Endpoints for uploading files, triggering extraction, and retrieving results.
"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from extraction.base_extractor import ExtractorFactory
from extraction.extractors import ExcelExtractor, PDFExtractor, CSVExtractor, ImageExtractor
from schemas.extraction_schema import ExtractionResult, FileType
from classification.ai_classifier import AIClassifier
from app.auth_utils import get_current_user

router = APIRouter(prefix="/api/extraction", tags=["extraction"])

# Initialize extractors and register them
excel_extractor = ExcelExtractor()
pdf_extractor = PDFExtractor()
csv_extractor = CSVExtractor()
image_extractor = ImageExtractor()

ExtractorFactory.register_extractor(FileType.EXCEL, excel_extractor)
ExtractorFactory.register_extractor(FileType.PDF, pdf_extractor)
ExtractorFactory.register_extractor(FileType.CSV, csv_extractor)
ExtractorFactory.register_extractor(FileType.IMAGE, image_extractor)

# Storage paths
UPLOAD_DIR = Path("data/uploads")
EXTRACTION_DIR = Path("data/extractions")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTION_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class UploadResponse(BaseModel):
    """Response after file upload."""
    file_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    message: str


class ExtractionStatusResponse(BaseModel):
    """Response for extraction status check."""
    file_id: str
    status: str  # pending, processing, completed, failed
    extraction_result: Optional[ExtractionResult] = None
    error: Optional[str] = None


class FileListItem(BaseModel):
    """Summary of an uploaded file."""
    file_id: str
    filename: str
    file_type: str
    upload_date: datetime
    extraction_status: str
    confidence_score: float


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_uploaded_file(upload_file: UploadFile, file_id: str) -> str:
    """Save uploaded file to disk and return path."""
    file_extension = Path(upload_file.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return str(file_path)


def save_extraction_result(file_id: str, result: ExtractionResult):
    """Save extraction result as JSON."""
    result_path = EXTRACTION_DIR / f"{file_id}.json"

    with result_path.open("w") as f:
        json.dump(result.model_dump(mode='json'), f, indent=2, default=str)


def load_extraction_result(file_id: str) -> Optional[ExtractionResult]:
    """Load extraction result from JSON."""
    result_path = EXTRACTION_DIR / f"{file_id}.json"

    if not result_path.exists():
        return None

    with result_path.open("r") as f:
        data = json.load(f)
        return ExtractionResult(**data)


def process_file_extraction(file_id: str, file_path: str):
    """
    Process file extraction in background.

    Steps:
    1. Get appropriate extractor
    2. Extract data
    3. Classify with AI (if enabled)
    4. Save results
    """
    try:
        # Get extractor
        extractor = ExtractorFactory.get_extractor(file_path)

        if not extractor:
            raise ValueError(f"No extractor available for file: {file_path}")

        # Extract data
        result = extractor.extract_with_validation(file_path)

        # Classify with AI (if API key available)
        try:
            classifier = AIClassifier()
            if classifier.is_available():
                result = classifier.classify_extraction(result)
        except Exception as e:
            # Classification is optional, continue without it
            result.extraction_notes.warnings.append(f"AI classification skipped: {str(e)}")

        # Save result
        save_extraction_result(file_id, result)

    except Exception as e:
        # Save error state
        error_result = {
            "file_id": file_id,
            "status": "failed",
            "error": str(e)
        }
        error_path = EXTRACTION_DIR / f"{file_id}_error.json"
        with error_path.open("w") as f:
            json.dump(error_result, f, indent=2)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    """
    Upload a financial document for extraction.

    Accepts: Excel, PDF, CSV, Image files
    Returns: file_id for tracking extraction status

    Process:
    1. Validate file type
    2. Save file to disk
    3. Trigger background extraction
    4. Return file_id immediately
    """

    # Validate file extension
    file_extension = Path(file.filename).suffix.lower()
    supported_extensions = ExtractorFactory.get_supported_extensions()

    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}. Supported: {', '.join(supported_extensions)}"
        )

    # Validate file size (max 50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {file_size / (1024*1024):.2f}MB. Max: 50MB"
        )

    # Generate file ID (using timestamp + filename hash)
    import hashlib
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename_hash = hashlib.md5(file.filename.encode()).hexdigest()[:8]
    file_id = f"{timestamp}_{filename_hash}"

    # Save uploaded file
    try:
        file_path = save_uploaded_file(file, file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Trigger background extraction
    background_tasks.add_task(process_file_extraction, file_id, file_path)

    # Determine file type
    if file_extension in ['.xlsx', '.xls', '.xlsm', '.xlsb']:
        file_type = "excel"
    elif file_extension == '.pdf':
        file_type = "pdf"
    elif file_extension == '.csv':
        file_type = "csv"
    elif file_extension in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
        file_type = "image"
    else:
        file_type = "unknown"

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_type=file_type,
        file_size=file_size,
        status="processing",
        message="File uploaded successfully. Extraction in progress."
    )


@router.get("/status/{file_id}", response_model=ExtractionStatusResponse)
async def get_extraction_status(
    file_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Get the extraction status and results for a file.

    Status values:
    - processing: Extraction in progress
    - completed: Extraction successful, result available
    - failed: Extraction failed, error available
    """

    # Check if result exists
    result = load_extraction_result(file_id)

    if result:
        return ExtractionStatusResponse(
            file_id=file_id,
            status="completed",
            extraction_result=result
        )

    # Check if error exists
    error_path = EXTRACTION_DIR / f"{file_id}_error.json"
    if error_path.exists():
        with error_path.open("r") as f:
            error_data = json.load(f)
            return ExtractionStatusResponse(
                file_id=file_id,
                status="failed",
                error=error_data.get("error", "Unknown error")
            )

    # Still processing
    return ExtractionStatusResponse(
        file_id=file_id,
        status="processing"
    )


@router.get("/list", response_model=List[FileListItem])
async def list_extracted_files(
    user: dict = Depends(get_current_user)
):
    """
    List all extracted files for the current user.

    Returns summary information for each file.
    """

    files = []

    for result_file in EXTRACTION_DIR.glob("*.json"):
        if result_file.name.endswith("_error.json"):
            continue

        try:
            result = load_extraction_result(result_file.stem)

            if result:
                files.append(FileListItem(
                    file_id=result.metadata.file_id,
                    filename=result.metadata.original_filename,
                    file_type=result.metadata.file_type.value,
                    upload_date=result.metadata.upload_date,
                    extraction_status="completed",
                    confidence_score=result.metadata.confidence_score
                ))
        except Exception:
            continue

    # Sort by upload date (newest first)
    files.sort(key=lambda x: x.upload_date, reverse=True)

    return files


@router.get("/result/{file_id}", response_model=ExtractionResult)
async def get_extraction_result(
    file_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Get the full extraction result for a file.

    Returns complete ExtractionResult with all data.
    """

    result = load_extraction_result(file_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Extraction result not found for file_id: {file_id}"
        )

    return result


@router.delete("/{file_id}")
async def delete_extraction(
    file_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Delete an uploaded file and its extraction results.

    Removes:
    - Uploaded file
    - Extraction result JSON
    - Error files (if any)
    """

    deleted_items = []

    # Delete uploaded file
    for upload_file in UPLOAD_DIR.glob(f"{file_id}*"):
        upload_file.unlink()
        deleted_items.append(str(upload_file))

    # Delete extraction result
    result_path = EXTRACTION_DIR / f"{file_id}.json"
    if result_path.exists():
        result_path.unlink()
        deleted_items.append(str(result_path))

    # Delete error file
    error_path = EXTRACTION_DIR / f"{file_id}_error.json"
    if error_path.exists():
        error_path.unlink()
        deleted_items.append(str(error_path))

    if not deleted_items:
        raise HTTPException(
            status_code=404,
            detail=f"No files found for file_id: {file_id}"
        )

    return {
        "message": f"Deleted {len(deleted_items)} items",
        "deleted": deleted_items
    }


@router.get("/health")
async def extraction_health():
    """
    Health check endpoint for extraction service.

    Returns status of all extractors.
    """
    return {
        "status": "healthy",
        "extractors": {
            "excel": "available",
            "pdf": "available",
            "csv": "available",
            "image": "available"
        },
        "upload_dir": str(UPLOAD_DIR),
        "extraction_dir": str(EXTRACTION_DIR),
        "supported_extensions": ExtractorFactory.get_supported_extensions()
    }
