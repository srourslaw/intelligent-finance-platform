"""
Bulk File Extraction Service
Extracts data from all PDFs and Excel files in a project folder
"""
import os
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.extraction import ExtractionJob, ExtractedData, JobStatus
from app.services.mineru_service import extract_with_mineru
import openpyxl
import pandas as pd


class FileExtractor:
    """Extract data from all files in a project directory"""

    def __init__(self, project_id: str, db: Session):
        self.project_id = project_id
        self.db = db
        self.base_path = Path(__file__).parent.parent.parent / "projects" / project_id / "data"
        self.supported_extensions = {
            'pdf': ['.pdf'],
            'excel': ['.xlsx', '.xls'],
            'csv': ['.csv']
        }

    def scan_files(self) -> List[Dict[str, str]]:
        """
        Scan project data folder for all supported files.

        Returns:
            List of file info dicts with path, name, type
        """
        files = []

        if not self.base_path.exists():
            return files

        # Recursively scan all files
        for root, dirs, filenames in os.walk(self.base_path):
            for filename in filenames:
                file_path = Path(root) / filename
                extension = file_path.suffix.lower()

                # Determine file type
                file_type = None
                if extension in self.supported_extensions['pdf']:
                    file_type = 'pdf'
                elif extension in self.supported_extensions['excel']:
                    file_type = 'excel'
                elif extension in self.supported_extensions['csv']:
                    file_type = 'csv'

                if file_type:
                    files.append({
                        'path': str(file_path),
                        'name': filename,
                        'type': file_type,
                        'size': file_path.stat().st_size
                    })

        return files

    def create_extraction_job(self) -> str:
        """
        Create a new extraction job in database.

        Returns:
            job_id string
        """
        files = self.scan_files()
        job_id = f"job_{uuid.uuid4().hex[:12]}"

        job = ExtractionJob(
            job_id=job_id,
            project_id=self.project_id,
            status=JobStatus.PENDING,
            total_files=len(files),
            processed_files=0,
            failed_files=0,
            progress_percent=0.0
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job_id

    def extract_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF using MinerU.

        Args:
            file_path: Absolute path to PDF file

        Returns:
            Dict with raw_text and extraction_status
        """
        try:
            result = extract_with_mineru(file_path)

            if result.get('success'):
                return {
                    'raw_text': result.get('text', ''),
                    'extraction_status': 'success',
                    'extraction_method': 'mineru',
                    'error_message': None
                }
            else:
                return {
                    'raw_text': '',
                    'extraction_status': 'failed',
                    'extraction_method': 'mineru',
                    'error_message': result.get('error', 'Unknown error')
                }
        except Exception as e:
            return {
                'raw_text': '',
                'extraction_status': 'failed',
                'extraction_method': 'mineru',
                'error_message': str(e)
            }

    def extract_excel(self, file_path: str) -> Dict[str, Any]:
        """
        Extract structured data from Excel file.

        Args:
            file_path: Absolute path to Excel file

        Returns:
            Dict with structured_data (JSON string) and extraction_status
        """
        try:
            # Use pandas for robust Excel reading
            df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets

            # Convert to structured format
            structured_data = {}
            raw_text_parts = []

            for sheet_name, sheet_df in df.items():
                # Convert sheet to dict
                sheet_data = sheet_df.to_dict(orient='records')
                structured_data[sheet_name] = sheet_data

                # Also create text representation for searching
                for row in sheet_data:
                    row_text = ' | '.join([f"{k}: {v}" for k, v in row.items() if pd.notna(v)])
                    raw_text_parts.append(row_text)

            return {
                'raw_text': '\n'.join(raw_text_parts),
                'structured_data': json.dumps(structured_data),
                'extraction_status': 'success',
                'extraction_method': 'pandas',
                'error_message': None
            }
        except Exception as e:
            return {
                'raw_text': '',
                'structured_data': None,
                'extraction_status': 'failed',
                'extraction_method': 'pandas',
                'error_message': str(e)
            }

    def extract_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from CSV file.

        Args:
            file_path: Absolute path to CSV file

        Returns:
            Dict with structured_data and extraction_status
        """
        try:
            df = pd.read_csv(file_path)

            # Convert to structured format
            structured_data = df.to_dict(orient='records')

            # Create text representation
            raw_text_parts = []
            for row in structured_data:
                row_text = ' | '.join([f"{k}: {v}" for k, v in row.items() if pd.notna(v)])
                raw_text_parts.append(row_text)

            return {
                'raw_text': '\n'.join(raw_text_parts),
                'structured_data': json.dumps(structured_data),
                'extraction_status': 'success',
                'extraction_method': 'pandas',
                'error_message': None
            }
        except Exception as e:
            return {
                'raw_text': '',
                'structured_data': None,
                'extraction_status': 'failed',
                'extraction_method': 'pandas',
                'error_message': str(e)
            }

    def process_single_file(self, file_info: Dict[str, str], job_id: str) -> bool:
        """
        Process a single file and store extracted data.

        Args:
            file_info: Dict with file path, name, type
            job_id: Job identifier

        Returns:
            True if successful, False if failed
        """
        file_type = file_info['type']
        file_path = file_info['path']

        # Extract based on file type
        if file_type == 'pdf':
            extraction_result = self.extract_pdf(file_path)
        elif file_type == 'excel':
            extraction_result = self.extract_excel(file_path)
        elif file_type == 'csv':
            extraction_result = self.extract_csv(file_path)
        else:
            return False

        # Store in database
        extracted_data = ExtractedData(
            job_id=job_id,
            project_id=self.project_id,
            file_path=file_path,
            file_name=file_info['name'],
            file_type=file_type,
            extraction_method=extraction_result.get('extraction_method'),
            raw_text=extraction_result.get('raw_text'),
            structured_data=extraction_result.get('structured_data'),
            extraction_status=extraction_result.get('extraction_status'),
            error_message=extraction_result.get('error_message')
        )

        self.db.add(extracted_data)
        self.db.commit()

        return extraction_result['extraction_status'] == 'success'

    def run_extraction(self, job_id: str):
        """
        Run full extraction for all files in project.

        Args:
            job_id: Job identifier
        """
        # Get job from database
        job = self.db.query(ExtractionJob).filter(ExtractionJob.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job {job_id} not found")

        # Update status to processing
        job.status = JobStatus.PROCESSING
        self.db.commit()

        # Scan files
        files = self.scan_files()
        total_files = len(files)

        # Process each file
        for idx, file_info in enumerate(files):
            try:
                success = self.process_single_file(file_info, job_id)

                # Update progress
                job.processed_files = idx + 1
                if not success:
                    job.failed_files += 1

                job.progress_percent = (job.processed_files / total_files) * 100
                self.db.commit()

            except Exception as e:
                job.failed_files += 1
                job.processed_files = idx + 1
                job.progress_percent = (job.processed_files / total_files) * 100
                self.db.commit()

        # Mark job as completed
        job.status = JobStatus.COMPLETED
        job.progress_percent = 100.0
        self.db.commit()

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current status of extraction job.

        Args:
            job_id: Job identifier

        Returns:
            Dict with job status information
        """
        job = self.db.query(ExtractionJob).filter(ExtractionJob.job_id == job_id).first()

        if not job:
            return None

        return {
            'job_id': job.job_id,
            'project_id': job.project_id,
            'status': job.status.value,
            'total_files': job.total_files,
            'processed_files': job.processed_files,
            'failed_files': job.failed_files,
            'progress_percent': job.progress_percent,
            'error_message': job.error_message,
            'metadata': job.job_metadata,  # JSON string with pipeline results
            'created_at': job.created_at.isoformat() if job.created_at else None,
            'updated_at': job.updated_at.isoformat() if job.updated_at else None
        }


def start_extraction(project_id: str, db: Session) -> str:
    """
    Main function to start bulk extraction for a project.

    Args:
        project_id: Project identifier
        db: Database session

    Returns:
        job_id string
    """
    extractor = FileExtractor(project_id, db)
    job_id = extractor.create_extraction_job()

    # Run extraction (in production, this should be a background task)
    extractor.run_extraction(job_id)

    return job_id


def get_extraction_status(job_id: str, db: Session) -> Optional[Dict[str, Any]]:
    """
    Get status of an extraction job.

    Args:
        job_id: Job identifier
        db: Database session

    Returns:
        Job status dict or None
    """
    extractor = FileExtractor("", db)  # project_id not needed for status check
    return extractor.get_job_status(job_id)
