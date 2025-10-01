"""
Project data endpoints
"""
from fastapi import APIRouter, HTTPException
from app.services.excel_processor import ExcelProcessor
from app.services.data_aggregator import DataAggregator
from app.models.schemas import DashboardData, HealthCheck
from typing import Dict, Any

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Initialize services
excel_processor = ExcelProcessor()
data_aggregator = DataAggregator()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Check if backend is running and Excel files are accessible"""
    files = excel_processor.check_files_exist()
    files_found = sum(1 for exists in files.values() if exists)

    return {
        "status": "healthy" if files_found > 0 else "warning",
        "message": f"Found {files_found}/4 Excel files",
        "excel_files_found": files_found
    }


@router.get("/dashboard")
async def get_dashboard_data() -> Dict[str, Any]:
    """
    Get complete dashboard data from Excel files
    Returns KPIs, budget, subcontractors, payments, variations, defects, insights
    """
    try:
        # Read all Excel files
        print("Reading Excel files...")

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
async def get_budget_data() -> Dict[str, Any]:
    """Get budget data only"""
    try:
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
async def get_subcontractors() -> Dict[str, Any]:
    """Get subcontractor data"""
    try:
        return excel_processor.read_subcontractors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/client-payments")
async def get_client_payments() -> Dict[str, Any]:
    """Get client payment data"""
    try:
        return excel_processor.read_client_payments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/defects")
async def get_defects() -> Dict[str, Any]:
    """Get defects data"""
    try:
        return excel_processor.read_defects()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timesheets")
async def get_timesheets() -> Dict[str, Any]:
    """Get timesheet data"""
    try:
        return excel_processor.read_timesheets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/purchase-orders")
async def get_purchase_orders() -> Dict[str, Any]:
    """Get purchase orders data"""
    try:
        return excel_processor.read_purchase_orders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cashflow")
async def get_cashflow(weeks: int = 12) -> Dict[str, Any]:
    """Get cashflow forecast"""
    try:
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
async def get_insights() -> Dict[str, Any]:
    """Get AI-generated insights"""
    try:
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
