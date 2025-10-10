"""
PDF Extraction Comparison & Testing Endpoint

This endpoint allows testing MinerU vs pdfplumber extraction side-by-side
and saves the results to organized JSON files for building financial statements.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from extraction.extractors.pdf_extractor import PDFExtractor
from app.services.mineru_service import get_mineru_service

router = APIRouter(prefix="/api/extraction", tags=["extraction-test"])

# Output directory for saved extractions
EXTRACTION_OUTPUT_DIR = Path("extracted_data")
EXTRACTION_OUTPUT_DIR.mkdir(exist_ok=True)


class Transaction(BaseModel):
    description: str
    amount: float
    date: str | None = None
    category: str | None = None
    confidence: float


class ExtractionMethodResult(BaseModel):
    method: str
    confidence: float
    text_length: int
    transactions_found: int
    processing_time: float
    text_preview: str
    transactions: List[Transaction]
    saved_to: str | None = None


class ComparisonResponse(BaseModel):
    file_name: str
    mineru: ExtractionMethodResult | None
    pdfplumber: ExtractionMethodResult | None


def save_extraction_to_json(
    file_name: str,
    method: str,
    extraction_data: Dict[str, Any],
    transactions: List[Dict[str, Any]]
) -> str:
    """
    Save extraction results to organized JSON structure.

    File structure:
    extracted_data/
        {filename}/
            mineru_extraction.json
            pdfplumber_extraction.json
            financial_summary.json  (aggregated for statements)
    """
    # Create directory for this file
    file_base = Path(file_name).stem
    output_dir = EXTRACTION_OUTPUT_DIR / file_base
    output_dir.mkdir(exist_ok=True, parents=True)

    # Prepare structured data for financial statements
    structured_data = {
        "metadata": {
            "file_name": file_name,
            "extraction_method": method,
            "extraction_date": datetime.utcnow().isoformat(),
            "confidence_score": extraction_data.get("confidence", 0.0),
        },
        "text_content": {
            "full_text": extraction_data.get("text", ""),
            "text_length": extraction_data.get("text_length", 0),
        },
        "transactions": transactions,
        "financial_summary": {
            "total_transactions": len(transactions),
            "total_amount": sum(t.get("amount", 0) for t in transactions),
            "expense_count": sum(1 for t in transactions if t.get("transaction_type") == "expense"),
            "income_count": sum(1 for t in transactions if t.get("transaction_type") == "income"),
        },
        "quality_metrics": {
            "confidence_score": extraction_data.get("confidence", 0.0),
            "completeness": len([t for t in transactions if t.get("date") and t.get("description") and t.get("amount")]) / max(len(transactions), 1),
        }
    }

    # Save method-specific file
    output_file = output_dir / f"{method}_extraction.json"
    with output_file.open("w") as f:
        json.dump(structured_data, f, indent=2, default=str)

    # Also save/update financial summary (aggregated from all methods)
    summary_file = output_dir / "financial_summary.json"
    if summary_file.exists():
        with summary_file.open("r") as f:
            summary = json.load(f)
    else:
        summary = {
            "file_name": file_name,
            "extraction_methods": {}
        }

    summary["extraction_methods"][method] = {
        "confidence": extraction_data.get("confidence", 0.0),
        "transactions_found": len(transactions),
        "total_amount": sum(t.get("amount", 0) for t in transactions),
        "extraction_date": datetime.utcnow().isoformat(),
    }

    # Choose best method for financial statements
    best_method = max(
        summary["extraction_methods"].items(),
        key=lambda x: (x[1]["confidence"], x[1]["transactions_found"])
    )[0]

    summary["recommended_for_statements"] = best_method
    summary["best_transactions"] = transactions if method == best_method else summary.get("best_transactions", [])

    with summary_file.open("w") as f:
        json.dump(summary, f, indent=2, default=str)

    return str(output_file.relative_to(Path.cwd()))


@router.post("/test-comparison", response_model=ComparisonResponse)
async def test_extraction_comparison(file: UploadFile = File(...)):
    """
    Test PDF extraction with both MinerU and pdfplumber, then save results.

    Returns comparison of both methods and saves structured JSON for financial statements.
    """

    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    # Save uploaded file temporarily
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / file.filename

    try:
        # Save uploaded file
        content = await file.read()
        with temp_file.open("wb") as f:
            f.write(content)

        # Extract with MinerU
        mineru_result = None
        try:
            start_time = time.time()
            extractor_mineru = PDFExtractor(use_mineru=True)
            extraction_mineru = extractor_mineru.extract(str(temp_file))
            processing_time_mineru = time.time() - start_time

            # Convert transactions to dict
            transactions_mineru = [
                {
                    "description": t.description,
                    "amount": t.amount,
                    "date": t.date.isoformat() if t.date else None,
                    "category": t.category,
                    "confidence": t.confidence,
                    "transaction_type": t.transaction_type,
                }
                for t in extraction_mineru.extracted_data.transactions
            ]

            # Save to JSON
            saved_path_mineru = save_extraction_to_json(
                file.filename,
                "mineru",
                {
                    "confidence": extraction_mineru.metadata.confidence_score,
                    "text": str(extraction_mineru.extracted_data)[:1000],  # Preview
                    "text_length": len(str(extraction_mineru.extracted_data)),
                },
                transactions_mineru
            )

            mineru_result = ExtractionMethodResult(
                method="mineru",
                confidence=extraction_mineru.metadata.confidence_score,
                text_length=len(str(extraction_mineru.extracted_data)),
                transactions_found=len(transactions_mineru),
                processing_time=processing_time_mineru,
                text_preview=str(extraction_mineru.extracted_data)[:500],
                transactions=[
                    Transaction(
                        description=t["description"],
                        amount=t["amount"],
                        date=t.get("date"),
                        category=t.get("category"),
                        confidence=t["confidence"]
                    )
                    for t in transactions_mineru[:10]  # Limit to first 10 for preview
                ],
                saved_to=saved_path_mineru
            )
        except Exception as e:
            print(f"MinerU extraction failed: {e}")

        # Extract with pdfplumber
        pdfplumber_result = None
        try:
            start_time = time.time()
            extractor_pdf = PDFExtractor(use_mineru=False)
            extraction_pdf = extractor_pdf.extract(str(temp_file))
            processing_time_pdf = time.time() - start_time

            # Convert transactions to dict
            transactions_pdf = [
                {
                    "description": t.description,
                    "amount": t.amount,
                    "date": t.date.isoformat() if t.date else None,
                    "category": t.category,
                    "confidence": t.confidence,
                    "transaction_type": t.transaction_type,
                }
                for t in extraction_pdf.extracted_data.transactions
            ]

            # Save to JSON
            saved_path_pdf = save_extraction_to_json(
                file.filename,
                "pdfplumber",
                {
                    "confidence": extraction_pdf.metadata.confidence_score,
                    "text": str(extraction_pdf.extracted_data)[:1000],
                    "text_length": len(str(extraction_pdf.extracted_data)),
                },
                transactions_pdf
            )

            pdfplumber_result = ExtractionMethodResult(
                method="pdfplumber",
                confidence=extraction_pdf.metadata.confidence_score,
                text_length=len(str(extraction_pdf.extracted_data)),
                transactions_found=len(transactions_pdf),
                processing_time=processing_time_pdf,
                text_preview=str(extraction_pdf.extracted_data)[:500],
                transactions=[
                    Transaction(
                        description=t["description"],
                        amount=t["amount"],
                        date=t.get("date"),
                        category=t.get("category"),
                        confidence=t["confidence"]
                    )
                    for t in transactions_pdf[:10]
                ],
                saved_to=saved_path_pdf
            )
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")

        return ComparisonResponse(
            file_name=file.filename,
            mineru=mineru_result,
            pdfplumber=pdfplumber_result
        )

    finally:
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()


@router.get("/extracted-data/{filename}")
async def get_extracted_data(filename: str):
    """
    Retrieve saved extraction data for a file.

    Returns the financial summary JSON that can be used for building statements.
    """
    file_base = Path(filename).stem
    summary_file = EXTRACTION_OUTPUT_DIR / file_base / "financial_summary.json"

    if not summary_file.exists():
        raise HTTPException(status_code=404, detail="No extraction data found for this file")

    with summary_file.open("r") as f:
        return json.load(f)
