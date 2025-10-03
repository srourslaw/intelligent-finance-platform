"""
Image OCR extractor using pytesseract.

Handles:
- JPG, JPEG, PNG, TIFF, BMP
- Scanned receipts and invoices
- OCR text extraction
- Preprocessing for better OCR results
"""

from typing import List, Optional
from datetime import datetime
from pathlib import Path

from extraction.base_extractor import BaseExtractor, detect_numbers_in_text, detect_date_in_text
from schemas.extraction_schema import (
    ExtractionResult,
    ExtractedData,
    Transaction,
    ExtractionNotes,
    DataQuality,
    ClassificationStats
)


class ImageExtractor(BaseExtractor):
    """Extract financial data from images using OCR."""

    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']
        self.extractor_name = "image_extractor"
        self.version = "1.0.0"

    def extract(self, file_path: str) -> ExtractionResult:
        """
        Extract data from image using OCR.

        Note: Requires pytesseract and Tesseract OCR installation.
        For MVP, provides basic extraction. Will enhance in Phase 2.
        """
        extraction_start = datetime.utcnow()

        # Initialize result components
        metadata = self.create_metadata(file_path, extraction_start)
        extracted_data = ExtractedData()
        extraction_notes = ExtractionNotes()
        transactions: List[Transaction] = []

        try:
            # Try to import OCR dependencies
            try:
                import pytesseract
                from PIL import Image
            except ImportError:
                extraction_notes.errors.append(
                    "OCR dependencies not installed (pytesseract, Pillow). "
                    "Please install: pip install pytesseract pillow"
                )
                return self._create_empty_result(metadata, extraction_notes)

            # Load image
            image = Image.open(file_path)

            # Preprocess image for better OCR
            image = self._preprocess_image(image)

            # Extract text with OCR
            text = pytesseract.image_to_string(image)

            if not text or len(text.strip()) < 10:
                extraction_notes.warnings.append("OCR extracted very little text")

            extraction_notes.warnings.append(f"OCR extracted {len(text)} characters")

            # Parse text for financial data
            transactions = self._extract_from_text(text, extraction_notes)

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
            extraction_notes.errors.append(f"Image OCR extraction error: {str(e)}")
            return self._create_empty_result(metadata, extraction_notes)

    def _preprocess_image(self, image):
        """
        Preprocess image for better OCR results.

        Techniques:
        - Convert to grayscale
        - Increase contrast
        - Denoise
        - Resize if too small
        """
        try:
            from PIL import ImageEnhance, ImageFilter

            # Convert to grayscale
            image = image.convert('L')

            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)

            # Denoise
            image = image.filter(ImageFilter.MedianFilter(size=3))

            # Resize if too small
            width, height = image.size
            if width < 1000 or height < 1000:
                scale = 2.0
                new_size = (int(width * scale), int(height * scale))
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            return image

        except Exception:
            # If preprocessing fails, return original
            return image

    def _extract_from_text(self, text: str, notes: ExtractionNotes) -> List[Transaction]:
        """Extract financial transactions from OCR text."""
        transactions = []

        # Split into lines
        lines = text.split('\n')

        # Look for receipt/invoice patterns
        total_amount = None
        vendor = None
        transaction_date = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to detect vendor (usually at top)
            if not vendor and len(line) > 3 and not any(char.isdigit() for char in line):
                vendor = line[:100]  # First non-numeric line likely vendor

            # Try to detect date
            if not transaction_date:
                date_detected = detect_date_in_text(line)
                if date_detected:
                    transaction_date = date_detected

            # Look for "TOTAL" or similar keywords
            if any(keyword in line.upper() for keyword in ['TOTAL', 'AMOUNT DUE', 'BALANCE', 'GRAND TOTAL']):
                numbers = detect_numbers_in_text(line)
                if numbers:
                    total_amount = max(numbers, key=abs)  # Largest number is likely the total

            # Extract line items (description + amount)
            numbers = detect_numbers_in_text(line)
            if numbers and not any(keyword in line.upper() for keyword in ['TOTAL', 'SUBTOTAL', 'TAX']):
                # This might be a line item
                description = line
                for num in numbers:
                    description = description.replace(f"${num:,.2f}", "").replace(f"{num:,.2f}", "")
                description = description.strip()

                if description and len(description) > 2:
                    transactions.append(Transaction(
                        date=transaction_date,
                        description=description[:500],
                        category=None,
                        amount=abs(max(numbers, key=abs)),
                        transaction_type="expense",
                        confidence=0.4,  # Low confidence for OCR
                        source_location="OCR Text",
                        vendor=vendor
                    ))

        # If no line items found but we have a total, create one transaction
        if not transactions and total_amount:
            transactions.append(Transaction(
                date=transaction_date,
                description=vendor or "Receipt",
                category=None,
                amount=abs(total_amount),
                transaction_type="expense",
                confidence=0.5,
                source_location="OCR Text - Total",
                vendor=vendor
            ))

        return transactions

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
            consistency_check="passed" if completeness > 0.2 else "failed",  # Low threshold for OCR
            validation_errors=notes.errors
        )

    def _calculate_initial_confidence(self, transactions: List[Transaction], notes: ExtractionNotes) -> float:
        """Calculate confidence score."""
        if not transactions:
            return 0.0

        # OCR is inherently low confidence
        confidence = 0.4

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
