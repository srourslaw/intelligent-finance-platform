"""
Unified Data Extractor
Orchestrates extraction from all file types
"""

from pathlib import Path
from typing import Dict, Any, List
import json

from .excel_extractor import ExcelExtractor
from .csv_extractor import CSVExtractor
from .pdf_extractor import PDFExtractor
from ..config.settings import OUTPUT_DIR


class DataExtractor:
    """Unified interface for extracting data from all file types"""

    def __init__(self):
        """Initialize data extractor"""
        self.extracted_data = []

    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from a single file

        Args:
            file_path: Path to file

        Returns:
            Extracted data dictionary
        """
        path = Path(file_path)
        file_type = path.suffix.lower()

        if file_type in ['.xlsx', '.xls']:
            extractor = ExcelExtractor(file_path)
            return extractor.extract()
        elif file_type == '.csv':
            extractor = CSVExtractor(file_path)
            return extractor.extract()
        elif file_type == '.pdf':
            extractor = PDFExtractor(file_path)
            return extractor.extract()
        else:
            return {
                'file_path': str(file_path),
                'error': f'Unsupported file type: {file_type}'
            }

    def extract_from_files(self, file_list: List[Dict]) -> List[Dict]:
        """
        Extract data from multiple files

        Args:
            file_list: List of file dictionaries from file scanner

        Returns:
            List of extracted data dictionaries
        """
        self.extracted_data = []

        print(f"\n{'='*60}")
        print(f"EXTRACTING DATA FROM {len(file_list)} FILES")
        print(f"{'='*60}\n")

        for idx, file_info in enumerate(file_list, 1):
            file_path = file_info['file_path']
            print(f"[{idx}/{len(file_list)}] Extracting: {file_info['filename']}...")

            try:
                data = self.extract_from_file(file_path)
                data['file_metadata'] = file_info
                self.extracted_data.append(data)

            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.extracted_data.append({
                    'file_path': file_path,
                    'error': str(e),
                    'file_metadata': file_info
                })

        self._print_summary()
        return self.extracted_data

    def extract_excel_files_only(self, file_list: List[Dict]) -> List[Dict]:
        """Extract only Excel files (faster for initial testing)"""
        excel_files = [f for f in file_list if f['file_type'] in ['.xlsx', '.xls']]
        return self.extract_from_files(excel_files)

    def _print_summary(self):
        """Print extraction summary"""
        print(f"\n{'='*60}")
        print(f"EXTRACTION SUMMARY")
        print(f"{'='*60}\n")

        total_files = len(self.extracted_data)
        successful = sum(1 for d in self.extracted_data if not d.get('error'))
        failed = total_files - successful

        print(f"Total files processed: {total_files}")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")

        # Count sheets and rows extracted
        total_sheets = 0
        total_rows = 0

        for data in self.extracted_data:
            if not data.get('error'):
                sheets = data.get('sheets', [])
                total_sheets += len(sheets)
                for sheet in sheets:
                    total_rows += sheet.get('row_count', 0)

        print(f"\nData extracted:")
        print(f"  Total sheets: {total_sheets}")
        print(f"  Total rows: {total_rows}")

        print(f"\n{'='*60}\n")

    def save_extracted_data(self, output_filename: str = 'extracted_data.json'):
        """Save extracted data to JSON file"""
        output_path = OUTPUT_DIR / output_filename

        with open(output_path, 'w') as f:
            json.dump({
                'total_files': len(self.extracted_data),
                'extracted_data': self.extracted_data
            }, f, indent=2, default=str)

        print(f"✅ Extracted data saved to: {output_path}")


def main():
    """Test function"""
    from ..extractors.file_scanner import FileScanner

    # Scan files
    scanner = FileScanner()
    files = scanner.scan()

    # Extract only Excel files for testing
    excel_files = [f for f in files if f['file_type'] in ['.xlsx', '.xls']][:5]

    # Extract data
    extractor = DataExtractor()
    extractor.extract_from_files(excel_files)
    extractor.save_extracted_data()


if __name__ == "__main__":
    main()
