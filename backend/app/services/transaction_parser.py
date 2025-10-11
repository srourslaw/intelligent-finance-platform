"""
Transaction Parser Service

Converts extracted raw data into normalized data points.
Handles both Excel files and PDF invoices.
"""

import pandas as pd
import re
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import uuid

from app.models.data_points import DataPoint, DataPointType, DataPointStatus

logger = logging.getLogger(__name__)


class TransactionParser:
    """Parse extracted data into normalized data points."""

    def __init__(self, project_id: str):
        self.project_id = project_id

    def parse_extracted_data(
        self,
        extracted_data: Any,
        source_file_id: str
    ) -> List[DataPoint]:
        """
        Parse extracted data based on file type.

        Args:
            extracted_data: ExtractedData model instance
            source_file_id: ID of source file

        Returns:
            List of DataPoint instances
        """
        file_type = extracted_data.file_type.lower()
        file_name = extracted_data.file_name

        logger.info(f"Parsing {file_name} ({file_type})")

        if file_type in ['xlsx', 'xls', 'csv']:
            return self._parse_excel_file(extracted_data, source_file_id)
        elif file_type == 'pdf':
            return self._parse_pdf_file(extracted_data, source_file_id)
        else:
            logger.warning(f"Unsupported file type: {file_type}")
            return []

    def _parse_excel_file(
        self,
        extracted_data: Any,
        source_file_id: str
    ) -> List[DataPoint]:
        """Parse Excel/CSV files into data points."""
        data_points = []
        file_name = extracted_data.file_name.lower()

        # Parse structured_data JSON if available
        if extracted_data.structured_data:
            try:
                structured = json.loads(extracted_data.structured_data)

                # Handle different Excel file types
                if 'budget' in file_name:
                    data_points = self._parse_budget_excel(
                        structured, source_file_id, extracted_data.file_name
                    )
                elif 'payment' in file_name:
                    data_points = self._parse_payments_excel(
                        structured, source_file_id, extracted_data.file_name
                    )
                elif 'subcontractor' in file_name:
                    data_points = self._parse_subcontractors_excel(
                        structured, source_file_id, extracted_data.file_name
                    )
                elif 'invoice' in file_name or 'receipt' in file_name:
                    data_points = self._parse_invoice_excel(
                        structured, source_file_id, extracted_data.file_name
                    )
                else:
                    # Generic Excel parser - try to identify columns
                    data_points = self._parse_generic_excel(
                        structured, source_file_id, extracted_data.file_name
                    )

            except Exception as e:
                logger.error(f"Error parsing Excel {extracted_data.file_name}: {e}", exc_info=True)

        return data_points

    def _parse_budget_excel(
        self,
        structured: Dict,
        source_file_id: str,
        file_name: str
    ) -> List[DataPoint]:
        """Parse Budget.xlsx into budget_item data points."""
        data_points = []

        # Budget.xlsx has: Item Name, Category, Budget Amount, Actual Spent, Variance
        rows = structured.get('rows', [])

        for idx, row in enumerate(rows):
            try:
                # Skip header rows
                if idx == 0 and ('Item' in str(row.get('Item Name', '')) or
                                 'Category' in str(row.get('Category', ''))):
                    continue

                item_name = str(row.get('Item Name', row.get('Item', '')))
                category = str(row.get('Category', ''))
                budget_amount = self._parse_amount(row.get('Budget Amount', row.get('Budget', 0)))
                actual_spent = self._parse_amount(row.get('Actual Spent', row.get('Actual', 0)))

                if not item_name or item_name.strip() == '' or budget_amount == 0:
                    continue

                # Create budget data point
                data_point = DataPoint(
                    id=str(uuid.uuid4()),
                    project_id=self.project_id,
                    source_file_id=source_file_id,
                    source_file_name=file_name,
                    source_file_type='xlsx',
                    source_location=f'Row {idx + 2}',  # Excel rows start at 1, +1 for header
                    data_point_type=DataPointType.BUDGET_ITEM,
                    status=DataPointStatus.EXTRACTED,
                    description=item_name,
                    amount=budget_amount,
                    category=category,
                    extraction_method='pandas',
                    structured_metadata=json.dumps({
                        'actual_spent': actual_spent,
                        'variance': budget_amount - actual_spent
                    })
                )
                data_points.append(data_point)

            except Exception as e:
                logger.warning(f"Error parsing budget row {idx}: {e}")
                continue

        logger.info(f"Parsed {len(data_points)} budget items from {file_name}")
        return data_points

    def _parse_payments_excel(
        self,
        structured: Dict,
        source_file_id: str,
        file_name: str
    ) -> List[DataPoint]:
        """Parse Payments.xlsx into payment data points."""
        data_points = []
        rows = structured.get('rows', [])

        for idx, row in enumerate(rows):
            try:
                if idx == 0:  # Skip header
                    continue

                payment_date = self._parse_date(row.get('Payment Date', row.get('Date', '')))
                vendor = str(row.get('Vendor', row.get('Contractor', '')))
                amount = self._parse_amount(row.get('Amount', row.get('Payment Amount', 0)))
                invoice_num = str(row.get('Invoice Number', row.get('Invoice #', '')))
                description = str(row.get('Description', f'Payment to {vendor}'))

                if not vendor or amount == 0:
                    continue

                data_point = DataPoint(
                    id=str(uuid.uuid4()),
                    project_id=self.project_id,
                    source_file_id=source_file_id,
                    source_file_name=file_name,
                    source_file_type='xlsx',
                    source_location=f'Row {idx + 2}',
                    data_point_type=DataPointType.PAYMENT,
                    status=DataPointStatus.EXTRACTED,
                    transaction_date=payment_date,
                    description=description,
                    amount=amount,
                    vendor=vendor,
                    invoice_number=invoice_num,
                    extraction_method='pandas'
                )
                data_points.append(data_point)

            except Exception as e:
                logger.warning(f"Error parsing payment row {idx}: {e}")
                continue

        logger.info(f"Parsed {len(data_points)} payments from {file_name}")
        return data_points

    def _parse_subcontractors_excel(
        self,
        structured: Dict,
        source_file_id: str,
        file_name: str
    ) -> List[DataPoint]:
        """Parse Subcontractors.xlsx into cost data points."""
        data_points = []
        rows = structured.get('rows', [])

        for idx, row in enumerate(rows):
            try:
                if idx == 0:  # Skip header
                    continue

                contractor_name = str(row.get('Contractor', row.get('Subcontractor', '')))
                trade = str(row.get('Trade', row.get('Specialty', '')))
                contract_amount = self._parse_amount(row.get('Contract Amount', row.get('Amount', 0)))
                paid_to_date = self._parse_amount(row.get('Paid to Date', 0))

                if not contractor_name or contract_amount == 0:
                    continue

                # Create contract data point
                data_point = DataPoint(
                    id=str(uuid.uuid4()),
                    project_id=self.project_id,
                    source_file_id=source_file_id,
                    source_file_name=file_name,
                    source_file_type='xlsx',
                    source_location=f'Row {idx + 2}',
                    data_point_type=DataPointType.CONTRACT,
                    status=DataPointStatus.EXTRACTED,
                    description=f'{trade} - {contractor_name}',
                    amount=contract_amount,
                    vendor=contractor_name,
                    category=trade,
                    extraction_method='pandas',
                    structured_metadata=json.dumps({
                        'paid_to_date': paid_to_date,
                        'remaining': contract_amount - paid_to_date
                    })
                )
                data_points.append(data_point)

            except Exception as e:
                logger.warning(f"Error parsing subcontractor row {idx}: {e}")
                continue

        logger.info(f"Parsed {len(data_points)} subcontractor contracts from {file_name}")
        return data_points

    def _parse_invoice_excel(
        self,
        structured: Dict,
        source_file_id: str,
        file_name: str
    ) -> List[DataPoint]:
        """Parse invoice/receipt Excel files."""
        data_points = []
        rows = structured.get('rows', [])

        for idx, row in enumerate(rows):
            try:
                if idx == 0:  # Skip header
                    continue

                description = str(row.get('Description', row.get('Item', '')))
                amount = self._parse_amount(row.get('Amount', row.get('Total', 0)))
                date = self._parse_date(row.get('Date', row.get('Invoice Date', '')))
                vendor = str(row.get('Vendor', row.get('Supplier', '')))

                if not description or amount == 0:
                    continue

                data_point = DataPoint(
                    id=str(uuid.uuid4()),
                    project_id=self.project_id,
                    source_file_id=source_file_id,
                    source_file_name=file_name,
                    source_file_type='xlsx',
                    source_location=f'Row {idx + 2}',
                    data_point_type=DataPointType.TRANSACTION,
                    status=DataPointStatus.EXTRACTED,
                    transaction_date=date,
                    description=description,
                    amount=amount,
                    vendor=vendor,
                    extraction_method='pandas'
                )
                data_points.append(data_point)

            except Exception as e:
                logger.warning(f"Error parsing invoice row {idx}: {e}")
                continue

        logger.info(f"Parsed {len(data_points)} invoice items from {file_name}")
        return data_points

    def _parse_generic_excel(
        self,
        structured: Dict,
        source_file_id: str,
        file_name: str
    ) -> List[DataPoint]:
        """
        Generic Excel parser - try to identify amount and description columns.
        """
        data_points = []
        rows = structured.get('rows', [])

        if not rows or len(rows) < 2:
            return data_points

        # Try to identify columns
        header = rows[0] if rows else {}
        amount_col = self._find_amount_column(header)
        description_col = self._find_description_column(header)
        date_col = self._find_date_column(header)
        vendor_col = self._find_vendor_column(header)

        logger.info(f"Generic parser columns: amount={amount_col}, desc={description_col}")

        if not amount_col or not description_col:
            logger.warning(f"Could not identify columns in {file_name}")
            return data_points

        for idx, row in enumerate(rows[1:], start=1):
            try:
                amount = self._parse_amount(row.get(amount_col, 0))
                description = str(row.get(description_col, ''))
                date = self._parse_date(row.get(date_col, '')) if date_col else None
                vendor = str(row.get(vendor_col, '')) if vendor_col else ''

                if not description or amount == 0:
                    continue

                data_point = DataPoint(
                    id=str(uuid.uuid4()),
                    project_id=self.project_id,
                    source_file_id=source_file_id,
                    source_file_name=file_name,
                    source_file_type='xlsx',
                    source_location=f'Row {idx + 2}',
                    data_point_type=DataPointType.TRANSACTION,
                    status=DataPointStatus.EXTRACTED,
                    transaction_date=date,
                    description=description,
                    amount=amount,
                    vendor=vendor,
                    extraction_method='pandas'
                )
                data_points.append(data_point)

            except Exception as e:
                logger.warning(f"Error parsing generic row {idx}: {e}")
                continue

        logger.info(f"Parsed {len(data_points)} items from generic Excel {file_name}")
        return data_points

    def _parse_pdf_file(
        self,
        extracted_data: Any,
        source_file_id: str
    ) -> List[DataPoint]:
        """Parse PDF invoices/receipts using MinerU extracted text."""
        data_points = []
        raw_text = extracted_data.raw_text

        if not raw_text:
            return data_points

        try:
            # Extract invoice metadata
            invoice_num = self._extract_invoice_number(raw_text)
            vendor = self._extract_vendor(raw_text)
            date = self._extract_date_from_text(raw_text)

            # Extract line items
            line_items = self._extract_line_items(raw_text)

            # Also try to extract total amount as fallback
            total_amount = self._extract_total_amount(raw_text)

            if line_items:
                # Create data points for each line item
                for idx, item in enumerate(line_items):
                    data_point = DataPoint(
                        id=str(uuid.uuid4()),
                        project_id=self.project_id,
                        source_file_id=source_file_id,
                        source_file_name=extracted_data.file_name,
                        source_file_type='pdf',
                        source_location=f'Line item {idx + 1}',
                        data_point_type=DataPointType.TRANSACTION,
                        status=DataPointStatus.EXTRACTED,
                        transaction_date=date,
                        description=item['description'],
                        amount=item['amount'],
                        vendor=vendor,
                        invoice_number=invoice_num,
                        extraction_method='mineru',
                        raw_text=item.get('raw_line', ''),
                        confidence_score=item.get('confidence', 0.8)
                    )
                    data_points.append(data_point)

            elif total_amount > 0:
                # If we can't extract line items, create single data point for total
                data_point = DataPoint(
                    id=str(uuid.uuid4()),
                    project_id=self.project_id,
                    source_file_id=source_file_id,
                    source_file_name=extracted_data.file_name,
                    source_file_type='pdf',
                    source_location='Total',
                    data_point_type=DataPointType.TRANSACTION,
                    status=DataPointStatus.EXTRACTED,
                    transaction_date=date,
                    description=f'Invoice {invoice_num}' if invoice_num else 'Invoice Total',
                    amount=total_amount,
                    vendor=vendor,
                    invoice_number=invoice_num,
                    extraction_method='mineru',
                    raw_text=raw_text[:500],  # First 500 chars
                    confidence_score=0.7  # Lower confidence for total-only extraction
                )
                data_points.append(data_point)

        except Exception as e:
            logger.error(f"Error parsing PDF {extracted_data.file_name}: {e}", exc_info=True)

        logger.info(f"Parsed {len(data_points)} items from PDF {extracted_data.file_name}")
        return data_points

    # Helper methods for parsing

    def _parse_amount(self, value: Any) -> float:
        """Parse amount from various formats."""
        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Remove currency symbols and commas
            cleaned = re.sub(r'[$,€£¥]', '', value.strip())
            cleaned = cleaned.replace('(', '-').replace(')', '')  # Handle negative numbers
            try:
                return float(cleaned)
            except ValueError:
                return 0.0

        return 0.0

    def _parse_date(self, value: Any) -> Optional[datetime]:
        """Parse date from various formats."""
        if isinstance(value, datetime):
            return value

        if isinstance(value, str) and value.strip():
            # Try common date formats
            formats = [
                '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y',
                '%Y/%m/%d', '%m-%d-%Y', '%d-%m-%Y',
                '%b %d, %Y', '%B %d, %Y'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except ValueError:
                    continue

        return None

    def _find_amount_column(self, header: Dict) -> Optional[str]:
        """Find amount column in Excel header."""
        amount_keywords = ['amount', 'total', 'cost', 'price', 'value', 'sum', 'payment']
        for col, val in header.items():
            if any(kw in str(val).lower() for kw in amount_keywords):
                return col
        return None

    def _find_description_column(self, header: Dict) -> Optional[str]:
        """Find description column in Excel header."""
        desc_keywords = ['description', 'item', 'name', 'details', 'transaction', 'expense']
        for col, val in header.items():
            if any(kw in str(val).lower() for kw in desc_keywords):
                return col
        return None

    def _find_date_column(self, header: Dict) -> Optional[str]:
        """Find date column in Excel header."""
        date_keywords = ['date', 'when', 'time']
        for col, val in header.items():
            if any(kw in str(val).lower() for kw in date_keywords):
                return col
        return None

    def _find_vendor_column(self, header: Dict) -> Optional[str]:
        """Find vendor column in Excel header."""
        vendor_keywords = ['vendor', 'supplier', 'contractor', 'payee', 'company']
        for col, val in header.items():
            if any(kw in str(val).lower() for kw in vendor_keywords):
                return col
        return None

    # PDF parsing helpers

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        """Extract invoice number from PDF text."""
        patterns = [
            r'Invoice\s*#?\s*:?\s*([A-Z0-9-]+)',
            r'Invoice Number\s*:?\s*([A-Z0-9-]+)',
            r'INV\s*#?\s*:?\s*([A-Z0-9-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_vendor(self, text: str) -> str:
        """Extract vendor name from PDF text (heuristic)."""
        # Usually vendor name is in first few lines
        lines = text.split('\n')[:10]
        for line in lines:
            line = line.strip()
            # Skip common invoice keywords
            if line and len(line) > 3 and not any(kw in line.lower() for kw in ['invoice', 'bill', 'receipt', 'page']):
                # Check if it looks like a company name (has uppercase letters)
                if any(c.isupper() for c in line) and len(line) < 100:
                    return line
        return 'Unknown Vendor'

    def _extract_date_from_text(self, text: str) -> Optional[datetime]:
        """Extract date from PDF text."""
        # Look for date patterns
        date_patterns = [
            r'Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Invoice Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self._parse_date(match.group(1))
        return None

    def _extract_total_amount(self, text: str) -> float:
        """Extract total amount from PDF."""
        patterns = [
            r'Total\s*:?\s*\$?\s*([\d,]+\.?\d*)',
            r'Amount Due\s*:?\s*\$?\s*([\d,]+\.?\d*)',
            r'Grand Total\s*:?\s*\$?\s*([\d,]+\.?\d*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self._parse_amount(match.group(1))
        return 0.0

    def _extract_line_items(self, text: str) -> List[Dict[str, Any]]:
        """Extract line items from PDF invoice."""
        line_items = []

        # Look for patterns like: "Description ... $Amount"
        # This is a simplified heuristic - real implementation would be more sophisticated
        lines = text.split('\n')

        for line in lines:
            # Look for lines with amounts
            amount_match = re.search(r'\$?\s*([\d,]+\.?\d{2})', line)
            if amount_match:
                amount = self._parse_amount(amount_match.group(1))
                if amount > 0:
                    # Get description (text before amount)
                    description = line[:amount_match.start()].strip()
                    if description and len(description) > 5:
                        line_items.append({
                            'description': description[:200],  # Limit length
                            'amount': amount,
                            'raw_line': line,
                            'confidence': 0.8
                        })

        return line_items


def create_transaction_parser(project_id: str) -> TransactionParser:
    """Factory function to create transaction parser."""
    return TransactionParser(project_id)
