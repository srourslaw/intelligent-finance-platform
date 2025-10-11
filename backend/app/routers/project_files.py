"""
API endpoint to get project file structure for the AI animation
"""
import os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/projects", tags=["project-files"])

PROJECTS_BASE_DIR = Path(__file__).parent.parent.parent / "projects"


def build_file_tree(directory: Path, relative_to: Path = None) -> Dict[str, Any]:
    """
    Build a nested file tree structure from a directory.

    Returns FileNode structure compatible with AIDataMappingAnimation component.
    """
    if relative_to is None:
        relative_to = directory

    # Get relative path for display
    rel_path = str(directory.relative_to(relative_to)) if directory != relative_to else "/"

    result = {
        "name": directory.name if directory != relative_to else "Project Files",
        "type": "folder",
        "path": rel_path,
        "isExpanded": True,
        "children": []
    }

    try:
        # Get all items in directory
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

        for item in items:
            # Skip hidden files and __pycache__
            if item.name.startswith('.') or item.name == '__pycache__':
                continue

            if item.is_dir():
                # Recursively build tree for subdirectories
                child_tree = build_file_tree(item, relative_to)
                result["children"].append(child_tree)
            else:
                # Add file
                file_type = get_file_type(item.suffix)
                result["children"].append({
                    "name": item.name,
                    "type": file_type,
                    "path": str(item.relative_to(relative_to))
                })

    except PermissionError:
        pass  # Skip directories we can't read

    return result


def get_file_type(extension: str) -> str:
    """Map file extension to type for the animation."""
    ext = extension.lower()

    if ext in ['.xlsx', '.xls', '.xlsm']:
        return 'excel'
    elif ext in ['.pdf']:
        return 'pdf'
    elif ext in ['.json']:
        return 'json'
    elif ext in ['.md', '.txt']:
        return 'md'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
        return 'image'
    elif ext in ['.csv']:
        return 'csv'
    elif ext in ['.py', '.js', '.ts', '.tsx']:
        return 'file'
    else:
        return 'file'


@router.get("/{project_id}/file-structure")
async def get_project_file_structure(project_id: str):
    """
    Get the file structure for a project's data directory.

    Returns a nested FileNode structure for the AI animation.
    """
    # Convert project_id to directory name (e.g., "proj_123" -> "project-123")
    project_dir_name = project_id.replace('_', '-').lower()
    project_path = PROJECTS_BASE_DIR / project_dir_name / "data"

    if not project_path.exists():
        # Try alternate format
        project_path = PROJECTS_BASE_DIR / project_id / "data"

    if not project_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Project directory not found: {project_id}"
        )

    if not project_path.is_dir():
        raise HTTPException(
            status_code=400,
            detail=f"Path is not a directory: {project_id}"
        )

    # Build the file tree
    file_tree = build_file_tree(project_path)

    return {
        "project_id": project_id,
        "file_structure": file_tree
    }


@router.get("/list")
async def list_available_projects():
    """List all available project directories."""
    if not PROJECTS_BASE_DIR.exists():
        return {"projects": []}

    projects = []
    for item in PROJECTS_BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            data_dir = item / "data"
            projects.append({
                "id": item.name,
                "name": item.name.replace('-', ' ').title(),
                "has_data": data_dir.exists()
            })

    return {"projects": projects}
