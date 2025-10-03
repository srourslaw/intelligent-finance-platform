"""
Pydantic models for financial data extraction.

This module defines the JSON schema for all extracted financial data,
ensuring type safety and validation across all extraction types
(Excel, PDF, CSV, OCR, etc.).
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class FileType(str, Enum):
    """Supported file types for extraction."""
    EXCEL = "excel"
    PDF = "pdf"
    CSV = "csv"
    IMAGE = "image"
    WORD = "word"
    UNKNOWN = "unknown"


class DocumentType(str, Enum):
    """Financial document classifications."""
    BALANCE_SHEET = "balance_sheet"
    INCOME_STATEMENT = "income_statement"
    CASH_FLOW = "cash_flow"
    GENERAL_LEDGER = "general_ledger"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    BANK_STATEMENT = "bank_statement"
    PAYROLL = "payroll"
    TAX_DOCUMENT = "tax_document"
    BUDGET = "budget"
    EXPENSE_REPORT = "expense_report"
    UNKNOWN = "unknown"


# ============================================================================
# METADATA MODELS
# ============================================================================

class TimePeriod(BaseModel):
    """Time period information for financial data."""
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    period_type: Optional[str] = Field(None, description="monthly, quarterly, yearly, etc.")


class CompanyInfo(BaseModel):
    """Company/project information."""
    name: Optional[str] = None
    department: Optional[str] = None
    project: Optional[str] = None


class FileMetadata(BaseModel):
    """Metadata about the uploaded and processed file."""
    file_id: str = Field(..., description="Unique identifier (hash or UUID)")
    original_filename: str
    file_path: str
    file_type: FileType
    file_size_bytes: int
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    extraction_date: Optional[datetime] = None
    processed_by: str = Field(default="extraction_engine_v1", description="Version of extractor")
    extraction_duration_seconds: Optional[float] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    document_classification: DocumentType = DocumentType.UNKNOWN
    time_period: Optional[TimePeriod] = None
    company_info: Optional[CompanyInfo] = None


# ============================================================================
# LINE ITEM MODELS
# ============================================================================

class FinancialLineItem(BaseModel):
    """A single financial line item with value and source tracking."""
    value: float
    confidence: float = Field(ge=0.0, le=1.0)
    source_location: Optional[str] = Field(None, description="e.g., 'Sheet1!B5', 'Page 2, Line 10'")
    raw_label: Optional[str] = Field(None, description="Original label from source document")
    notes: Optional[str] = None


# ============================================================================
# BALANCE SHEET MODELS
# ============================================================================

class CurrentAssets(BaseModel):
    """Current assets section of balance sheet."""
    cash_on_hand: Optional[FinancialLineItem] = None
    cash_in_bank_operating: Optional[FinancialLineItem] = None
    cash_in_bank_payroll: Optional[FinancialLineItem] = None
    accounts_receivable: Optional[FinancialLineItem] = None
    allowance_for_doubtful_accounts: Optional[FinancialLineItem] = None
    inventory_raw_materials: Optional[FinancialLineItem] = None
    inventory_work_in_progress: Optional[FinancialLineItem] = None
    inventory_finished_goods: Optional[FinancialLineItem] = None
    prepaid_expenses: Optional[FinancialLineItem] = None
    other_current_assets: Optional[FinancialLineItem] = None


class NonCurrentAssets(BaseModel):
    """Non-current (fixed) assets section."""
    land: Optional[FinancialLineItem] = None
    buildings: Optional[FinancialLineItem] = None
    equipment: Optional[FinancialLineItem] = None
    vehicles: Optional[FinancialLineItem] = None
    furniture_and_fixtures: Optional[FinancialLineItem] = None
    accumulated_depreciation: Optional[FinancialLineItem] = None
    intangible_assets: Optional[FinancialLineItem] = None
    long_term_investments: Optional[FinancialLineItem] = None
    other_non_current_assets: Optional[FinancialLineItem] = None


class Assets(BaseModel):
    """All assets."""
    current: Optional[CurrentAssets] = None
    non_current: Optional[NonCurrentAssets] = None


class CurrentLiabilities(BaseModel):
    """Current liabilities section."""
    accounts_payable: Optional[FinancialLineItem] = None
    credit_card_debt: Optional[FinancialLineItem] = None
    short_term_loans: Optional[FinancialLineItem] = None
    current_portion_long_term_debt: Optional[FinancialLineItem] = None
    accrued_expenses: Optional[FinancialLineItem] = None
    taxes_payable: Optional[FinancialLineItem] = None
    unearned_revenue: Optional[FinancialLineItem] = None
    other_current_liabilities: Optional[FinancialLineItem] = None


class LongTermLiabilities(BaseModel):
    """Long-term liabilities section."""
    mortgage_payable: Optional[FinancialLineItem] = None
    long_term_debt: Optional[FinancialLineItem] = None
    bonds_payable: Optional[FinancialLineItem] = None
    deferred_tax_liability: Optional[FinancialLineItem] = None
    other_long_term_liabilities: Optional[FinancialLineItem] = None


class Liabilities(BaseModel):
    """All liabilities."""
    current: Optional[CurrentLiabilities] = None
    long_term: Optional[LongTermLiabilities] = None


class Equity(BaseModel):
    """Equity section."""
    share_capital: Optional[FinancialLineItem] = None
    retained_earnings: Optional[FinancialLineItem] = None
    additional_paid_in_capital: Optional[FinancialLineItem] = None
    treasury_stock: Optional[FinancialLineItem] = None
    other_comprehensive_income: Optional[FinancialLineItem] = None


class BalanceSheet(BaseModel):
    """Complete balance sheet structure."""
    assets: Optional[Assets] = None
    liabilities: Optional[Liabilities] = None
    equity: Optional[Equity] = None


# ============================================================================
# INCOME STATEMENT MODELS
# ============================================================================

class Revenue(BaseModel):
    """Revenue section."""
    product_sales: Optional[FinancialLineItem] = None
    service_revenue: Optional[FinancialLineItem] = None
    other_revenue: Optional[FinancialLineItem] = None
    sales_returns_and_allowances: Optional[FinancialLineItem] = None
    sales_discounts: Optional[FinancialLineItem] = None


class COGS(BaseModel):
    """Cost of Goods Sold section."""
    purchases: Optional[FinancialLineItem] = None
    direct_labor: Optional[FinancialLineItem] = None
    direct_materials: Optional[FinancialLineItem] = None
    manufacturing_overhead: Optional[FinancialLineItem] = None
    freight_in: Optional[FinancialLineItem] = None


class OperatingExpenses(BaseModel):
    """Operating expenses section."""
    salaries_and_wages: Optional[FinancialLineItem] = None
    rent: Optional[FinancialLineItem] = None
    utilities: Optional[FinancialLineItem] = None
    insurance: Optional[FinancialLineItem] = None
    depreciation: Optional[FinancialLineItem] = None
    amortization: Optional[FinancialLineItem] = None
    marketing: Optional[FinancialLineItem] = None
    advertising: Optional[FinancialLineItem] = None
    office_supplies: Optional[FinancialLineItem] = None
    professional_fees: Optional[FinancialLineItem] = None
    repairs_and_maintenance: Optional[FinancialLineItem] = None
    travel: Optional[FinancialLineItem] = None
    meals_and_entertainment: Optional[FinancialLineItem] = None
    telephone: Optional[FinancialLineItem] = None
    internet: Optional[FinancialLineItem] = None
    bad_debt_expense: Optional[FinancialLineItem] = None
    other_operating_expenses: Optional[FinancialLineItem] = None


class OtherIncomeExpense(BaseModel):
    """Other income and expenses (non-operating)."""
    interest_income: Optional[FinancialLineItem] = None
    interest_expense: Optional[FinancialLineItem] = None
    dividend_income: Optional[FinancialLineItem] = None
    gain_loss_on_sale_of_assets: Optional[FinancialLineItem] = None
    other_income: Optional[FinancialLineItem] = None
    other_expense: Optional[FinancialLineItem] = None


class IncomeStatement(BaseModel):
    """Complete income statement structure."""
    revenue: Optional[Revenue] = None
    cogs: Optional[COGS] = None
    operating_expenses: Optional[OperatingExpenses] = None
    other_income_expense: Optional[OtherIncomeExpense] = None


# ============================================================================
# CASH FLOW MODELS
# ============================================================================

class OperatingActivities(BaseModel):
    """Cash flow from operating activities."""
    net_profit: Optional[FinancialLineItem] = None
    depreciation: Optional[FinancialLineItem] = None
    amortization: Optional[FinancialLineItem] = None
    changes_in_accounts_receivable: Optional[FinancialLineItem] = None
    changes_in_inventory: Optional[FinancialLineItem] = None
    changes_in_accounts_payable: Optional[FinancialLineItem] = None
    changes_in_accrued_expenses: Optional[FinancialLineItem] = None
    other_operating_adjustments: Optional[FinancialLineItem] = None


class InvestingActivities(BaseModel):
    """Cash flow from investing activities."""
    purchase_of_ppe: Optional[FinancialLineItem] = None
    sale_of_ppe: Optional[FinancialLineItem] = None
    purchase_of_investments: Optional[FinancialLineItem] = None
    sale_of_investments: Optional[FinancialLineItem] = None
    other_investing_activities: Optional[FinancialLineItem] = None


class FinancingActivities(BaseModel):
    """Cash flow from financing activities."""
    proceeds_from_debt: Optional[FinancialLineItem] = None
    repayment_of_debt: Optional[FinancialLineItem] = None
    proceeds_from_equity: Optional[FinancialLineItem] = None
    dividends_paid: Optional[FinancialLineItem] = None
    other_financing_activities: Optional[FinancialLineItem] = None


class CashFlow(BaseModel):
    """Complete cash flow statement structure."""
    operating: Optional[OperatingActivities] = None
    investing: Optional[InvestingActivities] = None
    financing: Optional[FinancingActivities] = None


# ============================================================================
# TRANSACTION MODEL
# ============================================================================

class Transaction(BaseModel):
    """Individual financial transaction (for invoices, receipts, etc.)."""
    date: Optional[str] = Field(None, description="Transaction date (YYYY-MM-DD)")
    description: str
    category: Optional[str] = Field(None, description="e.g., 'operating_expenses.rent'")
    amount: float
    transaction_type: Literal["income", "expense", "transfer"] = "expense"
    confidence: float = Field(ge=0.0, le=1.0)
    source_location: Optional[str] = None
    vendor: Optional[str] = None
    account: Optional[str] = None
    reference_number: Optional[str] = None


# ============================================================================
# EXTRACTION RESULTS
# ============================================================================

class ExtractionNotes(BaseModel):
    """Notes, warnings, and errors from extraction process."""
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    unmapped_items: List[Dict[str, Any]] = Field(default_factory=list)


class DataQuality(BaseModel):
    """Data quality metrics."""
    completeness_score: float = Field(ge=0.0, le=1.0)
    consistency_check: str = Field(default="not_checked")  # passed, failed, not_checked
    duplicate_check: str = Field(default="not_checked")
    balance_sheet_balanced: Optional[bool] = None
    validation_errors: List[str] = Field(default_factory=list)


class ClassificationStats(BaseModel):
    """Statistics about AI classification."""
    total_items: int = 0
    classified: int = 0
    unmapped: int = 0
    avg_confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ExtractedData(BaseModel):
    """All extracted financial data."""
    balance_sheet: Optional[BalanceSheet] = None
    income_statement: Optional[IncomeStatement] = None
    cash_flow: Optional[CashFlow] = None
    transactions: List[Transaction] = Field(default_factory=list)


# ============================================================================
# MAIN EXTRACTION RESULT MODEL
# ============================================================================

class ExtractionResult(BaseModel):
    """
    Complete extraction result for a single file.

    This is the root model that encompasses all extracted data,
    metadata, validation results, and quality metrics.
    """
    metadata: FileMetadata
    extracted_data: ExtractedData
    extraction_notes: ExtractionNotes = Field(default_factory=ExtractionNotes)
    data_quality: DataQuality = Field(default_factory=DataQuality)
    classification_stats: ClassificationStats = Field(default_factory=ClassificationStats)

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {
                    "file_id": "abc123def456",
                    "original_filename": "Q3_2024_Expenses.xlsx",
                    "file_path": "/uploads/project-a/Q3_2024_Expenses.xlsx",
                    "file_type": "excel",
                    "file_size_bytes": 45678,
                    "document_classification": "expense_report",
                    "confidence_score": 0.95
                },
                "extracted_data": {
                    "income_statement": {
                        "operating_expenses": {
                            "rent": {
                                "value": 3000,
                                "confidence": 0.98,
                                "source_location": "Sheet1!B5",
                                "raw_label": "Office Rent"
                            }
                        }
                    },
                    "transactions": [
                        {
                            "date": "2024-07-15",
                            "description": "Monthly rent payment",
                            "category": "operating_expenses.rent",
                            "amount": 3000,
                            "transaction_type": "expense",
                            "confidence": 0.98
                        }
                    ]
                },
                "data_quality": {
                    "completeness_score": 0.87,
                    "consistency_check": "passed"
                },
                "classification_stats": {
                    "total_items": 45,
                    "classified": 42,
                    "unmapped": 3,
                    "avg_confidence": 0.91
                }
            }
        }


# ============================================================================
# AGGREGATED DATA MODEL (for combining multiple files)
# ============================================================================

class AggregatedFinancialData(BaseModel):
    """
    Aggregated financial data from multiple extraction results.
    Used for consolidation across multiple files.
    """
    project_id: str
    aggregation_date: datetime = Field(default_factory=datetime.utcnow)
    source_file_ids: List[str] = Field(default_factory=list)
    time_period: Optional[TimePeriod] = None

    # Consolidated financial statements
    balance_sheet: Optional[BalanceSheet] = None
    income_statement: Optional[IncomeStatement] = None
    cash_flow: Optional[CashFlow] = None
    transactions: List[Transaction] = Field(default_factory=list)

    # Aggregation metadata
    total_files_processed: int = 0
    conflicts_detected: int = 0
    conflicts_resolved: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "project-a-123-sunset-blvd",
                "source_file_ids": ["abc123", "def456", "ghi789"],
                "total_files_processed": 3,
                "balance_sheet": {
                    "assets": {
                        "current": {
                            "cash_on_hand": {
                                "value": 150000,
                                "confidence": 0.95
                            }
                        }
                    }
                }
            }
        }
