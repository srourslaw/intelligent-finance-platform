"""
Template Population API

Endpoints for generating populated Excel templates from aggregated financial data.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path
import logging
from datetime import datetime
import json

from app.auth import get_current_user
from app.services.template_populator import TemplatePopulator, populate_template_from_aggregation

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/templates",
    tags=["templates"],
    dependencies=[Depends(get_current_user)]
)

# In-memory storage for template generation jobs (replace with Redis in production)
template_jobs = {}


class TemplatePopulationRequest(BaseModel):
    """Request to populate a template"""
    aggregation_file_path: str
    template_name: Optional[str] = "default"
    add_lineage_sheet: bool = True


class TemplatePopulationResponse(BaseModel):
    """Response for template population request"""
    job_id: str
    status: str
    message: str
    output_path: Optional[str] = None


@router.post("/populate", response_model=TemplatePopulationResponse)
async def populate_template(
    request: TemplatePopulationRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Populate an Excel template with aggregated financial data.

    This endpoint:
    1. Loads aggregated financial data from JSON file
    2. Populates the Excel template with the data
    3. Preserves formulas and formatting
    4. Adds data lineage sheet (optional)
    5. Returns path to populated template
    """
    try:
        # Validate aggregation file exists
        aggregation_path = Path(request.aggregation_file_path)
        if not aggregation_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Aggregation file not found: {request.aggregation_file_path}"
            )

        # Load aggregated data
        with open(aggregation_path, 'r') as f:
            aggregated_data = json.load(f)

        # Determine template path
        templates_dir = Path("data/templates")
        templates_dir.mkdir(parents=True, exist_ok=True)

        if request.template_name == "default":
            template_path = templates_dir / "financial_template.xlsx"
        else:
            template_path = templates_dir / f"{request.template_name}.xlsx"

        if not template_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Template not found: {template_path.name}"
            )

        # Generate job ID
        job_id = f"template_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Initialize job status
        template_jobs[job_id] = {
            "status": "processing",
            "started_at": datetime.now().isoformat(),
            "user": user.get("email", "unknown")
        }

        # Populate template in background
        background_tasks.add_task(
            _populate_template_background,
            job_id,
            str(template_path),
            aggregated_data,
            request.add_lineage_sheet
        )

        logger.info(f"📊 Template population job {job_id} started by {user.get('email')}")

        return TemplatePopulationResponse(
            job_id=job_id,
            status="processing",
            message="Template population started"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting template population: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _populate_template_background(
    job_id: str,
    template_path: str,
    aggregated_data: Dict[str, Any],
    add_lineage_sheet: bool
):
    """Background task to populate template"""
    try:
        # Populate template
        populator = TemplatePopulator(template_path)
        output_path = populator.populate(
            aggregated_data=aggregated_data,
            add_lineage_sheet=add_lineage_sheet
        )

        # Update job status
        template_jobs[job_id].update({
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "output_path": output_path
        })

        logger.info(f"✅ Template population job {job_id} completed: {output_path}")

    except Exception as e:
        logger.error(f"❌ Template population job {job_id} failed: {e}")
        template_jobs[job_id].update({
            "status": "failed",
            "completed_at": datetime.now().isoformat(),
            "error": str(e)
        })


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str, user: dict = Depends(get_current_user)):
    """
    Get status of a template population job.
    """
    if job_id not in template_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return template_jobs[job_id]


@router.get("/download/{job_id}")
async def download_template(job_id: str, user: dict = Depends(get_current_user)):
    """
    Download a populated template.
    """
    if job_id not in template_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = template_jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Current status: {job['status']}"
        )

    output_path = Path(job["output_path"])

    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Template file not found")

    return FileResponse(
        path=output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=output_path.name
    )


@router.post("/populate-from-project/{project_id}")
async def populate_template_from_project(
    project_id: str,
    background_tasks: BackgroundTasks,
    template_name: Optional[str] = "default",
    user: dict = Depends(get_current_user)
):
    """
    Convenience endpoint: Find latest aggregation for a project and populate template.
    """
    # Find latest aggregation file for project
    aggregated_dir = Path("data/aggregated")

    if not aggregated_dir.exists():
        raise HTTPException(
            status_code=404,
            detail="No aggregated data found"
        )

    # Find all aggregation files for this project
    project_files = list(aggregated_dir.glob(f"{project_id}_*.json"))

    if not project_files:
        raise HTTPException(
            status_code=404,
            detail=f"No aggregated data found for project {project_id}"
        )

    # Get most recent file
    latest_file = max(project_files, key=lambda p: p.stat().st_mtime)

    # Use the main populate endpoint
    return await populate_template(
        request=TemplatePopulationRequest(
            aggregation_file_path=str(latest_file),
            template_name=template_name
        ),
        background_tasks=background_tasks,
        user=user
    )


@router.get("/list")
async def list_available_templates(user: dict = Depends(get_current_user)):
    """
    List all available Excel templates.
    """
    templates_dir = Path("data/templates")

    if not templates_dir.exists():
        return {"templates": []}

    templates = []
    for template_file in templates_dir.glob("*.xlsx"):
        templates.append({
            "name": template_file.stem,
            "filename": template_file.name,
            "size_bytes": template_file.stat().st_size,
            "modified_at": datetime.fromtimestamp(template_file.stat().st_mtime).isoformat()
        })

    return {"templates": templates}


@router.get("/jobs")
async def list_template_jobs(user: dict = Depends(get_current_user)):
    """
    List all template population jobs for current user.
    """
    user_email = user.get("email", "unknown")
    user_jobs = {
        job_id: job_data
        for job_id, job_data in template_jobs.items()
        if job_data.get("user") == user_email
    }

    return {"jobs": user_jobs}
