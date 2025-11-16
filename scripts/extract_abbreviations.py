#!/usr/bin/env python3
"""
Extract abbreviations and connector codes from Via Quickguide
This builds a reference dictionary for all technical abbreviations
"""

import json
import os
import pdfplumber
import re
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = "../data/via/v74"
PDF_PATH = "../manuals/viaserie abkürzungen.pdf"

class AbbreviationExtractor:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def extract_abbreviations(self):
        """Extract abbreviations from quickguide PDF"""
        print("\n📋 Extracting abbreviations from quickguide...")

        abbreviations = {}  # code -> description

        try:
            with pdfplumber.open(PDF_PATH) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Parse abbreviation entries
                        # Pattern: CODE Description
                        # Split by newline and process
                        lines = text.split('\n')

                        for line in lines:
                            line = line.strip()
                            if not line or len(line) < 2:
                                continue

                            # Try to extract code and description
                            # Codes typically start with letter(s) followed by numbers or specific patterns
                            match = re.match(r'^([A-Z0-9]+(?:[A-Z0-9]+)*)\s+(.+)$', line)

                            if match:
                                code = match.group(1)
                                description = match.group(2).strip()

                                # Skip if this looks like a header or partial match
                                if len(code) > 1 and len(description) > 3:
                                    # Store if we haven't seen this code
                                    if code not in abbreviations:
                                        abbreviations[code] = {
                                            "code": code,
                                            "description_de": description,
                                            "extraction_status": "from_quickguide"
                                        }

            print(f"✅ Found {len(abbreviations)} abbreviations/codes")
            return list(abbreviations.values())

        except FileNotFoundError:
            print(f"⚠️  Quickguide PDF not found: {PDF_PATH}")
            return []

    def create_abbreviations_json(self):
        """Create abbreviations.json"""
        print("\n" + "="*80)
        print("CREATING abbreviations.json (from quickguide)")
        print("="*80)

        abbreviations = self.extract_abbreviations()

        abbrev_data = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "source": "Abbreviations Quickguide",
                "extraction_date": datetime.now().isoformat(),
                "status": "Populated from abbreviations guide",
                "total_abbreviations": len(abbreviations),
                "note": "Reference dictionary for technical abbreviations and connector codes"
            },
            "abbreviations": abbreviations if abbreviations else []
        }

        output_path = f"{self.output_dir}/abbreviations.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(abbrev_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")
        print(f"   Contains: {len(abbreviations)} abbreviations/codes")
        return abbreviations

def main():
    print("="*80)
    print("EXTRACTING ABBREVIATIONS FROM VIA QUICKGUIDE")
    print("="*80)

    extractor = AbbreviationExtractor(OUTPUT_DIR)
    extractor.create_abbreviations_json()

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("✅ Abbreviations extracted from quickguide")
    print("✅ Ready to use as reference for error code context")

if __name__ == "__main__":
    main()
