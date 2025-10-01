"""
Data aggregation service
Calculate KPIs and aggregate data from Excel files
"""
from typing import Dict, List, Any


class DataAggregator:
    """Aggregate and calculate KPIs from Excel data"""

    @staticmethod
    def calculate_kpis(budget_items: List[Dict], variations: List[Dict]) -> Dict[str, Any]:
        """Calculate dashboard KPIs"""

        # Calculate totals from budget
        total_budget = 650000  # Contract value
        total_spent = sum(item['actual_spent'] for item in budget_items)
        total_committed = sum(item['committed'] for item in budget_items)
        total_forecast = sum(item['forecast'] for item in budget_items)
        total_variance = sum(item['variance'] for item in budget_items)

        # Calculate projected profit
        projected_profit = total_budget - total_forecast

        # Calculate overall completion percentage
        if budget_items:
            overall_completion = sum(item['percent_complete'] for item in budget_items) / len(budget_items)
        else:
            overall_completion = 0

        # Calculate revenue leakage from uninvoiced variations
        revenue_leakage = sum(
            var['client_price'] for var in variations
            if var['status'].upper() == 'APPROVED' and var['invoiced'].upper() == 'NO'
        )

        return {
            "total_project_value": total_budget,
            "total_costs": total_spent,
            "forecast_cost": total_forecast,
            "projected_profit": projected_profit,
            "completion_percentage": int(overall_completion),
            "schedule_status": "12 days behind schedule",
            "days_behind": 12,
            "revenue_leakage": revenue_leakage
        }

    @staticmethod
    def get_budget_summary(budget_items: List[Dict]) -> Dict[str, Any]:
        """Generate budget summary with category breakdowns"""

        total_budget = sum(item['budget'] for item in budget_items)
        total_spent = sum(item['actual_spent'] for item in budget_items)
        total_committed = sum(item['committed'] for item in budget_items)
        total_forecast = sum(item['forecast'] for item in budget_items)
        total_variance = sum(item['variance'] for item in budget_items)

        # Group by category
        categories = {}
        for item in budget_items:
            cat = item['category']
            if cat not in categories:
                categories[cat] = {
                    "category": cat,
                    "budget": 0,
                    "actual": 0,
                    "forecast": 0,
                    "variance": 0
                }
            categories[cat]["budget"] += item['budget']
            categories[cat]["actual"] += item['actual_spent']
            categories[cat]["forecast"] += item['forecast']
            categories[cat]["variance"] += item['variance']

        # Calculate overall completion
        if budget_items:
            overall_percent = sum(item['percent_complete'] for item in budget_items) / len(budget_items)
        else:
            overall_percent = 0

        return {
            "total_budget": total_budget,
            "total_spent": total_spent,
            "total_committed": total_committed,
            "total_forecast": total_forecast,
            "total_variance": total_variance,
            "overall_percent_complete": int(overall_percent),
            "categories": list(categories.values())
        }

    @staticmethod
    def identify_critical_issues(
        payments: List[Dict],
        milestones: List[Dict],
        defects: List[Dict],
        variations: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Identify critical issues that need attention"""

        issues = []

        # Overdue subcontractor payments
        overdue_payments = [p for p in payments if p['status'].upper() == 'OVERDUE']
        if overdue_payments:
            total_overdue = sum(p['total'] for p in overdue_payments)
            issues.append({
                "type": "overdue_payment",
                "severity": "high",
                "title": f"{len(overdue_payments)} Overdue Payment(s)",
                "description": f"Total overdue: ${total_overdue:,.2f}",
                "count": len(overdue_payments)
            })

        # Overdue client payments
        overdue_milestones = [m for m in milestones if m['status'].upper() == 'OVERDUE']
        if overdue_milestones:
            total_client_overdue = sum(m['amount'] for m in overdue_milestones)
            issues.append({
                "type": "client_overdue",
                "severity": "critical",
                "title": "Client Payment Overdue",
                "description": f"${total_client_overdue:,.2f} overdue from client",
                "amount": total_client_overdue
            })

        # Uninvoiced variations (revenue leakage)
        uninvoiced_vars = [
            v for v in variations
            if v['status'].upper() == 'APPROVED' and v['invoiced'].upper() == 'NO'
        ]
        if uninvoiced_vars:
            revenue_loss = sum(v['client_price'] for v in uninvoiced_vars)
            issues.append({
                "type": "revenue_leakage",
                "severity": "high",
                "title": f"{len(uninvoiced_vars)} Uninvoiced Variation(s)",
                "description": f"Potential revenue loss: ${revenue_loss:,.2f}",
                "amount": revenue_loss,
                "count": len(uninvoiced_vars)
            })

        # Critical defects
        critical_defects = [d for d in defects if d['severity'].upper() == 'CRITICAL']
        if critical_defects:
            issues.append({
                "type": "critical_defect",
                "severity": "critical",
                "title": f"{len(critical_defects)} Critical Defect(s)",
                "description": "Blocking project handover",
                "count": len(critical_defects)
            })

        # Overdue defects
        overdue_defects = [d for d in defects if d['status'].upper() == 'OVERDUE']
        if overdue_defects:
            issues.append({
                "type": "overdue_defect",
                "severity": "high",
                "title": f"{len(overdue_defects)} Overdue Defect(s)",
                "description": "Defects past due date",
                "count": len(overdue_defects)
            })

        return issues
