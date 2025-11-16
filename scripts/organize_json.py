#!/usr/bin/env python3
"""
Convert raw extracted data → Organized JSON files
ESC POC - Data Organization Tool
Automatically parses extracted PDF text and populates JSON templates
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = "../data/via/v74"
RAW_DIR = "../extracted_raw"

class JSONOrganizer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.statistics = {}

    def read_raw_page(self, page_num):
        """Read extracted text from a single page"""
        try:
            with open(f"{RAW_DIR}/page_{page_num:02d}_text.txt", 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def parse_error_codes(self):
        """Parse error codes from extracted pages (page 113+)"""
        print("\n📖 Parsing error codes from extracted pages...")

        f_codes = []

        # Error codes are on pages 113-127 (FEHLERTABELLE section)
        for page_num in range(113, 140):
            content = self.read_raw_page(page_num)
            if not content:
                continue

            # Find lines with F-codes: "F XX YY" pattern with complete description
            # Pattern matches: F followed by space, 2 digits, space, 2 digits, space, then description
            f_code_pattern = r'^F\s+(\d{2})\s+(\d{2})\s+(.+?)(?=\n(?:F\s+\d{2}\s+\d{2}|A\s+\d{2}|Z\s|V\d+\.\d+))'

            matches = re.finditer(f_code_pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                family = match.group(1)
                number = match.group(2)
                description = match.group(3).strip()

                # Clean up description - normalize whitespace but keep full content
                description = re.sub(r'\s+', ' ', description)
                # Remove page numbers at end
                description = re.sub(r'\s*V\d+\.\d+\s*-\s*\d+/\d+\s*.*$', '', description)

                f_code = {
                    "code": f"F{family} {number}",
                    "family": family,
                    "number": number,
                    "description_de": description if description else "N/A",
                    "manual_page": page_num,
                    "extraction_status": "parsed"
                }
                f_codes.append(f_code)

        print(f"✅ Found {len(f_codes)} F-codes (full descriptions)")
        return f_codes

    def create_error_codes_json(self):
        """Create error_codes.json with parsed data"""
        print("\n" + "="*80)
        print("CREATING error_codes.json")
        print("="*80)

        f_codes = self.parse_error_codes()

        error_codes = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "113-127",
                "extraction_date": datetime.now().isoformat(),
                "status": "Populated from PDF extraction",
                "total_f_codes": len(f_codes),
                "total_a_codes": 0,
                "note": "F-codes automatically extracted from pages 113-127"
            },
            "f_codes": f_codes,
            "a_codes": [
                {
                    "code": "A07",
                    "description_de": "Fotozelle unterbrochen",
                    "description_en": "Photocell interrupted",
                    "manual_page": 106,
                    "extraction_status": "example"
                }
            ]
        }

        output_path = f"{self.output_dir}/error_codes.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(error_codes, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")
        print(f"   Contains: {len(f_codes)} error codes")

    def parse_parameters(self):
        """Parse parameters from extracted pages (page 141+)"""
        print("\n📖 Parsing parameters from extracted pages...")

        parameters_dict = {}  # Use dict to deduplicate by code

        # Parameters are on pages 141-155 (VÍA SERIE Parameter section)
        for page_num in range(141, 156):
            content = self.read_raw_page(page_num)
            if not content:
                continue

            # Find lines with P-codes: "P####" pattern
            param_pattern = r'^P(\d{4})\s+(.+?)(?=\nP\d{4}|\nZ$|\n\n\nTECHNISCHES)'

            matches = re.finditer(param_pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                code = match.group(1)
                description = match.group(2).strip()

                # Clean up description - take first line
                description_lines = description.split('\n')
                description = description_lines[0].strip()

                # Clean up extra whitespace
                description = re.sub(r'\s+', ' ', description)

                # Only add if not already present, or if this entry has better description
                if code not in parameters_dict:
                    parameters_dict[code] = {
                        "code": f"P{code}",
                        "description_de": description[:150] if description else "N/A",
                        "manual_page": page_num,
                        "extraction_status": "parsed"
                    }
                elif description and len(description) > 5:
                    # Update if we found a better (longer) description
                    if len(description) > len(parameters_dict[code]["description_de"]):
                        parameters_dict[code]["description_de"] = description[:150]
                        parameters_dict[code]["manual_page"] = page_num

        # Convert dict to list
        parameters = list(parameters_dict.values())

        print(f"✅ Found {len(parameters)} unique parameters (after deduplication)")
        return parameters

    def create_parameters_json(self):
        """Create parameters.json with parsed data"""
        print("\n" + "="*80)
        print("CREATING parameters.json")
        print("="*80)

        parameters = self.parse_parameters()

        param_data = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "141-155",
                "extraction_date": datetime.now().isoformat(),
                "status": "Populated from PDF extraction",
                "total_parameters": len(parameters),
                "note": "Parameters automatically extracted from pages 141-155"
            },
            "parameters": parameters if parameters else [
                {
                    "code": "P0001",
                    "description_de": "Beispiel Parameter",
                    "manual_page": 141,
                    "extraction_status": "example"
                }
            ]
        }

        output_path = f"{self.output_dir}/parameters.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(param_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")
        print(f"   Contains: {len(parameters)} parameters")

    def create_hardware_json(self):
        """Create hardware.json with template"""
        print("\n" + "="*80)
        print("CREATING hardware.json")
        print("="*80)

        hardware = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "12-50",
                "extraction_date": datetime.now().isoformat(),
                "status": "Template - manual data entry needed",
                "total_boards": 0,
                "note": "Hardware information should be extracted from pages 12-50"
            },
            "boards": [
                {
                    "name": "SMQ Board",
                    "location": "Machine room control cabinet",
                    "function": "Safety monitoring and control",
                    "connectors": ["XTSS", "XKV", "XSM1"],
                    "extraction_status": "example"
                }
            ]
        }

        output_path = f"{self.output_dir}/hardware.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(hardware, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")

    def create_contacts_json(self):
        """Create contacts.json with template"""
        print("\n" + "="*80)
        print("CREATING contacts.json")
        print("="*80)

        contacts = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "154-155",
                "extraction_date": datetime.now().isoformat(),
                "status": "Template - manual data entry needed",
                "total_contacts": 0,
                "note": "Service contact information from pages 154-155 (ANHANG II)"
            },
            "contacts": [
                {
                    "code": "7H",
                    "name": "Shaft Door Contact",
                    "location": "Door safety system",
                    "function": "Monitors shaft door closure",
                    "extraction_status": "example"
                }
            ]
        }

        output_path = f"{self.output_dir}/contacts.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")

    def create_connectors_json(self):
        """Create connectors.json with template"""
        print("\n" + "="*80)
        print("CREATING connectors.json")
        print("="*80)

        connectors = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "14-50",
                "extraction_date": datetime.now().isoformat(),
                "status": "Template - manual data entry needed",
                "total_connectors": 0,
                "note": "Wiring connector information from pages 14-50"
            },
            "connectors": [
                {
                    "code": "XSSH2",
                    "board": "SMQ",
                    "purpose": "Safety circuit connection",
                    "pins": [1, 2, 3, 4],
                    "extraction_status": "example"
                }
            ]
        }

        output_path = f"{self.output_dir}/connectors.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(connectors, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")

    def create_quirks_json(self):
        """Create quirks.json with template"""
        print("\n" + "="*80)
        print("CREATING quirks.json")
        print("="*80)

        quirks = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "source": "manual + field_knowledge",
                "extraction_date": datetime.now().isoformat(),
                "status": "Template - awaiting field data",
                "note": "Known issues and workarounds - updated from field experience"
            },
            "known_issues": [
                {
                    "component": "CAB Board",
                    "problem": "Bus-Signal-Verarbeitung fehlerhaft",
                    "symptoms": [
                        "Türen öffnen/schließen manchmal nicht (sporadisch)",
                        "A07 Falschmeldung",
                        "Tür reagiert zeitweise nicht auf Befehle"
                    ],
                    "frequency_via": 0.40,
                    "solution": "CAB Board austauschen",
                    "extraction_status": "example"
                }
            ]
        }

        output_path = f"{self.output_dir}/quirks.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(quirks, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")

def main():
    print("="*80)
    print("ESC POC - JSON ORGANIZATION TOOL")
    print("="*80)
    print(f"\nCreating JSON files in: {OUTPUT_DIR}")
    print(f"Reading from: {RAW_DIR}")

    organizer = JSONOrganizer(OUTPUT_DIR)

    # Create all JSON files
    organizer.create_error_codes_json()
    organizer.create_parameters_json()
    organizer.create_hardware_json()
    organizer.create_contacts_json()
    organizer.create_connectors_json()
    organizer.create_quirks_json()

    # Summary
    print("\n" + "="*80)
    print("ORGANIZATION SUMMARY")
    print("="*80)
    print(f"Templates created: 6")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\n✅ JSON files ready!")
    print("\nNext steps:")
    print("1. Review the generated JSON files")
    print("2. For error_codes.json: Already has parsed data from PDF")
    print("3. For other files: Complete the manual data entry using extracted_raw/")
    print("4. Run: python validate_data.py")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
