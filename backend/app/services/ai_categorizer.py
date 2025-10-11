"""
AI Categorization Service

Maps extracted transactions to MASTER Financial Statement Template categories
using keyword matching and LLM-based classification.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class AICategorizer:
    """Service for categorizing transactions using AI and keyword matching."""

    def __init__(self, template_dict: Dict[str, Any]):
        """
        Initialize categorizer with template dictionary.

        Args:
            template_dict: Parsed MASTER template dictionary
        """
        self.template_dict = template_dict
        self.categories = self._extract_categories()
        self.keyword_map = self._build_keyword_map()

    def _extract_categories(self) -> List[str]:
        """Extract all category names from template."""
        categories = []
        for section_name, section_data in self.template_dict.items():
            if isinstance(section_data, dict) and 'items' in section_data:
                for item in section_data['items']:
                    if 'name' in item:
                        categories.append(item['name'])
        return categories

    def _build_keyword_map(self) -> Dict[str, List[str]]:
        """
        Build keyword map for each category based on common construction terms.

        Returns:
            Dictionary mapping category names to lists of keywords
        """
        # Common keyword patterns for construction categories
        keyword_map = {
            # Revenue categories
            'Contract Revenue': ['contract', 'revenue', 'income', 'payment received', 'billing'],
            'Change Orders': ['change order', 'co ', 'variation', 'extra work', 'additional work'],
            'Progress Payments': ['progress payment', 'draw', 'milestone payment', 'invoice'],

            # Direct Costs - Materials
            'Concrete & Cement': ['concrete', 'cement', 'ready-mix', 'rebar', 'reinforcement'],
            'Steel & Metal': ['steel', 'metal', 'beam', 'column', 'rebar', 'reinforcing'],
            'Lumber & Wood': ['lumber', 'wood', 'timber', 'plywood', 'framing', '2x4', '2x6'],
            'Drywall & Gypsum': ['drywall', 'gypsum', 'sheetrock', 'wallboard', 'taping', 'mud'],
            'Roofing Materials': ['roofing', 'shingles', 'underlayment', 'flashing', 'ridge vent'],
            'Insulation': ['insulation', 'fiberglass', 'foam', 'r-value', 'vapor barrier'],
            'Doors & Windows': ['door', 'window', 'glazing', 'frame', 'sill', 'threshold'],
            'Flooring Materials': ['flooring', 'tile', 'carpet', 'hardwood', 'laminate', 'vinyl'],
            'Paint & Coatings': ['paint', 'primer', 'stain', 'coating', 'sealer', 'varnish'],
            'Plumbing Materials': ['plumbing', 'pipe', 'fixture', 'faucet', 'drain', 'copper', 'pvc'],
            'Electrical Materials': ['electrical', 'wire', 'cable', 'conduit', 'breaker', 'panel', 'outlet'],
            'HVAC Materials': ['hvac', 'ductwork', 'furnace', 'air conditioner', 'thermostat', 'venting'],
            'Masonry Materials': ['masonry', 'brick', 'block', 'mortar', 'grout', 'stone'],

            # Direct Costs - Labor
            'Carpenters': ['carpenter', 'framer', 'framing', 'trim carpenter', 'cabinet'],
            'Electricians': ['electrician', 'electrical contractor', 'electric'],
            'Plumbers': ['plumber', 'plumbing contractor'],
            'HVAC Technicians': ['hvac tech', 'hvac contractor', 'heating', 'cooling'],
            'General Laborers': ['laborer', 'general labor', 'helper', 'cleanup crew'],
            'Foremen/Supervisors': ['foreman', 'supervisor', 'superintendent', 'project manager'],
            'Masons': ['mason', 'bricklayer', 'block layer'],
            'Painters': ['painter', 'painting contractor'],
            'Drywall Installers': ['drywaller', 'drywall installer', 'taper'],
            'Roofers': ['roofer', 'roofing contractor'],
            'Concrete Workers': ['concrete finisher', 'cement mason', 'concrete crew'],
            'Equipment Operators': ['operator', 'excavator operator', 'backhoe', 'crane operator'],

            # Direct Costs - Equipment
            'Heavy Equipment Rental': ['excavator', 'backhoe', 'bulldozer', 'crane', 'loader', 'rental'],
            'Small Tools & Equipment': ['saw', 'drill', 'nail gun', 'compressor', 'generator', 'tool'],
            'Safety Equipment': ['safety', 'ppe', 'harness', 'hardhat', 'gloves', 'vest', 'boots'],
            'Scaffolding': ['scaffold', 'staging', 'platform'],
            'Formwork': ['formwork', 'forms', 'shoring'],

            # Direct Costs - Subcontractors
            'Foundation Subcontractor': ['foundation', 'footing', 'basement', 'slab'],
            'Framing Subcontractor': ['framing sub', 'frame contractor'],
            'Electrical Subcontractor': ['electrical sub', 'electric contractor'],
            'Plumbing Subcontractor': ['plumbing sub', 'plumber'],
            'HVAC Subcontractor': ['hvac sub', 'mechanical contractor'],
            'Roofing Subcontractor': ['roofing sub', 'roofer'],
            'Drywall Subcontractor': ['drywall sub'],
            'Painting Subcontractor': ['painting sub', 'painter'],
            'Flooring Subcontractor': ['flooring sub', 'tile contractor', 'carpet installer'],
            'Landscaping Subcontractor': ['landscaping', 'landscape contractor', 'irrigation'],

            # Indirect Costs
            'Site Utilities': ['utility', 'water', 'sewer', 'electric hookup', 'temporary power'],
            'Permits & Fees': ['permit', 'fee', 'inspection', 'license', 'municipal'],
            'Insurance': ['insurance', 'liability', 'workers comp', 'bond', 'premium'],
            'Office Supplies': ['office', 'supplies', 'paper', 'printer', 'stationery'],
            'Vehicle Expenses': ['vehicle', 'truck', 'fuel', 'gas', 'mileage', 'maintenance'],
            'Professional Services': ['architect', 'engineer', 'consultant', 'legal', 'accounting'],
            'Marketing & Advertising': ['marketing', 'advertising', 'website', 'signs'],
            'Warehouse/Storage': ['warehouse', 'storage', 'rent', 'lease'],
            'Equipment Maintenance': ['maintenance', 'repair', 'service', 'parts'],
            'Project Management Software': ['software', 'subscription', 'procore', 'quickbooks'],

            # General keywords
            'Waste Disposal': ['waste', 'disposal', 'dumpster', 'trash', 'debris removal'],
            'Transportation': ['transportation', 'delivery', 'freight', 'shipping'],
            'Testing & Inspection': ['testing', 'inspection', 'lab', 'quality control'],
        }

        return keyword_map

    def categorize_transaction(
        self,
        description: str,
        amount: float,
        vendor: Optional[str] = None,
        use_llm: bool = False
    ) -> Tuple[str, float]:
        """
        Categorize a single transaction.

        Args:
            description: Transaction description
            amount: Transaction amount
            vendor: Vendor name (optional)
            use_llm: Whether to use LLM for ambiguous cases

        Returns:
            Tuple of (category_name, confidence_score)
        """
        # First try keyword matching
        category, confidence = self._keyword_match(description, vendor)

        if confidence < 0.6 and use_llm:
            # Fall back to LLM for low-confidence matches
            category, confidence = self._llm_categorize(description, amount, vendor)

        return category, confidence

    def _keyword_match(self, description: str, vendor: Optional[str] = None) -> Tuple[str, float]:
        """
        Match transaction using keyword patterns.

        Args:
            description: Transaction description
            vendor: Vendor name

        Returns:
            Tuple of (category_name, confidence_score)
        """
        text = (description + " " + (vendor or "")).lower()

        best_category = "Uncategorized"
        best_score = 0.0

        for category, keywords in self.keyword_map.items():
            score = 0
            matches = 0

            for keyword in keywords:
                if keyword.lower() in text:
                    matches += 1
                    # Longer keywords get higher weight
                    score += len(keyword.split())

            if matches > 0:
                # Calculate confidence based on number and quality of matches
                confidence = min(0.95, (matches * score) / len(keywords) + 0.5)
                if confidence > best_score:
                    best_score = confidence
                    best_category = category

        # If no keyword match, try to infer from amount and context
        if best_score == 0.0:
            best_category, best_score = self._infer_from_context(description, vendor)

        return best_category, best_score

    def _infer_from_context(self, description: str, vendor: Optional[str] = None) -> Tuple[str, float]:
        """
        Infer category from contextual clues.

        Args:
            description: Transaction description
            vendor: Vendor name

        Returns:
            Tuple of (category_name, confidence_score)
        """
        text = (description + " " + (vendor or "")).lower()

        # Common vendor/business type patterns
        if any(x in text for x in ['home depot', 'lowes', "lowe's", 'menards', 'hardware']):
            return 'General Materials', 0.7

        if any(x in text for x in ['supply', 'supplier', 'materials']):
            return 'General Materials', 0.65

        if any(x in text for x in ['contractor', 'construction', 'builders']):
            return 'Subcontractors', 0.6

        if any(x in text for x in ['labor', 'payroll', 'wages']):
            return 'General Laborers', 0.6

        if any(x in text for x in ['rental', 'rent', 'lease']):
            return 'Heavy Equipment Rental', 0.6

        return 'Uncategorized', 0.3

    def _llm_categorize(
        self,
        description: str,
        amount: float,
        vendor: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Use LLM to categorize ambiguous transactions.

        Args:
            description: Transaction description
            amount: Transaction amount
            vendor: Vendor name

        Returns:
            Tuple of (category_name, confidence_score)
        """
        try:
            import google.generativeai as genai

            # Configure API
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                logger.warning("GOOGLE_API_KEY not set, falling back to keyword matching")
                return 'Uncategorized', 0.3

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')

            # Build prompt
            prompt = f"""You are a construction financial categorization expert.

Categorize this transaction into ONE of these categories:
{', '.join(self.categories[:50])}  # Limit categories to avoid token overflow

Transaction Details:
- Description: {description}
- Amount: ${amount:,.2f}
- Vendor: {vendor or 'Unknown'}

Respond with ONLY the category name, nothing else."""

            response = model.generate_content(prompt)
            predicted_category = response.text.strip()

            # Validate category exists in template
            if predicted_category in self.categories:
                return predicted_category, 0.8
            else:
                # LLM returned invalid category, use best keyword match
                return self._keyword_match(description, vendor)

        except Exception as e:
            logger.error(f"LLM categorization failed: {e}")
            return 'Uncategorized', 0.3

    def categorize_batch(
        self,
        transactions: List[Dict[str, Any]],
        use_llm: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Categorize a batch of transactions.

        Args:
            transactions: List of transaction dictionaries with keys:
                - description (str)
                - amount (float)
                - vendor (str, optional)
            use_llm: Whether to use LLM for low-confidence matches

        Returns:
            List of transactions with added 'category' and 'confidence' fields
        """
        categorized = []

        for txn in transactions:
            description = txn.get('description', '')
            amount = txn.get('amount', 0.0)
            vendor = txn.get('vendor')

            category, confidence = self.categorize_transaction(
                description, amount, vendor, use_llm
            )

            categorized_txn = txn.copy()
            categorized_txn['category'] = category
            categorized_txn['confidence'] = confidence
            categorized.append(categorized_txn)

        return categorized

    def get_category_summary(self, categorized_transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for categorized transactions.

        Args:
            categorized_transactions: List of categorized transactions

        Returns:
            Dictionary with category summaries
        """
        summary = {
            'total_transactions': len(categorized_transactions),
            'categories': {},
            'uncategorized_count': 0,
            'low_confidence_count': 0,
            'average_confidence': 0.0
        }

        total_confidence = 0.0

        for txn in categorized_transactions:
            category = txn.get('category', 'Uncategorized')
            amount = txn.get('amount', 0.0)
            confidence = txn.get('confidence', 0.0)

            total_confidence += confidence

            if category == 'Uncategorized':
                summary['uncategorized_count'] += 1

            if confidence < 0.6:
                summary['low_confidence_count'] += 1

            if category not in summary['categories']:
                summary['categories'][category] = {
                    'count': 0,
                    'total_amount': 0.0,
                    'avg_confidence': 0.0,
                    'confidence_sum': 0.0
                }

            summary['categories'][category]['count'] += 1
            summary['categories'][category]['total_amount'] += amount
            summary['categories'][category]['confidence_sum'] += confidence

        # Calculate averages
        if len(categorized_transactions) > 0:
            summary['average_confidence'] = total_confidence / len(categorized_transactions)

        for cat_data in summary['categories'].values():
            if cat_data['count'] > 0:
                cat_data['avg_confidence'] = cat_data['confidence_sum'] / cat_data['count']
            del cat_data['confidence_sum']  # Remove temporary field

        return summary


def create_categorizer(template_dict: Dict[str, Any]) -> AICategorizer:
    """
    Factory function to create categorizer instance.

    Args:
        template_dict: Parsed MASTER template dictionary

    Returns:
        AICategorizer instance
    """
    return AICategorizer(template_dict)
