"""
CSV Extractor Module
Extracts financial data from CSV files
"""

import csv
from pathlib import Path
from typing import List, Dict, Any
import codecs


class CSVExtractor:
    """Extract data from CSV files"""

    def __init__(self, file_path: str):
        """
        Initialize CSV extractor

        Args:
            file_path: Path to CSV file
        """
        self.file_path = Path(file_path)

    def extract(self) -> Dict[str, Any]:
        """
        Extract data from CSV file

        Returns:
            Dictionary with extracted data
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'cp1252']

            for encoding in encodings:
                try:
                    return self._extract_with_encoding(encoding)
                except UnicodeDecodeError:
                    continue

            # If all encodings fail, try with errors='ignore'
            return self._extract_with_encoding('utf-8', errors='ignore')

        except Exception as e:
            return {
                'file_path': str(self.file_path),
                'filename': self.file_path.name,
                'error': str(e),
                'data': []
            }

    def _extract_with_encoding(self, encoding: str, errors: str = 'strict') -> Dict[str, Any]:
        """Extract data with specific encoding"""

        with open(self.file_path, 'r', encoding=encoding, errors=errors) as f:
            # Auto-detect delimiter
            sample = f.read(1024)
            f.seek(0)

            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                delimiter = dialect.delimiter
            except:
                delimiter = ','  # Default to comma

            reader = csv.DictReader(f, delimiter=delimiter)

            headers = reader.fieldnames or []
            data_rows = []

            for row_idx, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                # Clean row data
                cleaned_row = {}
                for key, value in row.items():
                    if key and value:
                        cleaned_row[key.strip()] = value.strip()
                    elif key:
                        cleaned_row[key.strip()] = None

                if any(v is not None for v in cleaned_row.values()):
                    cleaned_row['_row_number'] = row_idx
                    data_rows.append(cleaned_row)

            return {
                'file_path': str(self.file_path),
                'filename': self.file_path.name,
                'headers': headers,
                'data': data_rows,
                'row_count': len(data_rows),
                'column_count': len(headers),
                'encoding': encoding,
                'delimiter': delimiter
            }


def main():
    """Test function"""
    # This would test with actual CSV files if they exist
    print("CSV Extractor ready")


if __name__ == "__main__":
    main()
