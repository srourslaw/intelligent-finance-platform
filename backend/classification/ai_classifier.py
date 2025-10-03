"""
AI-powered classification using Claude API.

Classifies extracted financial line items into standard categories
using Anthropic's Claude API.
"""

import os
from typing import List, Dict, Optional, Tuple
from anthropic import Anthropic

from schemas.extraction_schema import (
    ExtractionResult,
    Transaction,
    DocumentType
)


class AIClassifier:
    """
    Classify financial line items using Claude API.

    Handles:
    - Transaction categorization
    - Document type classification
    - Confidence scoring
    """

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None

        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)

        # Standard financial categories
        self.categories = self._load_categories()

    def is_available(self) -> bool:
        """Check if Claude API is available."""
        return self.client is not None

    def _load_categories(self) -> Dict[str, List[str]]:
        """
        Load standard financial categories.

        This is our category hierarchy that Claude will map items to.
        """
        return {
            "balance_sheet": {
                "assets": {
                    "current": [
                        "cash_on_hand",
                        "cash_in_bank_operating",
                        "cash_in_bank_payroll",
                        "accounts_receivable",
                        "inventory_raw_materials",
                        "inventory_work_in_progress",
                        "inventory_finished_goods",
                        "prepaid_expenses"
                    ],
                    "non_current": [
                        "land",
                        "buildings",
                        "equipment",
                        "vehicles",
                        "furniture_and_fixtures",
                        "accumulated_depreciation",
                        "intangible_assets"
                    ]
                },
                "liabilities": {
                    "current": [
                        "accounts_payable",
                        "credit_card_debt",
                        "short_term_loans",
                        "accrued_expenses",
                        "taxes_payable"
                    ],
                    "long_term": [
                        "mortgage_payable",
                        "long_term_debt",
                        "bonds_payable"
                    ]
                },
                "equity": [
                    "share_capital",
                    "retained_earnings",
                    "additional_paid_in_capital"
                ]
            },
            "income_statement": {
                "revenue": [
                    "product_sales",
                    "service_revenue",
                    "other_revenue"
                ],
                "cogs": [
                    "purchases",
                    "direct_labor",
                    "direct_materials",
                    "manufacturing_overhead"
                ],
                "operating_expenses": [
                    "salaries_and_wages",
                    "rent",
                    "utilities",
                    "insurance",
                    "depreciation",
                    "marketing",
                    "advertising",
                    "office_supplies",
                    "professional_fees",
                    "repairs_and_maintenance",
                    "travel",
                    "meals_and_entertainment",
                    "telephone",
                    "internet"
                ],
                "other_income_expense": [
                    "interest_income",
                    "interest_expense",
                    "dividend_income",
                    "gain_loss_on_sale_of_assets"
                ]
            },
            "cash_flow": {
                "operating": [
                    "net_profit",
                    "depreciation",
                    "changes_in_accounts_receivable",
                    "changes_in_inventory",
                    "changes_in_accounts_payable"
                ],
                "investing": [
                    "purchase_of_ppe",
                    "sale_of_ppe",
                    "purchase_of_investments"
                ],
                "financing": [
                    "proceeds_from_debt",
                    "repayment_of_debt",
                    "dividends_paid"
                ]
            }
        }

    def classify_extraction(self, result: ExtractionResult) -> ExtractionResult:
        """
        Classify all transactions in an extraction result.

        Updates:
        - Transaction categories
        - Confidence scores
        - Document type
        - Classification stats
        """

        if not self.is_available():
            result.extraction_notes.warnings.append(
                "Claude API not available - skipping classification"
            )
            return result

        # Classify document type
        result.metadata.document_classification = self._classify_document_type(result)

        # Classify transactions
        transactions = result.extracted_data.transactions

        if transactions:
            classified_count = 0
            total_confidence = 0.0

            for transaction in transactions:
                category, confidence = self._classify_transaction(transaction)

                if category:
                    transaction.category = category
                    transaction.confidence = confidence
                    classified_count += 1
                    total_confidence += confidence

            # Update classification stats
            result.classification_stats.total_items = len(transactions)
            result.classification_stats.classified = classified_count
            result.classification_stats.unmapped = len(transactions) - classified_count
            result.classification_stats.avg_confidence = (
                total_confidence / classified_count if classified_count > 0 else 0.0
            )

            # Update overall confidence
            result.metadata.confidence_score = result.classification_stats.avg_confidence

        return result

    def _classify_document_type(self, result: ExtractionResult) -> DocumentType:
        """
        Classify the type of financial document.

        Uses filename, content patterns, and Claude API.
        """

        filename = result.metadata.original_filename.lower()

        # Rule-based classification first (fast and free)
        if any(keyword in filename for keyword in ['balance', 'sheet', 'assets', 'liabilities']):
            return DocumentType.BALANCE_SHEET

        if any(keyword in filename for keyword in ['income', 'profit', 'loss', 'p&l', 'p l']):
            return DocumentType.INCOME_STATEMENT

        if any(keyword in filename for keyword in ['cash flow', 'cashflow']):
            return DocumentType.CASH_FLOW

        if any(keyword in filename for keyword in ['invoice', 'bill']):
            return DocumentType.INVOICE

        if any(keyword in filename for keyword in ['receipt']):
            return DocumentType.RECEIPT

        if any(keyword in filename for keyword in ['bank statement', 'statement']):
            return DocumentType.BANK_STATEMENT

        if any(keyword in filename for keyword in ['expense', 'expenses']):
            return DocumentType.EXPENSE_REPORT

        if any(keyword in filename for keyword in ['budget']):
            return DocumentType.BUDGET

        # Use Claude API for ambiguous cases
        if self.client and result.extracted_data.transactions:
            try:
                # Sample first few transactions
                sample_transactions = result.extracted_data.transactions[:5]
                descriptions = [t.description for t in sample_transactions]

                prompt = f"""You are a financial document classifier.

Based on the filename "{result.metadata.original_filename}" and these sample transactions:
{descriptions}

What type of financial document is this?

Options:
- balance_sheet
- income_statement
- cash_flow
- general_ledger
- invoice
- receipt
- bank_statement
- expense_report
- budget

Respond with ONLY the document type, nothing else."""

                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=50,
                    messages=[{"role": "user", "content": prompt}]
                )

                doc_type_str = message.content[0].text.strip().lower()

                # Map to enum
                doc_type_map = {
                    'balance_sheet': DocumentType.BALANCE_SHEET,
                    'income_statement': DocumentType.INCOME_STATEMENT,
                    'cash_flow': DocumentType.CASH_FLOW,
                    'general_ledger': DocumentType.GENERAL_LEDGER,
                    'invoice': DocumentType.INVOICE,
                    'receipt': DocumentType.RECEIPT,
                    'bank_statement': DocumentType.BANK_STATEMENT,
                    'expense_report': DocumentType.EXPENSE_REPORT,
                    'budget': DocumentType.BUDGET
                }

                return doc_type_map.get(doc_type_str, DocumentType.UNKNOWN)

            except Exception as e:
                result.extraction_notes.warnings.append(
                    f"Document type classification failed: {str(e)}"
                )

        return DocumentType.UNKNOWN

    def _classify_transaction(self, transaction: Transaction) -> Tuple[Optional[str], float]:
        """
        Classify a single transaction.

        Returns: (category_path, confidence)
        Example: ("operating_expenses.rent", 0.95)
        """

        description = transaction.description

        # Rule-based classification first (fast and free)
        rule_category = self._rule_based_classification(description)
        if rule_category:
            return rule_category, 0.85  # High confidence for rule-based

        # Use Claude API for ambiguous cases
        if self.client:
            try:
                prompt = f"""You are a financial transaction classifier.

Classify this transaction into ONE of the following categories:

REVENUE:
- product_sales
- service_revenue
- other_revenue

COST OF GOODS SOLD:
- purchases
- direct_labor
- direct_materials
- manufacturing_overhead

OPERATING EXPENSES:
- salaries_and_wages
- rent
- utilities
- insurance
- depreciation
- marketing
- advertising
- office_supplies
- professional_fees
- repairs_and_maintenance
- travel
- meals_and_entertainment
- telephone
- internet

OTHER:
- interest_income
- interest_expense

Transaction description: "{description}"

Respond in this exact format:
category: <category_name>
confidence: <0.0-1.0>

Example:
category: operating_expenses.rent
confidence: 0.95
"""

                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=100,
                    messages=[{"role": "user", "content": prompt}]
                )

                response_text = message.content[0].text.strip()

                # Parse response
                lines = response_text.split('\n')
                category = None
                confidence = 0.0

                for line in lines:
                    if line.startswith('category:'):
                        category = line.split(':', 1)[1].strip()
                    elif line.startswith('confidence:'):
                        try:
                            confidence = float(line.split(':', 1)[1].strip())
                        except ValueError:
                            confidence = 0.5

                # Add prefix if not present
                if category and '.' not in category:
                    if category in ['product_sales', 'service_revenue', 'other_revenue']:
                        category = f"revenue.{category}"
                    elif category in ['purchases', 'direct_labor', 'direct_materials', 'manufacturing_overhead']:
                        category = f"cogs.{category}"
                    elif category in ['interest_income', 'interest_expense']:
                        category = f"other_income_expense.{category}"
                    else:
                        category = f"operating_expenses.{category}"

                return category, confidence

            except Exception as e:
                transaction.notes = f"Classification error: {str(e)}"
                return None, 0.0

        return None, 0.0

    def _rule_based_classification(self, description: str) -> Optional[str]:
        """
        Fast rule-based classification using keywords.

        Returns category path or None.
        """

        desc_lower = description.lower()

        # Common mappings
        rules = {
            'revenue': {
                'keywords': ['revenue', 'sales', 'income', 'payment received', 'customer payment'],
                'category': 'revenue.product_sales'
            },
            'rent': {
                'keywords': ['rent', 'lease', 'rental'],
                'category': 'operating_expenses.rent'
            },
            'utilities': {
                'keywords': ['utility', 'utilities', 'electric', 'electricity', 'water', 'gas', 'power'],
                'category': 'operating_expenses.utilities'
            },
            'salaries': {
                'keywords': ['salary', 'salaries', 'wages', 'payroll', 'employee', 'staff'],
                'category': 'operating_expenses.salaries_and_wages'
            },
            'insurance': {
                'keywords': ['insurance'],
                'category': 'operating_expenses.insurance'
            },
            'marketing': {
                'keywords': ['marketing', 'advertising', 'promotion', 'ad spend'],
                'category': 'operating_expenses.marketing'
            },
            'office_supplies': {
                'keywords': ['office supplies', 'supplies', 'stationery'],
                'category': 'operating_expenses.office_supplies'
            },
            'travel': {
                'keywords': ['travel', 'flight', 'hotel', 'accommodation', 'airfare'],
                'category': 'operating_expenses.travel'
            },
            'meals': {
                'keywords': ['meal', 'meals', 'restaurant', 'food', 'dining'],
                'category': 'operating_expenses.meals_and_entertainment'
            },
            'telephone': {
                'keywords': ['phone', 'telephone', 'mobile', 'cell'],
                'category': 'operating_expenses.telephone'
            },
            'internet': {
                'keywords': ['internet', 'wifi', 'broadband', 'hosting'],
                'category': 'operating_expenses.internet'
            }
        }

        for rule_name, rule_data in rules.items():
            for keyword in rule_data['keywords']:
                if keyword in desc_lower:
                    return rule_data['category']

        return None
