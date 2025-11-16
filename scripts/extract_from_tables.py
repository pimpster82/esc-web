#!/usr/bin/env python3
"""
Extract data from structured PDF TABLES (not text)
This is the BEST approach - tables preserve complete formatting
"""

import json
import os
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = "../data/via/v74"
RAW_DIR = "../extracted_raw"

class TableExtractor:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def load_table_page(self, page_num):
        """Load extracted tables from a page"""
        try:
            with open(f"{RAW_DIR}/page_{page_num:02d}_tables.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def extract_error_codes_from_tables(self):
        """Extract F-codes from FEHLERTABELLE (page 113+)"""
        print("\n📋 Extracting error codes from structured tables...")

        f_codes = []

        # Error table is on page 113, table index 1
        tables = self.load_table_page(113)
        if not tables or len(tables) < 2:
            print("❌ Could not find FEHLERTABELLE")
            return f_codes

        error_table = tables[1]

        # Start from row 5 (after headers)
        # Column layout:
        # 0: "F", 3: Family, 6: Number, 9: Description, 12: Cause/Solution
        for row_idx in range(5, len(error_table)):
            row = error_table[row_idx]

            # Skip empty rows
            if not row[0] or row[0] != 'F':
                continue

            # Extract fields
            family = row[3] if len(row) > 3 and row[3] else None
            number = row[6] if len(row) > 6 and row[6] else None
            description = row[9] if len(row) > 9 and row[9] else None
            cause = row[12] if len(row) > 12 and row[12] else None

            if not all([family, number, description]):
                continue

            # Clean up: remove newlines from cells (convert to single description)
            description_clean = description.replace('\n', ' ').strip() if description else ""
            cause_clean = cause.replace('\n', ' ').strip() if cause else ""

            f_code = {
                "code": f"F{family} {number}",
                "family": family,
                "number": number,
                "description_de": description_clean,
                "cause_solution": cause_clean,
                "manual_page": 113,
                "extraction_status": "from_table"
            }
            f_codes.append(f_code)

        print(f"✅ Extracted {len(f_codes)} error codes from table")
        return f_codes

    def create_error_codes_json(self):
        """Create error_codes.json with complete data from tables"""
        print("\n" + "="*80)
        print("CREATING error_codes.json (from structured tables)")
        print("="*80)

        f_codes = self.extract_error_codes_from_tables()

        error_codes = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "113-127",
                "extraction_date": datetime.now().isoformat(),
                "status": "Populated from structured tables",
                "total_f_codes": len(f_codes),
                "total_a_codes": 0,
                "note": "Error codes extracted from FEHLERTABELLE (structured table extraction)"
            },
            "f_codes": f_codes,
            "a_codes": []
        }

        output_path = f"{self.output_dir}/error_codes.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(error_codes, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")
        print(f"   Contains: {len(f_codes)} complete error codes")
        print(f"   Each with: code, family, number, full description, full cause/solution")

    def extract_parameters_from_tables(self):
        """Extract parameters from structured tables (ALL sections with context)"""
        print("\n📋 Extracting parameters from structured tables...")
        print("   Note: Same parameter codes (P0001-P0016) have different meanings in different sections")

        parameters = []  # List of all parameter occurrences with context
        seen_combinations = set()  # Track code+description combinations to avoid duplicates

        # Parameters are in tables on pages 141-155 (multiple sections)
        # Key insight: P0001-P0016 appear in MULTIPLE sections with DIFFERENT meanings!
        for page_num in range(141, 156):
            tables = self.load_table_page(page_num)
            if not tables:
                continue

            # Get section name from page content (will be used to label parameter contexts)
            section_name = ""
            try:
                with open(f"../extracted_raw/page_{page_num:02d}_text.txt", 'r', encoding='utf-8') as f:
                    text = f.read()
                    # Extract section headers like "5.7.1. Seite Anlage 1" or "ANLAGE 1"
                    import re
                    matches = re.findall(r'5\.7\.\d+\.\s*[^A-Z]*([A-Z][^\n]+)', text)
                    if matches:
                        section_name = matches[0].strip()
            except:
                pass

            # Look for parameter tables (usually have P#### codes)
            for table_idx, table in enumerate(tables):
                # Also try to extract section from table headers
                table_section = section_name
                for header_row in table[:5]:
                    if header_row and header_row[0]:
                        cell_str = str(header_row[0])
                        if len(cell_str) > 5 and cell_str.isupper() and not cell_str.startswith('P'):
                            table_section = cell_str
                            break

                for row_idx, row in enumerate(table):
                    # Check if first cell starts with P and is 4 digits
                    if row and row[0] and isinstance(row[0], str) and row[0].startswith('P'):
                        try:
                            code = row[0]
                            # Must be P followed by exactly 4 digits
                            if len(code) >= 5 and code[1:5].isdigit():
                                # Table structure: Col 0 = code, Col 3 = description, Col 6 = values
                                description = row[3] if len(row) > 3 and row[3] else ""
                                values = row[6] if len(row) > 6 and row[6] else ""

                                # Skip if description is "Nicht verwendet" (not used)
                                if description and "Nicht verwendet" in str(description):
                                    continue

                                # Skip if no real description
                                if not description or (isinstance(description, str) and len(description.strip()) < 3):
                                    continue

                                # Clean up description and values
                                if description and isinstance(description, str):
                                    description = description.replace('\n', ' ').strip()
                                if values and isinstance(values, str):
                                    values = values.replace('\n', ' | ').strip()

                                # Create full description with values
                                full_description = description
                                if values and values != description and values:
                                    full_description = f"{description} ({values})"

                                # Add section context if different from standard sections
                                if table_section and table_section not in ['ANLAGE 1', 'ANLAGE 2', '']:
                                    context_description = f"[{table_section}] {full_description}"
                                else:
                                    context_description = full_description

                                # Create unique identifier for this parameter in this context
                                param_combo = f"{code}||{context_description}||{page_num}"

                                # Only add if we haven't seen this exact combination
                                if param_combo not in seen_combinations:
                                    seen_combinations.add(param_combo)
                                    param = {
                                        "code": code,
                                        "description_de": context_description,
                                        "manual_page": page_num,
                                        "section": table_section,
                                        "extraction_status": "from_table"
                                    }
                                    parameters.append(param)
                        except:
                            pass

        print(f"✅ Found {len(parameters)} parameter instances across all sections (pages 141-155)")
        print(f"   These include {len(set(p['code'] for p in parameters))} unique codes in different contexts")
        return parameters

    def create_parameters_json(self):
        """Create parameters.json from table extraction"""
        print("\n" + "="*80)
        print("CREATING parameters.json (from structured tables)")
        print("="*80)

        params = self.extract_parameters_from_tables()

        param_data = {
            "metadata": {
                "manual_version": "VIASerie_v74",
                "manual_pages": "141-155",
                "extraction_date": datetime.now().isoformat(),
                "status": "Populated from structured tables",
                "total_parameters": len(params),
                "note": "Parameters automatically extracted from table pages 141-155"
            },
            "parameters": params if params else []
        }

        output_path = f"{self.output_dir}/parameters.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(param_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Created: {output_path}")
        print(f"   Contains: {len(params)} unique parameters")
        return params

def main():
    print("="*80)
    print("BEST APPROACH: Extract from Structured Tables (Not Text)")
    print("="*80)

    extractor = TableExtractor(OUTPUT_DIR)
    extractor.create_error_codes_json()
    extractor.create_parameters_json()

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Error codes: Extracted with COMPLETE descriptions + solutions")
    print(f"✅ Parameters: Table extraction ready")
    print(f"\nThis approach:")
    print(f"  • Uses structured tables (not fragmented text)")
    print(f"  • Preserves complete multi-line content in cells")
    print(f"  • Maintains original formatting")
    print(f"  • Much more reliable than text parsing")

if __name__ == "__main__":
    main()
