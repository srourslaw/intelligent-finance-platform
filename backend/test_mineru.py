#!/usr/bin/env python3
"""
Test script for MinerU integration.

Tests:
1. MinerU service initialization
2. PDF extraction from real project file
3. Comparison with pdfplumber extraction
4. Confidence score comparison

Usage:
    python3 test_mineru.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.mineru_service import MinerUService, get_mineru_service
from extraction.extractors.pdf_extractor import PDFExtractor


def test_mineru_service():
    """Test MinerU service initialization."""
    print("=" * 60)
    print("Test 1: MinerU Service Initialization")
    print("=" * 60)

    service = get_mineru_service(enable_ocr=True)

    if service and service.is_available():
        print("✅ MinerU service initialized successfully")
        print(f"   OCR enabled: {service.enable_ocr}")
        return service
    else:
        print("❌ MinerU service not available")
        print("   Make sure magic-pdf is installed: pip install magic-pdf")
        return None


def test_pdf_extraction_mineru(service, pdf_path):
    """Test PDF extraction with MinerU."""
    print("\n" + "=" * 60)
    print("Test 2: PDF Extraction with MinerU")
    print("=" * 60)
    print(f"PDF: {Path(pdf_path).name}")

    try:
        result = service.extract_pdf(str(pdf_path))

        print(f"✅ Extraction successful")
        print(f"   Text length: {len(result.get('text', ''))} characters")
        print(f"   Tables found: {len(result.get('tables', []))}")
        print(f"   Images found: {len(result.get('images', []))}")
        print(f"   Confidence: {result.get('confidence', 0):.2f}")
        print(f"   Structure blocks: {len(result.get('structure', []))}")

        # Show first 500 characters of text
        text = result.get('text', '')
        if text:
            print(f"\n   First 500 chars of text:")
            print(f"   {text[:500]}...")

        return result

    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_pdf_extraction_pdfplumber(pdf_path):
    """Test PDF extraction with pdfplumber (original method)."""
    print("\n" + "=" * 60)
    print("Test 3: PDF Extraction with pdfplumber (Baseline)")
    print("=" * 60)
    print(f"PDF: {Path(pdf_path).name}")

    try:
        extractor = PDFExtractor(use_mineru=False)
        result = extractor.extract(str(pdf_path))

        print(f"✅ Extraction successful")
        print(f"   Transactions extracted: {len(result.extracted_data.transactions)}")
        print(f"   Confidence: {result.metadata.confidence_score:.2f}")
        print(f"   Warnings: {len(result.extraction_notes.warnings)}")
        print(f"   Errors: {len(result.extraction_notes.errors)}")

        # Show transactions
        if result.extracted_data.transactions:
            print(f"\n   Sample transactions:")
            for i, txn in enumerate(result.extracted_data.transactions[:3], 1):
                print(f"   {i}. {txn.description[:60]} - ${txn.amount:.2f}")

        return result

    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_pdf_extraction_mineru_integrated(pdf_path):
    """Test PDF extraction with MinerU through PDFExtractor."""
    print("\n" + "=" * 60)
    print("Test 4: PDF Extraction with MinerU (Integrated)")
    print("=" * 60)
    print(f"PDF: {Path(pdf_path).name}")

    try:
        extractor = PDFExtractor(use_mineru=True)
        result = extractor.extract(str(pdf_path))

        print(f"✅ Extraction successful")
        print(f"   Extractor: {extractor.extractor_name}")
        print(f"   Transactions extracted: {len(result.extracted_data.transactions)}")
        print(f"   Confidence: {result.metadata.confidence_score:.2f}")
        print(f"   Warnings: {len(result.extraction_notes.warnings)}")
        print(f"   Errors: {len(result.extraction_notes.errors)}")

        # Show transactions
        if result.extracted_data.transactions:
            print(f"\n   Sample transactions:")
            for i, txn in enumerate(result.extracted_data.transactions[:3], 1):
                print(f"   {i}. {txn.description[:60]} - ${txn.amount:.2f} (conf: {txn.confidence:.2f})")

        return result

    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all tests."""
    print("\n")
    print("🧪 MinerU Integration Test Suite")
    print("=" * 60)

    # Find a test PDF
    project_data = Path(__file__).parent / "projects" / "project-a-123-sunset-blvd" / "data"

    # Try to find an invoice PDF
    test_pdfs = list(project_data.glob("**/Tax_Invoice_*.pdf"))
    if not test_pdfs:
        test_pdfs = list(project_data.glob("**/*.pdf"))

    if not test_pdfs:
        print("❌ No PDF files found in project data")
        return

    test_pdf = test_pdfs[0]
    print(f"\n📄 Test PDF: {test_pdf.relative_to(project_data.parent)}")
    print(f"   Size: {test_pdf.stat().st_size / 1024:.2f} KB")

    # Test 1: Service initialization
    service = test_mineru_service()

    if service:
        # Test 2: Direct MinerU extraction
        test_pdf_extraction_mineru(service, test_pdf)

    # Test 3: Baseline pdfplumber extraction
    test_pdf_extraction_pdfplumber(test_pdf)

    if service:
        # Test 4: Integrated MinerU extraction
        test_pdf_extraction_mineru_integrated(test_pdf)

    print("\n" + "=" * 60)
    print("✅ Test suite complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
