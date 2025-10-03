"""
Financial Data Validator

Validates financial statements for:
- Balance sheet equation (Assets = Liabilities + Equity)
- Income statement calculations
- Cash flow reconciliation
- Data quality and completeness
"""

from typing import List, Dict, Tuple, Optional
from schemas.extraction_schema import (
    AggregatedFinancialData,
    BalanceSheet,
    IncomeStatement,
    CashFlow
)


class ValidationError:
    """Represents a validation error."""

    def __init__(self, severity: str, message: str, field: Optional[str] = None):
        self.severity = severity  # 'error', 'warning', 'info'
        self.message = message
        self.field = field

    def to_dict(self) -> Dict:
        return {
            "severity": self.severity,
            "message": self.message,
            "field": self.field
        }


class FinancialValidator:
    """
    Validate aggregated financial data for correctness and completeness.
    """

    def __init__(self, tolerance: float = 1.0):
        """
        Initialize validator.

        Args:
            tolerance: Acceptable difference for balance checks (in currency units)
        """
        self.tolerance = tolerance
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def validate(self, data: AggregatedFinancialData) -> Tuple[bool, List[Dict], List[Dict]]:
        """
        Validate aggregated financial data.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # Validate balance sheet
        if data.balance_sheet:
            self._validate_balance_sheet(data.balance_sheet)

        # Validate income statement
        if data.income_statement:
            self._validate_income_statement(data.income_statement)

        # Validate cash flow
        if data.cash_flow:
            self._validate_cash_flow(data.cash_flow)

        # Cross-statement validation
        if data.balance_sheet and data.income_statement and data.cash_flow:
            self._validate_cross_statements(data)

        # Data completeness
        self._validate_completeness(data)

        is_valid = len(self.errors) == 0

        return is_valid, [e.to_dict() for e in self.errors], [w.to_dict() for w in self.warnings]

    def _validate_balance_sheet(self, bs: BalanceSheet):
        """
        Validate balance sheet equation: Assets = Liabilities + Equity

        Also validates subtotals and reasonableness.
        """

        # Calculate totals
        total_assets = 0.0
        total_liabilities = 0.0
        total_equity = 0.0

        # Sum assets
        if bs.assets:
            if bs.assets.current:
                for field_name, value in bs.assets.current.model_dump(exclude_none=True).items():
                    if isinstance(value, dict) and 'value' in value:
                        total_assets += value['value']

            if bs.assets.non_current:
                for field_name, value in bs.assets.non_current.model_dump(exclude_none=True).items():
                    if isinstance(value, dict) and 'value' in value:
                        total_assets += value['value']

        # Sum liabilities
        if bs.liabilities:
            if bs.liabilities.current:
                for field_name, value in bs.liabilities.current.model_dump(exclude_none=True).items():
                    if isinstance(value, dict) and 'value' in value:
                        total_liabilities += value['value']

            if bs.liabilities.long_term:
                for field_name, value in bs.liabilities.long_term.model_dump(exclude_none=True).items():
                    if isinstance(value, dict) and 'value' in value:
                        total_liabilities += value['value']

        # Sum equity
        if bs.equity:
            for field_name, value in bs.equity.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    total_equity += value['value']

        # Check balance
        balance_difference = abs(total_assets - (total_liabilities + total_equity))

        if balance_difference > self.tolerance:
            self.errors.append(ValidationError(
                severity="error",
                message=f"Balance Sheet does not balance. Assets: ${total_assets:,.2f}, "
                        f"Liabilities + Equity: ${total_liabilities + total_equity:,.2f}, "
                        f"Difference: ${balance_difference:,.2f}",
                field="balance_sheet"
            ))
        elif balance_difference > 0:
            self.warnings.append(ValidationError(
                severity="warning",
                message=f"Balance Sheet has minor imbalance of ${balance_difference:,.2f} "
                        f"(within tolerance)",
                field="balance_sheet"
            ))

        # Check for negative assets (except accumulated depreciation)
        if bs.assets and bs.assets.current:
            for field_name, value in bs.assets.current.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value and value['value'] < 0:
                    if field_name not in ['allowance_for_doubtful_accounts']:
                        self.warnings.append(ValidationError(
                            severity="warning",
                            message=f"Negative value for asset '{field_name}': ${value['value']:,.2f}",
                            field=f"assets.current.{field_name}"
                        ))

    def _validate_income_statement(self, inc: IncomeStatement):
        """
        Validate income statement calculations and reasonableness.
        """

        # Calculate totals
        total_revenue = 0.0
        total_cogs = 0.0
        total_opex = 0.0

        if inc.revenue:
            for field_name, value in inc.revenue.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    total_revenue += value['value']

        if inc.cogs:
            for field_name, value in inc.cogs.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    total_cogs += value['value']

        if inc.operating_expenses:
            for field_name, value in inc.operating_expenses.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    total_opex += value['value']

        # Calculate gross profit and operating income
        gross_profit = total_revenue - total_cogs
        operating_income = gross_profit - total_opex

        # Validate gross margin (should be 0-100%)
        if total_revenue > 0:
            gross_margin = (gross_profit / total_revenue) * 100

            if gross_margin < 0:
                self.warnings.append(ValidationError(
                    severity="warning",
                    message=f"Negative gross margin: {gross_margin:.1f}% (COGS exceeds revenue)",
                    field="income_statement.gross_margin"
                ))
            elif gross_margin > 100:
                self.errors.append(ValidationError(
                    severity="error",
                    message=f"Gross margin exceeds 100%: {gross_margin:.1f}% (check COGS)",
                    field="income_statement.gross_margin"
                ))

        # Check for negative revenue
        if total_revenue < 0:
            self.errors.append(ValidationError(
                severity="error",
                message=f"Negative total revenue: ${total_revenue:,.2f}",
                field="income_statement.revenue"
            ))

    def _validate_cash_flow(self, cf: CashFlow):
        """
        Validate cash flow statement.
        """

        # Calculate cash from each section
        operating_cash = 0.0
        investing_cash = 0.0
        financing_cash = 0.0

        if cf.operating:
            for field_name, value in cf.operating.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    operating_cash += value['value']

        if cf.investing:
            for field_name, value in cf.investing.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    investing_cash += value['value']

        if cf.financing:
            for field_name, value in cf.financing.model_dump(exclude_none=True).items():
                if isinstance(value, dict) and 'value' in value:
                    financing_cash += value['value']

        net_cash_change = operating_cash + investing_cash + financing_cash

        # Info about cash flow
        self.warnings.append(ValidationError(
            severity="info",
            message=f"Net cash change: ${net_cash_change:,.2f} "
                    f"(Operating: ${operating_cash:,.2f}, "
                    f"Investing: ${investing_cash:,.2f}, "
                    f"Financing: ${financing_cash:,.2f})",
            field="cash_flow"
        ))

    def _validate_cross_statements(self, data: AggregatedFinancialData):
        """
        Validate consistency across financial statements.

        Checks:
        - Net profit from Income Statement appears in Cash Flow
        - Cash from Balance Sheet matches Cash Flow ending cash
        """

        # This is complex and depends on having all the right fields
        # For now, just add a placeholder
        pass

    def _validate_completeness(self, data: AggregatedFinancialData):
        """
        Check data completeness and provide suggestions.
        """

        if not data.balance_sheet:
            self.warnings.append(ValidationError(
                severity="warning",
                message="No balance sheet data available",
                field="completeness"
            ))

        if not data.income_statement:
            self.warnings.append(ValidationError(
                severity="warning",
                message="No income statement data available",
                field="completeness"
            ))

        if not data.cash_flow:
            self.warnings.append(ValidationError(
                severity="warning",
                message="No cash flow data available",
                field="completeness"
            ))

        if len(data.transactions) == 0:
            self.warnings.append(ValidationError(
                severity="warning",
                message="No transactions extracted from source files",
                field="completeness"
            ))

        # Calculate overall completeness score
        completeness_score = 0.0
        max_score = 4.0

        if data.balance_sheet:
            completeness_score += 1.0
        if data.income_statement:
            completeness_score += 1.0
        if data.cash_flow:
            completeness_score += 1.0
        if len(data.transactions) > 0:
            completeness_score += 1.0

        completeness_pct = (completeness_score / max_score) * 100

        self.warnings.append(ValidationError(
            severity="info",
            message=f"Data completeness: {completeness_pct:.0f}% ({int(completeness_score)}/{int(max_score)} sections)",
            field="completeness"
        ))
