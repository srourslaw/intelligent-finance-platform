"""
File upload endpoints for Excel files
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import shutil
from typing import Dict, Any
from app.routers.auth import get_current_user, User

router = APIRouter(prefix="/api/uploads", tags=["uploads"])

# Base directory for uploaded files
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "dummy_data"


@router.post("/budget")
async def upload_budget_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Upload MASTER_PROJECT_BUDGET.xlsx file"""
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

        # Create directory if it doesn't exist
        target_dir = UPLOAD_DIR / "12_BUDGET_TRACKING"
        target_dir.mkdir(parents=True, exist_ok=True)

        # Save the file
        file_path = target_dir / "MASTER_PROJECT_BUDGET.xlsx"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": "Budget file uploaded successfully",
            "filename": file.filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/subcontractors")
async def upload_subcontractor_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Upload Subcontractor_Register.xlsx file"""
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

        target_dir = UPLOAD_DIR / "07_SUBCONTRACTORS"
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / "Subcontractor_Register.xlsx"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": "Subcontractor file uploaded successfully",
            "filename": file.filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/client-payments")
async def upload_client_payments_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Upload Client_Payment_Tracker.xlsx file"""
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

        target_dir = UPLOAD_DIR / "11_CLIENT_BILLING"
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / "Client_Payment_Tracker.xlsx"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": "Client payments file uploaded successfully",
            "filename": file.filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/defects")
async def upload_defects_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Upload Defects_And_Snagging.xlsx file"""
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

        target_dir = UPLOAD_DIR / "15_DEFECTS_SNAGGING"
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / "Defects_And_Snagging.xlsx"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": "Defects file uploaded successfully",
            "filename": file.filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/timesheets")
async def upload_timesheets_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Upload Timesheets_September_2024.xlsx file"""
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

        target_dir = UPLOAD_DIR / "09_TIMESHEETS"
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / "Timesheets_September_2024.xlsx"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": "Timesheets file uploaded successfully",
            "filename": file.filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/purchase-orders")
async def upload_purchase_orders_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Upload Purchase_Orders_Master.xlsx file"""
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

        target_dir = UPLOAD_DIR / "10_PURCHASE_ORDERS"
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / "Purchase_Orders_Master.xlsx"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "message": "Purchase orders file uploaded successfully",
            "filename": file.filename,
            "path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
