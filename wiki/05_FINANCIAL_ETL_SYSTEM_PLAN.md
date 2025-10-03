# Financial ETL System - Implementation Plan

**Created**: 2025-10-03
**Status**: Planning Phase
**Goal**: Build a file-by-file financial data extraction system that feeds our existing dashboard

---

## 🎯 Executive Summary

We're building an **AI-powered financial data extraction pipeline** that:
1. Accepts messy financial files (Excel, PDF, CSV)
2. Extracts data one file at a time into structured JSON
3. Uses AI to classify and map line items to our standard categories
4. Aggregates all extractions intelligently
5. Feeds data to our existing React dashboard automatically

**Key Innovation**: Process files individually with full audit trails, rather than overwhelming AI with everything at once.

---

## 📊 Current State (What We Already Have)

### ✅ Built & Deployed:
- **Frontend**: React dashboard on Vercel with 7 financial statement tabs
  - Balance Sheet with validation
  - Income Statement with margins
  - Cash Flow Statement
  - Equity Statement
  - Ratios Dashboard (30+ ratios)
  - Assumptions & Instructions
- **Backend**: FastAPI on Render
  - JWT authentication
  - Project-based routing
  - API endpoints for budget, financial statements, documents
- **Data**: JSON files in backend for project `project-a-123-sunset-blvd`
- **GitHub**: All code version controlled

### ❌ What We Don't Have:
- Automated file upload and processing
- AI-powered data extraction from Excel/PDF
- Classification of line items to standard categories
- Aggregation of multiple files
- File monitoring system
- Confidence scoring and validation

---

## 🎯 The Problem We're Solving

**Current Workflow** (Manual):
1. Client sends 50 Excel files, 20 PDFs, invoices, receipts
2. Someone manually opens each file
3. Copies data into financial model
4. Categorizes each line item
5. Aggregates everything
6. Updates dashboard manually
7. Takes days/weeks, error-prone

**Desired Workflow** (Automated):
1. Client uploads files to system
2. System processes each file automatically
3. AI extracts and classifies data
4. System aggregates and validates
5. Dashboard updates in real-time
6. Takes minutes, traceable

---

## 🏗️ System Architecture (Simplified)

```
┌─────────────────────────────────────────────────────────┐
│  REACT DASHBOARD (Vercel)                               │
│  - File upload UI                                        │
│  - Processing status                                     │
│  - View extracted data                                   │
│  - Financial statements (existing)                       │
└─────────────────────────────────────────────────────────┘
                          ↕ REST API
┌─────────────────────────────────────────────────────────┐
│  FASTAPI BACKEND (Render)                               │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  FILE UPLOAD ENDPOINT                          │    │
│  │  - Accept file                                  │    │
│  │  - Save to storage                             │    │
│  │  - Queue for processing                        │    │
│  └────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  EXTRACTION ENGINE                             │    │
│  │  - Detect file type (Excel/PDF/CSV)            │    │
│  │  - Extract structured data                     │    │
│  │  - Output to JSON with metadata                │    │
│  └────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  AI CLASSIFIER (Claude/GPT API)                │    │
│  │  - Map line items to categories                │    │
│  │  - Assign confidence scores                    │    │
│  │  - Flag unmapped items                         │    │
│  └────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  VALIDATOR                                     │    │
│  │  - Check balance sheet balances                │    │
│  │  - Validate data types                         │    │
│  │  - Detect duplicates                           │    │
│  └────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  JSON STORAGE (per file)                       │    │
│  │  - Store extracted data                        │    │
│  │  - Store metadata & lineage                    │    │
│  │  - Store confidence scores                     │    │
│  └────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  AGGREGATION ENGINE                            │    │
│  │  - Combine all JSONs                           │    │
│  │  - Resolve conflicts                           │    │
│  │  - Calculate totals                            │    │
│  └────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌────────────────────────────────────────────────┐    │
│  │  CONSOLIDATED DATA API                         │    │
│  │  - Serve to dashboard                          │    │
│  │  - Provide drill-down to sources               │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 3-Phase Implementation Plan

### **Phase 1: MVP - Single File Processing** (2 weeks)
**Goal**: Prove the concept works with manual uploads

#### Deliverables:
1. **JSON Schema** (`schemas/extraction_schema.json`)
   - Structure for Balance Sheet items
   - Structure for Income Statement items
   - Structure for Cash Flow items
   - Metadata fields (source, confidence, timestamp)

2. **Excel Extractor** (`backend/extraction/excel_extractor.py`)
   - Read .xlsx files
   - Detect data tables
   - Extract to JSON schema
   - Handle merged cells, formulas

3. **Simple Upload Endpoint** (`backend/routes/upload.py`)
   - POST /api/upload - accept single file
   - Save to backend/uploads/
   - Return file_id

4. **AI Classifier** (`backend/classification/ai_classifier.py`)
   - Use Claude API to classify line items
   - Map to our standard categories
   - Return confidence scores
   - Cost: ~$0.01-0.05 per file

5. **Dashboard Upload UI** (React component)
   - Simple file upload form
   - Show processing status
   - Display extracted JSON
   - Show confidence scores

#### Success Criteria:
- Upload 1 Excel file
- See extracted JSON
- AI classifies 90%+ of items correctly
- View results in dashboard

#### Cost Estimation:
- Claude API: $0.01-0.05 per file
- Storage: negligible on Render
- Processing time: 10-30 seconds per file

---

### **Phase 2: Batch Processing & Aggregation** (2 weeks)
**Goal**: Handle multiple files and aggregate data

#### Deliverables:
1. **Batch Upload**
   - Upload multiple files at once
   - Processing queue
   - Progress tracking

2. **PDF Extractor** (`backend/extraction/pdf_extractor.py`)
   - Extract text from PDFs
   - OCR for scanned documents
   - Tabular data detection

3. **CSV Extractor** (`backend/extraction/csv_extractor.py`)
   - Simple CSV parsing
   - Auto-detect columns

4. **Aggregation Engine** (`backend/aggregation/aggregator.py`)
   - Combine multiple JSONs
   - Detect duplicates
   - Handle conflicts (higher confidence wins)
   - Calculate totals

5. **Validation System** (`backend/validation/validator.py`)
   - Balance Sheet balancing check
   - Income Statement validation
   - Cross-statement validation

6. **Dashboard Enhancement**
   - View all uploaded files
   - See aggregated results
   - Drill down to source files
   - Edit/correct classifications

#### Success Criteria:
- Upload 10-20 files
- System aggregates correctly
- Balance Sheet balances
- Can trace each number to source file

---

### **Phase 3: Automation & Production** (2 weeks)
**Goal**: Production-ready system with monitoring

#### Deliverables:
1. **Webhook/Trigger System**
   - Alternative to file monitoring (Render limitation)
   - Email forwarding integration
   - Zapier/Make.com integration
   - API trigger endpoint

2. **Conflict Resolution UI**
   - Show conflicting data
   - Let user choose which to keep
   - Learn from choices

3. **Export Templates**
   - Generate populated Excel
   - Export to PDF
   - CSV export

4. **Audit Trail**
   - Complete data lineage
   - Processing history
   - User actions log

5. **Error Handling & Recovery**
   - Retry failed extractions
   - Email notifications
   - Error dashboard

6. **Documentation**
   - User guide
   - API documentation
   - Deployment guide

#### Success Criteria:
- System handles 100+ files
- Reliable processing
- Clear error messages
- Production deployed

---

## 🔧 Technical Decisions

### **Data Storage Strategy**

**Option 1: File-based JSON** (Recommended for MVP)
```
backend/
  data/
    projects/
      project-a-123-sunset-blvd/
        extractions/
          file_hash_1.json
          file_hash_2.json
        aggregated/
          consolidated.json
```
- ✅ Simple, no DB needed
- ✅ Version controllable
- ✅ Works on Render
- ❌ Not scalable to 1000s of files

**Option 2: PostgreSQL** (For production scale)
- ✅ Scalable
- ✅ Queryable
- ✅ Render supports it
- ❌ Adds complexity
- ❌ Costs more

**Decision**: Start with Option 1, migrate to Option 2 in Phase 3 if needed.

---

### **AI Classification Approach**

**Option 1: Rule-based + Fuzzy Matching** (Free, 70% accuracy)
```python
if "revenue" in item.lower() or "sales" in item.lower():
    category = "revenue.product_sales"
```
- ✅ Free
- ✅ Fast
- ❌ Limited accuracy

**Option 2: LLM API (Claude/GPT)** (Best, 95% accuracy)
```python
prompt = f"Classify '{item}' into financial category..."
response = claude.classify(prompt)
```
- ✅ High accuracy
- ✅ Handles context
- ❌ Costs $0.01-0.05 per file

**Option 3: Hybrid** (Recommended)
- Use rules for obvious cases (free)
- Use LLM for ambiguous items only
- Cost: ~$0.001-0.01 per file

**Decision**: Hybrid approach - Phase 1 uses LLM for everything (prove it works), Phase 2 optimizes with rules.

---

### **File Monitoring Challenge**

**Problem**: Render uses ephemeral containers - can't watch local folders reliably.

**Solutions**:

1. **Manual Upload** (Phase 1)
   - User uploads via dashboard
   - Simple, works immediately

2. **Cloud Storage Integration** (Phase 2)
   - Watch Google Drive folder (API)
   - Watch Dropbox folder (API)
   - Webhook when file added

3. **Email Forwarding** (Phase 2)
   - User forwards files to special email
   - System processes attachments
   - SendGrid/Mailgun webhook

4. **API Trigger** (Phase 3)
   - Zapier/Make.com integration
   - Client's system POSTs to our API

**Decision**: Phase 1 = Manual upload, Phase 2 = Email + Cloud storage, Phase 3 = Full automation

---

## 📐 JSON Schema Design

### Standard Category Hierarchy
```
balance_sheet:
  assets:
    current:
      - cash_on_hand
      - cash_in_bank_operating
      - accounts_receivable
      - inventory_raw_materials
    non_current:
      - land
      - buildings
      - equipment
  liabilities:
    current:
      - accounts_payable
      - credit_card_debt
    long_term:
      - mortgage_payable
      - long_term_debt
  equity:
    - share_capital
    - retained_earnings

income_statement:
  revenue:
    - product_sales
    - service_revenue
  cogs:
    - purchases
    - direct_labor
  operating_expenses:
    - salaries_and_wages
    - rent
    - utilities
    - marketing

cash_flow:
  operating:
    - net_profit
    - depreciation
  investing:
    - purchase_of_ppe
  financing:
    - repayment_of_debt
```

### Extraction JSON Format
```json
{
  "metadata": {
    "file_id": "abc123",
    "filename": "Q3_2024_Expenses.xlsx",
    "upload_date": "2025-10-03T10:30:00Z",
    "file_type": "excel",
    "file_size_bytes": 45678,
    "extracted_by": "excel_extractor_v1",
    "extraction_duration_seconds": 12.5,
    "document_type": "expense_report"
  },

  "extracted_data": {
    "balance_sheet": {
      "assets": {
        "current": {
          "cash_on_hand": {
            "value": 50000,
            "confidence": 0.98,
            "source_cell": "Sheet1!B5",
            "raw_label": "Petty Cash"
          }
        }
      }
    },

    "transactions": [
      {
        "date": "2024-07-15",
        "description": "Office rent payment",
        "amount": 3000,
        "category": "operating_expenses.rent",
        "confidence": 0.95,
        "source_row": "Sheet1!Row_12"
      }
    ]
  },

  "validation": {
    "balance_sheet_balanced": true,
    "completeness_score": 0.87,
    "warnings": ["Cell B56 contains formula"],
    "errors": []
  },

  "classification_stats": {
    "total_items": 45,
    "classified": 42,
    "unmapped": 3,
    "avg_confidence": 0.91
  }
}
```

---

## 💰 Cost Analysis

### Per File Costs:
- **Excel Extraction**: Free (pandas/openpyxl)
- **PDF Extraction**: Free (pdfplumber) or $0.001 for OCR
- **AI Classification**: $0.01-0.05 (Claude API)
- **Storage**: $0.0001
- **Processing**: Free (Render compute)

**Total per file**: ~$0.01-0.05

### Monthly Estimates:
- **100 files/month**: $1-5
- **1000 files/month**: $10-50
- **10000 files/month**: $100-500

**Optimization**: Use rule-based for 70% of items → reduce costs by 70%

---

## ⚠️ Risks & Mitigation

### Risk 1: AI Classification Inaccuracy
- **Mitigation**:
  - Show confidence scores
  - Allow manual corrections
  - Learn from corrections (Phase 3)
  - Hybrid approach with rules

### Risk 2: File Format Variations
- **Mitigation**:
  - Start with common formats
  - Build robust parsers
  - Graceful degradation
  - Clear error messages

### Risk 3: Render Container Restarts
- **Mitigation**:
  - Store all data in persistent locations
  - Use external storage (S3) for large files
  - Stateless processing design
  - Idempotent operations

### Risk 4: Cost Overruns (API calls)
- **Mitigation**:
  - Set per-project budgets
  - Implement rate limiting
  - Use caching
  - Hybrid classification

### Risk 5: Performance (Large Files)
- **Mitigation**:
  - Async processing
  - Progress updates
  - Timeout handling
  - Background jobs

---

## 📊 Success Metrics

### Phase 1 MVP:
- ✅ 1 file uploaded and extracted
- ✅ AI classification accuracy >90%
- ✅ Processing time <30 seconds
- ✅ JSON output validates correctly

### Phase 2 Batch:
- ✅ 20 files processed successfully
- ✅ Aggregation produces correct totals
- ✅ Balance Sheet balances
- ✅ 100% data lineage trackable

### Phase 3 Production:
- ✅ 100+ files processed
- ✅ <1% error rate
- ✅ Average processing <20 seconds
- ✅ User satisfaction >4/5
- ✅ Cost per file <$0.02

---

## 🚀 Getting Started (Phase 1)

### Week 1: Foundation
**Day 1-2**: JSON Schema Design
- Design complete schema
- Create Pydantic models
- Write validation tests

**Day 3-4**: Excel Extractor
- Build basic Excel reader
- Handle common formats
- Test with sample files

**Day 5**: Upload Endpoint
- API endpoint for file upload
- Storage handling
- Return file metadata

### Week 2: Intelligence
**Day 1-2**: AI Classifier
- Claude API integration
- Prompt engineering
- Confidence scoring

**Day 3-4**: Dashboard Integration
- Upload UI component
- Show extraction results
- Display confidence scores

**Day 5**: Testing & Refinement
- End-to-end testing
- Fix issues
- Documentation

---

## 📝 Documentation Requirements

### For Each Phase:
1. **Code Comments**: Explain complex logic
2. **API Documentation**: All endpoints documented
3. **User Guide**: How to upload files
4. **Developer Guide**: How to add new extractors
5. **Troubleshooting**: Common issues and fixes

### Deliverables:
- `README.md` updates
- `wiki/06_ETL_USER_GUIDE.md`
- `wiki/07_ETL_DEVELOPER_GUIDE.md`
- API docs (FastAPI auto-generated)

---

## 🎯 What We're NOT Building (Scope Control)

### Not in MVP:
- ❌ File monitoring/watching folders
- ❌ Multi-tenant support
- ❌ White-label customization
- ❌ ML model training/retraining
- ❌ QuickBooks/Xero integrations
- ❌ Advanced reporting
- ❌ Mobile app
- ❌ Slack/Teams notifications
- ❌ Email processing
- ❌ Real-time collaboration

### Maybe Later (Phase 4+):
- Cloud storage monitoring (Google Drive, Dropbox)
- Email forwarding integration
- Improved classification with feedback loop
- Export to accounting software
- Advanced analytics

---

## 🔄 Checkpoint System

After each phase, we will:
1. Update this document with actual results
2. Update `CHECKPOINT_[DATE].md`
3. Update `03_DEVELOPMENT_LOG.md`
4. Commit all changes to GitHub
5. Tag release (v1.1.0, v1.2.0, etc.)
6. Create summary document

### Checkpoint Template:
```markdown
## Phase [X] Checkpoint - [DATE]

### Completed:
- [List what was built]

### Working Features:
- [What user can do now]

### Known Issues:
- [Any bugs or limitations]

### Next Phase Goals:
- [What's coming next]

### Files Modified:
- [List of changed files]

### Git Commits:
- [Commit hashes and messages]
```

---

## 📞 Support & Questions

If resuming this project after a break:
1. Read this document completely
2. Check latest `CHECKPOINT_[DATE].md`
3. Review `03_DEVELOPMENT_LOG.md`
4. Check git log for recent changes
5. Verify current deployment status (Vercel + Render)

---

**Last Updated**: 2025-10-03
**Next Review**: After Phase 1 completion
**Owner**: Hussein Srour
**Status**: 📋 Planning - Ready to Begin Phase 1
