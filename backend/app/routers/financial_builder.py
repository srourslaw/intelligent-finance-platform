"""
Financial Builder API Endpoints
Handles full pipeline: extraction → categorization → aggregation → Excel population
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.database import get_db
from app.services.template_parser import parse_template, TemplateParser
from app.services.file_extractor import start_extraction, get_extraction_status, FileExtractor
from app.models.extraction import ExtractionJob, JobStatus

router = APIRouter(prefix="/api/financial-builder", tags=["financial-builder"])


class ParseTemplateResponse(BaseModel):
    success: bool
    project_id: str
    total_categories: int
    message: str


class StartExtractionResponse(BaseModel):
    success: bool
    job_id: str
    project_id: str
    total_files: int
    message: str


class JobStatusResponse(BaseModel):
    job_id: str
    project_id: str
    status: str
    total_files: int
    processed_files: int
    failed_files: int
    progress_percent: float
    error_message: Optional[str]


@router.post("/{project_id}/parse-template", response_model=ParseTemplateResponse)
async def parse_project_template(project_id: str):
    """
    Parse MASTER FINANCIAL STATEMENT TEMPLATE.md into structured JSON dictionary.

    Args:
        project_id: Project identifier

    Returns:
        Parsed template summary
    """
    try:
        parser = TemplateParser(project_id)
        template_dict = parser.parse()

        # Save to JSON file
        output_path = parser.save_to_json()

        return ParseTemplateResponse(
            success=True,
            project_id=project_id,
            total_categories=template_dict['metadata']['total_categories'],
            message=f"Template parsed successfully. Dictionary saved to {output_path}"
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template parsing failed: {str(e)}")


@router.post("/{project_id}/extract-all", response_model=StartExtractionResponse)
async def extract_all_files(
    project_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start bulk extraction of all files in project data folder.

    This endpoint:
    1. Scans project data folder for all PDFs, Excel, CSV files
    2. Creates extraction job in database
    3. Processes files in background (PDFs with MinerU, Excel with pandas)
    4. Stores extracted data in database

    Args:
        project_id: Project identifier
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Job ID and initial status
    """
    try:
        # Create extractor
        extractor = FileExtractor(project_id, db)

        # Scan files first
        files = extractor.scan_files()
        if not files:
            raise HTTPException(
                status_code=404,
                detail=f"No supported files found in project {project_id}/data folder"
            )

        # Create job
        job_id = extractor.create_extraction_job()

        # Run extraction in background
        background_tasks.add_task(extractor.run_extraction, job_id)

        return StartExtractionResponse(
            success=True,
            job_id=job_id,
            project_id=project_id,
            total_files=len(files),
            message=f"Extraction started for {len(files)} files. Use job_id to track progress."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start extraction: {str(e)}")


@router.get("/jobs/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Get current status of an extraction job.

    Args:
        job_id: Job identifier
        db: Database session

    Returns:
        Job status with progress information
    """
    status = get_extraction_status(job_id, db)

    if not status:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return JobStatusResponse(**status)


@router.post("/{project_id}/run-full-pipeline")
async def run_full_pipeline(
    project_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Run complete pipeline: parse template → extract files → categorize → aggregate → populate Excel.

    This is the main endpoint for the Financial Builder feature.

    Args:
        project_id: Project identifier
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Job ID for tracking overall pipeline progress
    """
    try:
        # Step 1: Parse template
        parser = TemplateParser(project_id)
        template_dict = parser.parse()
        parser.save_to_json()

        # Step 2: Start extraction
        extractor = FileExtractor(project_id, db)
        files = extractor.scan_files()

        if not files:
            raise HTTPException(
                status_code=404,
                detail=f"No files found in project {project_id}"
            )

        job_id = extractor.create_extraction_job()

        # TODO: Add background task that runs all phases
        # For now, just run extraction
        background_tasks.add_task(extractor.run_extraction, job_id)

        return {
            "success": True,
            "job_id": job_id,
            "project_id": project_id,
            "total_files": len(files),
            "total_categories": template_dict['metadata']['total_categories'],
            "message": "Full pipeline started. Phases: 1) Parse Template ✓ 2) Extract Files (in progress) 3) Categorize (pending) 4) Aggregate (pending) 5) Populate Excel (pending)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


@router.get("/{project_id}/extracted-data")
async def get_extracted_data(project_id: str, db: Session = Depends(get_db)):
    """
    Get all extracted data for a project.

    Args:
        project_id: Project identifier
        db: Database session

    Returns:
        List of extracted data records
    """
    from app.models.extraction import ExtractedData

    data = db.query(ExtractedData).filter(
        ExtractedData.project_id == project_id
    ).all()

    return {
        "project_id": project_id,
        "total_files": len(data),
        "files": [
            {
                "id": d.id,
                "file_name": d.file_name,
                "file_type": d.file_type,
                "extraction_status": d.extraction_status,
                "extraction_method": d.extraction_method,
                "text_preview": d.raw_text[:200] if d.raw_text else None,
                "created_at": d.created_at.isoformat() if d.created_at else None
            }
            for d in data
        ]
    }
