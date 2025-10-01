# Dummy Data - Project A: 123 Sunset Boulevard

## Overview

This directory contains comprehensive, realistic dummy data for a construction project that demonstrates typical industry chaos and data quality issues. The data is designed to showcase how the Intelligent Finance Platform extracts value from messy, real-world financial information.

## Key Files

### `project_a_comprehensive_data.json`
Complete project financial data in structured JSON format. This represents what AI would extract from messy Excel files, PDFs, and scanned documents.

**Contents:**
- Project metadata and status
- Complete budget breakdown (50+ line items across all phases)
- Subcontractor register with payment history
- Client payment milestones and variations
- Defects register
- Data quality issues tracker

### Individual Category READMEs
Each subdirectory contains detailed README files explaining the type of messy data typically found:
- `01_LAND_PURCHASE/` - Land acquisition documents
- `06_PURCHASE_ORDERS_INVOICES/` - Purchase orders and invoices
- `07_SUBCONTRACTORS/` - Subcontractor agreements and payments
- `11_CLIENT_BILLING/` - Client invoicing and variations
- `12_BUDGET_TRACKING/` - Budget spreadsheets and tracking

## Project Financial Summary

**Contract Value:** $650,000
**Spent to Date:** $574,600
**Forecast Final:** $658,500 ⚠️ **OVER BUDGET**
**Projected Profit/(Loss):** **($8,500)** ❌
**Schedule Status:** 12 days behind ⚠️
**Completion:** 65%

## Critical Issues Demonstrated

### 1. Revenue Leakage: $6,460
- 4 approved variations NOT invoiced to client
- Lost revenue impacting profitability

### 2. Cash Flow Problem: $130,000
- Client payment 5 days overdue
- Cannot pay subcontractors

### 3. Overdue Subbie Payment: $18,500
- Premier Bricklaying invoice overdue
- Relationship risk

### 4. Critical Defect: Shower Leak
- 16 days overdue for fix
- Blocking project handover

### 5. Insurance Expiry Risk
- Concrete Crew insurance expires in 71 days
- Compliance risk

## Data Realism

This data intentionally includes:
- **Inconsistent Formatting**: Mixed number formats, date formats, phone formats
- **Missing Data**: Some fields blank, some optional data missing
- **Manual Errors**: Totals that don't quite add up
- **Scattered Notes**: "URGENT", "check this", "???"
- **Status Variations**: "PAID", "Paid", "paid", "complete", "COMPLETE"
- **Data Quality Issues**: Tracked and flagged for AI recommendations

## How to Use This Data

### For Development (Phase 3+)
Import `project_a_comprehensive_data.json` into your application:

```typescript
import projectData from '../dummy_data/project_a_comprehensive_data.json';

// Access budget data
const budget = projectData.budgetSummary;

// Access subcontractors
const subbies = projectData.subcontractors;

// Access client payments
const payments = projectData.clientPayments;

// Get data quality issues
const issues = projectData.dataQualityIssues;
```

### For Demo/Presentation
Use this data to demonstrate:
1. **Problem Recognition**: "Look at all these issues in typical construction data"
2. **AI Value**: "Our platform automatically identifies these problems"
3. **Actionable Insights**: "Here's exactly what to fix and when"

## Documentation

See `wiki/DUMMY_DATA_GUIDE.md` for complete documentation of:
- Full project details
- All data structures
- Issue categories and severity
- How AI would extract and analyze this data
- Platform value proposition

## Next Steps

This realistic dummy data enables:
- **Phase 3**: Demo data integration - Connect dashboard to this JSON
- **Phase 4**: Financial statements - Generate income statement, balance sheet, cash flow
- **Phase 5**: Advanced features - Budget drill-down, variation tracking, defects management
- **Phase 6**: AI demonstration - Show automated issue detection and recommendations

---

**This data will convince construction companies we understand their chaos and can solve it.**
