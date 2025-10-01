# Data Structure

## Input Data Types (Messy Data)

### 1. Land Purchase Documents
**Format**: PDFs, scanned documents, Excel
**Contents**:
- Purchase agreements
- Land titles and deeds
- Closing costs breakdown
- Lawyer fees
- Survey costs
- Title insurance

### 2. Purchase Orders & Invoices
**Format**: PDFs, Excel, scanned receipts
**Contents**:
- Vendor invoices
- Material purchase orders
- Equipment rental invoices
- Supply receipts
- Payment terms and dates

### 3. Subcontractor Documents
**Format**: PDFs, Word docs, Excel
**Contents**:
- Subcontractor agreements
- Progress billing
- Change orders
- Lien waivers
- Certificates of insurance

### 4. Client Billing
**Format**: Excel, PDFs
**Contents**:
- Client invoices
- Payment schedules
- Draw requests
- Progress billing
- Payment receipts

### 5. Budget Tracking
**Format**: Excel spreadsheets
**Contents**:
- Line item budgets
- Cost codes
- Budget vs. actual
- Variance analysis
- Forecast to complete

## Normalized Data Models

### Project Model
```typescript
interface Project {
  id: string;
  name: string;
  client: string;
  address: string;
  startDate: Date;
  estimatedCompletionDate: Date;
  actualCompletionDate?: Date;
  status: 'planning' | 'active' | 'completed' | 'on-hold';
  totalBudget: number;
  totalCosts: number;
  totalRevenue: number;
  profitMargin: number;
  createdAt: Date;
  updatedAt: Date;
}
```

### Transaction Model
```typescript
interface Transaction {
  id: string;
  projectId: string;
  date: Date;
  type: 'expense' | 'revenue' | 'payment';
  category: TransactionCategory;
  description: string;
  amount: number;
  vendor?: string;
  invoiceNumber?: string;
  paymentMethod?: string;
  status: 'pending' | 'paid' | 'overdue';
  attachments?: string[]; // URLs to uploaded files
  createdAt: Date;
  updatedAt: Date;
}

type TransactionCategory =
  | 'land-purchase'
  | 'materials'
  | 'labor'
  | 'subcontractor'
  | 'equipment-rental'
  | 'permits'
  | 'insurance'
  | 'utilities'
  | 'professional-fees'
  | 'client-payment'
  | 'other';
```

### Budget Model
```typescript
interface Budget {
  id: string;
  projectId: string;
  lineItems: BudgetLineItem[];
  totalBudget: number;
  totalSpent: number;
  remainingBudget: number;
  lastUpdated: Date;
}

interface BudgetLineItem {
  id: string;
  category: string;
  costCode: string;
  description: string;
  budgetedAmount: number;
  actualAmount: number;
  variance: number;
  variancePercentage: number;
  notes?: string;
}
```

### Subcontractor Model
```typescript
interface Subcontractor {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  trade: string;
  insuranceExpiry?: Date;
  w9OnFile: boolean;
  projects: SubcontractorProject[];
}

interface SubcontractorProject {
  projectId: string;
  contractAmount: number;
  amountPaid: number;
  amountOwed: number;
  status: 'active' | 'completed';
  startDate: Date;
  completionDate?: Date;
}
```

### Invoice Model
```typescript
interface Invoice {
  id: string;
  projectId: string;
  invoiceNumber: string;
  vendor: string;
  issueDate: Date;
  dueDate: Date;
  amount: number;
  paidAmount: number;
  status: 'unpaid' | 'partial' | 'paid' | 'overdue';
  lineItems: InvoiceLineItem[];
  attachmentUrl?: string;
  paidDate?: Date;
}

interface InvoiceLineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
}
```

### Financial Statement Models

#### Income Statement
```typescript
interface IncomeStatement {
  projectId: string;
  period: DateRange;
  revenue: {
    clientPayments: number;
    total: number;
  };
  expenses: {
    landPurchase: number;
    materials: number;
    labor: number;
    subcontractors: number;
    equipmentRental: number;
    permits: number;
    insurance: number;
    utilities: number;
    professionalFees: number;
    other: number;
    total: number;
  };
  grossProfit: number;
  grossProfitMargin: number;
  netIncome: number;
  netProfitMargin: number;
}
```

#### Balance Sheet
```typescript
interface BalanceSheet {
  projectId: string;
  asOfDate: Date;
  assets: {
    currentAssets: {
      cash: number;
      accountsReceivable: number;
      total: number;
    };
    fixedAssets: {
      land: number;
      construction: number;
      total: number;
    };
    totalAssets: number;
  };
  liabilities: {
    currentLiabilities: {
      accountsPayable: number;
      accruals: number;
      total: number;
    };
    longTermLiabilities: {
      loans: number;
      total: number;
    };
    totalLiabilities: number;
  };
  equity: {
    ownerEquity: number;
    retainedEarnings: number;
    total: number;
  };
}
```

#### Cash Flow Statement
```typescript
interface CashFlowStatement {
  projectId: string;
  period: DateRange;
  operatingActivities: {
    cashFromCustomers: number;
    cashToSuppliers: number;
    cashToEmployees: number;
    netCashFromOperations: number;
  };
  investingActivities: {
    landPurchase: number;
    equipmentPurchase: number;
    netCashFromInvesting: number;
  };
  financingActivities: {
    loansReceived: number;
    loansRepaid: number;
    netCashFromFinancing: number;
  };
  netCashFlow: number;
  beginningCash: number;
  endingCash: number;
}
```

## Database Schemas (Planned - PostgreSQL)

### Projects Table
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  client VARCHAR(255) NOT NULL,
  address TEXT,
  start_date DATE NOT NULL,
  estimated_completion_date DATE,
  actual_completion_date DATE,
  status VARCHAR(50) NOT NULL,
  total_budget DECIMAL(12,2) DEFAULT 0,
  total_costs DECIMAL(12,2) DEFAULT 0,
  total_revenue DECIMAL(12,2) DEFAULT 0,
  profit_margin DECIMAL(5,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id UUID REFERENCES users(id)
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  type VARCHAR(50) NOT NULL,
  category VARCHAR(100) NOT NULL,
  description TEXT,
  amount DECIMAL(12,2) NOT NULL,
  vendor VARCHAR(255),
  invoice_number VARCHAR(100),
  payment_method VARCHAR(50),
  status VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_project_id ON transactions(project_id);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_category ON transactions(category);
```

### Budgets Table
```sql
CREATE TABLE budgets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE UNIQUE,
  total_budget DECIMAL(12,2) NOT NULL,
  total_spent DECIMAL(12,2) DEFAULT 0,
  remaining_budget DECIMAL(12,2) DEFAULT 0,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budget_line_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  budget_id UUID REFERENCES budgets(id) ON DELETE CASCADE,
  category VARCHAR(100) NOT NULL,
  cost_code VARCHAR(50),
  description TEXT,
  budgeted_amount DECIMAL(12,2) NOT NULL,
  actual_amount DECIMAL(12,2) DEFAULT 0,
  variance DECIMAL(12,2) DEFAULT 0,
  variance_percentage DECIMAL(5,2) DEFAULT 0,
  notes TEXT
);
```

## Data Transformation Pipeline

### Phase 1: File Upload
1. User uploads PDF/Excel file
2. Store raw file in S3
3. Create upload record in database
4. Queue for processing

### Phase 2: Data Extraction
1. Identify file type (PDF, Excel, image)
2. Extract text/data using appropriate parser:
   - PDF: PyPDF2 or pdfplumber
   - Excel: pandas
   - Images: OCR (Tesseract/AWS Textract)
3. Send extracted text to AI for structured extraction

### Phase 3: AI Processing
1. Use OpenAI API to extract structured data:
   ```
   Prompt: "Extract transaction details from the following invoice:
   - Date
   - Vendor
   - Amount
   - Line items
   - Invoice number"
   ```
2. Receive structured JSON response
3. Validate extracted data

### Phase 4: Validation
1. Check for required fields
2. Validate data types and formats
3. Check for duplicates
4. Flag suspicious entries

### Phase 5: Storage
1. Store validated transactions in database
2. Update project totals
3. Update budget calculations
4. Link to original uploaded file

### Phase 6: Notification
1. Notify user of processing completion
2. Display extracted data for review
3. Allow manual corrections if needed

## Data Validation Rules

### Transaction Validation
- Amount must be > 0
- Date cannot be in future
- Category must match predefined list
- Invoice number must be unique per vendor

### Budget Validation
- Line item amounts must sum to total budget
- Cost codes must follow standard format
- Variance calculations must be accurate

### Invoice Validation
- Due date must be after issue date
- Line items must sum to invoice total
- Vendor must exist in system
