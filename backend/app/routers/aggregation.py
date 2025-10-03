"""
Aggregation API Routes - Combine multiple extraction results into consolidated financial data.

Endpoints:
- POST /aggregate - Trigger aggregation of extraction results
- GET /result/{project_id} - Get aggregated financial data
- GET /validate/{project_id} - Get validation results for aggregated data
- GET /list - List all aggregations for the current user
- DELETE /{project_id} - Delete aggregation result
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional
from datetime import datetime
import json

from app.auth_utils import get_current_user
from schemas.extraction_schema import (
    AggregatedFinancialData,
    ExtractionResult,
    TimePeriod
)
from aggregation.engine import AggregationEngine, load_extraction_results
from validation.validator import FinancialValidator

router = APIRouter(prefix="/aggregation", tags=["aggregation"])

# Storage paths
AGGREGATION_DIR = Path("data/aggregations")
EXTRACTION_DIR = Path("data/extractions")
AGGREGATION_DIR.mkdir(parents=True, exist_ok=True)


def get_aggregation_path(project_id: str) -> Path:
    """Get file path for aggregation result."""
    return AGGREGATION_DIR / f"{project_id}.json"


def get_validation_path(project_id: str) -> Path:
    """Get file path for validation result."""
    return AGGREGATION_DIR / f"{project_id}_validation.json"


def save_aggregation_result(project_id: str, aggregated_data: AggregatedFinancialData):
    """Save aggregation result to JSON file."""
    file_path = get_aggregation_path(project_id)

    with file_path.open("w") as f:
        json.dump(aggregated_data.model_dump(mode='json'), f, indent=2, default=str)


def load_aggregation_result(project_id: str) -> Optional[AggregatedFinancialData]:
    """Load aggregation result from JSON file."""
    file_path = get_aggregation_path(project_id)

    if not file_path.exists():
        return None

    with file_path.open("r") as f:
        data = json.load(f)
        return AggregatedFinancialData(**data)


def save_validation_result(project_id: str, validation_data: Dict):
    """Save validation result to JSON file."""
    file_path = get_validation_path(project_id)

    with file_path.open("w") as f:
        json.dump(validation_data, f, indent=2)


def load_validation_result(project_id: str) -> Optional[Dict]:
    """Load validation result from JSON file."""
    file_path = get_validation_path(project_id)

    if not file_path.exists():
        return None

    with file_path.open("r") as f:
        return json.load(f)


@router.post("/aggregate")
async def create_aggregation(
    project_id: str = Query(..., description="Project identifier for this aggregation"),
    file_ids: Optional[List[str]] = Query(None, description="Specific file IDs to aggregate (if None, aggregates all)"),
    time_period_start: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    time_period_end: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Aggregate multiple extraction results into consolidated financial data.

    This endpoint:
    1. Loads specified extraction results (or all if file_ids not provided)
    2. Combines transactions and removes duplicates
    3. Builds consolidated Balance Sheet, Income Statement, Cash Flow
    4. Validates the aggregated data
    5. Saves results to disk

    Args:
        project_id: Unique identifier for this aggregation (e.g., "Q1_2024", "annual_2023")
        file_ids: Optional list of specific file IDs to include
        time_period_start: Optional start date for filtering transactions
        time_period_end: Optional end date for filtering transactions

    Returns:
        Aggregation summary with file count, validation status, and project_id
    """

    try:
        # Load extraction results
        if file_ids:
            # Load specific files
            extraction_results = []
            for file_id in file_ids:
                file_path = EXTRACTION_DIR / f"{file_id}.json"
                if file_path.exists():
                    with file_path.open("r") as f:
                        data = json.load(f)
                        extraction_results.append(ExtractionResult(**data))
                else:
                    raise HTTPException(status_code=404, detail=f"File {file_id} not found")
        else:
            # Load all extraction results
            extraction_results = load_extraction_results(EXTRACTION_DIR)

        if not extraction_results:
            raise HTTPException(status_code=400, detail="No extraction results found to aggregate")

        # Create time period if provided
        time_period = None
        if time_period_start and time_period_end:
            time_period = TimePeriod(
                start_date=time_period_start,
                end_date=time_period_end,
                period_type="custom"
            )

        # Run aggregation
        engine = AggregationEngine()
        aggregated_data = engine.aggregate_extractions(
            extraction_results=extraction_results,
            project_id=project_id,
            time_period=time_period
        )

        # Validate aggregated data
        validator = FinancialValidator(tolerance=1.0)
        is_valid, errors, warnings = validator.validate(aggregated_data)

        # Save aggregation result
        save_aggregation_result(project_id, aggregated_data)

        # Save validation result
        validation_result = {
            "project_id": project_id,
            "validation_date": datetime.utcnow().isoformat(),
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings
        }
        save_validation_result(project_id, validation_result)

        return {
            "project_id": project_id,
            "status": "completed",
            "files_processed": aggregated_data.total_files_processed,
            "transactions_aggregated": len(aggregated_data.transactions),
            "duplicates_removed": engine.duplicates_removed,
            "conflicts_detected": aggregated_data.conflicts_detected,
            "conflicts_resolved": aggregated_data.conflicts_resolved,
            "validation": {
                "is_valid": is_valid,
                "error_count": len(errors),
                "warning_count": len(warnings)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Aggregation failed: {str(e)}")


@router.get("/result/{project_id}")
async def get_aggregation_result(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get aggregated financial data for a project.

    Returns the complete AggregatedFinancialData including:
    - Balance Sheet (Assets, Liabilities, Equity)
    - Income Statement (Revenue, COGS, Operating Expenses)
    - Cash Flow (Operating, Investing, Financing)
    - All aggregated transactions
    - Data lineage and source file tracking
    """

    aggregated_data = load_aggregation_result(project_id)

    if not aggregated_data:
        raise HTTPException(status_code=404, detail=f"Aggregation '{project_id}' not found")

    return aggregated_data


@router.get("/validate/{project_id}")
async def get_validation_result(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get validation results for aggregated data.

    Returns:
    - is_valid: Whether data passes all validation checks
    - errors: Critical issues that need fixing (e.g., balance sheet doesn't balance)
    - warnings: Non-critical issues or suggestions (e.g., negative gross margin)
    """

    validation_result = load_validation_result(project_id)

    if not validation_result:
        raise HTTPException(status_code=404, detail=f"Validation for '{project_id}' not found")

    return validation_result


@router.get("/list")
async def list_aggregations(
    current_user: dict = Depends(get_current_user)
):
    """
    List all aggregations for the current user.

    Returns summary information for each aggregation including:
    - project_id
    - aggregation_date
    - file count
    - validation status
    """

    aggregations = []

    for json_file in AGGREGATION_DIR.glob("*.json"):
        # Skip validation files
        if "_validation" in json_file.name:
            continue

        try:
            with json_file.open("r") as f:
                data = json.load(f)

                # Load validation data if exists
                project_id = json_file.stem
                validation = load_validation_result(project_id)

                aggregations.append({
                    "project_id": data.get("project_id"),
                    "aggregation_date": data.get("aggregation_date"),
                    "total_files_processed": data.get("total_files_processed"),
                    "transaction_count": len(data.get("transactions", [])),
                    "has_balance_sheet": data.get("balance_sheet") is not None,
                    "has_income_statement": data.get("income_statement") is not None,
                    "has_cash_flow": data.get("cash_flow") is not None,
                    "validation": {
                        "is_valid": validation.get("is_valid") if validation else None,
                        "error_count": len(validation.get("errors", [])) if validation else 0,
                        "warning_count": len(validation.get("warnings", [])) if validation else 0
                    } if validation else None
                })
        except Exception as e:
            print(f"Error loading aggregation {json_file}: {e}")
            continue

    # Sort by aggregation date (newest first)
    aggregations.sort(key=lambda x: x.get("aggregation_date", ""), reverse=True)

    return aggregations


@router.delete("/{project_id}")
async def delete_aggregation(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete aggregation and validation results for a project.
    """

    aggregation_file = get_aggregation_path(project_id)
    validation_file = get_validation_path(project_id)

    if not aggregation_file.exists():
        raise HTTPException(status_code=404, detail=f"Aggregation '{project_id}' not found")

    # Delete files
    aggregation_file.unlink()
    if validation_file.exists():
        validation_file.unlink()

    return {"message": f"Aggregation '{project_id}' deleted successfully"}


@router.get("/health")
async def health_check():
    """Health check endpoint for aggregation service."""
    return {
        "status": "healthy",
        "service": "aggregation",
        "aggregation_count": len(list(AGGREGATION_DIR.glob("*.json"))) // 2  # Divide by 2 to exclude validation files
    }
