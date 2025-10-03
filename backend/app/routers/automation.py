"""
Automation API Routes

Endpoints for automated file processing and pipeline management.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.auth_utils import get_current_user
from automation.file_pipeline import get_pipeline

router = APIRouter(prefix="/api/automation", tags=["automation"])


# ============================================================================
# FILE PROCESSING PIPELINE
# ============================================================================

@router.post("/process-new-files")
async def process_new_files(
    user: dict = Depends(get_current_user)
):
    """
    Scan upload directories and process new files.

    Automatically:
    1. Scans email_uploads and webhook_uploads directories
    2. Extracts content from new files
    3. Classifies documents with AI
    4. Extracts transactions
    5. Detects and assigns project IDs

    Returns processing statistics.
    """
    pipeline = get_pipeline()

    try:
        result = await pipeline.scan_and_process()

        return {
            "message": f"Processed {result['processed']} new files",
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline processing failed: {str(e)}"
        )


@router.get("/statistics")
async def get_pipeline_statistics(
    user: dict = Depends(get_current_user)
):
    """
    Get file processing pipeline statistics.

    Returns:
    - Total files processed
    - Total errors
    - Processing success rate
    """
    pipeline = get_pipeline()
    stats = pipeline.get_statistics()

    total = stats.get("total_processed", 0) + stats.get("total_errors", 0)
    success_rate = (stats.get("total_processed", 0) / total * 100) if total > 0 else 0

    return {
        **stats,
        "success_rate": round(success_rate, 2)
    }


@router.get("/health")
async def automation_health():
    """
    Health check for automation service.
    """
    pipeline = get_pipeline()
    stats = pipeline.get_statistics()

    return {
        "status": "healthy",
        "service": "automation_pipeline",
        "statistics": stats
    }
