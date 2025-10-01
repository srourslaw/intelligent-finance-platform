"""
Document viewer service
Converts Excel, PDF, and images to viewable formats
"""
import base64
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
from PyPDF2 import PdfReader


class DocumentViewer:
    """Service for viewing documents in the browser"""

    def __init__(self, project_id: str = "project-a-123-sunset-blvd"):
        self.project_id = project_id
        self.base_dir = Path(__file__).parent.parent.parent / "projects" / project_id / "data"

    def get_file_tree(self, project_id: str = "project-a-123-sunset-blvd") -> List[Dict[str, Any]]:
        """Get file tree structure from dummy_data folders"""
        files = []

        if not self.base_dir.exists():
            return files

        # Walk through all directories
        for root, dirs, filenames in os.walk(self.base_dir):
            for filename in filenames:
                # Skip hidden files and non-relevant files
                if filename.startswith('.') or filename == '.DS_Store':
                    continue

                file_path = Path(root) / filename
                relative_path = file_path.relative_to(self.base_dir)

                # Determine file type
                file_ext = filename.lower().split('.')[-1]
                if file_ext in ['xlsx', 'xls']:
                    file_type = 'excel'
                elif file_ext == 'pdf':
                    file_type = 'pdf'
                elif file_ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                    file_type = 'image'
                else:
                    file_type = 'other'

                # Get file stats
                try:
                    stat = file_path.stat()
                    size = stat.st_size
                    modified = stat.st_mtime
                except:
                    size = 0
                    modified = 0

                files.append({
                    "filename": filename,
                    "path": str(relative_path),
                    "type": file_type,
                    "size": size,
                    "modified": modified,
                    "folder": str(relative_path.parent)
                })

        return files

    def excel_to_json(self, file_path: Path, max_rows: int = 50) -> Dict[str, Any]:
        """Convert Excel file to JSON table data (first N rows of each sheet)"""
        try:
            full_path = self.base_dir / file_path

            if not full_path.exists():
                return {"error": f"File not found: {file_path}"}

            # Read all sheet names
            excel_file = pd.ExcelFile(full_path)
            sheets = {}

            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(full_path, sheet_name=sheet_name, nrows=max_rows)

                    # Convert to JSON-serializable format
                    df = df.fillna("")  # Replace NaN with empty string

                    sheets[sheet_name] = {
                        "columns": df.columns.tolist(),
                        "data": df.values.tolist(),
                        "row_count": len(df),
                        "total_rows": len(pd.read_excel(full_path, sheet_name=sheet_name))
                    }
                except Exception as e:
                    sheets[sheet_name] = {"error": f"Error reading sheet: {str(e)}"}

            return {
                "type": "excel",
                "filename": file_path.name,
                "sheets": sheets,
                "sheet_names": excel_file.sheet_names
            }

        except Exception as e:
            return {"error": f"Error reading Excel file: {str(e)}"}

    def pdf_to_preview(self, file_path: Path) -> Dict[str, Any]:
        """Extract PDF content with formatting"""
        try:
            full_path = self.base_dir / file_path

            if not full_path.exists():
                return {"error": f"File not found: {file_path}"}

            reader = PdfReader(str(full_path))

            pages = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                pages.append({
                    "page_number": i + 1,
                    "text": text
                })

            return {
                "type": "pdf",
                "filename": file_path.name,
                "page_count": len(reader.pages),
                "pages": pages[:10],  # First 10 pages only
                "metadata": {
                    "title": reader.metadata.get("/Title", "") if reader.metadata else "",
                    "author": reader.metadata.get("/Author", "") if reader.metadata else "",
                }
            }

        except Exception as e:
            return {"error": f"Error reading PDF file: {str(e)}"}

    def image_to_base64(self, file_path: Path) -> Dict[str, Any]:
        """Convert image to base64 for display"""
        try:
            full_path = self.base_dir / file_path

            if not full_path.exists():
                return {"error": f"File not found: {file_path}"}

            with open(full_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')

            # Determine MIME type
            ext = file_path.suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/png')

            return {
                "type": "image",
                "filename": file_path.name,
                "data": f"data:{mime_type};base64,{encoded}",
                "mime_type": mime_type
            }

        except Exception as e:
            return {"error": f"Error reading image file: {str(e)}"}

    def get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Get file metadata"""
        try:
            full_path = self.base_dir / file_path

            if not full_path.exists():
                return {"error": f"File not found: {file_path}"}

            stat = full_path.stat()

            return {
                "filename": file_path.name,
                "path": str(file_path),
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": stat.st_mtime,
                "extension": file_path.suffix,
                "exists": True
            }

        except Exception as e:
            return {"error": f"Error getting file metadata: {str(e)}"}

    def preview_file(self, file_path: str, max_rows: int = 50) -> Dict[str, Any]:
        """Preview any file type"""
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext in ['.xlsx', '.xls']:
            return self.excel_to_json(path, max_rows)
        elif ext == '.pdf':
            return self.pdf_to_preview(path)
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
            return self.image_to_base64(path)
        else:
            return {"error": f"Unsupported file type: {ext}"}
