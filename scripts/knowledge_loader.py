"""
Knowledge Loader - Load and index Via Series manual data
Reads JSON files and creates searchable knowledge base for AI diagnostics
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class KnowledgeLoader:
    """Load and manage Via Series elevator manual data"""

    def __init__(self, data_dir: str = "../data/via/v74"):
        """Initialize knowledge loader with data directory"""
        self.data_dir = Path(data_dir)
        self.error_codes = []
        self.parameters = []
        self.abbreviations = []
        self.practical_guides = []
        self.loaded = False

    def load_all(self) -> bool:
        """Load all data files"""
        try:
            self.load_error_codes()
            self.load_parameters()
            self.load_abbreviations()
            self.load_practical_guides()
            self.loaded = True
            return True
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return False

    def load_error_codes(self) -> List[Dict]:
        """Load error codes from JSON"""
        filepath = self.data_dir / "error_codes.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.error_codes = data.get('f_codes', [])
                print(f"✅ Loaded {len(self.error_codes)} error codes")
                return self.error_codes
        except FileNotFoundError:
            print(f"❌ Error codes file not found: {filepath}")
            return []

    def load_parameters(self) -> List[Dict]:
        """Load parameters from JSON"""
        filepath = self.data_dir / "parameters.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.parameters = data.get('parameters', [])
                print(f"✅ Loaded {len(self.parameters)} parameters")
                return self.parameters
        except FileNotFoundError:
            print(f"❌ Parameters file not found: {filepath}")
            return []

    def load_abbreviations(self) -> List[Dict]:
        """Load component abbreviations from JSON"""
        filepath = self.data_dir / "abbreviations.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.abbreviations = data.get('abbreviations', [])
                print(f"✅ Loaded {len(self.abbreviations)} components/abbreviations")
                return self.abbreviations
        except FileNotFoundError:
            print(f"❌ Abbreviations file not found: {filepath}")
            return []

    def load_practical_guides(self) -> List[Dict]:
        """Load practical diagnostic guides from JSON"""
        filepath = self.data_dir / "practical_guides.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.practical_guides = data.get('diagnostic_guides', [])
                print(f"✅ Loaded {len(self.practical_guides)} practical diagnostic guides")
                return self.practical_guides
        except FileNotFoundError:
            print(f"⚠️  Practical guides file not found: {filepath}")
            return []
        except Exception as e:
            print(f"⚠️  Error loading practical guides: {e}")
            return []

    def get_error_by_code(self, code: str) -> Optional[Dict]:
        """Find error code by exact match"""
        code_clean = code.upper().strip()
        for error in self.error_codes:
            if error.get('code', '').upper() == code_clean:
                return error
        return None

    def get_parameter_by_code(self, code: str) -> List[Dict]:
        """Find all parameter instances by code (can appear multiple times with different meanings)"""
        code_clean = code.upper().strip()
        matches = []
        for param in self.parameters:
            if param.get('code', '').upper() == code_clean:
                matches.append(param)
        return matches

    def get_abbreviation(self, code: str) -> Optional[Dict]:
        """Find component/abbreviation"""
        code_clean = code.upper().strip()
        for abbrev in self.abbreviations:
            if abbrev.get('code', '').upper() == code_clean:
                return abbrev
        return None

    def search_errors_by_description(self, query: str) -> List[Dict]:
        """Search error codes by description"""
        query_lower = query.lower()
        results = []
        for error in self.error_codes:
            desc = error.get('description_de', '').lower()
            cause = error.get('cause_solution', '').lower()
            if query_lower in desc or query_lower in cause:
                results.append(error)
        return results

    def search_parameters_by_description(self, query: str) -> List[Dict]:
        """Search parameters by description"""
        query_lower = query.lower()
        results = []
        for param in self.parameters:
            desc = param.get('description_de', '').lower()
            if query_lower in desc:
                results.append(param)
        return results

    def search_abbreviations(self, query: str) -> List[Dict]:
        """Search abbreviations/components"""
        query_lower = query.lower()
        results = []
        for abbrev in self.abbreviations:
            code = abbrev.get('code', '').lower()
            desc = abbrev.get('description_de', '').lower()
            if code in query_lower or desc in query_lower or query_lower in code or query_lower in desc:
                results.append(abbrev)
        return results

    def search_practical_guides(self, query: str) -> List[Dict]:
        """Search practical diagnostic guides by title or related errors"""
        query_lower = query.lower()
        results = []
        for guide in self.practical_guides:
            title = guide.get('title', '').lower()
            problem = guide.get('problem', '').lower()
            related_errors = [e.lower() for e in guide.get('related_errors', [])]

            # Check if query matches title, problem, or related error codes
            if (query_lower in title or
                query_lower in problem or
                any(query_lower in err for err in related_errors)):
                results.append(guide)
        return results

    def get_summary(self) -> Dict:
        """Get summary of loaded data"""
        return {
            "error_codes": len(self.error_codes),
            "parameters": len(self.parameters),
            "abbreviations": len(self.abbreviations),
            "practical_guides": len(self.practical_guides),
            "total": len(self.error_codes) + len(self.parameters) + len(self.abbreviations),
            "loaded": self.loaded
        }

    def export_for_ai_context(self) -> str:
        """Export all data as formatted text for Claude context"""
        context = "# Via Series Elevator Control Manual - Knowledge Base\n\n"

        # Error codes
        context += "## ERROR CODES (F-Codes) - 26 entries\n"
        for code in self.error_codes:
            context += f"\n### {code.get('code')}\n"
            context += f"- Description: {code.get('description_de')}\n"
            if code.get('cause_solution'):
                context += f"- Cause/Solution: {code.get('cause_solution')}\n"
            context += f"- Manual Page: {code.get('manual_page')}\n"

        # Parameters
        context += "\n\n## PARAMETERS (P-Codes) - 93 instances\n"
        seen_params = set()
        for param in self.parameters:
            param_key = f"{param.get('code')}_{param.get('description_de')}"
            if param_key not in seen_params:
                context += f"\n### {param.get('code')}\n"
                context += f"- {param.get('description_de')}\n"
                if param.get('section'):
                    context += f"- Section: {param.get('section')}\n"
                context += f"- Manual Page: {param.get('manual_page')}\n"
                seen_params.add(param_key)

        # Abbreviations
        context += "\n\n## COMPONENTS & ABBREVIATIONS - 151 entries\n"
        for abbrev in self.abbreviations:
            context += f"\n### {abbrev.get('code')}\n"
            context += f"- {abbrev.get('description_de')}\n"

        # Practical diagnostic guides
        if self.practical_guides:
            context += f"\n\n## PRACTICAL DIAGNOSTIC GUIDES - {len(self.practical_guides)} guides\n"
            for guide in self.practical_guides:
                context += f"\n### {guide.get('title')}\n"
                context += f"- Problem: {guide.get('problem')}\n"
                context += f"- Related Error Codes: {', '.join(guide.get('related_errors', []))}\n"
                context += f"- Difficulty: {guide.get('difficulty_level')}\n"
                if guide.get('diagnosis_steps'):
                    context += f"- Diagnosis Steps: {len(guide.get('diagnosis_steps'))} steps\n"

        return context


if __name__ == "__main__":
    # Test the loader
    loader = KnowledgeLoader()

    print("Loading Via Series knowledge base...\n")
    if loader.load_all():
        print("\n" + "="*50)
        print("✅ Knowledge Base Loaded Successfully")
        print("="*50)
        print(json.dumps(loader.get_summary(), indent=2))

        print("\n" + "="*50)
        print("Example: Error Code F01 02")
        print("="*50)
        error = loader.get_error_by_code("F01 02")
        if error:
            print(json.dumps(error, indent=2, ensure_ascii=False))

        print("\n" + "="*50)
        print("Example: Search for 'Tür' in descriptions")
        print("="*50)
        results = loader.search_errors_by_description("Tür")
        print(f"Found {len(results)} error codes:")
        for r in results[:3]:
            print(f"  - {r.get('code')}: {r.get('description_de')}")
    else:
        print("❌ Failed to load knowledge base")
