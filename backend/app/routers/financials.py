"""
Financial consolidation endpoints
Serves AI-consolidated financial data to the dashboard
"""
from fastapi import APIRouter, HTTPException, Depends
from app.routers.auth import get_current_user, User
from typing import Dict, Any
from pathlib import Path
import json

router = APIRouter(prefix="/api/financials", tags=["financials"])


@router.get("/consolidated")
async def get_consolidated_financials(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get AI-consolidated financial data for a project

    Returns:
        - Balance Sheet data (assets, liabilities, equity)
        - Income Statement data (revenue, expenses, profit)
        - Financial metrics and ratios
        - Classification statistics
    """
    try:
        # Load consolidated data from JSON output
        consolidated_file = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "consolidated_data.json"

        if not consolidated_file.exists():
            raise HTTPException(
                status_code=404,
                detail="Consolidated data not found. Run the consolidation pipeline first."
            )

        with open(consolidated_file, 'r') as f:
            data = json.load(f)

        return {
            "project_id": project_id,
            "consolidated_data": data.get("consolidated_data", {}),
            "totals": data.get("totals", {}),
            "status": "success"
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Consolidated financial data not found"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/line-items")
async def get_classified_line_items(
    project_id: str = "project-a-123-sunset-blvd",
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get classified line items with confidence scores

    Args:
        limit: Maximum number of items to return (default 100)
    """
    try:
        classified_file = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "classified_items.json"

        if not classified_file.exists():
            raise HTTPException(
                status_code=404,
                detail="Classified items not found"
            )

        with open(classified_file, 'r') as f:
            data = json.load(f)

        items = data.get("classified_items", [])

        return {
            "project_id": project_id,
            "total_items": len(items),
            "items": items[:limit],
            "showing": min(limit, len(items))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/balance-sheet")
async def get_balance_sheet(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get Balance Sheet data in structured format
    """
    try:
        consolidated_file = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "consolidated_data.json"

        with open(consolidated_file, 'r') as f:
            data = json.load(f)

        consolidated = data.get("consolidated_data", {})
        totals = data.get("totals", {})

        return {
            "project_id": project_id,
            "balance_sheet": {
                "assets": {
                    "current": {
                        "items": consolidated.get("current_assets", {}),
                        "total": totals.get("current_assets", 0)
                    },
                    "non_current": {
                        "items": consolidated.get("non_current_assets", {}),
                        "total": totals.get("non_current_assets", 0)
                    },
                    "total": totals.get("total_assets", 0)
                },
                "liabilities": {
                    "current": {
                        "items": consolidated.get("current_liabilities", {}),
                        "total": totals.get("current_liabilities", 0)
                    },
                    "long_term": {
                        "items": consolidated.get("long_term_liabilities", {}),
                        "total": totals.get("long_term_liabilities", 0)
                    },
                    "total": totals.get("total_liabilities", 0)
                },
                "equity": {
                    "items": consolidated.get("equity", {}),
                    "total": totals.get("total_equity", 0)
                },
                "balance_check": totals.get("balance_check", 0)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/income-statement")
async def get_income_statement(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get Income Statement (P&L) data in structured format
    """
    try:
        consolidated_file = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "consolidated_data.json"

        with open(consolidated_file, 'r') as f:
            data = json.load(f)

        consolidated = data.get("consolidated_data", {})
        totals = data.get("totals", {})

        # Calculate margins
        revenue = totals.get("total_revenue", 0)
        gross_margin = (totals.get("gross_profit", 0) / revenue * 100) if revenue > 0 else 0
        operating_margin = (totals.get("operating_income", 0) / revenue * 100) if revenue > 0 else 0
        net_margin = (totals.get("net_income", 0) / revenue * 100) if revenue > 0 else 0

        return {
            "project_id": project_id,
            "income_statement": {
                "revenue": {
                    "items": consolidated.get("revenue", {}),
                    "total": revenue
                },
                "cost_of_goods_sold": {
                    "items": consolidated.get("cost_of_goods_sold", {}),
                    "total": totals.get("total_cogs", 0)
                },
                "gross_profit": {
                    "amount": totals.get("gross_profit", 0),
                    "margin_percent": gross_margin
                },
                "operating_expenses": {
                    "items": consolidated.get("operating_expenses", {}),
                    "total": totals.get("total_operating_expenses", 0)
                },
                "operating_income": {
                    "amount": totals.get("operating_income", 0),
                    "margin_percent": operating_margin
                },
                "other_income": {
                    "items": consolidated.get("other_income", {}),
                    "total": totals.get("total_other_income", 0)
                },
                "other_expenses": {
                    "items": consolidated.get("other_expenses", {}),
                    "total": totals.get("total_other_expenses", 0)
                },
                "net_income": {
                    "amount": totals.get("net_income", 0),
                    "margin_percent": net_margin
                }
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/financial-ratios")
async def get_financial_ratios(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Calculate and return key financial ratios
    """
    try:
        consolidated_file = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "consolidated_data.json"

        with open(consolidated_file, 'r') as f:
            data = json.load(f)

        totals = data.get("totals", {})

        # Extract values
        current_assets = totals.get("current_assets", 0)
        current_liabilities = totals.get("current_liabilities", 0)
        total_assets = totals.get("total_assets", 0)
        total_liabilities = totals.get("total_liabilities", 0)
        total_equity = totals.get("total_equity", 0)
        revenue = totals.get("total_revenue", 0)
        gross_profit = totals.get("gross_profit", 0)
        operating_income = totals.get("operating_income", 0)
        net_income = totals.get("net_income", 0)

        # Calculate ratios
        ratios = {
            "liquidity": {
                "current_ratio": current_assets / current_liabilities if current_liabilities > 0 else 0,
                "working_capital": current_assets - current_liabilities
            },
            "profitability": {
                "gross_profit_margin": (gross_profit / revenue * 100) if revenue > 0 else 0,
                "operating_margin": (operating_income / revenue * 100) if revenue > 0 else 0,
                "net_profit_margin": (net_income / revenue * 100) if revenue > 0 else 0,
                "roa": (net_income / total_assets * 100) if total_assets > 0 else 0,
                "roe": (net_income / total_equity * 100) if total_equity > 0 else 0
            },
            "leverage": {
                "debt_to_equity": total_liabilities / total_equity if total_equity > 0 else 0,
                "debt_to_assets": total_liabilities / total_assets if total_assets > 0 else 0,
                "equity_ratio": total_equity / total_assets if total_assets > 0 else 0
            }
        }

        return {
            "project_id": project_id,
            "ratios": ratios
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run-consolidation")
async def run_consolidation(
    project_id: str = "project-a-123-sunset-blvd",
    excel_only: bool = True,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Run the AI consolidation pipeline to regenerate financial data

    Args:
        excel_only: Process only Excel files (faster, default True)
    """
    try:
        from financial_consolidation.main import FinancialConsolidationPipeline

        # Run pipeline
        pipeline = FinancialConsolidationPipeline()
        pipeline.run(excel_only=excel_only, save_intermediates=True)

        return {
            "status": "success",
            "message": "Financial consolidation completed",
            "project_id": project_id,
            "files_processed": len(pipeline.file_inventory),
            "line_items_extracted": len(pipeline.all_line_items),
            "classification_rate": f"{(len([i for i in pipeline.classified_items if i['classification'] == 'classified']) / len(pipeline.classified_items) * 100):.1f}%"
            if pipeline.classified_items else "0%"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consolidation failed: {str(e)}")


@router.get("/stats")
async def get_consolidation_stats(
    project_id: str = "project-a-123-sunset-blvd",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get statistics about the consolidation process
    """
    try:
        # Load various stats from output files
        file_inventory_path = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "file_inventory.json"
        classified_items_path = Path(__file__).parent.parent.parent / "financial_consolidation" / "output" / "classified_items.json"

        stats = {}

        if file_inventory_path.exists():
            with open(file_inventory_path, 'r') as f:
                inventory = json.load(f)
                stats["files_discovered"] = inventory.get("total_files", 0)
                stats["scan_date"] = inventory.get("scan_date")

        if classified_items_path.exists():
            with open(classified_items_path, 'r') as f:
                classified = json.load(f)
                items = classified.get("classified_items", [])
                total = len(items)
                classified_count = sum(1 for i in items if i.get("classification") == "classified")

                stats["total_line_items"] = total
                stats["classified_items"] = classified_count
                stats["unclassified_items"] = total - classified_count
                stats["classification_rate"] = f"{(classified_count / total * 100):.1f}%" if total > 0 else "0%"

        return {
            "project_id": project_id,
            "stats": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
