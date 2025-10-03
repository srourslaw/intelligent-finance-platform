"""
File Scanner Module
Discovers and catalogs all financial files in the project directory
"""

import os
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime

from ..config.settings import (
    PROJECT_DATA_DIR,
    SUPPORTED_FILE_TYPES,
    DOCUMENT_TYPE_KEYWORDS
)


class FileScanner:
    """Scan directories for financial files"""

    def __init__(self, base_dir: Path = None):
        """
        Initialize file scanner

        Args:
            base_dir: Base directory to scan (default: PROJECT_DATA_DIR)
        """
        self.base_dir = base_dir or PROJECT_DATA_DIR
        self.files_inventory = []

    def scan(self, recursive: bool = True) -> List[Dict]:
        """
        Scan directory for supported file types

        Args:
            recursive: Whether to scan subdirectories

        Returns:
            List of file metadata dictionaries
        """
        print(f"\n{'='*60}")
        print(f"SCANNING DIRECTORY: {self.base_dir}")
        print(f"{'='*60}\n")

        if not self.base_dir.exists():
            print(f"❌ Directory does not exist: {self.base_dir}")
            return []

        self.files_inventory = []

        if recursive:
            # Recursively scan all subdirectories
            for root, dirs, files in os.walk(self.base_dir):
                for file in files:
                    file_path = Path(root) / file
                    self._add_file_if_supported(file_path)
        else:
            # Scan only base directory
            for file_path in self.base_dir.iterdir():
                if file_path.is_file():
                    self._add_file_if_supported(file_path)

        self._print_summary()
        return self.files_inventory

    def _add_file_if_supported(self, file_path: Path):
        """Add file to inventory if it's a supported type"""
        if file_path.suffix.lower() in SUPPORTED_FILE_TYPES:
            # Skip temporary/system files
            if file_path.name.startswith('~$') or file_path.name.startswith('.'):
                return

            metadata = self._extract_metadata(file_path)
            self.files_inventory.append(metadata)

    def _extract_metadata(self, file_path: Path) -> Dict:
        """
        Extract metadata from file

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file metadata
        """
        stat = file_path.stat()

        # Determine folder category
        folder_category = self._determine_folder_category(file_path)

        # Guess document type from filename and folder
        document_type = self._guess_document_type(file_path, folder_category)

        return {
            'file_path': str(file_path),
            'filename': file_path.name,
            'file_type': file_path.suffix.lower(),
            'folder': file_path.parent.name,
            'folder_category': folder_category,
            'document_type': document_type,
            'size_bytes': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 2),
            'modified_date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'relative_path': str(file_path.relative_to(self.base_dir))
        }

    def _determine_folder_category(self, file_path: Path) -> str:
        """Determine financial category from folder structure"""
        parts = file_path.parts

        # Look for numbered folders (e.g., 01_LAND_PURCHASE)
        for part in reversed(parts):
            if part.startswith(('01_', '02_', '03_', '04_', '05_', '06_', '07_', '08_',
                              '09_', '10_', '11_', '12_', '13_', '14_', '15_', '16_',
                              '17_', '18_', '19_', '20_', '21_', '22_')):
                return part

        return file_path.parent.name

    def _guess_document_type(self, file_path: Path, folder_category: str) -> str:
        """
        Guess document type from filename and folder

        Args:
            file_path: Path to file
            folder_category: Folder category

        Returns:
            Guessed document type
        """
        filename_lower = file_path.name.lower()
        folder_lower = folder_category.lower()

        # Check for specific document types
        if any(kw in filename_lower for kw in ['balance_sheet', 'balance sheet']):
            return 'balance_sheet'
        elif any(kw in filename_lower for kw in ['income_statement', 'income statement', 'p&l', 'profit and loss']):
            return 'income_statement'
        elif any(kw in filename_lower for kw in ['cash_flow', 'cash flow', 'cashflow']):
            return 'cash_flow'
        elif any(kw in filename_lower for kw in ['invoice', 'tax_invoice']):
            return 'invoice'
        elif any(kw in filename_lower for kw in ['register', 'tracker', 'log']):
            return 'register'
        elif any(kw in filename_lower for kw in ['budget', 'forecast']):
            return 'budget'
        elif any(kw in filename_lower for kw in ['schedule', 'aging']):
            return 'schedule'
        elif any(kw in filename_lower for kw in ['statement', 'bank_statement']):
            return 'statement'
        elif any(kw in filename_lower for kw in ['chart_of_accounts', 'chart of accounts', 'coa']):
            return 'chart_of_accounts'
        elif any(kw in filename_lower for kw in ['trial_balance', 'trial balance']):
            return 'trial_balance'
        elif any(kw in filename_lower for kw in ['general_ledger', 'general ledger', 'gl']):
            return 'general_ledger'

        # Check folder for hints
        if 'invoice' in folder_lower:
            return 'invoice'
        elif 'billing' in folder_lower:
            return 'billing'
        elif 'budget' in folder_lower:
            return 'budget'
        elif 'monthly_close' in folder_lower or 'close' in folder_lower:
            return 'financial_statement'
        elif 'general_ledger' in folder_lower or 'gl' in folder_lower:
            return 'general_ledger'

        return 'unknown'

    def _print_summary(self):
        """Print summary statistics"""
        print(f"\n{'='*60}")
        print(f"FILE DISCOVERY SUMMARY")
        print(f"{'='*60}\n")

        total_files = len(self.files_inventory)
        print(f"Total files found: {total_files}")

        # Group by file type
        file_types = {}
        for file in self.files_inventory:
            ft = file['file_type']
            file_types[ft] = file_types.get(ft, 0) + 1

        print(f"\nBy file type:")
        for ft, count in sorted(file_types.items()):
            print(f"  {ft}: {count}")

        # Group by document type
        doc_types = {}
        for file in self.files_inventory:
            dt = file['document_type']
            doc_types[dt] = doc_types.get(dt, 0) + 1

        print(f"\nBy document type:")
        for dt, count in sorted(doc_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {dt}: {count}")

        # Group by folder category
        folders = {}
        for file in self.files_inventory:
            folder = file['folder_category']
            folders[folder] = folders.get(folder, 0) + 1

        print(f"\nBy folder category (top 10):")
        for folder, count in sorted(folders.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {folder}: {count}")

        # Total size
        total_size_kb = sum(file['size_kb'] for file in self.files_inventory)
        print(f"\nTotal size: {total_size_kb:.2f} KB ({total_size_kb/1024:.2f} MB)")

        print(f"\n{'='*60}\n")

    def save_inventory(self, output_path: Path = None):
        """
        Save file inventory to JSON

        Args:
            output_path: Path to save JSON file
        """
        if output_path is None:
            output_path = Path(__file__).parent.parent / 'output' / 'file_inventory.json'

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump({
                'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'base_directory': str(self.base_dir),
                'total_files': len(self.files_inventory),
                'files': self.files_inventory
            }, f, indent=2)

        print(f"✅ File inventory saved to: {output_path}")

    def filter_by_type(self, file_type: str) -> List[Dict]:
        """Filter inventory by file type"""
        return [f for f in self.files_inventory if f['file_type'] == file_type]

    def filter_by_document_type(self, document_type: str) -> List[Dict]:
        """Filter inventory by document type"""
        return [f for f in self.files_inventory if f['document_type'] == document_type]

    def filter_by_folder(self, folder_category: str) -> List[Dict]:
        """Filter inventory by folder category"""
        return [f for f in self.files_inventory if f['folder_category'] == folder_category]


def main():
    """Main function for testing"""
    scanner = FileScanner()
    files = scanner.scan(recursive=True)
    scanner.save_inventory()

    print(f"\nExample files found:")
    for file in files[:5]:
        print(f"  - {file['filename']} ({file['document_type']}) in {file['folder_category']}")


if __name__ == "__main__":
    main()
