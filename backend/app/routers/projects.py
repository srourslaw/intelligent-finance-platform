"""
Project data endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from app.services.excel_processor import ExcelProcessor
from app.services.data_aggregator import DataAggregator
from app.models.schemas import DashboardData, HealthCheck
from app.routers.auth import get_current_user, User
from typing import Dict, Any, List
from pathlib import Path
import json

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Services will be initialized per-request with project_id
data_aggregator = DataAggregator()


@router.get("/list")
async def list_projects(current_user: User = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """List all available projects"""
    try:
        projects_dir = Path(__file__).parent.parent.parent / "projects"

        if not projects_dir.exists():
            return []

        projects = []
        for project_folder in projects_dir.iterdir():
            if project_folder.is_dir():
                project_info_file = project_folder / "project_info.json"

                if project_info_file.exists():
                    with open(project_info_file, 'r') as f:
                        project_info = json.load(f)
                        projects.append(project_info)

        # Sort by project name
        projects.sort(key=lambda x: x.get('project_name', ''))

        return projects
    except Exception as e:
        print(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthCheck)
async def health_check(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
):
    """Check if backend is running and Excel files are accessible"""
    excel_processor = ExcelProcessor(project_id=project_id)
    files = excel_processor.check_files_exist()
    files_found = sum(1 for exists in files.values() if exists)

    return {
        "status": "healthy" if files_found > 0 else "warning",
        "message": f"Found {files_found}/6 Excel files for {project_id}",
        "excel_files_found": files_found
    }


@router.get("/dashboard")
async def get_dashboard_data(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get complete dashboard data from Excel files for a specific project
    Returns KPIs, budget, subcontractors, payments, variations, defects, insights
    """
    try:
        # Initialize processor for this project
        excel_processor = ExcelProcessor(project_id=project_id)

        # Read all Excel files
        print(f"Reading Excel files for project: {project_id}")

        budget_data = excel_processor.read_budget_file()
        budget_items = budget_data.get("items", [])

        subcontractor_data = excel_processor.read_subcontractors()
        subcontractors = subcontractor_data.get("subcontractors", [])
        payments = subcontractor_data.get("payments", [])

        client_data = excel_processor.read_client_payments()
        milestones = client_data.get("milestones", [])
        variations = client_data.get("variations", [])

        defects_data = excel_processor.read_defects()
        defects = defects_data.get("defects", [])

        # Calculate KPIs and aggregations
        kpis = data_aggregator.calculate_kpis(budget_items, variations)
        budget_summary = data_aggregator.get_budget_summary(budget_items)
        critical_issues = data_aggregator.identify_critical_issues(
            payments, milestones, defects, variations
        )
        cashflow = data_aggregator.get_cashflow_forecast(budget_items, milestones, variations)
        insights = data_aggregator.generate_insights(
            budget_items, subcontractors, payments, milestones, variations, defects
        )

        print(f"Dashboard data prepared:")
        print(f"  - Budget items: {len(budget_items)}")
        print(f"  - Subcontractors: {len(subcontractors)}")
        print(f"  - Payments: {len(payments)}")
        print(f"  - Milestones: {len(milestones)}")
        print(f"  - Variations: {len(variations)}")
        print(f"  - Defects: {len(defects)}")
        print(f"  - Critical issues: {len(critical_issues)}")
        print(f"  - Insights: {len(insights)}")

        return {
            "kpis": kpis,
            "budget_summary": budget_summary,
            "budget_items": budget_items[:20],  # Limit to first 20 for initial load
            "subcontractors": subcontractors,
            "payments": payments,
            "milestones": milestones,
            "variations": variations,
            "defects": defects,
            "critical_issues": critical_issues,
            "cashflow": cashflow,
            "insights": insights
        }

    except Exception as e:
        print(f"Error in get_dashboard_data: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading Excel files: {str(e)}")


@router.get("/budget")
async def get_budget_data(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get budget data for a specific project"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)
        budget_data = excel_processor.read_budget_file()
        budget_items = budget_data.get("items", [])
        budget_summary = data_aggregator.get_budget_summary(budget_items)

        return {
            "summary": budget_summary,
            "items": budget_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subcontractors")
async def get_subcontractors(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get subcontractor data"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)
        return excel_processor.read_subcontractors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/client-payments")
async def get_client_payments(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get client payment data"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)
        return excel_processor.read_client_payments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/defects")
async def get_defects(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get defects data"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)
        return excel_processor.read_defects()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timesheets")
async def get_timesheets(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get timesheet data"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)
        return excel_processor.read_timesheets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/purchase-orders")
async def get_purchase_orders(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get purchase orders data"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)
        return excel_processor.read_purchase_orders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cashflow")
async def get_cashflow(
    weeks: int = 12,
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get cashflow forecast"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)

        budget_data = excel_processor.read_budget_file()
        budget_items = budget_data.get("items", [])

        client_data = excel_processor.read_client_payments()
        milestones = client_data.get("milestones", [])
        variations = client_data.get("variations", [])

        cashflow = data_aggregator.get_cashflow_forecast(budget_items, milestones, variations, weeks)
        return cashflow
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def get_insights(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get AI-generated insights"""
    try:
        excel_processor = ExcelProcessor(project_id=project_id)

        # Read all Excel files
        budget_data = excel_processor.read_budget_file()
        budget_items = budget_data.get("items", [])

        subcontractor_data = excel_processor.read_subcontractors()
        subcontractors = subcontractor_data.get("subcontractors", [])
        payments = subcontractor_data.get("payments", [])

        client_data = excel_processor.read_client_payments()
        milestones = client_data.get("milestones", [])
        variations = client_data.get("variations", [])

        defects_data = excel_processor.read_defects()
        defects = defects_data.get("defects", [])

        insights = data_aggregator.generate_insights(
            budget_items, subcontractors, payments, milestones, variations, defects
        )

        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
