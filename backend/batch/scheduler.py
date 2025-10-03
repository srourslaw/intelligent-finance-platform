"""
Batch Processing Scheduler

Handles scheduled jobs for:
- Periodic aggregations
- Automated file processing
- Scheduled reports
- Maintenance tasks

Uses APScheduler for job scheduling.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore

logger = logging.getLogger(__name__)

# Job configuration storage
JOBS_DIR = Path("data/batch_jobs")
JOBS_DIR.mkdir(parents=True, exist_ok=True)


class BatchScheduler:
    """
    Manages scheduled batch jobs for the ETL system.

    Features:
    - Cron-like scheduling
    - Interval-based scheduling
    - Job persistence
    - Job status tracking
    - Error handling and retry logic
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler(
            jobstores={'default': MemoryJobStore()},
            timezone='UTC'
        )
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self._load_jobs()

    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Batch scheduler started")

    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
            logger.info("Batch scheduler shutdown")

    def add_aggregation_job(
        self,
        job_id: str,
        project_id: str,
        schedule: str,
        file_ids: Optional[list] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Add a scheduled aggregation job.

        Args:
            job_id: Unique identifier for the job
            project_id: Project to aggregate
            schedule: Cron expression (e.g., "0 2 * * *" for 2am daily)
            file_ids: Specific files to aggregate (None = all)
            enabled: Whether job is active

        Returns:
            Job configuration dictionary
        """

        job_config = {
            "job_id": job_id,
            "job_type": "aggregation",
            "project_id": project_id,
            "schedule": schedule,
            "file_ids": file_ids,
            "enabled": enabled,
            "created_at": datetime.utcnow().isoformat(),
            "last_run": None,
            "next_run": None,
            "status": "pending"
        }

        if enabled:
            # Parse cron expression
            trigger = CronTrigger.from_crontab(schedule, timezone='UTC')

            # Add job to scheduler
            self.scheduler.add_job(
                func=self._run_aggregation_job,
                trigger=trigger,
                id=job_id,
                args=[job_id, project_id, file_ids],
                replace_existing=True
            )

            # Get next run time
            job = self.scheduler.get_job(job_id)
            if job:
                job_config["next_run"] = job.next_run_time.isoformat()

        # Save job configuration
        self.jobs[job_id] = job_config
        self._save_job(job_id, job_config)

        logger.info(f"Added aggregation job: {job_id} with schedule: {schedule}")
        return job_config

    def add_interval_job(
        self,
        job_id: str,
        job_type: str,
        interval_minutes: int,
        job_func,
        job_args: tuple = (),
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Add an interval-based job.

        Args:
            job_id: Unique identifier
            job_type: Type of job (e.g., "cleanup", "monitor")
            interval_minutes: Run every N minutes
            job_func: Function to execute
            job_args: Arguments for the function
            enabled: Whether job is active
        """

        job_config = {
            "job_id": job_id,
            "job_type": job_type,
            "interval_minutes": interval_minutes,
            "enabled": enabled,
            "created_at": datetime.utcnow().isoformat(),
            "last_run": None,
            "next_run": None,
            "status": "pending"
        }

        if enabled:
            trigger = IntervalTrigger(minutes=interval_minutes, timezone='UTC')

            self.scheduler.add_job(
                func=job_func,
                trigger=trigger,
                id=job_id,
                args=job_args,
                replace_existing=True
            )

            job = self.scheduler.get_job(job_id)
            if job:
                job_config["next_run"] = job.next_run_time.isoformat()

        self.jobs[job_id] = job_config
        self._save_job(job_id, job_config)

        logger.info(f"Added interval job: {job_id} with interval: {interval_minutes} minutes")
        return job_config

    def remove_job(self, job_id: str) -> bool:
        """Remove a scheduled job."""
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]

            # Delete job file
            job_file = JOBS_DIR / f"{job_id}.json"
            if job_file.exists():
                job_file.unlink()

            logger.info(f"Removed job: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing job {job_id}: {e}")
            return False

    def pause_job(self, job_id: str) -> bool:
        """Pause a scheduled job."""
        try:
            self.scheduler.pause_job(job_id)
            if job_id in self.jobs:
                self.jobs[job_id]["enabled"] = False
                self._save_job(job_id, self.jobs[job_id])
            logger.info(f"Paused job: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error pausing job {job_id}: {e}")
            return False

    def resume_job(self, job_id: str) -> bool:
        """Resume a paused job."""
        try:
            self.scheduler.resume_job(job_id)
            if job_id in self.jobs:
                self.jobs[job_id]["enabled"] = True
                self._save_job(job_id, self.jobs[job_id])
            logger.info(f"Resumed job: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error resuming job {job_id}: {e}")
            return False

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job configuration."""
        if job_id in self.jobs:
            job_config = self.jobs[job_id].copy()

            # Update next_run from scheduler
            scheduled_job = self.scheduler.get_job(job_id)
            if scheduled_job:
                job_config["next_run"] = scheduled_job.next_run_time.isoformat()

            return job_config
        return None

    def list_jobs(self) -> list:
        """List all jobs."""
        jobs_list = []
        for job_id, config in self.jobs.items():
            job_info = config.copy()

            # Update next_run from scheduler
            scheduled_job = self.scheduler.get_job(job_id)
            if scheduled_job:
                job_info["next_run"] = scheduled_job.next_run_time.isoformat()

            jobs_list.append(job_info)

        return jobs_list

    def _run_aggregation_job(self, job_id: str, project_id: str, file_ids: Optional[list]):
        """
        Execute aggregation job.

        This is called by the scheduler. It imports the aggregation engine
        and runs the aggregation process.
        """
        logger.info(f"Starting aggregation job: {job_id} for project: {project_id}")

        try:
            # Update job status
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "running"
                self.jobs[job_id]["last_run"] = datetime.utcnow().isoformat()
                self._save_job(job_id, self.jobs[job_id])

            # Import here to avoid circular dependencies
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent))

            from aggregation.engine import AggregationEngine, load_extraction_results
            from validation.validator import FinancialValidator

            # Load extraction results
            extraction_dir = Path("data/extractions")
            if file_ids:
                # Load specific files
                from schemas.extraction_schema import ExtractionResult
                extraction_results = []
                for file_id in file_ids:
                    file_path = extraction_dir / f"{file_id}.json"
                    if file_path.exists():
                        with file_path.open("r") as f:
                            data = json.load(f)
                            extraction_results.append(ExtractionResult(**data))
            else:
                # Load all files
                extraction_results = load_extraction_results(extraction_dir)

            if not extraction_results:
                logger.warning(f"No extraction results found for job: {job_id}")
                if job_id in self.jobs:
                    self.jobs[job_id]["status"] = "no_data"
                    self._save_job(job_id, self.jobs[job_id])
                return

            # Run aggregation
            engine = AggregationEngine()
            aggregated_data = engine.aggregate_extractions(
                extraction_results=extraction_results,
                project_id=project_id,
                time_period=None
            )

            # Validate
            validator = FinancialValidator(tolerance=1.0)
            is_valid, errors, warnings = validator.validate(aggregated_data)

            # Save results
            aggregation_dir = Path("data/aggregations")
            aggregation_file = aggregation_dir / f"{project_id}.json"
            with aggregation_file.open("w") as f:
                json.dump(aggregated_data.model_dump(mode='json'), f, indent=2, default=str)

            validation_file = aggregation_dir / f"{project_id}_validation.json"
            with validation_file.open("w") as f:
                json.dump({
                    "project_id": project_id,
                    "validation_date": datetime.utcnow().isoformat(),
                    "is_valid": is_valid,
                    "errors": errors,
                    "warnings": warnings
                }, f, indent=2)

            # Update job status
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "completed"
                self.jobs[job_id]["last_result"] = {
                    "files_processed": aggregated_data.total_files_processed,
                    "transactions": len(aggregated_data.transactions),
                    "is_valid": is_valid,
                    "errors": len(errors),
                    "warnings": len(warnings)
                }
                self._save_job(job_id, self.jobs[job_id])

            logger.info(f"Completed aggregation job: {job_id}")

        except Exception as e:
            logger.error(f"Error in aggregation job {job_id}: {e}", exc_info=True)
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "failed"
                self.jobs[job_id]["last_error"] = str(e)
                self._save_job(job_id, self.jobs[job_id])

    def _save_job(self, job_id: str, config: Dict[str, Any]):
        """Save job configuration to disk."""
        job_file = JOBS_DIR / f"{job_id}.json"
        with job_file.open("w") as f:
            json.dump(config, f, indent=2)

    def _load_jobs(self):
        """Load job configurations from disk."""
        for job_file in JOBS_DIR.glob("*.json"):
            try:
                with job_file.open("r") as f:
                    config = json.load(f)
                    job_id = config["job_id"]
                    self.jobs[job_id] = config

                    # Re-add to scheduler if enabled
                    if config.get("enabled", False):
                        if config["job_type"] == "aggregation":
                            trigger = CronTrigger.from_crontab(config["schedule"], timezone='UTC')
                            self.scheduler.add_job(
                                func=self._run_aggregation_job,
                                trigger=trigger,
                                id=job_id,
                                args=[job_id, config["project_id"], config.get("file_ids")],
                                replace_existing=True
                            )

                logger.info(f"Loaded job: {job_id}")
            except Exception as e:
                logger.error(f"Error loading job {job_file}: {e}")


# Global scheduler instance
_scheduler: Optional[BatchScheduler] = None


def get_scheduler() -> BatchScheduler:
    """Get or create the global scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = BatchScheduler()
        _scheduler.start()
    return _scheduler


def shutdown_scheduler():
    """Shutdown the global scheduler."""
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown()
        _scheduler = None
