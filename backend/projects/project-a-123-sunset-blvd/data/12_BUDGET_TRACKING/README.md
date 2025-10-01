# Budget Tracking - Realistic Construction Data

## Overview
This directory contains budget tracking data for Project A - 123 Sunset Boulevard. The data demonstrates typical construction company chaos: inconsistent formatting, manual calculations with errors, scattered notes, and incomplete tracking.

## File: project_budget_data.json

This JSON represents data extracted from a messy Excel file (MASTER_PROJECT_BUDGET.xlsx) that would typically have:
- 4 sheets with 50+ budget line items
- Color-coded cells with no legend
- Merged header cells
- Manual totals that don't match formulas
- Mixed decimal formats
- Random notes like "check this", "URGENT", "???"
- Some #REF! errors
- Empty rows scattered throughout

### Key Issues Demonstrated:
1. **Over Budget Items**: Several categories show negative variances
2. **Missing Data**: Some committed amounts blank
3. **Inconsistent Formatting**: Currency shown as $1,234.56, $1234.5, $1,235
4. **Manual Errors**: Totals don't always add up correctly
5. **Poor Documentation**: Vague notes, unclear status

### Budget Summary Highlights:
- **Total Budget**: $650,000
- **Total Spent**: $574,600
- **Committed (not yet invoiced)**: $38,900
- **Forecast Final**: $658,500 ⚠️ OVER BUDGET
- **Variance**: -$8,500 ⚠️ LOSS PROJECTED

###Categories with Issues:
- Design Revisions: $740 over (client kept changing)
- Site Prep: $420 over (rock excavation)
- Foundation: $890 over (extra waterproofing)
- Roofing: $650 over (tile breakage)
- Plumbing: $580 over (upgrade fixtures)
- Electrical: $1,240 over (additional circuits)
- Kitchen: $2,100 over (client upgrade not charged!)

## Realistic Construction Chaos Elements:

### Data Quality Issues:
- Inconsistent number formatting
- Missing purchase order references
- Vague supplier names ("John's Plumbing" vs "John Smith Plumbing Pty Ltd")
- Date inconsistencies
- Multiple versions of same document

### Common Problems:
- Verbal quotes not documented
- Variations approved but not invoiced
- Retention amounts not tracked properly
- Sub-contractor payments delayed
- Invoice/PO mismatches

### Financial Tracking Gaps:
- Some costs recorded but not allocated to categories
- Petty cash not always logged
- Owner supplies not tracked
- Warranty costs unknown
- Defect rectification budget missing

## How AI Would Help:
The Intelligent Finance Platform would:
1. Extract and normalize all budget line items
2. Flag over-budget categories immediately
3. Identify uninvoiced variations
4. Track committed vs actual spend
5. Predict final cost based on % complete
6. Alert on missing documentation
7. Reconcile invoices to POs automatically
8. Generate accurate financial statements
