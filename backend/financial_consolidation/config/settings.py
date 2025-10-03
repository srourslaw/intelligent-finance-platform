"""
Configuration settings for financial consolidation system
"""

import os
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DATA_DIR = BASE_DIR / "projects" / "project-a-123-sunset-blvd" / "data"

# File types to process
SUPPORTED_FILE_TYPES = ['.xlsx', '.xls', '.csv', '.pdf']

# Classification confidence thresholds
MIN_CONFIDENCE_THRESHOLD = 0.75  # 75% minimum confidence
HIGH_CONFIDENCE_THRESHOLD = 0.90  # 90% high confidence
FUZZY_MATCH_THRESHOLD = 80  # 80% similarity for fuzzy matching

# Excel settings
EXCEL_MAX_ROWS_TO_SCAN = 10000  # Limit scanning to prevent memory issues
EXCEL_HEADER_ROW_SEARCH_LIMIT = 10  # Search first 10 rows for headers

# Output settings
OUTPUT_DIR = BASE_DIR / "financial_consolidation" / "output"
OUTPUT_FILENAME = "Consolidated_Financial_Model.xlsx"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "financial_consolidation" / "logs" / "consolidation.log"

# Document type keywords
DOCUMENT_TYPE_KEYWORDS = {
    'balance_sheet': ['balance sheet', 'statement of financial position', 'assets', 'liabilities', 'equity'],
    'income_statement': ['income statement', 'profit and loss', 'p&l', 'statement of operations', 'revenue', 'expenses'],
    'cash_flow': ['cash flow', 'statement of cash flows', 'operating activities', 'investing activities'],
    'invoice': ['invoice', 'tax invoice', 'bill', 'statement'],
    'register': ['register', 'tracker', 'log', 'ledger'],
    'budget': ['budget', 'forecast', 'projection'],
    'schedule': ['schedule', 'aging', 'amortization']
}

# Financial periods
PERIODS = ['Jun 2024', 'Jul 2024', 'Aug 2024', 'Sep 2024']
START_DATE = '2024-06-01'
END_DATE = '2024-09-30'

# Currency
DEFAULT_CURRENCY = 'AUD'
CURRENCY_SYMBOLS = {'AUD': '$', 'USD': '$', 'EUR': '€', 'GBP': '£'}

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create logs directory
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
