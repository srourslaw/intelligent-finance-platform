"""
Batch Processing API Routes

Endpoints for managing scheduled jobs and batch operations.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from app.auth_utils import get_current_user
from batch.scheduler import get_scheduler

router = APIRouter(prefix="/api/batch", tags=["batch"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateAggregationJobRequest(BaseModel):
    """Request to create a scheduled aggregation job."""
    job_id: str
    project_id: str
    schedule: str  # Cron expression
    file_ids: Optional[List[str]] = None
    enabled: bool = True


class JobResponse(BaseModel):
    """Response with job details."""
    job_id: str
    job_type: str
    project_id: Optional[str] = None
    schedule: Optional[str] = None
    interval_minutes: Optional[int] = None
    enabled: bool
    created_at: str
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    status: str
    last_result: Optional[dict] = None
    last_error: Optional[str] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/jobs/aggregation", response_model=JobResponse)
async def create_aggregation_job(
    request: CreateAggregationJobRequest,
    user: dict = Depends(get_current_user)
):
    """
    Create a scheduled aggregation job.

    Schedule format (cron expression):
    - "0 2 * * *" = Daily at 2am
    - "0 */4 * * *" = Every 4 hours
    - "0 0 * * 0" = Weekly on Sunday at midnight
    - "0 0 1 * *" = Monthly on 1st at midnight

    Examples:
    ```json
    {
      "job_id": "daily_aggregation",
      "project_id": "Q4_2024",
      "schedule": "0 2 * * *",
      "enabled": true
    }
    ```
    """

    scheduler = get_scheduler()

    try:
        job_config = scheduler.add_aggregation_job(
            job_id=request.job_id,
            project_id=request.project_id,
            schedule=request.schedule,
            file_ids=request.file_ids,
            enabled=request.enabled
        )

        return JobResponse(**job_config)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid schedule: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get("/jobs", response_model=List[JobResponse])
async def list_jobs(
    user: dict = Depends(get_current_user)
):
    """
    List all scheduled jobs.

    Returns all jobs with their current status, next run time, and last results.
    """

    scheduler = get_scheduler()
    jobs = scheduler.list_jobs()

    return [JobResponse(**job) for job in jobs]


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Get details for a specific job.
    """

    scheduler = get_scheduler()
    job_config = scheduler.get_job(job_id)

    if not job_config:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    return JobResponse(**job_config)


@router.post("/jobs/{job_id}/pause")
async def pause_job(
    job_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Pause a scheduled job.

    The job will not run until resumed.
    """

    scheduler = get_scheduler()
    success = scheduler.pause_job(job_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found or cannot be paused")

    return {"message": f"Job '{job_id}' paused", "job_id": job_id, "status": "paused"}


@router.post("/jobs/{job_id}/resume")
async def resume_job(
    job_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Resume a paused job.
    """

    scheduler = get_scheduler()
    success = scheduler.resume_job(job_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found or cannot be resumed")

    return {"message": f"Job '{job_id}' resumed", "job_id": job_id, "status": "active"}


@router.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Delete a scheduled job permanently.

    This removes the job from the scheduler and deletes its configuration.
    """

    scheduler = get_scheduler()
    success = scheduler.remove_job(job_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    return {"message": f"Job '{job_id}' deleted", "job_id": job_id}


@router.post("/jobs/{job_id}/run")
async def run_job_now(
    job_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Trigger a job to run immediately (outside its schedule).

    This runs the job once without affecting its schedule.
    """

    scheduler = get_scheduler()
    job_config = scheduler.get_job(job_id)

    if not job_config:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    try:
        # Trigger the job
        if job_config["job_type"] == "aggregation":
            scheduler._run_aggregation_job(
                job_id,
                job_config["project_id"],
                job_config.get("file_ids")
            )

        return {
            "message": f"Job '{job_id}' triggered",
            "job_id": job_id,
            "status": "running"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run job: {str(e)}")


@router.get("/health")
async def batch_health():
    """
    Health check for batch processing service.
    """

    scheduler = get_scheduler()
    jobs = scheduler.list_jobs()

    return {
        "status": "healthy",
        "service": "batch_processing",
        "scheduler_running": scheduler.scheduler.running,
        "total_jobs": len(jobs),
        "enabled_jobs": len([j for j in jobs if j["enabled"]]),
        "active_jobs": len([j for j in jobs if j["status"] == "running"])
    }
