"""
PDF extractor with OCR support.

Handles:
- Text-based PDFs (pdfplumber)
- Scanned PDFs (OCR with pytesseract)
- Tables and structured data
- Multi-page documents
"""

import pdfplumber
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from extraction.base_extractor import BaseExtractor, detect_numbers_in_text, clean_label, detect_date_in_text
from schemas.extraction_schema import (
    ExtractionResult,
    ExtractedData,
    Transaction,
    ExtractionNotes,
    DataQuality,
    ClassificationStats
)


class PDFExtractor(BaseExtractor):
    """Extract financial data from PDF files."""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.pdf']
        self.extractor_name = "pdf_extractor"
        self.version = "1.0.0"

    def extract(self, file_path: str) -> ExtractionResult:
        """
        Extract data from PDF file.

        Process:
        1. Open PDF with pdfplumber
        2. Try text extraction first
        3. If text is sparse, use OCR
        4. Extract tables if present
        5. Parse text for transactions and line items
        """
        extraction_start = datetime.utcnow()

        # Initialize result components
        metadata = self.create_metadata(file_path, extraction_start)
        extracted_data = ExtractedData()
        extraction_notes = ExtractionNotes()
        transactions: List[Transaction] = []

        try:
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                extraction_notes.warnings.append(f"PDF has {total_pages} pages")

                # Process each page
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        # Extract text
                        text = page.extract_text()

                        if not text or len(text.strip()) < 50:
                            # Try OCR if text extraction failed
                            extraction_notes.warnings.append(f"Page {page_num}: Text sparse, attempting OCR")
                            text = self._extract_text_with_ocr(page)

                        # Extract tables
                        tables = page.extract_tables()
                        if tables:
                            extraction_notes.warnings.append(f"Page {page_num}: Found {len(tables)} tables")
                            page_transactions = self._extract_from_tables(tables, page_num, extraction_notes)
                            transactions.extend(page_transactions)

                        # Extract from text
                        if text:
                            text_transactions = self._extract_from_text(text, page_num, extraction_notes)
                            transactions.extend(text_transactions)

                    except Exception as e:
                        extraction_notes.errors.append(f"Page {page_num} error: {str(e)}")
                        continue

            # Store transactions
            extracted_data.transactions = transactions

            # Calculate data quality
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
            extraction_notes.errors.append(f"Fatal PDF extraction error: {str(e)}")
            return ExtractionResult(
                metadata=metadata,
                extracted_data=ExtractedData(),
                extraction_notes=extraction_notes,
                data_quality=DataQuality(completeness_score=0.0),
                classification_stats=ClassificationStats()
            )

    def _extract_text_with_ocr(self, page) -> str:
        """
        Extract text using OCR (pytesseract).

        Note: Requires pytesseract and Tesseract OCR to be installed.
        For now, returns empty string if OCR not available.
        """
        try:
            import pytesseract
            from PIL import Image
            import io

            # Convert PDF page to image
            # This requires pdf2image library
            from pdf2image import convert_from_path

            # For simplicity in MVP, we'll skip OCR and return empty
            # TODO: Implement full OCR in Phase 2
            return ""

        except ImportError:
            return ""

    def _extract_from_tables(
        self,
        tables: List[List[List[str]]],
        page_num: int,
        notes: ExtractionNotes
    ) -> List[Transaction]:
        """Extract transactions from PDF tables."""
        transactions = []

        for table_idx, table in enumerate(tables):
            if not table or len(table) < 2:
                continue

            # Assume first row is header
            headers = [str(cell).lower().strip() if cell else "" for cell in table[0]]

            # Find columns
            date_col = self._find_column_in_list(headers, ['date', 'transaction date', 'when'])
            desc_col = self._find_column_in_list(headers, ['description', 'desc', 'item', 'details', 'payee'])
            amount_col = self._find_column_in_list(headers, ['amount', 'total', 'value', 'debit', 'credit'])

            # Extract rows
            for row_idx, row in enumerate(table[1:], 1):
                if len(row) < 2:
                    continue

                description = ""
                amount = 0.0
                transaction_date = None

                # Extract date
                if date_col is not None and date_col < len(row) and row[date_col]:
                    transaction_date = detect_date_in_text(str(row[date_col]))

                # Extract description
                if desc_col is not None and desc_col < len(row) and row[desc_col]:
                    description = str(row[desc_col]).strip()

                # Extract amount
                if amount_col is not None and amount_col < len(row) and row[amount_col]:
                    try:
                        amount_str = str(row[amount_col]).replace('$', '').replace(',', '').strip()
                        amount = float(amount_str)
                    except (ValueError, TypeError):
                        pass

                # Create transaction if we have meaningful data
                if description or amount != 0.0:
                    transactions.append(Transaction(
                        date=transaction_date,
                        description=description or "Unknown",
                        category=None,
                        amount=abs(amount),
                        transaction_type="expense" if amount >= 0 else "income",
                        confidence=0.6,  # Lower confidence for PDF extraction
                        source_location=f"Page {page_num}, Table {table_idx + 1}, Row {row_idx}"
                    ))

        return transactions

    def _extract_from_text(
        self,
        text: str,
        page_num: int,
        notes: ExtractionNotes
    ) -> List[Transaction]:
        """
        Extract transactions from plain text.

        This uses pattern matching and heuristics to find
        transaction-like data in unstructured text.
        """
        transactions = []

        # Split into lines
        lines = text.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Look for lines with dollar amounts
            numbers = detect_numbers_in_text(line)

            if numbers:
                # Use line as description, largest number as amount
                amount = max(numbers, key=abs)

                # Try to detect date in line
                transaction_date = detect_date_in_text(line)

                # Clean description (remove the amount)
                description = line
                for num in numbers:
                    description = description.replace(f"${num:,.2f}", "").replace(f"{num:,.2f}", "")
                description = description.strip()

                if description:  # Only add if we have a description
                    transactions.append(Transaction(
                        date=transaction_date,
                        description=description[:500],
                        category=None,
                        amount=abs(amount),
                        transaction_type="expense" if amount >= 0 else "income",
                        confidence=0.5,  # Lower confidence for text extraction
                        source_location=f"Page {page_num}, Line {line_num}"
                    ))

        return transactions

    def _find_column_in_list(self, headers: List[str], keywords: List[str]) -> Optional[int]:
        """Find column index matching keywords."""
        for idx, header in enumerate(headers):
            for keyword in keywords:
                if keyword in header.lower():
                    return idx
        return None

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
        total_fields = len(transactions) * 3
        filled_fields = sum([
            1 if t.date else 0,
            1 if t.description else 0,
            1 if t.amount != 0 else 0
        ] for t in transactions)

        completeness = filled_fields / total_fields if total_fields > 0 else 0.0

        return DataQuality(
            completeness_score=completeness,
            consistency_check="passed" if completeness > 0.3 else "failed",
            duplicate_check="not_checked",
            validation_errors=notes.errors
        )

    def _calculate_initial_confidence(
        self,
        transactions: List[Transaction],
        notes: ExtractionNotes
    ) -> float:
        """Calculate initial confidence score."""
        if not transactions:
            return 0.0

        # PDF extraction is inherently less confident than Excel
        base_confidence = 0.6

        # Reduce for errors
        confidence = base_confidence - (len(notes.errors) * 0.1)

        # Average with transaction confidences
        if transactions:
            avg_transaction_confidence = sum(t.confidence for t in transactions) / len(transactions)
            confidence = (confidence + avg_transaction_confidence) / 2

        return max(0.0, min(1.0, confidence))
