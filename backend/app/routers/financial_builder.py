"""
Financial Builder API Endpoints
Handles full pipeline: extraction → categorization → aggregation → Excel population
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.services.template_parser import parse_template, TemplateParser
from app.services.file_extractor import start_extraction, get_extraction_status, FileExtractor
from app.services.ai_categorizer import create_categorizer
from app.services.excel_populator import create_excel_populator
from app.models.extraction import ExtractionJob, JobStatus, ExtractedData
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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

        # Run full pipeline in background
        background_tasks.add_task(
            run_pipeline_phases,
            project_id,
            job_id,
            template_dict,
            db
        )

        return {
            "success": True,
            "job_id": job_id,
            "project_id": project_id,
            "total_files": len(files),
            "total_categories": template_dict['metadata']['total_categories'],
            "message": "Full pipeline started. Phases: 1) Parse Template ✓ 2) Extract Files (starting) 3) Categorize (pending) 4) Populate Excel (pending)"
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


def run_pipeline_phases(
    project_id: str,
    job_id: str,
    template_dict: Dict[str, Any],
    db: Session
):
    """
    Background task to run all pipeline phases sequentially.

    Phases:
    1. Extract all files (PDFs, Excel, CSV)
    2. Categorize transactions using AI
    3. Aggregate and calculate totals
    4. Populate Excel financial model

    Args:
        project_id: Project identifier
        job_id: Extraction job ID
        template_dict: Parsed template dictionary
        db: Database session
    """
    try:
        logger.info(f"[{project_id}] Pipeline started - Job ID: {job_id}")

        # Phase 1: Extract files
        logger.info(f"[{project_id}] Phase 1: Extracting files...")
        extractor = FileExtractor(project_id, db)
        extractor.run_extraction(job_id)

        # Wait for extraction to complete
        job = db.query(ExtractionJob).filter(ExtractionJob.job_id == job_id).first()
        if not job or job.status != JobStatus.COMPLETED:
            logger.error(f"[{project_id}] Extraction phase failed or incomplete")
            return

        logger.info(f"[{project_id}] Phase 1 complete: {job.processed_files} files extracted")

        # Phase 2: Retrieve extracted data
        logger.info(f"[{project_id}] Phase 2: Retrieving extracted data...")
        extracted_data = db.query(ExtractedData).filter(
            ExtractedData.project_id == project_id,
            ExtractedData.extraction_status == "success"
        ).all()

        # Convert extracted data to transactions list
        transactions = []
        for data_record in extracted_data:
            # Parse structured_data JSON
            if data_record.structured_data:
                try:
                    structured = json.loads(data_record.structured_data)
                    # Handle different extraction formats
                    if 'transactions' in structured:
                        for txn in structured['transactions']:
                            transactions.append({
                                'description': txn.get('description', ''),
                                'amount': float(txn.get('amount', 0)),
                                'vendor': txn.get('vendor', ''),
                                'date': txn.get('date', ''),
                                'source_file': data_record.file_name
                            })
                    elif 'rows' in structured:
                        # Excel/CSV format
                        for row in structured['rows']:
                            transactions.append({
                                'description': str(row.get('description', row.get('item', ''))),
                                'amount': float(row.get('amount', row.get('cost', 0))),
                                'vendor': str(row.get('vendor', '')),
                                'date': str(row.get('date', '')),
                                'source_file': data_record.file_name
                            })
                except Exception as e:
                    logger.warning(f"Failed to parse structured data for {data_record.file_name}: {e}")

        logger.info(f"[{project_id}] Phase 2 complete: {len(transactions)} transactions collected")

        if not transactions:
            logger.warning(f"[{project_id}] No transactions found, creating empty report")
            transactions = []

        # Phase 3: Categorize transactions
        logger.info(f"[{project_id}] Phase 3: Categorizing {len(transactions)} transactions...")
        categorizer = create_categorizer(template_dict)
        categorized_transactions = categorizer.categorize_batch(transactions, use_llm=False)

        # Get summary statistics
        summary = categorizer.get_category_summary(categorized_transactions)
        logger.info(f"[{project_id}] Phase 3 complete: {summary['total_transactions']} categorized, "
                   f"{summary['uncategorized_count']} uncategorized, "
                   f"avg confidence {summary['average_confidence']:.2%}")

        # Phase 4: Populate Excel
        logger.info(f"[{project_id}] Phase 4: Populating Excel financial model...")

        # Prepare data for Excel
        excel_data = {
            'categorized_transactions': categorized_transactions,
            'summary': summary
        }

        # Generate output path
        # Use /tmp for cloud deployments (Render, etc.) where file system is ephemeral
        base_dir = Path("/tmp") if os.getenv("RENDER") else Path("data")
        output_dir = base_dir / "projects" / project_id / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"Financial_Model_{timestamp}.xlsx"

        # Create Excel file
        populator = create_excel_populator()
        excel_path = populator.create_financial_model(
            excel_data,
            str(output_path),
            project_name=project_id
        )

        logger.info(f"[{project_id}] Phase 4 complete: Excel generated at {excel_path}")

        # Update job with final results
        job.status = JobStatus.COMPLETED
        job.metadata = json.dumps({
            'total_transactions': len(transactions),
            'categorized': len(categorized_transactions),
            'uncategorized_count': summary['uncategorized_count'],
            'average_confidence': summary['average_confidence'],
            'excel_path': excel_path,
            'pipeline_complete': True
        })
        db.commit()

        logger.info(f"[{project_id}] Full pipeline COMPLETE!")

    except Exception as e:
        logger.error(f"[{project_id}] Pipeline failed: {str(e)}", exc_info=True)
        # Update job status to failed
        try:
            job = db.query(ExtractionJob).filter(ExtractionJob.job_id == job_id).first()
            if job:
                job.status = JobStatus.FAILED
                job.error_message = f"Pipeline failed: {str(e)}"
                db.commit()
        except:
            pass
