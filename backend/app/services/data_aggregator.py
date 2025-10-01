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

    @staticmethod
    def get_cashflow_forecast(
        budget_items: List[Dict],
        milestones: List[Dict],
        variations: List[Dict],
        weeks: int = 12
    ) -> Dict[str, Any]:
        """Generate cashflow forecast for next N weeks"""
        from datetime import datetime, timedelta

        # Calculate weekly burn rate from budget
        total_forecast = sum(item['forecast'] for item in budget_items)
        total_spent = sum(item['actual_spent'] for item in budget_items)
        remaining_spend = total_forecast - total_spent

        # Average weekly burn rate
        weekly_burn_rate = remaining_spend / weeks if weeks > 0 else 0

        # Expected income from milestones and variations
        expected_income = sum(m['amount'] for m in milestones if m['status'].upper() in ['PENDING', 'SUBMITTED'])
        expected_income += sum(v['client_price'] for v in variations if v['status'].upper() == 'APPROVED' and v['invoiced'].upper() == 'NO')

        # Generate weekly forecast
        weekly_forecast = []
        current_date = datetime.now()
        cumulative_cash = 0

        for week in range(weeks):
            week_start = current_date + timedelta(weeks=week)
            week_end = week_start + timedelta(days=6)

            # Estimate cash in/out for the week
            cash_in = expected_income / weeks if weeks > 0 else 0
            cash_out = weekly_burn_rate
            net_cash = cash_in - cash_out
            cumulative_cash += net_cash

            weekly_forecast.append({
                "week": week + 1,
                "week_start": week_start.strftime("%Y-%m-%d"),
                "week_end": week_end.strftime("%Y-%m-%d"),
                "cash_in": round(cash_in, 2),
                "cash_out": round(cash_out, 2),
                "net_cash": round(net_cash, 2),
                "cumulative_cash": round(cumulative_cash, 2)
            })

        return {
            "forecast_weeks": weeks,
            "weekly_burn_rate": round(weekly_burn_rate, 2),
            "expected_income": round(expected_income, 2),
            "weekly_forecast": weekly_forecast
        }

    @staticmethod
    def generate_insights(
        budget_items: List[Dict],
        subcontractors: List[Dict],
        payments: List[Dict],
        milestones: List[Dict],
        variations: List[Dict],
        defects: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Generate AI-style insights from project data"""

        insights = []

        # Budget variance insights
        over_budget_items = [item for item in budget_items if item['variance'] < -1000]
        if over_budget_items:
            total_overrun = sum(abs(item['variance']) for item in over_budget_items)
            insights.append({
                "type": "budget_variance",
                "priority": "high",
                "title": "Budget Overruns Detected",
                "message": f"{len(over_budget_items)} line items are over budget by ${total_overrun:,.2f} total",
                "recommendation": "Review cost allocation and consider value engineering opportunities",
                "data": {"count": len(over_budget_items), "amount": total_overrun}
            })

        # Cash flow insight
        total_budget = 650000
        total_spent = sum(item['actual_spent'] for item in budget_items)
        burn_rate = (total_spent / total_budget * 100) if total_budget > 0 else 0

        completion_rate = sum(item['percent_complete'] for item in budget_items) / len(budget_items) if budget_items else 0

        if burn_rate > completion_rate + 10:
            insights.append({
                "type": "cash_flow",
                "priority": "critical",
                "title": "Spending Outpacing Progress",
                "message": f"You've spent {burn_rate:.1f}% of budget but only completed {completion_rate:.1f}% of work",
                "recommendation": "Investigate cost overruns and accelerate completion of in-progress items",
                "data": {"burn_rate": burn_rate, "completion_rate": completion_rate}
            })

        # Revenue leakage insight
        uninvoiced_variations = [v for v in variations if v['status'].upper() == 'APPROVED' and v['invoiced'].upper() == 'NO']
        if uninvoiced_variations:
            revenue_loss = sum(v['client_price'] for v in uninvoiced_variations)
            insights.append({
                "type": "revenue_opportunity",
                "priority": "high",
                "title": "Uninvoiced Approved Variations",
                "message": f"${revenue_loss:,.2f} in approved variations not yet invoiced",
                "recommendation": "Issue invoices immediately to improve cash flow and recover costs",
                "data": {"count": len(uninvoiced_variations), "amount": revenue_loss}
            })

        # Subcontractor payment insight
        overdue_payments = [p for p in payments if p['status'].upper() == 'OVERDUE']
        if overdue_payments:
            total_overdue = sum(p['total'] for p in overdue_payments)
            insights.append({
                "type": "payment_risk",
                "priority": "high",
                "title": "Overdue Subcontractor Payments",
                "message": f"{len(overdue_payments)} payment(s) overdue totaling ${total_overdue:,.2f}",
                "recommendation": "Prioritize payments to maintain contractor relationships and avoid work stoppages",
                "data": {"count": len(overdue_payments), "amount": total_overdue}
            })

        # Defect trend insight
        critical_defects = [d for d in defects if d['severity'].upper() == 'CRITICAL']
        if critical_defects:
            insights.append({
                "type": "quality_risk",
                "priority": "critical",
                "title": "Critical Defects Require Attention",
                "message": f"{len(critical_defects)} critical defect(s) blocking project handover",
                "recommendation": "Mobilize resources to resolve critical defects immediately",
                "data": {"count": len(critical_defects)}
            })

        # Completion forecast
        if budget_items:
            avg_completion = sum(item['percent_complete'] for item in budget_items) / len(budget_items)
            if avg_completion > 80:
                insights.append({
                    "type": "milestone",
                    "priority": "medium",
                    "title": "Project Nearing Completion",
                    "message": f"Project is {avg_completion:.1f}% complete - prepare for handover activities",
                    "recommendation": "Schedule final inspections, prepare documentation, and plan defect rectification",
                    "data": {"completion_rate": avg_completion}
                })

        return insights
