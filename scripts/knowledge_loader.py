"""
Knowledge Loader - Load and index elevator manual data
Supports both General (universal) and Manufacturer-specific knowledge
Reads JSON files and creates searchable knowledge base for AI diagnostics
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class KnowledgeLoader:
    """Load and manage elevator knowledge base with support for general and manufacturer-specific data"""

    def __init__(self, base_data_dir: str = "../data"):
        """
        Initialize knowledge loader with support for new hierarchical structure

        Args:
            base_data_dir: Root data directory (supports both old and new structure)
        """
        self.base_dir = Path(base_data_dir)

        # General/universal knowledge
        self.general_dir = self.base_dir / "general"
        self.practical_guides = []

        # Manufacturer-specific knowledge
        self.manufacturers_dir = self.base_dir / "manufacturers"
        self.error_codes = []
        self.parameters = []
        self.components = []
        self.quirks = []

        # Image index
        self.image_index = {}

        # Loading status
        self.loaded = False
        self.active_manufacturer = "via"
        self.active_version = "v74"

    def load_all(self, manufacturer: str = "via", version: str = "v74") -> bool:
        """
        Load all knowledge bases (general + manufacturer-specific)

        Args:
            manufacturer: Manufacturer name (e.g., 'via')
            version: System version (e.g., 'v74')

        Returns:
            True if loading successful
        """
        try:
            self.active_manufacturer = manufacturer
            self.active_version = version

            # Load general/universal knowledge
            self.load_practical_guides()

            # Load manufacturer-specific knowledge
            self.load_error_codes(manufacturer, version)
            self.load_parameters(manufacturer, version)
            self.load_components(manufacturer, version)
            self.load_quirks(manufacturer, version)

            # Load image index
            self.load_image_index()

            self.loaded = True
            return True
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return False

    # ==================== GENERAL/UNIVERSAL KNOWLEDGE ====================

    def load_practical_guides(self) -> List[Dict]:
        """Load universal practical diagnostic guides"""
        # Try new structure first
        filepath = self.general_dir / "practical_guides" / "universal_guides.json"

        if not filepath.exists():
            # Fall back to old structure
            filepath = self.base_dir / "via" / "v74" / "practical_guides.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.practical_guides = data.get('diagnostic_guides', [])
                print(f"✅ Loaded {len(self.practical_guides)} practical diagnostic guides (universal)")
                return self.practical_guides
        except FileNotFoundError:
            print(f"⚠️  Practical guides not found: {filepath}")
            return []
        except Exception as e:
            print(f"⚠️  Error loading practical guides: {e}")
            return []

    # ==================== MANUFACTURER-SPECIFIC KNOWLEDGE ====================

    def load_error_codes(self, manufacturer: str = "via", version: str = "v74") -> List[Dict]:
        """Load error codes from manufacturer-specific data"""
        # Try new structure first
        filepath = self.manufacturers_dir / manufacturer / version / "knowledge" / "error_codes.json"

        if not filepath.exists():
            # Fall back to old structure
            filepath = self.base_dir / manufacturer / version / "error_codes.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.error_codes = data.get('f_codes', [])
                print(f"✅ Loaded {len(self.error_codes)} error codes ({manufacturer}/{version})")
                return self.error_codes
        except FileNotFoundError:
            print(f"❌ Error codes file not found: {filepath}")
            return []

    def load_parameters(self, manufacturer: str = "via", version: str = "v74") -> List[Dict]:
        """Load parameters from manufacturer-specific data"""
        filepath = self.manufacturers_dir / manufacturer / version / "knowledge" / "parameters.json"

        if not filepath.exists():
            filepath = self.base_dir / manufacturer / version / "parameters.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.parameters = data.get('parameters', [])
                print(f"✅ Loaded {len(self.parameters)} parameters ({manufacturer}/{version})")
                return self.parameters
        except FileNotFoundError:
            print(f"❌ Parameters file not found: {filepath}")
            return []

    def load_components(self, manufacturer: str = "via", version: str = "v74") -> List[Dict]:
        """Load component abbreviations from manufacturer-specific data"""
        # Try new structure (renamed to components.json)
        filepath = self.manufacturers_dir / manufacturer / version / "knowledge" / "components.json"

        if not filepath.exists():
            # Try old structure (abbreviations.json)
            filepath = self.base_dir / manufacturer / version / "abbreviations.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.components = data.get('abbreviations', [])
                print(f"✅ Loaded {len(self.components)} components ({manufacturer}/{version})")
                return self.components
        except FileNotFoundError:
            print(f"❌ Components file not found: {filepath}")
            return []

    def load_quirks(self, manufacturer: str = "via", version: str = "v74") -> List[Dict]:
        """Load manufacturer-specific quirks and special behaviors"""
        filepath = self.manufacturers_dir / manufacturer / version / "knowledge" / "quirks.json"

        if not filepath.exists():
            filepath = self.base_dir / manufacturer / version / "quirks.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.quirks = data.get('quirks', [])
                print(f"✅ Loaded {len(self.quirks)} manufacturer quirks ({manufacturer}/{version})")
                return self.quirks
        except FileNotFoundError:
            # Quirks are optional
            print(f"⚠️  Quirks file not found (optional): {filepath}")
            return []

    # ==================== IMAGE INDEX ====================

    def load_image_index(self) -> Dict:
        """Load image reference index"""
        filepath = self.base_dir / "lookups" / "image_index.json"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.image_index = data.get('images', {})
                print(f"✅ Loaded image index with references to procedure diagrams")
                return self.image_index
        except FileNotFoundError:
            print(f"⚠️  Image index not found (optional): {filepath}")
            return {}

    # ==================== SEARCH METHODS ====================

    def get_error_by_code(self, code: str) -> Optional[Dict]:
        """Find error code by exact match"""
        code_clean = code.upper().strip()
        for error in self.error_codes:
            if error.get('code', '').upper() == code_clean:
                return error
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

    def search_components(self, query: str) -> List[Dict]:
        """Search components/abbreviations"""
        query_lower = query.lower()
        results = []
        for comp in self.components:
            code = comp.get('code', '').lower()
            desc = comp.get('description_de', '').lower()
            if code in query_lower or desc in query_lower or query_lower in code or query_lower in desc:
                results.append(comp)
        return results

    def search_abbreviations(self, query: str) -> List[Dict]:
        """Backward-compatible alias for search_components()"""
        return self.search_components(query)

    def search_practical_guides(self, query: str) -> List[Dict]:
        """Search practical diagnostic guides by title or related errors"""
        query_lower = query.lower()
        results = []
        for guide in self.practical_guides:
            title = guide.get('title', '').lower()
            problem = guide.get('problem', '').lower()
            related_errors = [e.lower() for e in guide.get('related_errors', [])]

            if (query_lower in title or
                query_lower in problem or
                any(query_lower in err for err in related_errors)):
                results.append(guide)
        return results

    def search_images_by_error(self, error_code: str) -> List[Dict]:
        """Find all images related to an error code"""
        results = []
        error_upper = error_code.upper()

        # Search in general images
        for img_type in self.image_index.get('general_images', {}).values():
            if isinstance(img_type, list):
                for img in img_type:
                    if error_upper in img.get('tags', []) or error_upper in img.get('error_codes', []):
                        results.append(img)

        # Search in manufacturer-specific images
        for mfg, versions in self.image_index.get(f'{self.active_manufacturer}_{self.active_version}_images', {}).items():
            if isinstance(versions, dict):
                for img_list in versions.values():
                    if isinstance(img_list, list):
                        for img in img_list:
                            if error_upper in img.get('tags', []) or error_upper in img.get('error_codes', []):
                                results.append(img)

        return results

    # ==================== SUMMARY & EXPORT ====================

    def get_summary(self) -> Dict:
        """Get summary of loaded data"""
        return {
            "error_codes": len(self.error_codes),
            "parameters": len(self.parameters),
            "components": len(self.components),
            "quirks": len(self.quirks),
            "practical_guides": len(self.practical_guides),
            "image_references": len(self.image_index),
            "total_knowledge_entries": (len(self.error_codes) + len(self.parameters) +
                                       len(self.components) + len(self.practical_guides)),
            "loaded": self.loaded,
            "active_manufacturer": self.active_manufacturer,
            "active_version": self.active_version
        }

    def export_for_ai_context(self) -> str:
        """Export all data as formatted text for Claude context"""
        context = "# Elevator Diagnostic Knowledge Base\n\n"
        context += f"**Active System**: {self.active_manufacturer.upper()} {self.active_version}\n\n"

        # Error codes
        context += "## ERROR CODES (F-Codes)\n"
        for code in self.error_codes:
            context += f"\n### {code.get('code')}\n"
            context += f"- Description: {code.get('description_de')}\n"
            if code.get('cause_solution'):
                context += f"- Cause/Solution: {code.get('cause_solution')}\n"

        # Parameters
        context += "\n\n## PARAMETERS (P-Codes)\n"
        seen_params = set()
        for param in self.parameters:
            param_key = f"{param.get('code')}_{param.get('description_de')}"
            if param_key not in seen_params:
                context += f"\n### {param.get('code')}\n"
                context += f"- {param.get('description_de')}\n"
                seen_params.add(param_key)

        # Components
        context += f"\n\n## COMPONENTS & ABBREVIATIONS\n"
        for comp in self.components:
            context += f"\n### {comp.get('code')}\n"
            context += f"- {comp.get('description_de')}\n"

        # Practical guides
        if self.practical_guides:
            context += f"\n\n## PRACTICAL DIAGNOSTIC GUIDES\n"
            for guide in self.practical_guides:
                context += f"\n### {guide.get('title')}\n"
                context += f"- Problem: {guide.get('problem')}\n"
                context += f"- Related Errors: {', '.join(guide.get('related_errors', []))}\n"

        return context


if __name__ == "__main__":
    # Test the loader
    loader = KnowledgeLoader()

    print("Loading knowledge base with new hierarchical structure...\n")
    if loader.load_all():
        print("\n" + "="*60)
        print("✅ Knowledge Base Loaded Successfully")
        print("="*60)
        summary = loader.get_summary()
        for key, val in summary.items():
            print(f"{key:25}: {val}")

        print("\n" + "="*60)
        print("Example: Search for Error Code F01 02")
        print("="*60)
        error = loader.get_error_by_code("F01 02")
        if error:
            print(f"Code: {error.get('code')}")
            print(f"Description: {error.get('description_de')}")
    else:
        print("❌ Failed to load knowledge base")
