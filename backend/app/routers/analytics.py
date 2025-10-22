"""
Analytics API Router
Endpoints for AI-powered insights and predictions
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.databricks_client import DatabricksClient
from app.routers.auth import get_current_user, User

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/status")
async def get_analytics_status(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Check Databricks connection status"""
    client = DatabricksClient()
    status = client.check_connection()
    return status


@router.get("/predictions/{project_id}")
async def get_predictions(
    project_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get ML predictions for budget categories"""
    client = DatabricksClient()
    predictions = client.get_budget_predictions(project_id)
    return predictions


@router.get("/anomalies/{project_id}")
async def get_anomalies(
    project_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Detect anomalies in project transactions"""
    client = DatabricksClient()
    anomalies = client.detect_anomalies(project_id)
    return anomalies


@router.get("/cash-flow-forecast/{project_id}")
async def get_cash_flow_forecast(
    project_id: str,
    days: int = 30,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get cash flow forecast for project"""
    client = DatabricksClient()
    forecast = client.get_cash_flow_forecast(project_id, days)
    return forecast


@router.get("/recommendations/{project_id}")
async def get_recommendations(
    project_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get AI-powered recommendations for project"""
    client = DatabricksClient()
    recommendations = client.get_smart_recommendations(project_id)
    return recommendations


@router.get("/insights/{project_id}")
async def get_all_insights(
    project_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get all AI insights for project (predictions + anomalies + forecast)"""
    client = DatabricksClient()

    predictions = client.get_budget_predictions(project_id)
    anomalies = client.detect_anomalies(project_id)
    forecast = client.get_cash_flow_forecast(project_id)

    # Calculate summary metrics
    high_risk_predictions = sum(
        1 for p in predictions.get("predictions", [])
        if p.get("risk_level") == "HIGH"
    )

    critical_anomalies = sum(
        1 for a in anomalies.get("anomalies", [])
        if a.get("severity") == "HIGH"
    )

    cash_flow_issues = sum(
        1 for w in forecast.get("weekly_forecast", [])
        if w.get("ending_balance", 0) < 0
    )

    return {
        "summary": {
            "high_risk_predictions": high_risk_predictions,
            "total_predictions": len(predictions.get("predictions", [])),
            "critical_anomalies": critical_anomalies,
            "total_anomalies": anomalies.get("total_anomalies", 0),
            "cash_flow_issues": cash_flow_issues,
            "overall_risk_score": predictions.get("overall_risk_score", 0),
            "overall_risk_level": predictions.get("overall_risk_level", "UNKNOWN")
        },
        "predictions": predictions,
        "anomalies": anomalies,
        "forecast": forecast
    }
