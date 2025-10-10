"""
AI-Powered Financial Document Extraction Service

Uses Anthropic Claude API to intelligently parse financial documents
(invoices, receipts, purchase orders) into structured transaction data.

Inspired by: https://github.com/Ramandsingh/nextjs_documents2
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from anthropic import Anthropic
from app.config import get_config

config = get_config()


class AIExtractionService:
    """
    Service for extracting structured financial data from raw text using AI.
    """

    def __init__(self):
        """Initialize the Anthropic client."""
        self.client = None
        if config.anthropic_api_key:
            try:
                self.client = Anthropic(api_key=config.anthropic_api_key)
            except Exception as e:
                print(f"Failed to initialize Anthropic client: {e}")

    def extract_transactions(self, raw_text: str, document_type: str = "invoice") -> Dict[str, Any]:
        """
        Extract structured transaction data from raw document text.

        Args:
            raw_text: The raw extracted text from the PDF
            document_type: Type of document (invoice, receipt, purchase_order, bank_statement)

        Returns:
            Structured dictionary with extracted financial data
        """
        if not self.client:
            return self._fallback_extraction(raw_text)

        try:
            prompt = self._build_extraction_prompt(raw_text, document_type)

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                temperature=0,  # Deterministic for consistent extraction
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse the JSON response
            extracted_data = json.loads(response.content[0].text)

            # Add metadata
            extracted_data["extraction_metadata"] = {
                "extracted_at": datetime.utcnow().isoformat(),
                "model": "claude-3-5-sonnet-20241022",
                "document_type": document_type,
                "confidence": self._calculate_confidence(extracted_data)
            }

            return extracted_data

        except Exception as e:
            print(f"AI extraction failed: {e}")
            return self._fallback_extraction(raw_text)

    def _build_extraction_prompt(self, raw_text: str, document_type: str) -> str:
        """
        Build a structured prompt for extracting financial data.

        Inspired by the nextjs_documents2 approach with detailed parsing rules.
        """
        return f"""You are a financial document parser. Extract structured data from the following {document_type}.

DOCUMENT TEXT:
{raw_text}

EXTRACTION RULES:
1. Extract ALL line items as separate transactions
2. Parse amounts as numbers (remove currency symbols, commas)
3. Handle negative amounts for credits/refunds
4. Extract dates in ISO format (YYYY-MM-DD)
5. Identify vendor/supplier information
6. Calculate totals, subtotals, tax amounts
7. Categorize transactions (materials, labor, services, etc.)
8. Handle multi-line descriptions by combining them

OUTPUT FORMAT (return ONLY valid JSON):
{{
  "document_info": {{
    "document_number": "string or null",
    "document_date": "YYYY-MM-DD or null",
    "vendor_name": "string or null",
    "vendor_abn": "string or null",
    "vendor_address": "string or null"
  }},
  "financial_summary": {{
    "subtotal": number,
    "tax_amount": number,
    "total_amount": number,
    "currency": "AUD"
  }},
  "transactions": [
    {{
      "description": "string",
      "quantity": number or null,
      "unit_price": number or null,
      "amount": number,
      "category": "materials|labor|services|equipment|other",
      "date": "YYYY-MM-DD or null",
      "confidence": 0.0-1.0
    }}
  ],
  "payment_terms": {{
    "payment_method": "string or null",
    "due_date": "YYYY-MM-DD or null",
    "account_details": "string or null"
  }}
}}

IMPORTANT:
- Return ONLY the JSON object, no markdown or explanations
- If a field cannot be determined, use null
- Confidence should reflect how certain you are about the extraction (0.0 = uncertain, 1.0 = certain)
- For amounts, use positive numbers for charges/expenses, negative for credits/refunds
"""

    def _calculate_confidence(self, extracted_data: Dict[str, Any]) -> float:
        """
        Calculate overall confidence score based on extracted data quality.
        """
        scores = []

        # Check if we have basic document info
        doc_info = extracted_data.get("document_info", {})
        if doc_info.get("document_number"):
            scores.append(0.2)
        if doc_info.get("vendor_name"):
            scores.append(0.2)

        # Check if we have financial data
        financial = extracted_data.get("financial_summary", {})
        if financial.get("total_amount"):
            scores.append(0.2)

        # Check if we have transactions
        transactions = extracted_data.get("transactions", [])
        if transactions:
            scores.append(0.2)
            # Average confidence of all transactions
            txn_confidences = [t.get("confidence", 0.5) for t in transactions]
            scores.append(sum(txn_confidences) / len(txn_confidences) * 0.2)

        return sum(scores) if scores else 0.0

    def _fallback_extraction(self, raw_text: str) -> Dict[str, Any]:
        """
        Fallback extraction when AI is not available.
        Returns basic structure with minimal data.
        """
        return {
            "document_info": {
                "document_number": None,
                "document_date": None,
                "vendor_name": None,
                "vendor_abn": None,
                "vendor_address": None
            },
            "financial_summary": {
                "subtotal": 0.0,
                "tax_amount": 0.0,
                "total_amount": 0.0,
                "currency": "AUD"
            },
            "transactions": [],
            "payment_terms": {
                "payment_method": None,
                "due_date": None,
                "account_details": None
            },
            "extraction_metadata": {
                "extracted_at": datetime.utcnow().isoformat(),
                "model": "fallback",
                "document_type": "unknown",
                "confidence": 0.0,
                "note": "AI extraction not available - ANTHROPIC_API_KEY not set"
            }
        }


# Singleton instance
_ai_extraction_service = None


def get_ai_extraction_service() -> AIExtractionService:
    """Get or create the AI extraction service singleton."""
    global _ai_extraction_service
    if _ai_extraction_service is None:
        _ai_extraction_service = AIExtractionService()
    return _ai_extraction_service
