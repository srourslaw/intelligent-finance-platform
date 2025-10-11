"""
Template Parser Service
Parses MASTER FINANCIAL STATEMENT TEMPLATE.md into structured JSON dictionary
"""
import re
from pathlib import Path
from typing import Dict, List, Any
import json


class TemplateParser:
    """Parse financial statement template MD files into structured dictionaries."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.base_path = Path(__file__).parent.parent.parent / "projects" / project_id
        self.template_path = self.base_path / "MASTER FINANCIAL STATEMENT TEMPLATE.md"

    def parse(self) -> Dict[str, Any]:
        """
        Parse the MASTER template into structured JSON.

        Returns:
            Dict with hierarchical structure of financial statement categories
        """
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        with open(self.template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse into structured format
        structure = {
            "balance_sheet": self._parse_balance_sheet(content),
            "income_statement": self._parse_income_statement(content),
            "cash_flow_statement": self._parse_cash_flow_statement(content),
            "metadata": {
                "project_id": self.project_id,
                "total_categories": 0
            }
        }

        # Count total categories
        structure["metadata"]["total_categories"] = self._count_categories(structure)

        return structure

    def _parse_balance_sheet(self, content: str) -> Dict[str, Any]:
        """Parse Balance Sheet section."""
        # Extract section between "BALANCE SHEET" and "INCOME STATEMENT"
        pattern = r'BALANCE SHEET\n\n(.*?)(?=INCOME STATEMENT|$)'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return {}

        section = match.group(1)

        return {
            "assets": self._parse_section(section, "ASSETS", "LIABILITIES"),
            "liabilities": self._parse_section(section, "LIABILITIES", "EQUITY"),
            "equity": self._parse_section(section, "EQUITY", "TOTAL LIABILITIES AND EQUITY")
        }

    def _parse_income_statement(self, content: str) -> Dict[str, Any]:
        """Parse Income Statement section."""
        pattern = r'INCOME STATEMENT.*?\n\n(.*?)(?=CASH FLOW STATEMENT|$)'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return {}

        section = match.group(1)

        return {
            "revenue": self._extract_items(section, "Revenue", "Cost of Goods Sold"),
            "cogs": self._extract_items(section, "Cost of Goods Sold", "Gross Profit"),
            "operating_expenses": self._extract_items(section, "Operating Expenses", "Operating Income"),
            "other_income": self._extract_items(section, "Other Income", "Other Expenses"),
            "other_expenses": self._extract_items(section, "Other Expenses", "Net Profit")
        }

    def _parse_cash_flow_statement(self, content: str) -> Dict[str, Any]:
        """Parse Cash Flow Statement section."""
        pattern = r'CASH FLOW STATEMENT\n\n(.*?)(?=STATEMENT OF CHANGES|$)'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return {}

        section = match.group(1)

        return {
            "operating_activities": self._extract_items(section, "Operating Activities", "Investing Activities"),
            "investing_activities": self._extract_items(section, "Investing Activities", "Financing Activities"),
            "financing_activities": self._extract_items(section, "Financing Activities", "Net Increase")
        }

    def _parse_section(self, content: str, start_marker: str, end_marker: str) -> Dict[str, Any]:
        """Parse a major section."""
        pattern = f'{start_marker}(.*?)(?={end_marker}|$)'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return {}

        section_text = match.group(1)
        items = self._extract_line_items(section_text)

        return {
            "items": items,
            "keywords": self._generate_keywords(items)
        }

    def _extract_items(self, content: str, start: str, end: str) -> Dict[str, Any]:
        """Extract items between two markers."""
        pattern = f'{start}.*?\n(.*?)(?={end}|$)'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return {"items": [], "keywords": []}

        text = match.group(1)
        items = self._extract_line_items(text)

        return {
            "items": items,
            "keywords": self._generate_keywords(items)
        }

    def _extract_line_items(self, text: str) -> List[str]:
        """
        Extract line items from text.

        Line items are lines that:
        - Are not empty
        - Don't start with numbers (ratios/metrics)
        - Don't contain '=' or '÷' (formulas)
        - Are not all caps (section headers)
        """
        lines = text.strip().split('\n')
        items = []

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip section headers (all caps with no lowercase)
            if line.isupper() and len(line) > 3:
                continue

            # Skip formulas/ratios
            if '=' in line or '÷' in line or '×' in line:
                continue

            # Skip ratio headers
            if 'Ratio' in line and ':' not in line:
                continue

            # Skip notes/metrics sections
            if line.startswith('Note') or line.startswith('KPI'):
                continue

            # Valid line item
            items.append(line)

        return items

    def _generate_keywords(self, items: List[str]) -> List[str]:
        """
        Generate searchable keywords from line items.

        Strategy:
        - Extract meaningful words (ignore common words)
        - Convert to lowercase
        - Remove special characters
        - Include variations (e.g., "receivable" and "receivables")
        """
        common_words = {
            'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were',
            'less', 'add', 'total', 'net', 'other', 'current', 'non'
        }

        keywords = set()

        for item in items:
            # Clean and split
            words = re.findall(r'\b[a-zA-Z]+\b', item.lower())

            for word in words:
                if len(word) > 2 and word not in common_words:
                    keywords.add(word)

                    # Add plural/singular variations
                    if word.endswith('s'):
                        keywords.add(word[:-1])
                    else:
                        keywords.add(word + 's')

        return sorted(list(keywords))

    def _count_categories(self, structure: Dict[str, Any]) -> int:
        """Count total number of categories in structure."""
        count = 0

        def count_recursive(obj):
            nonlocal count
            if isinstance(obj, dict):
                if 'items' in obj:
                    count += len(obj['items'])
                for value in obj.values():
                    count_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    count_recursive(item)

        count_recursive(structure)
        return count

    def save_to_json(self, output_path: Path = None):
        """Save parsed template to JSON file."""
        structure = self.parse()

        if output_path is None:
            output_path = self.base_path / "template_dictionary.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2)

        return output_path


def parse_template(project_id: str) -> Dict[str, Any]:
    """
    Main function to parse template for a project.

    Args:
        project_id: Project identifier

    Returns:
        Parsed template dictionary
    """
    parser = TemplateParser(project_id)
    return parser.parse()


if __name__ == "__main__":
    # Test with project-a
    project_id = "project-a-123-sunset-blvd"
    parser = TemplateParser(project_id)

    print(f"Parsing template for {project_id}...")
    template = parser.parse()

    print(f"\nTemplate parsed successfully!")
    print(f"Total categories: {template['metadata']['total_categories']}")

    # Save to JSON
    output_path = parser.save_to_json()
    print(f"Saved to: {output_path}")

    # Print sample
    print("\nSample - Income Statement Revenue:")
    print(json.dumps(template['income_statement']['revenue'], indent=2))
