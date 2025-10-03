"""
Financial Consolidator
Aggregates and consolidates classified financial data
"""

from typing import Dict, List
from collections import defaultdict


class FinancialConsolidator:
    """Consolidate classified financial line items into aggregated categories"""

    def __init__(self):
        """Initialize consolidator"""
        self.consolidated_data = {
            'current_assets': {},
            'non_current_assets': {},
            'current_liabilities': {},
            'long_term_liabilities': {},
            'equity': {},
            'revenue': {},
            'cost_of_goods_sold': {},
            'operating_expenses': {},
            'other_income': {},
            'other_expenses': {}
        }

    def consolidate(self, classified_items: List[Dict]) -> Dict:
        """
        Consolidate classified line items

        Args:
            classified_items: List of classified line items

        Returns:
            Consolidated financial data by category
        """
        # Reset consolidated data
        for category in self.consolidated_data:
            self.consolidated_data[category] = defaultdict(float)

        # Aggregate amounts by template line
        for item in classified_items:
            if item['classification'] != 'classified':
                continue

            main_category = item.get('main_category')
            template_line = item.get('template_line', 'Unclassified')
            amount = item.get('original_item', {}).get('amount', 0)

            if main_category in self.consolidated_data and amount:
                self.consolidated_data[main_category][template_line] += float(amount)

        # Convert defaultdicts to regular dicts
        result = {}
        for category, items in self.consolidated_data.items():
            result[category] = dict(items)

        return result

    def get_totals(self, consolidated_data: Dict) -> Dict:
        """Calculate totals for each major category"""
        totals = {}

        for category, items in consolidated_data.items():
            total = sum(items.values())
            totals[category] = total

        # Calculate high-level totals
        totals['total_assets'] = totals.get('current_assets', 0) + totals.get('non_current_assets', 0)
        totals['total_liabilities'] = totals.get('current_liabilities', 0) + totals.get('long_term_liabilities', 0)
        totals['total_equity'] = totals.get('equity', 0)

        totals['total_revenue'] = totals.get('revenue', 0)
        totals['total_cogs'] = totals.get('cost_of_goods_sold', 0)
        totals['total_operating_expenses'] = totals.get('operating_expenses', 0)
        totals['total_other_income'] = totals.get('other_income', 0)
        totals['total_other_expenses'] = totals.get('other_expenses', 0)

        # Calculate profit metrics
        totals['gross_profit'] = totals['total_revenue'] - totals['total_cogs']
        totals['operating_income'] = totals['gross_profit'] - totals['total_operating_expenses']
        totals['net_income'] = (totals['operating_income'] +
                               totals['total_other_income'] -
                               totals['total_other_expenses'])

        # Balance check
        totals['balance_check'] = totals['total_assets'] - (totals['total_liabilities'] + totals['total_equity'])

        return totals

    def generate_summary(self, consolidated_data: Dict, totals: Dict) -> str:
        """Generate human-readable summary"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("CONSOLIDATED FINANCIAL SUMMARY")
        lines.append("=" * 80)

        # Balance Sheet
        lines.append("\n📊 BALANCE SHEET")
        lines.append("-" * 80)
        lines.append(f"Total Assets:             ${totals['total_assets']:,.2f}")
        lines.append(f"  Current Assets:         ${totals.get('current_assets', 0):,.2f}")
        lines.append(f"  Non-Current Assets:     ${totals.get('non_current_assets', 0):,.2f}")
        lines.append(f"\nTotal Liabilities:        ${totals['total_liabilities']:,.2f}")
        lines.append(f"  Current Liabilities:    ${totals.get('current_liabilities', 0):,.2f}")
        lines.append(f"  Long-term Liabilities:  ${totals.get('long_term_liabilities', 0):,.2f}")
        lines.append(f"\nTotal Equity:             ${totals['total_equity']:,.2f}")
        lines.append(f"\nBalance Check:            ${totals['balance_check']:,.2f} (should be 0)")

        # Income Statement
        lines.append("\n\n💰 INCOME STATEMENT")
        lines.append("-" * 80)
        lines.append(f"Revenue:                  ${totals['total_revenue']:,.2f}")
        lines.append(f"Cost of Goods Sold:       ${totals['total_cogs']:,.2f}")
        lines.append(f"Gross Profit:             ${totals['gross_profit']:,.2f}")

        if totals['total_revenue'] > 0:
            gp_margin = (totals['gross_profit'] / totals['total_revenue']) * 100
            lines.append(f"  Gross Profit Margin:    {gp_margin:.1f}%")

        lines.append(f"\nOperating Expenses:       ${totals['total_operating_expenses']:,.2f}")
        lines.append(f"Operating Income (EBIT):  ${totals['operating_income']:,.2f}")

        if totals['total_revenue'] > 0:
            op_margin = (totals['operating_income'] / totals['total_revenue']) * 100
            lines.append(f"  Operating Margin:       {op_margin:.1f}%")

        lines.append(f"\nOther Income:             ${totals['total_other_income']:,.2f}")
        lines.append(f"Other Expenses:           ${totals['total_other_expenses']:,.2f}")
        lines.append(f"\nNet Income:               ${totals['net_income']:,.2f}")

        if totals['total_revenue'] > 0:
            net_margin = (totals['net_income'] / totals['total_revenue']) * 100
            lines.append(f"  Net Profit Margin:      {net_margin:.1f}%")

        # Top line items
        lines.append("\n\n📋 TOP LINE ITEMS BY CATEGORY")
        lines.append("-" * 80)

        for category, items in consolidated_data.items():
            if items:
                lines.append(f"\n{category.replace('_', ' ').title()}:")
                sorted_items = sorted(items.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
                for line_item, amount in sorted_items:
                    lines.append(f"  {line_item:.<50} ${amount:>12,.2f}")

        lines.append("\n" + "=" * 80 + "\n")

        return "\n".join(lines)


def main():
    """Test function"""
    # Sample classified items
    test_items = [
        {
            'classification': 'classified',
            'main_category': 'current_assets',
            'template_line': 'Cash and Cash Equivalents',
            'confidence': 1.0,
            'original_item': {'description': 'Cash in Bank', 'amount': 50000}
        },
        {
            'classification': 'classified',
            'main_category': 'current_assets',
            'template_line': 'Accounts Receivable',
            'confidence': 1.0,
            'original_item': {'description': 'AR from customers', 'amount': 25000}
        },
        {
            'classification': 'classified',
            'main_category': 'revenue',
            'template_line': 'Sales Revenue',
            'confidence': 1.0,
            'original_item': {'description': 'Construction Revenue', 'amount': 650000}
        },
        {
            'classification': 'classified',
            'main_category': 'cost_of_goods_sold',
            'template_line': 'Materials - COGS',
            'confidence': 1.0,
            'original_item': {'description': 'BuildMart Materials', 'amount': 125000}
        },
        {
            'classification': 'classified',
            'main_category': 'operating_expenses',
            'template_line': 'Rent Expense',
            'confidence': 1.0,
            'original_item': {'description': 'Office Rent', 'amount': 12000}
        }
    ]

    consolidator = FinancialConsolidator()
    consolidated = consolidator.consolidate(test_items)
    totals = consolidator.get_totals(consolidated)
    summary = consolidator.generate_summary(consolidated, totals)

    print(summary)


if __name__ == "__main__":
    main()
