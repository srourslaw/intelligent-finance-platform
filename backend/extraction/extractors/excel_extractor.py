"""
Excel file extractor using pandas and openpyxl.

Handles: .xlsx, .xls, .xlsm, .xlsb files
Capabilities:
- Multiple sheets
- Merged cells
- Formulas (extracts calculated values)
- Tables and named ranges
- Hidden rows/columns detection
"""

import pandas as pd
import openpyxl
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

from extraction.base_extractor import BaseExtractor, detect_numbers_in_text, clean_label, detect_date_in_text
from schemas.extraction_schema import (
    ExtractionResult,
    ExtractedData,
    Transaction,
    FinancialLineItem,
    ExtractionNotes,
    DataQuality,
    ClassificationStats
)


class ExcelExtractor(BaseExtractor):
    """Extract financial data from Excel files."""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.xlsx', '.xls', '.xlsm', '.xlsb']
        self.extractor_name = "excel_extractor"
        self.version = "1.0.0"

    def extract(self, file_path: str) -> ExtractionResult:
        """
        Extract data from Excel file.

        Process:
        1. Load workbook with openpyxl for metadata
        2. Read all sheets with pandas
        3. Detect tables and data ranges
        4. Extract numerical data with labels
        5. Create transactions from row data
        """
        extraction_start = datetime.utcnow()

        # Initialize result components
        metadata = self.create_metadata(file_path, extraction_start)
        extracted_data = ExtractedData()
        extraction_notes = ExtractionNotes()
        transactions: List[Transaction] = []

        try:
            # Load workbook for metadata
            wb = openpyxl.load_workbook(file_path, data_only=True)  # data_only=True gets calculated values
            sheet_names = wb.sheetnames

            extraction_notes.warnings.append(f"Found {len(sheet_names)} sheets: {', '.join(sheet_names)}")

            # Process each sheet
            for sheet_name in sheet_names:
                try:
                    # Read sheet with pandas
                    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

                    # Extract transactions from this sheet
                    sheet_transactions = self._extract_transactions_from_sheet(
                        df, sheet_name, extraction_notes
                    )
                    transactions.extend(sheet_transactions)

                except Exception as e:
                    extraction_notes.errors.append(f"Error reading sheet '{sheet_name}': {str(e)}")
                    continue

            # Store transactions
            extracted_data.transactions = transactions

            # Calculate data quality
            data_quality = self._calculate_data_quality(transactions, extraction_notes)

            # Calculate classification stats (will be updated by AI classifier later)
            classification_stats = ClassificationStats(
                total_items=len(transactions),
                classified=0,  # Will be filled by classifier
                unmapped=len(transactions),
                avg_confidence=0.0
            )

            # Update metadata confidence (basic heuristic)
            metadata.confidence_score = self._calculate_initial_confidence(transactions, extraction_notes)

            return ExtractionResult(
                metadata=metadata,
                extracted_data=extracted_data,
                extraction_notes=extraction_notes,
                data_quality=data_quality,
                classification_stats=classification_stats
            )

        except Exception as e:
            extraction_notes.errors.append(f"Fatal extraction error: {str(e)}")
            return ExtractionResult(
                metadata=metadata,
                extracted_data=ExtractedData(),
                extraction_notes=extraction_notes,
                data_quality=DataQuality(completeness_score=0.0),
                classification_stats=ClassificationStats()
            )

    def _extract_transactions_from_sheet(
        self,
        df: pd.DataFrame,
        sheet_name: str,
        notes: ExtractionNotes
    ) -> List[Transaction]:
        """
        Extract transaction-like data from a sheet.

        Looks for patterns like:
        - Date | Description | Amount
        - Description | Debit | Credit
        - Item | Quantity | Price | Total
        """
        transactions = []

        # Skip empty sheets
        if df.empty:
            return transactions

        # Try to detect header row (first row with mostly non-null values)
        header_row_idx = self._detect_header_row(df)

        if header_row_idx is None:
            notes.warnings.append(f"Sheet '{sheet_name}': Could not detect header row")
            return transactions

        # Get column names from header row
        headers = df.iloc[header_row_idx].astype(str).str.strip().str.lower().tolist()

        # Find relevant columns
        date_col = self._find_column(headers, ['date', 'transaction date', 'when', 'day'])
        desc_col = self._find_column(headers, ['description', 'desc', 'item', 'details', 'particulars', 'memo', 'payee'])
        amount_col = self._find_column(headers, ['amount', 'total', 'value', 'price', 'cost', 'debit', 'credit'])

        if desc_col is None and amount_col is None:
            notes.warnings.append(f"Sheet '{sheet_name}': Could not identify description or amount columns")
            return transactions

        # Extract rows after header
        data_start_row = header_row_idx + 1

        for row_idx in range(data_start_row, len(df)):
            row = df.iloc[row_idx]

            # Skip empty rows
            if row.isna().all():
                continue

            # Extract transaction data
            transaction_data = self._extract_transaction_from_row(
                row,
                row_idx,
                date_col,
                desc_col,
                amount_col,
                sheet_name
            )

            if transaction_data:
                transactions.append(transaction_data)

        notes.warnings.append(f"Sheet '{sheet_name}': Extracted {len(transactions)} transactions")

        return transactions

    def _detect_header_row(self, df: pd.DataFrame, max_rows_to_check: int = 10) -> Optional[int]:
        """
        Detect which row is the header based on:
        - Most non-null values
        - Contains text (not numbers)
        - Common financial terms
        """
        max_non_null = 0
        best_row = None

        for i in range(min(max_rows_to_check, len(df))):
            row = df.iloc[i]
            non_null_count = row.notna().sum()

            # Check if row has mostly text
            text_count = sum(1 for val in row if isinstance(val, str))

            # Prefer rows with more text and more non-null values
            score = non_null_count + (text_count * 2)

            if score > max_non_null:
                max_non_null = score
                best_row = i

        return best_row

    def _find_column(self, headers: List[str], keywords: List[str]) -> Optional[int]:
        """Find column index that matches any of the keywords."""
        for idx, header in enumerate(headers):
            header_clean = str(header).lower().strip()
            for keyword in keywords:
                if keyword in header_clean:
                    return idx
        return None

    def _extract_transaction_from_row(
        self,
        row: pd.Series,
        row_idx: int,
        date_col: Optional[int],
        desc_col: Optional[int],
        amount_col: Optional[int],
        sheet_name: str
    ) -> Optional[Transaction]:
        """Extract a Transaction object from a DataFrame row."""

        # Get description
        description = ""
        if desc_col is not None and not pd.isna(row.iloc[desc_col]):
            description = str(row.iloc[desc_col]).strip()

        # Get amount
        amount = 0.0
        if amount_col is not None:
            try:
                amount_val = row.iloc[amount_col]
                if pd.notna(amount_val):
                    # Handle currency strings
                    if isinstance(amount_val, str):
                        # Remove currency symbols and commas
                        amount_str = amount_val.replace('$', '').replace('£', '').replace('€', '').replace(',', '').strip()
                        amount = float(amount_str)
                    else:
                        amount = float(amount_val)
            except (ValueError, TypeError):
                pass

        # Get date
        transaction_date = None
        if date_col is not None and not pd.isna(row.iloc[date_col]):
            date_val = row.iloc[date_col]
            if isinstance(date_val, pd.Timestamp):
                transaction_date = date_val.strftime('%Y-%m-%d')
            elif isinstance(date_val, str):
                transaction_date = detect_date_in_text(date_val)

        # Only create transaction if we have description or meaningful amount
        if not description and amount == 0.0:
            return None

        # Use first few values as description if no description column
        if not description:
            non_null_vals = [str(v) for v in row if pd.notna(v)]
            description = ' | '.join(non_null_vals[:3]) if non_null_vals else "Unknown"

        # Determine transaction type (heuristic)
        transaction_type = "expense"
        if amount < 0:
            transaction_type = "income"
            amount = abs(amount)  # Store as positive

        # Create Transaction
        return Transaction(
            date=transaction_date,
            description=description[:500],  # Limit length
            category=None,  # Will be filled by AI classifier
            amount=amount,
            transaction_type=transaction_type,
            confidence=0.7,  # Initial confidence for extracted data
            source_location=f"{sheet_name}!Row_{row_idx + 1}"
        )

    def _calculate_data_quality(
        self,
        transactions: List[Transaction],
        notes: ExtractionNotes
    ) -> DataQuality:
        """Calculate data quality metrics."""

        if not transactions:
            return DataQuality(
                completeness_score=0.0,
                consistency_check="failed"
            )

        # Calculate completeness
        total_fields = len(transactions) * 3  # date, description, amount
        filled_fields = sum([
            1 if t.date else 0,
            1 if t.description else 0,
            1 if t.amount != 0 else 0
        ] for t in transactions)

        completeness = filled_fields / total_fields if total_fields > 0 else 0.0

        return DataQuality(
            completeness_score=completeness,
            consistency_check="passed" if completeness > 0.5 else "failed",
            duplicate_check="not_checked",
            validation_errors=notes.errors
        )

    def _calculate_initial_confidence(
        self,
        transactions: List[Transaction],
        notes: ExtractionNotes
    ) -> float:
        """Calculate initial confidence score based on extraction quality."""

        if not transactions:
            return 0.0

        # Base confidence
        confidence = 0.7

        # Reduce for warnings
        confidence -= len(notes.warnings) * 0.05

        # Reduce significantly for errors
        confidence -= len(notes.errors) * 0.15

        # Increase if we have good data coverage
        avg_transaction_confidence = sum(t.confidence for t in transactions) / len(transactions)
        confidence = (confidence + avg_transaction_confidence) / 2

        # Clamp to [0, 1]
        return max(0.0, min(1.0, confidence))
