"""
CSV file extractor.

Handles:
- Standard CSV files
- Tab-separated files
- Auto-detection of delimiters
- Various encodings
"""

import pandas as pd
import csv
from typing import List, Optional
from datetime import datetime

from extraction.base_extractor import BaseExtractor, detect_date_in_text
from schemas.extraction_schema import (
    ExtractionResult,
    ExtractedData,
    Transaction,
    ExtractionNotes,
    DataQuality,
    ClassificationStats
)


class CSVExtractor(BaseExtractor):
    """Extract financial data from CSV files."""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.csv', '.tsv', '.txt']
        self.extractor_name = "csv_extractor"
        self.version = "1.0.0"

    def extract(self, file_path: str) -> ExtractionResult:
        """Extract data from CSV file."""
        extraction_start = datetime.utcnow()

        # Initialize result components
        metadata = self.create_metadata(file_path, extraction_start)
        extracted_data = ExtractedData()
        extraction_notes = ExtractionNotes()
        transactions: List[Transaction] = []

        try:
            # Try to detect delimiter
            delimiter = self._detect_delimiter(file_path)
            extraction_notes.warnings.append(f"Detected delimiter: '{delimiter}'")

            # Read CSV
            df = pd.read_csv(file_path, delimiter=delimiter)

            extraction_notes.warnings.append(f"Found {len(df)} rows, {len(df.columns)} columns")

            # Normalize column names
            df.columns = [str(col).strip().lower() for col in df.columns]

            # Find relevant columns
            date_col = self._find_column(df.columns.tolist(), ['date', 'transaction date', 'when', 'day'])
            desc_col = self._find_column(df.columns.tolist(), ['description', 'desc', 'item', 'details', 'payee', 'memo'])
            amount_col = self._find_column(df.columns.tolist(), ['amount', 'total', 'value', 'debit', 'credit', 'price'])

            if desc_col is None and amount_col is None:
                extraction_notes.errors.append("Could not identify description or amount columns")
                return self._create_empty_result(metadata, extraction_notes)

            # Extract each row as a transaction
            for row_idx, row in df.iterrows():
                transaction = self._extract_transaction(row, row_idx, date_col, desc_col, amount_col)
                if transaction:
                    transactions.append(transaction)

            # Store transactions
            extracted_data.transactions = transactions

            # Data quality
            data_quality = self._calculate_data_quality(transactions, extraction_notes)

            # Classification stats
            classification_stats = ClassificationStats(
                total_items=len(transactions),
                classified=0,
                unmapped=len(transactions),
                avg_confidence=0.0
            )

            # Update metadata
            metadata.confidence_score = self._calculate_initial_confidence(transactions, extraction_notes)

            return ExtractionResult(
                metadata=metadata,
                extracted_data=extracted_data,
                extraction_notes=extraction_notes,
                data_quality=data_quality,
                classification_stats=classification_stats
            )

        except Exception as e:
            extraction_notes.errors.append(f"CSV extraction error: {str(e)}")
            return self._create_empty_result(metadata, extraction_notes)

    def _detect_delimiter(self, file_path: str) -> str:
        """Detect CSV delimiter (comma, tab, semicolon, etc.)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = f.read(4096)  # Read first 4KB
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                return delimiter
        except Exception:
            # Default to comma
            return ','

    def _find_column(self, columns: List[str], keywords: List[str]) -> Optional[str]:
        """Find column name matching keywords."""
        for col in columns:
            for keyword in keywords:
                if keyword in col.lower():
                    return col
        return None

    def _extract_transaction(
        self,
        row: pd.Series,
        row_idx: int,
        date_col: Optional[str],
        desc_col: Optional[str],
        amount_col: Optional[str]
    ) -> Optional[Transaction]:
        """Extract transaction from CSV row."""

        # Skip empty rows
        if row.isna().all():
            return None

        # Extract description
        description = ""
        if desc_col and not pd.isna(row[desc_col]):
            description = str(row[desc_col]).strip()

        # Extract amount
        amount = 0.0
        if amount_col:
            try:
                amount_val = row[amount_col]
                if pd.notna(amount_val):
                    if isinstance(amount_val, str):
                        amount_str = amount_val.replace('$', '').replace(',', '').strip()
                        amount = float(amount_str)
                    else:
                        amount = float(amount_val)
            except (ValueError, TypeError):
                pass

        # Extract date
        transaction_date = None
        if date_col and not pd.isna(row[date_col]):
            date_val = row[date_col]
            if isinstance(date_val, pd.Timestamp):
                transaction_date = date_val.strftime('%Y-%m-%d')
            elif isinstance(date_val, str):
                transaction_date = detect_date_in_text(date_val)

        # Only create if we have meaningful data
        if not description and amount == 0.0:
            return None

        # Use row values as description if missing
        if not description:
            non_null = [str(v) for v in row if pd.notna(v)]
            description = ' | '.join(non_null[:3]) if non_null else "Unknown"

        return Transaction(
            date=transaction_date,
            description=description[:500],
            category=None,
            amount=abs(amount),
            transaction_type="expense" if amount >= 0 else "income",
            confidence=0.8,  # High confidence for CSV
            source_location=f"Row {row_idx + 2}"  # +2 for 1-index and header
        )

    def _calculate_data_quality(self, transactions: List[Transaction], notes: ExtractionNotes) -> DataQuality:
        """Calculate data quality."""
        if not transactions:
            return DataQuality(completeness_score=0.0, consistency_check="failed")

        total_fields = len(transactions) * 3
        filled_fields = sum([
            1 if t.date else 0,
            1 if t.description else 0,
            1 if t.amount != 0 else 0
        ] for t in transactions)

        completeness = filled_fields / total_fields if total_fields > 0 else 0.0

        return DataQuality(
            completeness_score=completeness,
            consistency_check="passed" if completeness > 0.5 else "failed",
            validation_errors=notes.errors
        )

    def _calculate_initial_confidence(self, transactions: List[Transaction], notes: ExtractionNotes) -> float:
        """Calculate confidence score."""
        if not transactions:
            return 0.0

        confidence = 0.8  # High base for CSV

        confidence -= len(notes.errors) * 0.1

        if transactions:
            avg = sum(t.confidence for t in transactions) / len(transactions)
            confidence = (confidence + avg) / 2

        return max(0.0, min(1.0, confidence))

    def _create_empty_result(self, metadata, notes) -> ExtractionResult:
        """Create empty result with errors."""
        return ExtractionResult(
            metadata=metadata,
            extracted_data=ExtractedData(),
            extraction_notes=notes,
            data_quality=DataQuality(completeness_score=0.0),
            classification_stats=ClassificationStats()
        )
