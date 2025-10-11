# Financial Builder - Production Pipeline Architecture

## Overview

**Goal**: Extract data from ALL files in any project folder → Map to MASTER template → Populate project-specific Financial Model Excel

**Key Requirement**: Must work for ANY project, not just project-a-123-sunset-blvd

---

## System Architecture

```
User selects project → Backend processes ALL files → AI categorization → Excel population
```

### Multi-Project Support Strategy

Each project has:
- Unique folder: `backend/projects/{project_id}/`
- Data subfolder: `backend/projects/{project_id}/data/` (contains 100+ files)
- MASTER template: `backend/projects/{project_id}/MASTER FINANCIAL STATEMENT TEMPLATE.md`
- Target Excel: `backend/projects/{project_id}/{project_id}_Financial_Model.xlsx`

**The pipeline is parameterized by `project_id`** - same code, different data sources.

---

## Phase 1: Template Parser

### Purpose
Parse the MASTER template MD file into a structured JSON dictionary for AI mapping.

### Input
```
backend/projects/{project_id}/MASTER FINANCIAL STATEMENT TEMPLATE.md
```

### Output (JSON Structure)
```json
{
  "balance_sheet": {
    "assets": {
      "current_assets": {
        "cash_and_cash_equivalents": {
          "items": [
            "Cash on Hand (Petty Cash)",
            "Cash in Bank - Operating Account",
            "Cash in Bank - Savings Account",
            "Cash in Bank - Payroll Account"
          ],
          "keywords": ["cash", "bank", "petty cash", "operating account"],
          "excel_cell": null  // To be mapped manually or via config
        },
        "accounts_receivable": {
          "items": [
            "Trade Receivables",
            "Notes Receivable (< 1 year)",
            "Receivables from Officers/Employees"
          ],
          "keywords": ["receivable", "debtors", "trade receivables", "AR"],
          "excel_cell": null
        }
      }
    }
  },
  "income_statement": {
    "revenue": {
      "items": [
        "Gross Sales Revenue",
        "Product Sales",
        "Service Revenue",
        "License Revenue"
      ],
      "keywords": ["sales", "revenue", "income", "billing", "invoices"],
      "excel_cell": null
    },
    "cogs": {
      "items": [
        "Raw Materials Purchased",
        "Direct Labor",
        "Manufacturing Overhead"
      ],
      "keywords": ["materials", "labor", "production", "manufacturing", "cost of goods"],
      "excel_cell": null
    },
    "operating_expenses": {
      "selling_expenses": {
        "items": [
          "Salaries - Sales Staff",
          "Sales Commissions",
          "Advertising and Promotion"
        ],
        "keywords": ["advertising", "marketing", "sales", "commissions"],
        "excel_cell": null
      },
      "administrative_expenses": {
        "items": [
          "Salaries - Administrative Staff",
          "Office Rent",
          "Utilities",
          "Insurance"
        ],
        "keywords": ["rent", "utilities", "insurance", "office", "admin"],
        "excel_cell": null
      }
    }
  }
}
```

### Algorithm
```python
def parse_master_template(project_id: str):
    """
    Parse MASTER template MD into hierarchical JSON dictionary.

    Steps:
    1. Read MD file line by line
    2. Detect sections: BALANCE SHEET, INCOME STATEMENT, CASH FLOW, etc.
    3. Build hierarchy based on indentation/headings
    4. Extract line items
    5. Generate keywords from line item names (using NLP)
    6. Store in structured JSON

    Returns: Dict with full template structure
    """
    template_path = f"backend/projects/{project_id}/MASTER FINANCIAL STATEMENT TEMPLATE.md"

    # Parse logic here
    # Use regex to detect sections
    # Build nested dict structure

    return template_dict
```

### API Endpoint
```
POST /api/financial-builder/{project_id}/parse-template
Response: { "template": {...}, "total_categories": 250 }
```

---

## Phase 2: Bulk File Extraction

### Purpose
Extract data from ALL files in project's data folder using appropriate method (MinerU for PDF, openpyxl for Excel).

### Input
```
backend/projects/{project_id}/data/
  - invoices/
    - invoice_001.pdf
    - invoice_002.pdf
  - contracts/
    - contract_electrician.pdf
  - bank_statements/
    - statement_jan.pdf
  - budgets/
    - budget_2024.xlsx
  - receipts/
    - receipt_*.pdf
```

### Process
```python
def extract_all_files(project_id: str):
    """
    Extract data from all files in project data folder.

    Steps:
    1. Scan project data folder recursively
    2. For each file:
       - If PDF: Use MinerU extraction
       - If Excel: Use openpyxl to read cells
       - If image: OCR with Tesseract (optional)
    3. Store extracted data with metadata
    4. Track progress (X/144 files)

    Returns: List of extracted transactions
    """
    data_path = f"backend/projects/{project_id}/data/"

    all_files = glob_recursive(data_path)
    extracted_data = []

    for idx, file_path in enumerate(all_files):
        if file_path.endswith('.pdf'):
            result = extract_pdf_mineru(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            result = extract_excel(file_path)
        else:
            continue

        extracted_data.append({
            "file_name": file_path,
            "transactions": result.transactions,
            "confidence": result.confidence,
            "extraction_date": datetime.now()
        })

        # Emit progress update
        emit_progress(project_id, "extraction", idx + 1, len(all_files))

    # Save to database
    save_extracted_data(project_id, extracted_data)

    return extracted_data
```

### Database Schema (SQLite or PostgreSQL)
```sql
CREATE TABLE extracted_data (
    id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT,  -- 'pdf', 'excel', 'image'
    extraction_method TEXT,  -- 'mineru', 'pdfplumber', 'openpyxl'
    transactions JSON,  -- Array of transaction objects
    confidence REAL,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_project (project_id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    extraction_id INTEGER REFERENCES extracted_data(id),
    description TEXT,
    amount REAL,
    date TEXT,
    category TEXT,  -- Will be set in Phase 3
    confidence REAL,
    raw_text TEXT,
    INDEX idx_project (project_id)
);
```

### API Endpoint
```
POST /api/financial-builder/{project_id}/extract-all
Response: {
    "status": "processing",
    "files_processed": 0,
    "total_files": 144,
    "job_id": "uuid"
}

GET /api/financial-builder/{project_id}/extract-all/status/{job_id}
Response: {
    "status": "processing" | "completed" | "error",
    "files_processed": 72,
    "total_files": 144,
    "progress_percent": 50,
    "extracted_transactions": 450
}
```

---

## Phase 3: AI Categorization & Mapping

### Purpose
Use AI to map each extracted transaction to the correct category in MASTER template.

### Algorithm
```python
def categorize_transactions(project_id: str):
    """
    AI-powered categorization using template dictionary.

    Steps:
    1. Load template dictionary (from Phase 1)
    2. Load all extracted transactions (from Phase 2)
    3. For each transaction:
       a. Extract features (description, amount, keywords)
       b. Use NLP/embeddings to match to template categories
       c. Calculate confidence score
       d. Assign category
    4. Flag low-confidence items for manual review
    5. Update database with categories

    Returns: Categorized transactions
    """
    template = load_template_dict(project_id)
    transactions = load_transactions(project_id)

    categorized = []

    for txn in transactions:
        # AI categorization logic
        best_match = find_best_category_match(
            txn.description,
            txn.amount,
            template
        )

        txn.category = best_match.category
        txn.confidence = best_match.confidence
        txn.template_path = best_match.path  # e.g., "income_statement.revenue"

        categorized.append(txn)

    # Update database
    update_transaction_categories(project_id, categorized)

    return categorized
```

### AI Matching Strategy

**Option 1: Keyword Matching (Simple, Fast)**
```python
def find_best_category_match(description, amount, template):
    # Extract keywords from description
    desc_keywords = extract_keywords(description)

    best_score = 0
    best_category = None

    # Search all template categories
    for category_path, category_data in flatten_template(template):
        # Match keywords
        overlap = set(desc_keywords) & set(category_data['keywords'])
        score = len(overlap) / len(category_data['keywords'])

        # Adjust based on amount (positive = revenue, negative = expense)
        if amount > 0 and 'revenue' in category_path:
            score *= 1.5
        elif amount < 0 and 'expense' in category_path:
            score *= 1.5

        if score > best_score:
            best_score = score
            best_category = category_path

    return {
        "category": best_category,
        "confidence": best_score
    }
```

**Option 2: LLM-based (More Accurate, Slower)**
```python
def find_best_category_match_llm(description, amount, template):
    # Use OpenAI/Claude API
    prompt = f"""
    Given this financial transaction:
    Description: {description}
    Amount: ${amount}

    Categorize it into one of these categories:
    {json.dumps(template, indent=2)}

    Return JSON: {{"category": "path.to.category", "confidence": 0.0-1.0, "reasoning": "..."}}
    """

    response = openai_api_call(prompt)
    return response
```

**Recommendation**: Start with Option 1 (keyword matching), add Option 2 as fallback for low confidence.

### API Endpoint
```
POST /api/financial-builder/{project_id}/categorize
Response: {
    "status": "completed",
    "total_transactions": 450,
    "categorized": 445,
    "low_confidence": 5,
    "categories": {
        "revenue": 120,
        "cogs": 80,
        "operating_expenses": 245,
        "other": 5
    }
}
```

---

## Phase 4: Data Aggregation

### Purpose
Aggregate all categorized transactions by template category for Excel population.

### Algorithm
```python
def aggregate_data(project_id: str):
    """
    Aggregate transactions by category.

    Steps:
    1. Load all categorized transactions
    2. Group by template category path
    3. Sum amounts per category
    4. Calculate totals and subtotals
    5. Prepare for Excel mapping

    Returns: Aggregated data ready for Excel
    """
    transactions = load_categorized_transactions(project_id)

    aggregated = {}

    for txn in transactions:
        category_path = txn.template_path

        if category_path not in aggregated:
            aggregated[category_path] = {
                "total_amount": 0,
                "transaction_count": 0,
                "source_files": set(),
                "confidence_avg": 0
            }

        aggregated[category_path]["total_amount"] += txn.amount
        aggregated[category_path]["transaction_count"] += 1
        aggregated[category_path]["source_files"].add(txn.file_name)
        aggregated[category_path]["confidence_avg"] += txn.confidence

    # Calculate averages
    for category in aggregated.values():
        category["confidence_avg"] /= category["transaction_count"]
        category["source_files"] = list(category["source_files"])

    return aggregated
```

### Output Example
```json
{
  "income_statement.revenue": {
    "total_amount": 1250000.00,
    "transaction_count": 120,
    "source_files": ["invoice_001.pdf", "contract_A.pdf", ...],
    "confidence_avg": 0.92
  },
  "income_statement.cogs.direct_labor": {
    "total_amount": -450000.00,
    "transaction_count": 80,
    "source_files": ["payroll_jan.xlsx", "labor_invoice.pdf", ...],
    "confidence_avg": 0.88
  }
}
```

### API Endpoint
```
POST /api/financial-builder/{project_id}/aggregate
Response: {
    "status": "completed",
    "aggregated_categories": 45,
    "total_revenue": 1250000,
    "total_expenses": -850000,
    "net_income": 400000
}
```

---

## Phase 5: Excel Cell Mapping

### Problem
We have aggregated data by template category, but we need to know WHICH Excel cell to populate.

### Solution: Excel Mapping Configuration

**Option A: Manual Mapping File (Recommended)**
```json
// backend/projects/{project_id}/excel_mapping.json
{
  "income_statement.revenue": "B10",
  "income_statement.cogs": "B25",
  "income_statement.operating_expenses.salaries": "B45",
  "balance_sheet.assets.cash": "B5",
  ...
}
```

**Option B: Sheet Name + Row Labels (More Flexible)**
```python
def find_excel_cell(workbook, category_path):
    """
    Find cell by searching for category name in Excel.

    Strategy:
    1. Split category path: "income_statement.revenue" → "Revenue"
    2. Search all sheets for cell containing "Revenue"
    3. Return cell to the right of label (value cell)
    """
    search_term = category_path.split('.')[-1].replace('_', ' ').title()

    for sheet in workbook.sheets:
        for row in sheet.rows:
            for cell in row:
                if search_term in cell.value:
                    # Value is typically in next column
                    return f"{chr(ord(cell.column) + 1)}{cell.row}"

    return None
```

**Recommendation**: Use Option A for critical categories, Option B as fallback.

---

## Phase 6: Excel Population

### Purpose
Write aggregated data to Excel file.

### Algorithm
```python
from openpyxl import load_workbook

def populate_excel(project_id: str):
    """
    Populate Excel Financial Model with aggregated data.

    Steps:
    1. Load aggregated data
    2. Load Excel mapping configuration
    3. Load target Excel file
    4. For each category:
       a. Find target cell
       b. Write value
       c. Preserve formatting
    5. Save updated Excel
    6. Create backup of original

    Returns: Path to populated Excel
    """
    aggregated = load_aggregated_data(project_id)
    mapping = load_excel_mapping(project_id)
    excel_path = f"backend/projects/{project_id}/{project_id}_Financial_Model.xlsx"

    # Backup original
    backup_excel(excel_path)

    # Load workbook
    wb = load_workbook(excel_path)
    sheet = wb.active  # or specify sheet name

    # Populate cells
    for category_path, data in aggregated.items():
        cell_ref = mapping.get(category_path)

        if cell_ref:
            sheet[cell_ref] = data["total_amount"]

            # Add comment with metadata
            cell = sheet[cell_ref]
            cell.comment = f"Auto-populated from {data['transaction_count']} transactions\nConfidence: {data['confidence_avg']:.2f}"

    # Save
    output_path = f"backend/projects/{project_id}/{project_id}_Financial_Model_POPULATED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(output_path)

    return output_path
```

### API Endpoint
```
POST /api/financial-builder/{project_id}/populate-excel
Response: {
    "status": "completed",
    "output_file": "project-a-123-sunset-blvd_Financial_Model_POPULATED_20251011_143022.xlsx",
    "cells_populated": 45,
    "download_url": "/api/download/{file_id}"
}
```

---

## Complete Pipeline Orchestration

### Master Endpoint
```python
@router.post("/api/financial-builder/{project_id}/run-full-pipeline")
async def run_full_pipeline(project_id: str, background_tasks: BackgroundTasks):
    """
    Orchestrate all 5 phases of the pipeline.

    Runs in background, emits progress updates via WebSocket or polling.
    """
    job_id = str(uuid4())

    # Start background job
    background_tasks.add_task(
        execute_pipeline,
        project_id,
        job_id
    )

    return {"job_id": job_id, "status": "started"}


async def execute_pipeline(project_id: str, job_id: str):
    try:
        # Phase 1: Parse template
        update_job_status(job_id, "template_parsing", 0)
        template = parse_master_template(project_id)
        update_job_status(job_id, "template_parsing", 100)

        # Phase 2: Extract all files
        update_job_status(job_id, "extraction", 0)
        extracted = await extract_all_files_async(project_id, job_id)
        update_job_status(job_id, "extraction", 100)

        # Phase 3: Categorize
        update_job_status(job_id, "categorization", 0)
        categorized = categorize_transactions(project_id)
        update_job_status(job_id, "categorization", 100)

        # Phase 4: Aggregate
        update_job_status(job_id, "aggregation", 0)
        aggregated = aggregate_data(project_id)
        update_job_status(job_id, "aggregation", 100)

        # Phase 5: Populate Excel
        update_job_status(job_id, "excel_population", 0)
        output_file = populate_excel(project_id)
        update_job_status(job_id, "excel_population", 100)

        # Complete
        complete_job(job_id, output_file)

    except Exception as e:
        fail_job(job_id, str(e))
```

### Progress Tracking
```python
# Store job status in Redis or SQLite
def update_job_status(job_id, stage, progress):
    db.update({
        "job_id": job_id,
        "stage": stage,
        "progress": progress,
        "updated_at": datetime.now()
    })
```

### Frontend Polling
```typescript
// Frontend polls this endpoint
GET /api/financial-builder/jobs/{job_id}/status
Response: {
    "job_id": "uuid",
    "stage": "extraction",
    "progress": 45,
    "stages": [
        {"name": "template_parsing", "status": "completed", "progress": 100},
        {"name": "extraction", "status": "processing", "progress": 45, "files_processed": 65, "total_files": 144},
        {"name": "categorization", "status": "pending", "progress": 0},
        ...
    ]
}
```

---

## Multi-Project Support Implementation

### Database Structure
```sql
-- Track projects
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT,
    folder_path TEXT,
    template_path TEXT,
    excel_path TEXT,
    created_at TIMESTAMP
);

-- All data tables have project_id foreign key
-- This ensures data isolation per project
```

### API Pattern
All endpoints follow pattern: `/api/financial-builder/{project_id}/...`

This ensures:
- Data isolation
- Easy scaling
- Clear project context

---

## Error Handling & Validation

### Validation Rules
1. **File Validation**
   - Check file exists before extraction
   - Validate PDF is readable
   - Validate Excel structure

2. **Data Validation**
   - Ensure amounts are numeric
   - Validate dates
   - Check for duplicates

3. **Confidence Thresholds**
   - Flag transactions with confidence < 0.7
   - Require manual review before Excel population

4. **Excel Validation**
   - Verify target cells exist
   - Don't overwrite formula cells
   - Preserve formatting

### Error Recovery
```python
# If extraction fails on file 72/144
# Save progress up to file 71
# Allow user to resume from file 72
```

---

## Performance Considerations

### For 144 Files:
- **Extraction**: ~2-5 minutes (depends on PDF size)
- **Categorization**: ~30 seconds (keyword matching)
- **Aggregation**: <1 second
- **Excel population**: ~5 seconds

**Total Estimated Time**: 3-6 minutes

### Optimization Strategies:
1. **Parallel Processing**: Extract multiple PDFs concurrently
2. **Caching**: Cache template dictionary
3. **Database Indexing**: Index on project_id
4. **Progress Checkpoints**: Save after each file

---

## Security Considerations

1. **File Upload Limits**: Max 100MB per file
2. **Path Traversal Prevention**: Validate project_id doesn't contain ../
3. **Excel Macros**: Disable macro execution
4. **Data Isolation**: Ensure users can only access their projects

---

## Testing Strategy

### Unit Tests
- Test template parser with sample MD
- Test extraction on sample PDFs
- Test categorization algorithm

### Integration Tests
- Run full pipeline on test project (10 files)
- Verify Excel output matches expectations

### End-to-End Test
- Create test project with known data
- Run pipeline
- Validate Excel contains correct values

---

## Deployment Considerations

### Requirements
```
Python 3.10+
FastAPI
openpyxl
pdfplumber
mineru (if using)
SQLite or PostgreSQL
```

### Environment Variables
```
PROJECT_BASE_PATH=/path/to/projects
MAX_FILE_SIZE_MB=100
EXTRACTION_TIMEOUT_SECONDS=300
ENABLE_LLM_CATEGORIZATION=false
OPENAI_API_KEY=xxx (if using LLM)
```

---

## Next Steps for Implementation

1. ✅ Frontend page created
2. Build template parser
3. Build bulk extraction endpoint
4. Build categorization engine
5. Build aggregation service
6. Build Excel populator
7. Test with project-a-123-sunset-blvd
8. Create excel_mapping.json for project
9. Test end-to-end
10. Deploy

---

## Questions for Review

1. **Excel Mapping**: Should I create a manual mapping file or auto-detect cells?
2. **LLM Integration**: Do you want to use OpenAI/Claude for categorization or stick with keyword matching?
3. **Manual Review**: Do you want a UI for reviewing low-confidence categorizations before Excel population?
4. **Progress Updates**: WebSocket or polling for real-time updates?
5. **Multi-user**: Will multiple users process different projects simultaneously?

---

**Status**: Architecture Complete - Ready for Your Feedback!
