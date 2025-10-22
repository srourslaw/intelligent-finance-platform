"""
Databricks Client Service
Connects FastAPI backend to Databricks for ML predictions and analytics
"""
import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd


class DatabricksClient:
    """Client for Databricks REST API and SQL Analytics"""

    def __init__(self):
        # These will be set from environment variables
        self.workspace_url = os.getenv("DATABRICKS_WORKSPACE_URL", "")
        self.token = os.getenv("DATABRICKS_TOKEN", "")
        self.cluster_id = os.getenv("DATABRICKS_CLUSTER_ID", "")

        # For local development/demo mode
        self.demo_mode = not self.workspace_url or not self.token

        if self.demo_mode:
            print("⚠️ Databricks running in DEMO MODE (no credentials found)")
            print("   Set DATABRICKS_WORKSPACE_URL and DATABRICKS_TOKEN for production")
        else:
            print(f"✓ Databricks client initialized: {self.workspace_url}")

    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make authenticated request to Databricks API"""
        if self.demo_mode:
            return self._demo_response(endpoint)

        url = f"{self.workspace_url}/api/2.0/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Databricks API error: {e}")
            return {"error": str(e)}

    def _demo_response(self, endpoint: str) -> Dict:
        """Return demo data when Databricks is not configured"""
        if "predict" in endpoint:
            return self._demo_predictions()
        elif "anomaly" in endpoint:
            return self._demo_anomalies()
        elif "forecast" in endpoint:
            return self._demo_forecast()
        return {"demo": True, "message": "Databricks not configured"}

    def _demo_predictions(self) -> Dict:
        """Demo budget predictions"""
        return {
            "demo_mode": True,
            "predictions": [
                {
                    "category": "Materials",
                    "current_spent": 168000,
                    "budget": 250000,
                    "predicted_final": 285000,
                    "predicted_overrun": 35000,
                    "confidence": 0.87,
                    "risk_level": "HIGH",
                    "weeks_to_overrun": 3,
                    "recommendation": "Review concrete supplier contracts. Consider bulk ordering to reduce per-unit costs."
                },
                {
                    "category": "Labour",
                    "current_spent": 45000,
                    "budget": 180000,
                    "predicted_final": 171000,
                    "predicted_overrun": -9000,
                    "confidence": 0.92,
                    "risk_level": "LOW",
                    "weeks_to_overrun": None,
                    "recommendation": "On track to finish under budget. Maintain current pace."
                },
                {
                    "category": "Subcontractors",
                    "current_spent": 89000,
                    "budget": 150000,
                    "predicted_final": 156000,
                    "predicted_overrun": 6000,
                    "confidence": 0.78,
                    "risk_level": "MEDIUM",
                    "weeks_to_overrun": 6,
                    "recommendation": "Minor overrun expected. Review scope with electrical subcontractor."
                }
            ],
            "overall_risk_score": 72,
            "overall_risk_level": "MODERATE",
            "generated_at": datetime.now().isoformat()
        }

    def _demo_anomalies(self) -> Dict:
        """Demo anomaly detection"""
        return {
            "demo_mode": True,
            "anomalies": [
                {
                    "id": "ANO-001",
                    "transaction_id": "BM-1234",
                    "date": "2024-09-20",
                    "description": "Concrete Mix - 40MPa",
                    "amount": 168000,
                    "category": "Materials",
                    "anomaly_type": "PRICE_SPIKE",
                    "severity": "HIGH",
                    "confidence": 0.94,
                    "details": "This purchase is 340% higher than typical concrete orders",
                    "historical_average": 49000,
                    "standard_deviations": 3.8,
                    "recommendation": "Verify quantity and pricing with supplier. Check for billing error.",
                    "auto_flagged": True
                },
                {
                    "id": "ANO-002",
                    "transaction_id": "PAY-456",
                    "date": "2024-09-18",
                    "description": "Duplicate invoice detected",
                    "amount": 7000,
                    "category": "Subcontractors",
                    "anomaly_type": "DUPLICATE",
                    "severity": "MEDIUM",
                    "confidence": 0.89,
                    "details": "Similar transaction found 2 days earlier",
                    "recommendation": "Review payment records. Possible duplicate billing.",
                    "auto_flagged": True
                }
            ],
            "total_anomalies": 2,
            "high_severity": 1,
            "medium_severity": 1,
            "low_severity": 0,
            "generated_at": datetime.now().isoformat()
        }

    def _demo_forecast(self) -> Dict:
        """Demo cash flow forecast"""
        today = datetime.now()
        return {
            "demo_mode": True,
            "forecast_period_days": 30,
            "weekly_forecast": [
                {
                    "week": 1,
                    "start_date": (today + timedelta(days=0)).strftime("%Y-%m-%d"),
                    "end_date": (today + timedelta(days=6)).strftime("%Y-%m-%d"),
                    "expected_inflow": 125000,
                    "expected_outflow": 45000,
                    "net_change": 80000,
                    "ending_balance": 234000,
                    "risk_level": "LOW",
                    "major_items": [
                        {"type": "inflow", "description": "Client Milestone 3 Payment", "amount": 125000}
                    ]
                },
                {
                    "week": 2,
                    "start_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "end_date": (today + timedelta(days=13)).strftime("%Y-%m-%d"),
                    "expected_inflow": 0,
                    "expected_outflow": 89000,
                    "net_change": -89000,
                    "ending_balance": 145000,
                    "risk_level": "LOW",
                    "major_items": [
                        {"type": "outflow", "description": "Subcontractor payments due", "amount": 89000}
                    ]
                },
                {
                    "week": 3,
                    "start_date": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
                    "end_date": (today + timedelta(days=20)).strftime("%Y-%m-%d"),
                    "expected_inflow": 0,
                    "expected_outflow": 156000,
                    "net_change": -156000,
                    "ending_balance": -11000,
                    "risk_level": "CRITICAL",
                    "major_items": [
                        {"type": "outflow", "description": "Materials delivery payment", "amount": 156000}
                    ]
                },
                {
                    "week": 4,
                    "start_date": (today + timedelta(days=21)).strftime("%Y-%m-%d"),
                    "end_date": (today + timedelta(days=27)).strftime("%Y-%m-%d"),
                    "expected_inflow": 0,
                    "expected_outflow": 23000,
                    "net_change": -23000,
                    "ending_balance": -34000,
                    "risk_level": "CRITICAL",
                    "major_items": [
                        {"type": "outflow", "description": "Labour payments", "amount": 23000}
                    ]
                }
            ],
            "recommendations": [
                {
                    "priority": "HIGH",
                    "title": "Cash Flow Crisis in Week 3",
                    "description": "Balance will go negative by $11,000 in week 3",
                    "actions": [
                        "Delay Week 3 material order by 5-7 days",
                        "Accelerate client milestone 4 payment",
                        "Arrange short-term credit line ($50,000)"
                    ]
                },
                {
                    "priority": "MEDIUM",
                    "title": "Maintain Minimum Balance",
                    "description": "Recommended minimum balance: $100,000",
                    "actions": [
                        "Restructure payment schedule",
                        "Negotiate extended payment terms with suppliers"
                    ]
                }
            ],
            "minimum_balance": -34000,
            "minimum_balance_date": (today + timedelta(days=27)).strftime("%Y-%m-%d"),
            "risk_assessment": "HIGH - Immediate action required",
            "generated_at": datetime.now().isoformat()
        }

    # Public API methods

    def get_budget_predictions(self, project_id: str) -> Dict[str, Any]:
        """Get ML predictions for budget categories"""
        endpoint = f"sql/statements/execute/{project_id}/predict"
        return self._make_request(endpoint)

    def detect_anomalies(self, project_id: str) -> Dict[str, Any]:
        """Detect anomalies in transactions"""
        endpoint = f"sql/statements/execute/{project_id}/anomalies"
        return self._make_request(endpoint)

    def get_cash_flow_forecast(self, project_id: str, days: int = 30) -> Dict[str, Any]:
        """Get cash flow forecast"""
        endpoint = f"sql/statements/execute/{project_id}/forecast?days={days}"
        return self._make_request(endpoint)

    def get_smart_recommendations(self, project_id: str) -> Dict[str, Any]:
        """Get AI-powered budget recommendations"""
        predictions = self.get_budget_predictions(project_id)
        anomalies = self.detect_anomalies(project_id)
        forecast = self.get_cash_flow_forecast(project_id)

        return {
            "predictions": predictions,
            "anomalies": anomalies,
            "forecast": forecast,
            "generated_at": datetime.now().isoformat()
        }

    def check_connection(self) -> Dict[str, Any]:
        """Check if Databricks connection is working"""
        if self.demo_mode:
            return {
                "status": "demo_mode",
                "connected": False,
                "message": "Running in demo mode. Set DATABRICKS credentials for production.",
                "demo_features_available": True
            }

        try:
            response = self._make_request("clusters/get", method="GET")
            return {
                "status": "connected",
                "connected": True,
                "workspace": self.workspace_url,
                "cluster_id": self.cluster_id
            }
        except Exception as e:
            return {
                "status": "error",
                "connected": False,
                "error": str(e)
            }
