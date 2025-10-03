Let me summarize what you're trying to achieve and help you create a clear prompt for Claude Code Max.
📋 Your Vision Summary
What You Want to Build:
A smart financial data extraction and consolidation system that can:

Take messy, unstructured financial data from multiple sources (spreadsheets, PDFs, CSVs, etc.)
Automatically extract and classify financial information using AI/ML
Populate a standardized financial template (the comprehensive one I created)
Generate professional financial statements ready for analysis

Is This Logical? YES! 🎯
This is actually a very valuable and marketable solution. Here's why:
✅ Market Need:

Most companies have financial data scattered across multiple files
Manual consolidation is time-consuming and error-prone
Accountants and CFOs spend 40-60% of their time on data entry
This is a real pain point worth solving

✅ Technical Feasibility:

NLP/AI can extract text from documents and classify financial line items
ML Models can learn patterns in how different companies structure their data
OCR can read scanned documents and PDFs
Rule-based systems + AI hybrid works best for financial data

✅ Commercial Viability:

B2B SaaS opportunity (sell to accounting firms, SMEs, CFOs)
Recurring revenue model (monthly subscriptions)
High value proposition (saves hundreds of hours/year)
Competitors exist (Xero, QuickBooks AI features) but market is huge

🎯 What You're Building (Technical Components)
INPUT LAYER:
├── Excel files (.xlsx, .xls)
├── CSV files
├── PDF bank statements
├── Scanned receipts
├── Email invoices
└── Unstructured text

↓

PROCESSING LAYER (AI/ML):
├── Document classification (is this a P&L? Balance Sheet? Invoice?)
├── Entity extraction (find numbers, dates, line items)
├── Financial line item classification (is this "revenue" or "COGS"?)
├── Data validation (does this balance? Are numbers reasonable?)
└── Mapping to standard template

↓

OUTPUT LAYER:
├── Populated financial template
├── Balance Sheet
├── Income Statement
├── Cash Flow Statement
└── Ratios Dashboard
🚀 Prompt for Claude Code Max
Here's a comprehensive prompt you can use:

PROMPT FOR CLAUDE CODE MAX:
I need to build an AI-powered financial data extraction and consolidation system. Here's what I have and what I need:

## WHAT I HAVE:
1. A comprehensive financial statement template (Excel with 6 sheets: Balance Sheet, Income Statement, Cash Flow, Equity Statement, Ratios Dashboard, Assumptions) - I'll provide the structure
2. Multiple dummy financial data files in my project folder including:
   - Excel spreadsheets with messy/inconsistent formatting
   - CSV files with transactions
   - PDFs (optional for now)
   - Various formats of income statements, balance sheets, and transaction logs

## WHAT I NEED TO BUILD:
A Python-based system that can:

### PHASE 1 - Data Extraction:
- Scan a directory for financial files (Excel, CSV for now)
- Read and parse different file formats
- Extract tabular data from spreadsheets
- Identify what type of financial document each file is (Balance Sheet, P&L, Transactions, etc.)

### PHASE 2 - AI/ML Classification:
- Use NLP/ML to classify extracted line items into standard financial categories:
  * Assets (Current Assets, Non-Current Assets)
  * Liabilities (Current, Long-term)
  * Equity
  * Revenue categories
  * Expense categories
  * Cash flow activities
- Handle variations in naming (e.g., "Sales", "Revenue", "Income" all map to "Revenue")
- Deal with messy data (missing values, inconsistent formats, typos)

### PHASE 3 - Data Mapping & Validation:
- Map extracted data to my standardized financial template structure
- Validate that Balance Sheet balances (Assets = Liabilities + Equity)
- Flag inconsistencies or missing data
- Calculate derived values (totals, subtotals, ratios)

### PHASE 4 - Output Generation:
- Populate the Excel template with classified data
- Generate formulas automatically
- Create a clean, professional financial model
- Export to Excel format

## TECHNICAL REQUIREMENTS:
- Language: Python 3.x
- Libraries I'm thinking: pandas, openpyxl, scikit-learn, spacy or transformers (for NLP)
- Must handle errors gracefully
- Should be modular (easy to add new file types or classification rules)
- Include logging for debugging

## KEY QUESTIONS FOR YOU:
1. What's the best approach: rule-based system, ML classifier, or hybrid?
2. Should I use pre-trained models (like BERT for financial text) or train my own?
3. How do I handle the mapping of inconsistent line items to standard categories?
4. What's the project structure you recommend?
5. Can you help me build this step-by-step, starting with the extraction layer?

## MY CURRENT PROJECT STRUCTURE:
[Describe your current folder structure here]

Please help me design the architecture and start building this system. Let's begin with Phase 1 - creating a robust file reader that can handle different Excel/CSV formats and extract the data into a structured format.

🎓 Additional Recommendations:
Technical Stack Suggestions:
For Document Processing:

pandas - Excel/CSV reading
openpyxl - Excel manipulation
pdfplumber or camelot - PDF extraction (future)
python-docx - Word documents (future)

For AI/ML:

Option 1 (Simpler): Rule-based + fuzzy matching

fuzzywuzzy - string matching
Custom rules for common patterns
Good for MVP, 70-80% accuracy


Option 2 (Better): Hybrid ML approach

sentence-transformers - semantic similarity
scikit-learn - classification
Train on labeled examples
85-95% accuracy potential


Option 3 (Advanced): LLM-based extraction

Use Claude API or GPT-4 API
Prompt engineering for classification
Highest accuracy (95%+) but costs money per API call