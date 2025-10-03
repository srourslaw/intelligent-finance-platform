"""
PDF Extractor Module
Extracts text and tables from PDF files
"""

from pathlib import Path
from typing import List, Dict, Any
import re


class PDFExtractor:
    """Extract data from PDF files"""

    def __init__(self, file_path: str):
        """
        Initialize PDF extractor

        Args:
            file_path: Path to PDF file
        """
        self.file_path = Path(file_path)

    def extract(self) -> Dict[str, Any]:
        """
        Extract text and data from PDF

        Returns:
            Dictionary with extracted data
        """
        try:
            # Try to import pdfplumber
            try:
                import pdfplumber
            except ImportError:
                return {
                    'file_path': str(self.file_path),
                    'filename': self.file_path.name,
                    'error': 'pdfplumber not installed',
                    'text': '',
                    'tables': [],
                    'note': 'Install with: pip install pdfplumber'
                }

            with pdfplumber.open(self.file_path) as pdf:
                text_content = []
                tables = []

                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append({
                            'page': page_num,
                            'text': page_text
                        })

                    # Extract tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table_idx, table in enumerate(page_tables):
                            if table:
                                tables.append({
                                    'page': page_num,
                                    'table_index': table_idx,
                                    'data': table
                                })

                # Extract financial data from text
                financial_data = self._extract_financial_data(text_content, tables)

                return {
                    'file_path': str(self.file_path),
                    'filename': self.file_path.name,
                    'num_pages': len(pdf.pages),
                    'text_content': text_content,
                    'tables': tables,
                    'financial_data': financial_data
                }

        except Exception as e:
            return {
                'file_path': str(self.file_path),
                'filename': self.file_path.name,
                'error': str(e),
                'text': '',
                'tables': []
            }

    def _extract_financial_data(self, text_content: List[Dict], tables: List[Dict]) -> Dict:
        """Extract financial information from text and tables"""
        financial_data = {
            'amounts': [],
            'dates': [],
            'invoice_numbers': [],
            'vendors': []
        }

        # Combine all text
        all_text = ' '.join([page['text'] for page in text_content if page.get('text')])

        # Extract currency amounts (e.g., $1,234.56 or 1234.56)
        amount_pattern = r'\$?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
        amounts = re.findall(amount_pattern, all_text)
        financial_data['amounts'] = [amt.replace('$', '').replace(',', '').strip() for amt in amounts]

        # Extract dates (various formats)
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # DD/MM/YYYY or MM/DD/YYYY
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # DD-MM-YYYY
            r'\d{4}-\d{1,2}-\d{1,2}'     # YYYY-MM-DD
        ]
        for pattern in date_patterns:
            dates = re.findall(pattern, all_text)
            financial_data['dates'].extend(dates)

        # Extract invoice numbers (common patterns)
        invoice_patterns = [
            r'INV[- ]?\d+',
            r'Invoice[: #]*\s*\d+',
            r'[A-Z]{2,4}-\d{3,6}'
        ]
        for pattern in invoice_patterns:
            invoice_nums = re.findall(pattern, all_text, re.IGNORECASE)
            financial_data['invoice_numbers'].extend(invoice_nums)

        return financial_data

    def extract_simple_text(self) -> str:
        """Extract all text as a single string"""
        data = self.extract()
        if data.get('error'):
            return f"Error: {data['error']}"

        text_parts = [page['text'] for page in data.get('text_content', [])]
        return '\n\n'.join(text_parts)


def main():
    """Test function"""
    print("PDF Extractor ready (requires pdfplumber)")
    print("Install with: pip install pdfplumber")


if __name__ == "__main__":
    main()
