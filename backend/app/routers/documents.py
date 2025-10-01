"""
Document management and preview endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Dict, Any, List
from app.services.document_viewer import DocumentViewer
from app.routers.auth import get_current_user, User

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize document viewer
doc_viewer = DocumentViewer()


@router.get("/list/{project_id}")
async def list_documents(
    project_id: str,
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    List all documents for a project
    Returns file tree structure
    """
    try:
        files = doc_viewer.get_file_tree(project_id)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@router.get("/preview/{project_id}/{file_path:path}")
async def preview_document(
    project_id: str,
    file_path: str,
    max_rows: int = 50,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Preview a document
    - For Excel: Returns JSON table data (first N rows of each sheet)
    - For PDF: Returns extracted text content
    - For Images: Returns base64 encoded image
    """
    try:
        preview = doc_viewer.preview_file(file_path, max_rows)

        if "error" in preview:
            raise HTTPException(status_code=404, detail=preview["error"])

        return preview

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error previewing document: {str(e)}")


@router.get("/metadata/{project_id}/{file_path:path}")
async def get_document_metadata(
    project_id: str,
    file_path: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get document metadata
    """
    try:
        metadata = doc_viewer.get_file_metadata(Path(file_path))

        if "error" in metadata:
            raise HTTPException(status_code=404, detail=metadata["error"])

        return metadata

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting metadata: {str(e)}")


@router.get("/download/{project_id}/{file_path:path}")
async def download_document(
    project_id: str,
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """
    Download a document file
    """
    try:
        full_path = doc_viewer.base_dir / file_path

        if not full_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

        return FileResponse(
            path=str(full_path),
            filename=full_path.name,
            media_type="application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


@router.get("/excel/{project_id}/{file_path:path}")
async def preview_excel(
    project_id: str,
    file_path: str,
    max_rows: int = 100,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Preview Excel file with more rows
    """
    try:
        preview = doc_viewer.excel_to_json(Path(file_path), max_rows)

        if "error" in preview:
            raise HTTPException(status_code=404, detail=preview["error"])

        return preview

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error previewing Excel: {str(e)}")


@router.get("/pdf/{project_id}/{file_path:path}")
async def preview_pdf(
    project_id: str,
    file_path: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Preview PDF file
    """
    try:
        preview = doc_viewer.pdf_to_preview(Path(file_path))

        if "error" in preview:
            raise HTTPException(status_code=404, detail=preview["error"])

        return preview

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error previewing PDF: {str(e)}")


@router.get("/image/{project_id}/{file_path:path}")
async def preview_image(
    project_id: str,
    file_path: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Preview image file (returns base64)
    """
    try:
        preview = doc_viewer.image_to_base64(Path(file_path))

        if "error" in preview:
            raise HTTPException(status_code=404, detail=preview["error"])

        return preview

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error previewing image: {str(e)}")
