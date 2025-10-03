"""
Line Item Classifier
Classifies financial line items into standard categories using rule-based and fuzzy matching
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from ..config.settings import MIN_CONFIDENCE_THRESHOLD, HIGH_CONFIDENCE_THRESHOLD, FUZZY_MATCH_THRESHOLD


class LineItemClassifier:
    """Classify financial line items into standard categories"""

    def __init__(self, config_path: str = None):
        """
        Initialize classifier

        Args:
            config_path: Path to account_categories.json config file
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'account_categories.json'

        # Load classification rules
        with open(config_path, 'r') as f:
            self.categories = json.load(f)

        # Build keyword index for faster lookup
        self.keyword_index = self._build_keyword_index()

    def _build_keyword_index(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        Build index mapping keywords to categories

        Returns:
            Dict mapping keywords to list of (main_category, sub_category, template_line)
        """
        index = {}

        for main_category, sub_categories in self.categories.items():
            for sub_category, config in sub_categories.items():
                keywords = config.get('keywords', [])
                template_line = config.get('template_line', sub_category)

                for keyword in keywords:
                    keyword_lower = keyword.lower()
                    if keyword_lower not in index:
                        index[keyword_lower] = []

                    index[keyword_lower].append((main_category, sub_category, template_line))

        return index

    def classify(self, description: str, amount: float = None) -> Dict:
        """
        Classify a financial line item

        Args:
            description: Line item description
            amount: Line item amount (optional, can help with classification)

        Returns:
            Classification result with category, confidence, etc.
        """
        if not description:
            return {
                'classification': 'unknown',
                'confidence': 0.0,
                'method': 'none',
                'description': description
            }

        description_lower = description.lower().strip()

        # Try exact keyword match first
        exact_match = self._exact_keyword_match(description_lower)
        if exact_match:
            return exact_match

        # Try fuzzy matching
        fuzzy_match = self._fuzzy_keyword_match(description_lower)
        if fuzzy_match and fuzzy_match['confidence'] >= MIN_CONFIDENCE_THRESHOLD:
            return fuzzy_match

        # Try pattern-based matching
        pattern_match = self._pattern_match(description_lower, amount)
        if pattern_match:
            return pattern_match

        # If no match, return unknown
        return {
            'classification': 'unknown',
            'main_category': 'unknown',
            'sub_category': 'unknown',
            'template_line': 'Unclassified',
            'confidence': 0.0,
            'method': 'none',
            'description': description
        }

    def _exact_keyword_match(self, description_lower: str) -> Optional[Dict]:
        """Try exact keyword matching"""
        for keyword, matches in self.keyword_index.items():
            if keyword in description_lower:
                # Check exclusions
                main_category, sub_category, template_line = matches[0]
                config = self.categories[main_category][sub_category]

                exclude_keywords = config.get('exclude', [])
                if any(excl.lower() in description_lower for excl in exclude_keywords):
                    continue

                return {
                    'classification': 'classified',
                    'main_category': main_category,
                    'sub_category': sub_category,
                    'template_line': template_line,
                    'gl_codes': config.get('gl_codes', []),
                    'confidence': 1.0,
                    'method': 'exact_keyword',
                    'matched_keyword': keyword,
                    'description': description_lower
                }

        return None

    def _fuzzy_keyword_match(self, description_lower: str) -> Optional[Dict]:
        """Try fuzzy string matching"""
        best_match = None
        best_score = 0

        for keyword, matches in self.keyword_index.items():
            # Use token set ratio for better matching
            score = fuzz.token_set_ratio(description_lower, keyword)

            if score > best_score and score >= FUZZY_MATCH_THRESHOLD:
                main_category, sub_category, template_line = matches[0]
                config = self.categories[main_category][sub_category]

                # Check exclusions
                exclude_keywords = config.get('exclude', [])
                if any(excl.lower() in description_lower for excl in exclude_keywords):
                    continue

                best_score = score
                best_match = {
                    'classification': 'classified',
                    'main_category': main_category,
                    'sub_category': sub_category,
                    'template_line': template_line,
                    'gl_codes': config.get('gl_codes', []),
                    'confidence': score / 100.0,  # Convert to 0-1 scale
                    'method': 'fuzzy_match',
                    'matched_keyword': keyword,
                    'description': description_lower
                }

        return best_match

    def _pattern_match(self, description_lower: str, amount: float = None) -> Optional[Dict]:
        """Try pattern-based matching using common patterns"""

        # Pattern: Amounts with certain characteristics
        if amount is not None:
            # Negative amounts often indicate contra-accounts or refunds
            if amount < 0:
                if any(kw in description_lower for kw in ['depreciation', 'amortization']):
                    return self._create_result('non_current_assets', 'accumulated_depreciation', 0.7, 'pattern')

            # Large amounts might indicate capital items
            if amount > 100000:
                if any(kw in description_lower for kw in ['land', 'building', 'property']):
                    return self._create_result('non_current_assets', 'land', 0.75, 'pattern')

        # Pattern: Common abbreviations
        abbreviations = {
            'AR': ('current_assets', 'accounts_receivable'),
            'AP': ('current_liabilities', 'accounts_payable'),
            'WIP': ('current_assets', 'inventory'),
            'COGS': ('cost_of_goods_sold', 'materials'),
            'R&M': ('operating_expenses', 'repairs_maintenance'),
            'P&L': None  # Indicator of income statement, not a line item
        }

        for abbr, category_info in abbreviations.items():
            if abbr.lower() in description_lower:
                if category_info:
                    main_cat, sub_cat = category_info
                    return self._create_result(main_cat, sub_cat, 0.7, 'pattern_abbr')

        return None

    def _create_result(self, main_category: str, sub_category: str, confidence: float, method: str) -> Dict:
        """Helper to create classification result"""
        config = self.categories.get(main_category, {}).get(sub_category, {})

        return {
            'classification': 'classified',
            'main_category': main_category,
            'sub_category': sub_category,
            'template_line': config.get('template_line', sub_category),
            'gl_codes': config.get('gl_codes', []),
            'confidence': confidence,
            'method': method
        }

    def classify_batch(self, line_items: List[Dict]) -> List[Dict]:
        """
        Classify multiple line items

        Args:
            line_items: List of dicts with 'description' and optionally 'amount'

        Returns:
            List of classification results
        """
        results = []

        for item in line_items:
            description = item.get('description', '')
            amount = item.get('amount')

            result = self.classify(description, amount)
            result['original_item'] = item

            results.append(result)

        return results

    def get_classification_stats(self, results: List[Dict]) -> Dict:
        """Get statistics about classification results"""
        total = len(results)
        classified = sum(1 for r in results if r['classification'] == 'classified')
        unknown = total - classified

        high_confidence = sum(1 for r in results if r['confidence'] >= HIGH_CONFIDENCE_THRESHOLD)
        medium_confidence = sum(1 for r in results if MIN_CONFIDENCE_THRESHOLD <= r['confidence'] < HIGH_CONFIDENCE_THRESHOLD)
        low_confidence = sum(1 for r in results if 0 < r['confidence'] < MIN_CONFIDENCE_THRESHOLD)

        return {
            'total': total,
            'classified': classified,
            'unknown': unknown,
            'classification_rate': (classified / total * 100) if total > 0 else 0,
            'high_confidence': high_confidence,
            'medium_confidence': medium_confidence,
            'low_confidence': low_confidence
        }


def main():
    """Test function"""
    classifier = LineItemClassifier()

    # Test cases
    test_items = [
        {'description': 'Cash in Bank - Operating Account', 'amount': 50000},
        {'description': 'Accounts Receivable from customers', 'amount': 25000},
        {'description': 'BuildMart Materials', 'amount': 15000},
        {'description': 'Office Rent - September 2024', 'amount': 3000},
        {'description': 'Depreciation - Buildings', 'amount': -2000},
        {'description': 'GST Collected', 'amount': 5000},
        {'description': 'Random Item XYZ', 'amount': 100},
    ]

    print("\nTesting Line Item Classifier:\n")
    print("=" * 80)

    results = classifier.classify_batch(test_items)

    for result in results:
        desc = result['original_item']['description']
        cat = result.get('template_line', 'Unknown')
        conf = result['confidence']
        method = result.get('method', 'none')

        print(f"\n{desc}")
        print(f"  → {cat}")
        print(f"  Confidence: {conf:.1%} ({method})")

    print("\n" + "=" * 80)

    stats = classifier.get_classification_stats(results)
    print(f"\nClassification Stats:")
    print(f"  Total: {stats['total']}")
    print(f"  Classified: {stats['classified']} ({stats['classification_rate']:.1f}%)")
    print(f"  Unknown: {stats['unknown']}")
    print(f"  High confidence: {stats['high_confidence']}")
    print(f"  Medium confidence: {stats['medium_confidence']}")


if __name__ == "__main__":
    main()
