# Financial Data Enhancement Plan
**Date Created:** October 3, 2025
**Project:** Project A - 123 Sunset Boulevard
**Purpose:** Roadmap to achieve comprehensive financial statement capability

---

## Executive Summary

This plan outlines the 3-phase approach to transform the current construction project tracking data into a comprehensive financial accounting system capable of producing GAAP-compliant financial statements, ratios, and analysis.

**Current State:** 70% Income Statement ready, 40% Balance Sheet ready, 60% Cash Flow ready
**Target State:** 90%+ comprehensive financial reporting capability
**Timeline:** Phase 1 (2-3 hours) → Phase 2 (1-2 days) → Phase 3 (ongoing)

---

## Phase 1: Essential Accounting Files (PRIORITY - DO FIRST)
**Timeline:** 2-3 hours
**Goal:** Create missing foundation for financial statements

### 1.1 General Ledger Foundation

**Create folder:** `/backend/projects/project-a-123-sunset-blvd/data/17_GENERAL_LEDGER/`

**Files to create:**

#### `Chart_of_Accounts.xlsx`
Structure:
```
Account Code | Account Name | Type | Category | SubCategory | Opening Balance
1000-1999   | Assets      | Asset | Current/Non-Current | Cash/AR/Inventory | $XXX
2000-2999   | Liabilities | Liability | Current/Long-Term | AP/Loans | $XXX
3000-3999   | Equity      | Equity | Capital/Retained | Owner's Equity | $XXX
4000-4999   | Revenue     | Income | Construction | Progress Billing | $0
5000-5999   | COGS        | Expense | Direct Costs | Materials/Labor/Subs | $0
6000-6999   | Operating   | Expense | Indirect | Admin/Permits/Design | $0
```

**Key GL Accounts:**
- 1100 - Cash at Bank
- 1200 - Accounts Receivable
- 1300 - Work in Progress
- 1500 - Land (Asset)
- 2100 - Accounts Payable
- 2200 - Loan Payable
- 3100 - Owner's Capital
- 3200 - Retained Earnings
- 4100 - Construction Revenue
- 5100 - Materials - COGS
- 5200 - Labor - COGS
- 5300 - Subcontractors - COGS
- 6100 - Design Fees
- 6200 - Permits & Approvals
- 6300 - Insurance
- 6400 - Financing Costs

#### `Trial_Balance_Monthly.xlsx`
Template with sheets for each month:
```
GL Account | Account Name | Debit | Credit | Balance
[Auto-populate from transactions]
```

#### `General_Journal.xlsx`
Transaction log:
```
Date | Entry# | GL Account | Debit | Credit | Description | Reference
```

### 1.2 Monthly Financial Close Packages

**Create folder:** `/backend/projects/project-a-123-sunset-blvd/data/19_MONTHLY_CLOSE/`

**Subfolders for each month:**
- `2024-06-Close/`
- `2024-07-Close/`
- `2024-08-Close/`
- `2024-09-Close/`

**Files in each month folder:**

#### `Income_Statement_[Month].xlsx`
```
REVENUE
  Construction Revenue               $XXX,XXX
  Variation Orders                   $XX,XXX
TOTAL REVENUE                        $XXX,XXX

COST OF GOODS SOLD
  Materials                          $XX,XXX
  Direct Labor                       $XX,XXX
  Subcontractors                     $XXX,XXX
TOTAL COGS                           $XXX,XXX

GROSS PROFIT                         $XXX,XXX
GROSS PROFIT MARGIN                  XX%

OPERATING EXPENSES
  Design & Engineering               $XX,XXX
  Permits & Approvals                $X,XXX
  Insurance                          $X,XXX
  Site Costs                         $X,XXX
TOTAL OPERATING EXPENSES             $XX,XXX

EBITDA                               $XX,XXX

  Depreciation                       $X,XXX
  Interest Expense                   $X,XXX

NET INCOME                           $XX,XXX
NET PROFIT MARGIN                    XX%
```

#### `Balance_Sheet_[Month].xlsx`
```
ASSETS
Current Assets:
  Cash at Bank                       $XXX,XXX
  Accounts Receivable                $XX,XXX
  Work in Progress                   $XXX,XXX
Total Current Assets                 $XXX,XXX

Non-Current Assets:
  Land                               $XXX,XXX
  Equipment (net)                    $XX,XXX
Total Non-Current Assets             $XXX,XXX

TOTAL ASSETS                         $XXX,XXX

LIABILITIES
Current Liabilities:
  Accounts Payable                   $XX,XXX
  Accrued Expenses                   $X,XXX
Total Current Liabilities            $XX,XXX

Long-Term Liabilities:
  Loan Payable                       $XXX,XXX
Total Long-Term Liabilities          $XXX,XXX

TOTAL LIABILITIES                    $XXX,XXX

EQUITY
  Owner's Capital                    $XXX,XXX
  Retained Earnings                  $(XX,XXX)
TOTAL EQUITY                         $XXX,XXX

TOTAL LIABILITIES & EQUITY           $XXX,XXX
```

#### `Cash_Flow_Statement_[Month].xlsx`
```
OPERATING ACTIVITIES
  Cash received from customers       $XXX,XXX
  Cash paid to suppliers             $(XXX,XXX)
  Cash paid to employees             $(XX,XXX)
  Cash paid for operating expenses   $(XX,XXX)
Net Cash from Operating              $XX,XXX

INVESTING ACTIVITIES
  Purchase of equipment              $(XX,XXX)
  Purchase of land                   $(XXX,XXX)
Net Cash from Investing              $(XXX,XXX)

FINANCING ACTIVITIES
  Loan drawdowns                     $XXX,XXX
  Loan repayments                    $(X,XXX)
  Owner contributions                $XXX,XXX
Net Cash from Financing              $XXX,XXX

NET CHANGE IN CASH                   $XX,XXX
Cash at beginning                    $XXX,XXX
Cash at end                          $XXX,XXX
```

### 1.3 Bank Reconciliation

**Create folder:** `/backend/projects/project-a-123-sunset-blvd/data/20_BANK_RECONCILIATION/`

#### `Bank_Reconciliation_Monthly.xlsx`
Sheets for each month:
```
Cash per Bank Statement              $XXX,XXX
Add: Deposits in transit             $XX,XXX
Less: Outstanding checks             $(XX,XXX)
Cash per Books                       $XXX,XXX

Reconciling Items:
Date | Description | Bank | Books | Difference | Status
```

### 1.4 Fixed Assets Register

**Create folder:** `/backend/projects/project-a-123-sunset-blvd/data/21_FIXED_ASSETS/`

#### `Fixed_Assets_Register.xlsx`
```
Asset ID | Description | Date Acquired | Cost | Salvage Value | Useful Life (yrs) | Depreciation Method | Accumulated Dep | Net Book Value | Location
FA-001  | Excavator   | 2024-01-15    | $85,000 | $5,000 | 10 | Straight-Line | $4,000 | $81,000 | Site A
FA-002  | Site Office | 2024-01-20    | $12,000 | $1,000 | 5  | Straight-Line | $1,100 | $10,900 | Site A
```

### 1.5 Payroll Register

**Create folder:** `/backend/projects/project-a-123-sunset-blvd/data/22_PAYROLL/`

#### `Payroll_Register.xlsx`
```
Employee ID | Name | Role | Pay Rate | Hours | Gross Pay | PAYG Tax | Super | Net Pay | Payment Date
EMP-001 | John Smith | Site Supervisor | $45/hr | 160 | $7,200 | $1,440 | $756 | $5,004 | 30/09/2024
```

---

## Phase 2: Enhance Existing Files (DO SECOND)
**Timeline:** 4-6 hours
**Goal:** Map existing data to GL accounts and add missing components

### 2.1 Add GL Account Mapping

**Files to update:**

#### `MASTER_PROJECT_BUDGET.xlsx`
Add column: "GL Account"
```
Category | Description | GL Account | Budget | Actual | Variance
Land     | Land Purchase | 1500 | $250,000 | $250,000 | $0
Materials | Concrete    | 5100 | $45,000  | $42,300  | $2,700
Labor     | Site Super  | 5200 | $28,000  | $31,240  | $(3,240)
```

#### `Client_Payment_Tracker.xlsx`
Add columns:
- "GL Account" (4100 - Construction Revenue)
- "Revenue Recognized" (% of completion method)
- "Deferred Revenue"

#### `Paid_Invoices_Register.xlsx` & `Pending_Invoices.xlsx`
Add columns:
- "GL Account" (map to specific COGS/Expense accounts)
- "Payment Terms"
- "Aging Bucket" (Current, 30, 60, 90+ days)

### 2.2 Add Opening Balances

Create: `Opening_Balances_June_2024.xlsx`
```
GL Account | Account Name | Opening Balance | Date
1100      | Cash at Bank | $100,000 | 01/06/2024
2200      | Loan Payable | $0       | 01/06/2024
3100      | Owner's Capital | $100,000 | 01/06/2024
```

### 2.3 Enhance Revenue Recognition

Create: `Revenue_Recognition_Schedule.xlsx`
```
Milestone | Contract Value | % Complete (Physical) | % Complete (Cost) | Revenue Earned | Revenue Billed | Deferred Revenue
Foundation | $130,000 | 100% | 100% | $130,000 | $130,000 | $0
Framing    | $195,000 | 80%  | 75%  | $146,250 | $97,500  | $(48,750)
```

### 2.4 Add AR/AP Aging

#### `AR_Aging_Report.xlsx`
```
Customer | Invoice# | Date | Total | Current | 30 Days | 60 Days | 90+ Days | Status
ABC Corp | INV-001 | 15/08/24 | $97,500 | $0 | $97,500 | $0 | $0 | OVERDUE
```

#### `AP_Aging_Report.xlsx`
```
Vendor | Invoice# | Date | Total | Current | 30 Days | 60 Days | 90+ Days | Priority
BuildMart | BMINV-1234 | 20/09/24 | $15,400 | $15,400 | $0 | $0 | $0 | NORMAL
```

---

## Phase 3: Update Supporting Documents (DO THIRD)
**Timeline:** 2-3 hours
**Goal:** Make PDFs realistic and aligned with Excel data

### 3.1 Contracts & Agreements

**Files to create/update in** `/backend/projects/project-a-123-sunset-blvd/data/01_LAND_PURCHASE/`:

- `Land_Purchase_Contract_Signed.pdf`
  - Purchase price: $250,000
  - Buyer: [Your Company Name]
  - Seller: Smith Family Trust
  - Settlement date: 15/01/2024
  - Include payment schedule

- `Title_Deed_123_Sunset_Blvd.pdf`
  - Property address
  - Lot/Plan details
  - Registered owner

### 3.2 Bank Statements

**Create in** `/backend/projects/project-a-123-sunset-blvd/data/20_BANK_RECONCILIATION/Bank_Statements/`:

- `Bank_Statement_June_2024.pdf`
- `Bank_Statement_July_2024.pdf`
- `Bank_Statement_August_2024.pdf`
- `Bank_Statement_September_2024.pdf`

**Content:**
- Opening balance
- Deposits (match Client_Payment_Tracker)
- Withdrawals (match Paid_Invoices)
- Closing balance

### 3.3 Tax Invoices

**Enhance existing invoices in** `/backend/projects/project-a-123-sunset-blvd/data/06_PURCHASE_ORDERS_INVOICES/`:

Ensure each PDF invoice includes:
- ABN
- Tax Invoice number
- GST breakdown
- Payment terms (Net 30/60)
- Match amounts in Paid_Invoices_Register.xlsx

### 3.4 Loan Documentation

**Create in** `/backend/projects/project-a-123-sunset-blvd/data/04_FINANCE_INSURANCE/`:

- `Loan_Agreement_Construction_Finance.pdf`
  - Loan amount: $650,000
  - Interest rate: 6.5% p.a.
  - Drawdown schedule
  - Repayment terms
  - Security (land + building)

### 3.5 Insurance Policies

- `Public_Liability_Insurance_Policy.pdf`
- `Contract_Works_Insurance_Policy.pdf`
- `Workers_Compensation_Certificate.pdf`

**Include:**
- Policy numbers
- Coverage amounts
- Expiry dates (match Subcontractor_Register)
- Premium amounts (match budget)

---

## Critical Data Consistency Rules

### Rule 1: All amounts must tie together
- Client billing in `Client_Payment_Tracker.xlsx`
- Bank deposits in `Bank_Reconciliation.xlsx`
- Revenue in `Income_Statement.xlsx`
- Must all match to the dollar

### Rule 2: GL balances must balance
- Total Debits = Total Credits (always)
- Assets = Liabilities + Equity (always)
- Beginning Balance + Net Income - Distributions = Ending Balance

### Rule 3: Dates must be logical
- Invoice date < Payment date
- PO date < Delivery date < Invoice date
- Loan drawdown dates match cashflow dates

### Rule 4: References must cross-link
- Invoice numbers in Excel must match PDF filenames
- PO numbers link PO → Delivery → Invoice
- GL account codes consistent across all files

---

## Data Quality Checklist

Before finalizing, verify:

- [ ] Trial Balance sums to zero (Debits = Credits)
- [ ] Balance Sheet balances (Assets = Liabilities + Equity)
- [ ] Cash per Bank Rec = Cash per Balance Sheet
- [ ] Revenue recognized matches % completion
- [ ] COGS matches materials + labor + subs spent
- [ ] All invoices have matching GL entries
- [ ] AR aging total = AR on Balance Sheet
- [ ] AP aging total = AP on Balance Sheet
- [ ] Loan balance per schedule = Loan on Balance Sheet
- [ ] All PDF amounts match Excel amounts
- [ ] No placeholder data ("Item 1", "Item 2", etc.)
- [ ] Dates are in correct sequence
- [ ] All formulas calculate correctly
- [ ] Month-over-month changes make sense

---

## Financial Statement Capability Targets

### After Phase 1:
- ✅ Can produce basic Income Statement
- ✅ Can produce basic Balance Sheet
- ✅ Can produce basic Cash Flow Statement
- ✅ Have GL foundation for compliance

### After Phase 2:
- ✅ Can produce comparative financial statements (monthly)
- ✅ Can calculate all financial ratios
- ✅ Have audit trail for all transactions
- ✅ Revenue recognized properly (% completion)

### After Phase 3:
- ✅ Supporting documentation matches financial statements
- ✅ Can withstand external audit review
- ✅ Tax-ready documentation
- ✅ Bank covenant compliance reporting ready

---

## Tools & Scripts Needed

### Python Script: `create_gl_foundation.py`
- Generate Chart of Accounts
- Create opening journal entries
- Populate Trial Balance

### Python Script: `generate_monthly_close.py`
- Pull data from existing Excel files
- Generate Income Statement
- Generate Balance Sheet
- Generate Cash Flow Statement
- Auto-calculate financial ratios

### Python Script: `create_realistic_pdfs.py`
- Generate PDF invoices from Excel data
- Generate bank statements
- Generate loan documentation
- Generate insurance certificates

---

## Success Metrics

**Phase 1 Complete when:**
1. All folders and files created
2. Chart of Accounts has 30+ accounts
3. Trial Balance for June 2024 exists and balances
4. All 4 monthly close packages exist

**Phase 2 Complete when:**
5. All existing Excel files have GL account mapping
6. Opening balances documented
7. AR/AP aging reports created
8. Revenue recognition schedule complete

**Phase 3 Complete when:**
9. 20+ realistic PDF documents created
10. All PDF amounts match Excel data
11. Data quality checklist 100% checked

**Overall Success:**
12. Can generate complete 3-statement financial package for any month
13. All financial ratios calculatable
14. Zero data inconsistencies
15. Demo-ready for client presentation

---

## Next Steps

1. ✅ Save this plan to wiki
2. ⏭️  Run `create_gl_foundation.py` script
3. ⏭️  Run `generate_monthly_close.py` script
4. ⏭️  Run `create_realistic_pdfs.py` script
5. ⏭️  QA all data for consistency
6. ⏭️  Update development log
7. ⏭️  Commit and push to GitHub

---

**Status:** Plan documented
**Next Action:** Execute Phase 1 - Create GL foundation files
**Estimated Completion:** 2-3 hours for Phase 1
