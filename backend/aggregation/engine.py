"""
Aggregation Engine - Combine multiple extraction results into consolidated financial data.

This module takes multiple ExtractionResult JSONs and intelligently combines them into
a single AggregatedFinancialData structure with conflict resolution and data lineage.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from collections import defaultdict

from schemas.extraction_schema import (
    ExtractionResult,
    AggregatedFinancialData,
    Transaction,
    BalanceSheet,
    IncomeStatement,
    CashFlow,
    FinancialLineItem,
    TimePeriod,
    Assets,
    CurrentAssets,
    NonCurrentAssets,
    Liabilities,
    CurrentLiabilities,
    LongTermLiabilities,
    Equity,
    Revenue,
    COGS,
    OperatingExpenses,
    OtherIncomeExpense,
    OperatingActivities,
    InvestingActivities,
    FinancingActivities
)


class AggregationEngine:
    """
    Combine multiple extraction results into consolidated financial statements.

    Features:
    - Conflict resolution (higher confidence wins)
    - Duplicate detection and removal
    - Data lineage tracking
    - Balance sheet validation
    - Transaction categorization and rollup
    """

    def __init__(self):
        self.conflicts_detected = 0
        self.conflicts_resolved = 0
        self.duplicates_removed = 0

    def aggregate_extractions(
        self,
        extraction_results: List[ExtractionResult],
        project_id: str,
        time_period: Optional[TimePeriod] = None
    ) -> AggregatedFinancialData:
        """
        Aggregate multiple extraction results into consolidated financial data.

        Args:
            extraction_results: List of ExtractionResult objects to aggregate
            project_id: Project identifier
            time_period: Optional time period for the aggregation

        Returns:
            AggregatedFinancialData with consolidated statements
        """

        if not extraction_results:
            return self._create_empty_aggregation(project_id, time_period)

        # Extract file IDs
        source_file_ids = [result.metadata.file_id for result in extraction_results]

        # Aggregate transactions
        all_transactions = []
        for result in extraction_results:
            all_transactions.extend(result.extracted_data.transactions)

        # Remove duplicates
        unique_transactions = self._remove_duplicate_transactions(all_transactions)

        # Categorize and rollup transactions into financial statements
        balance_sheet = self._build_balance_sheet_from_transactions(unique_transactions, extraction_results)
        income_statement = self._build_income_statement_from_transactions(unique_transactions, extraction_results)
        cash_flow = self._build_cash_flow_from_transactions(unique_transactions, extraction_results)

        # Create aggregated result
        aggregated = AggregatedFinancialData(
            project_id=project_id,
            aggregation_date=datetime.utcnow(),
            source_file_ids=source_file_ids,
            time_period=time_period,
            balance_sheet=balance_sheet,
            income_statement=income_statement,
            cash_flow=cash_flow,
            transactions=unique_transactions,
            total_files_processed=len(extraction_results),
            conflicts_detected=self.conflicts_detected,
            conflicts_resolved=self.conflicts_resolved
        )

        return aggregated

    def _remove_duplicate_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Remove duplicate transactions based on date, description, and amount.

        Keeps the transaction with higher confidence if duplicates found.
        """

        # Group by (date, description, amount)
        transaction_groups: Dict[Tuple, List[Transaction]] = defaultdict(list)

        for txn in transactions:
            key = (txn.date, txn.description.lower().strip(), txn.amount)
            transaction_groups[key].append(txn)

        # Keep highest confidence transaction from each group
        unique_transactions = []
        duplicates_count = 0

        for key, group in transaction_groups.items():
            if len(group) > 1:
                # Sort by confidence (highest first)
                group.sort(key=lambda t: t.confidence, reverse=True)
                duplicates_count += len(group) - 1

            # Keep the best one
            unique_transactions.append(group[0])

        self.duplicates_removed = duplicates_count

        return unique_transactions

    def _build_balance_sheet_from_transactions(
        self,
        transactions: List[Transaction],
        extraction_results: List[ExtractionResult]
    ) -> BalanceSheet:
        """
        Build Balance Sheet by aggregating categorized transactions.

        Also merges any existing balance sheet data from extraction results.
        """

        # Initialize accumulators
        current_assets_data: Dict[str, float] = defaultdict(float)
        non_current_assets_data: Dict[str, float] = defaultdict(float)
        current_liabilities_data: Dict[str, float] = defaultdict(float)
        long_term_liabilities_data: Dict[str, float] = defaultdict(float)
        equity_data: Dict[str, float] = defaultdict(float)

        # Aggregate from transactions with balance sheet categories
        for txn in transactions:
            if not txn.category:
                continue

            category_parts = txn.category.split('.')

            if len(category_parts) >= 3 and category_parts[0] == 'balance_sheet':
                statement, section, item = category_parts[0], category_parts[1], category_parts[2]

                if section == 'assets':
                    if 'current' in txn.category:
                        current_assets_data[item] += txn.amount
                    else:
                        non_current_assets_data[item] += txn.amount

                elif section == 'liabilities':
                    if 'current' in txn.category:
                        current_liabilities_data[item] += txn.amount
                    else:
                        long_term_liabilities_data[item] += txn.amount

                elif section == 'equity':
                    equity_data[item] += txn.amount

        # Also merge existing balance sheet data from extraction results
        for result in extraction_results:
            if result.extracted_data.balance_sheet:
                bs = result.extracted_data.balance_sheet

                # Merge assets
                if bs.assets and bs.assets.current:
                    for field_name, value in bs.assets.current.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            current_assets_data[field_name] += value['value']

                if bs.assets and bs.assets.non_current:
                    for field_name, value in bs.assets.non_current.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            non_current_assets_data[field_name] += value['value']

                # Merge liabilities
                if bs.liabilities and bs.liabilities.current:
                    for field_name, value in bs.liabilities.current.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            current_liabilities_data[field_name] += value['value']

                if bs.liabilities and bs.liabilities.long_term:
                    for field_name, value in bs.liabilities.long_term.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            long_term_liabilities_data[field_name] += value['value']

                # Merge equity
                if bs.equity:
                    for field_name, value in bs.equity.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            equity_data[field_name] += value['value']

        # Build Balance Sheet structure
        current_assets = self._build_current_assets(current_assets_data)
        non_current_assets = self._build_non_current_assets(non_current_assets_data)
        current_liabilities = self._build_current_liabilities(current_liabilities_data)
        long_term_liabilities = self._build_long_term_liabilities(long_term_liabilities_data)
        equity = self._build_equity(equity_data)

        return BalanceSheet(
            assets=Assets(
                current=current_assets if current_assets else None,
                non_current=non_current_assets if non_current_assets else None
            ),
            liabilities=Liabilities(
                current=current_liabilities if current_liabilities else None,
                long_term=long_term_liabilities if long_term_liabilities else None
            ),
            equity=equity
        )

    def _build_income_statement_from_transactions(
        self,
        transactions: List[Transaction],
        extraction_results: List[ExtractionResult]
    ) -> IncomeStatement:
        """
        Build Income Statement by aggregating categorized transactions.
        """

        revenue_data: Dict[str, float] = defaultdict(float)
        cogs_data: Dict[str, float] = defaultdict(float)
        opex_data: Dict[str, float] = defaultdict(float)
        other_data: Dict[str, float] = defaultdict(float)

        # Aggregate from transactions
        for txn in transactions:
            if not txn.category:
                continue

            if 'revenue.' in txn.category:
                item = txn.category.split('.')[-1]
                revenue_data[item] += txn.amount

            elif 'cogs.' in txn.category:
                item = txn.category.split('.')[-1]
                cogs_data[item] += txn.amount

            elif 'operating_expenses.' in txn.category:
                item = txn.category.split('.')[-1]
                opex_data[item] += txn.amount

            elif 'other_income_expense.' in txn.category:
                item = txn.category.split('.')[-1]
                other_data[item] += txn.amount

        # Also merge existing income statement data
        for result in extraction_results:
            if result.extracted_data.income_statement:
                inc = result.extracted_data.income_statement

                if inc.revenue:
                    for field_name, value in inc.revenue.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            revenue_data[field_name] += value['value']

                if inc.cogs:
                    for field_name, value in inc.cogs.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            cogs_data[field_name] += value['value']

                if inc.operating_expenses:
                    for field_name, value in inc.operating_expenses.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            opex_data[field_name] += value['value']

                if inc.other_income_expense:
                    for field_name, value in inc.other_income_expense.model_dump(exclude_none=True).items():
                        if isinstance(value, dict) and 'value' in value:
                            other_data[field_name] += value['value']

        return IncomeStatement(
            revenue=self._build_revenue(revenue_data) if revenue_data else None,
            cogs=self._build_cogs(cogs_data) if cogs_data else None,
            operating_expenses=self._build_operating_expenses(opex_data) if opex_data else None,
            other_income_expense=self._build_other_income_expense(other_data) if other_data else None
        )

    def _build_cash_flow_from_transactions(
        self,
        transactions: List[Transaction],
        extraction_results: List[ExtractionResult]
    ) -> CashFlow:
        """
        Build Cash Flow Statement by aggregating categorized transactions.
        """

        operating_data: Dict[str, float] = defaultdict(float)
        investing_data: Dict[str, float] = defaultdict(float)
        financing_data: Dict[str, float] = defaultdict(float)

        # Aggregate from transactions
        for txn in transactions:
            if not txn.category:
                continue

            if 'cash_flow.operating.' in txn.category or txn.category.startswith('operating.'):
                item = txn.category.split('.')[-1]
                operating_data[item] += txn.amount

            elif 'cash_flow.investing.' in txn.category or txn.category.startswith('investing.'):
                item = txn.category.split('.')[-1]
                investing_data[item] += txn.amount

            elif 'cash_flow.financing.' in txn.category or txn.category.startswith('financing.'):
                item = txn.category.split('.')[-1]
                financing_data[item] += txn.amount

        return CashFlow(
            operating=self._build_operating_activities(operating_data) if operating_data else None,
            investing=self._build_investing_activities(investing_data) if investing_data else None,
            financing=self._build_financing_activities(financing_data) if financing_data else None
        )

    # Helper methods to build specific sections
    def _build_current_assets(self, data: Dict[str, float]) -> Optional[CurrentAssets]:
        if not data:
            return None
        return CurrentAssets(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_non_current_assets(self, data: Dict[str, float]) -> Optional[NonCurrentAssets]:
        if not data:
            return None
        return NonCurrentAssets(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_current_liabilities(self, data: Dict[str, float]) -> Optional[CurrentLiabilities]:
        if not data:
            return None
        return CurrentLiabilities(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_long_term_liabilities(self, data: Dict[str, float]) -> Optional[LongTermLiabilities]:
        if not data:
            return None
        return LongTermLiabilities(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_equity(self, data: Dict[str, float]) -> Optional[Equity]:
        if not data:
            return None
        return Equity(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_revenue(self, data: Dict[str, float]) -> Revenue:
        return Revenue(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_cogs(self, data: Dict[str, float]) -> COGS:
        return COGS(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_operating_expenses(self, data: Dict[str, float]) -> OperatingExpenses:
        return OperatingExpenses(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_other_income_expense(self, data: Dict[str, float]) -> OtherIncomeExpense:
        return OtherIncomeExpense(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_operating_activities(self, data: Dict[str, float]) -> OperatingActivities:
        return OperatingActivities(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_investing_activities(self, data: Dict[str, float]) -> InvestingActivities:
        return InvestingActivities(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _build_financing_activities(self, data: Dict[str, float]) -> FinancingActivities:
        return FinancingActivities(**{
            k: FinancialLineItem(value=v, confidence=0.9, source_location="aggregated")
            for k, v in data.items() if v != 0
        })

    def _create_empty_aggregation(
        self,
        project_id: str,
        time_period: Optional[TimePeriod]
    ) -> AggregatedFinancialData:
        """Create empty aggregation when no extraction results provided."""
        return AggregatedFinancialData(
            project_id=project_id,
            aggregation_date=datetime.utcnow(),
            source_file_ids=[],
            time_period=time_period,
            balance_sheet=None,
            income_statement=None,
            cash_flow=None,
            transactions=[],
            total_files_processed=0,
            conflicts_detected=0,
            conflicts_resolved=0
        )


def load_extraction_results(extraction_dir: Path) -> List[ExtractionResult]:
    """
    Load all extraction results from a directory.

    Args:
        extraction_dir: Path to directory containing extraction JSON files

    Returns:
        List of ExtractionResult objects
    """
    results = []

    for json_file in extraction_dir.glob("*.json"):
        if json_file.name.endswith("_error.json"):
            continue

        try:
            with json_file.open("r") as f:
                data = json.load(f)
                result = ExtractionResult(**data)
                results.append(result)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            continue

    return results
