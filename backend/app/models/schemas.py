"""
Pydantic schemas for API request/response models
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class BudgetItem(BaseModel):
    category: str
    description: str
    budget: float
    actual_spent: float
    committed: float
    forecast: float
    variance: float
    percent_complete: int
    notes: Optional[str] = None


class BudgetSummary(BaseModel):
    total_budget: float
    total_spent: float
    total_committed: float
    total_forecast: float
    total_variance: float
    overall_percent_complete: int
    categories: List[dict]


class Subcontractor(BaseModel):
    id: str
    company_name: str
    contact: str
    phone: str
    email: Optional[str] = None
    abn: str
    license: str
    insurance_expiry: str
    contract_value: float
    status: str


class Payment(BaseModel):
    payment_id: str
    subcontractor: str
    invoice_num: str
    description: str
    amount: float
    gst: float
    total: float
    due_date: str
    status: str


class ClientMilestone(BaseModel):
    milestone: str
    invoice_num: str
    description: str
    amount: float
    due_date: str
    paid_date: Optional[str] = None
    status: str


class Variation(BaseModel):
    vo_num: str
    date: str
    description: str
    cost: float
    client_price: float
    status: str
    invoiced: str


class Defect(BaseModel):
    id: str
    location: str
    trade: str
    description: str
    severity: str
    reported_date: str
    due_date: str
    status: str
    notes: Optional[str] = None


class KPIData(BaseModel):
    total_project_value: float
    total_costs: float
    forecast_cost: float
    projected_profit: float
    completion_percentage: int
    schedule_status: str
    days_behind: int
    revenue_leakage: float


class DashboardData(BaseModel):
    """Complete dashboard data response"""
    kpis: KPIData
    budget_summary: BudgetSummary
    budget_items: List[BudgetItem]
    subcontractors: List[Subcontractor]
    payments: List[Payment]
    milestones: List[ClientMilestone]
    variations: List[Variation]
    defects: List[Defect]


class HealthCheck(BaseModel):
    status: str
    message: str
    excel_files_found: int
