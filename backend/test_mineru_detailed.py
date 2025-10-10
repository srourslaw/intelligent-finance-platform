#!/usr/bin/env python3
"""
Detailed MinerU test to see exactly what's being extracted.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.mineru_service import get_mineru_service
from extraction.base_extractor import detect_numbers_in_text

def main():
    print("=" * 80)
    print("Detailed MinerU Extraction Test")
    print("=" * 80)

    # Get service
    service = get_mineru_service()
    if not service:
        print("❌ MinerU not available")
        return

    # Test PDF
    pdf_path = Path("projects/project-a-123-sunset-blvd/data/06_PURCHASE_ORDERS_INVOICES/Invoices_Paid/Tax_Invoice_PP-9012.pdf")

    print(f"\n📄 PDF: {pdf_path.name}\n")

    # Extract
    result = service.extract_pdf(str(pdf_path))

    text = result.get('text', '')

    print("=" * 80)
    print("FULL EXTRACTED TEXT:")
    print("=" * 80)
    print(text)
    print("=" * 80)

    # Analyze each line
    print("\n" + "=" * 80)
    print("LINE-BY-LINE ANALYSIS:")
    print("=" * 80)

    lines = text.split('\n')
    transaction_count = 0

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        # Check for numbers
        numbers = detect_numbers_in_text(line)

        if numbers:
            transaction_count += 1
            print(f"\nLine {i}: ✅ HAS NUMBERS")
            print(f"   Text: {line[:80]}")
            print(f"   Numbers found: {numbers}")
        else:
            print(f"Line {i}: {line[:80]}")

    print("\n" + "=" * 80)
    print(f"Summary: Found {transaction_count} lines with dollar amounts")
    print("=" * 80)

if __name__ == "__main__":
    main()
