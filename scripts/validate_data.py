#!/usr/bin/env python3
"""
Validate extracted JSON data
LIFTEC POC - Data Validation Tool
"""

import json
import os
from pathlib import Path

DATA_DIR = "../data/via/v74"

class DataValidator:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.validation_results = {}
        self.total_errors = 0

    def validate_json_file(self, filename):
        """Validate JSON file structure and content"""
        filepath = os.path.join(self.data_dir, filename)

        print(f"\n📋 Validating: {filename}")
        print("-" * 80)

        result = {
            "file": filename,
            "exists": False,
            "valid_json": False,
            "checks": {},
            "errors": []
        }

        # Check file exists
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            result["errors"].append("File not found")
            self.total_errors += 1
            return result

        result["exists"] = True

        # Try to load JSON
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Valid JSON")
            result["valid_json"] = True
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            result["errors"].append(f"Invalid JSON: {e}")
            self.total_errors += 1
            return result

        # File-specific validation
        if "error_codes" in filename:
            self._validate_error_codes(data, result)
        elif "parameters" in filename:
            self._validate_parameters(data, result)
        elif "hardware" in filename:
            self._validate_hardware(data, result)
        elif "contacts" in filename:
            self._validate_contacts(data, result)
        elif "connectors" in filename:
            self._validate_connectors(data, result)
        elif "quirks" in filename:
            self._validate_quirks(data, result)

        # Print results
        print(f"\nValidation results:")
        for check_name, (passed, message) in result["checks"].items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}: {message}")

        if result["errors"]:
            print(f"\nErrors found:")
            for error in result["errors"]:
                print(f"  ❌ {error}")
                self.total_errors += 1

        return result

    def _validate_error_codes(self, data, result):
        """Validate error_codes.json structure"""
        # Check metadata
        has_metadata = "metadata" in data
        result["checks"]["metadata"] = (has_metadata, "metadata section present" if has_metadata else "Missing metadata")

        # Check sections
        has_f_codes = "f_codes" in data and isinstance(data["f_codes"], list)
        result["checks"]["f_codes"] = (has_f_codes, f"{len(data.get('f_codes', []))} F-codes" if has_f_codes else "Missing f_codes")

        has_a_codes = "a_codes" in data and isinstance(data["a_codes"], list)
        result["checks"]["a_codes"] = (has_a_codes, f"{len(data.get('a_codes', []))} A-codes" if has_a_codes else "Missing a_codes")

        # Check first entry
        if has_f_codes and len(data["f_codes"]) > 0:
            first_code = data["f_codes"][0]
            required_fields = ["code", "family", "number", "description_de"]
            has_required_fields = all(field in first_code for field in required_fields)
            result["checks"]["required_fields"] = (has_required_fields, "All required fields present" if has_required_fields else "Missing required fields")

    def _validate_parameters(self, data, result):
        """Validate parameters.json structure"""
        has_metadata = "metadata" in data
        result["checks"]["metadata"] = (has_metadata, "metadata section present" if has_metadata else "Missing metadata")

        has_parameters = "parameters" in data and isinstance(data["parameters"], list)
        result["checks"]["parameters"] = (has_parameters, f"{len(data.get('parameters', []))} parameters" if has_parameters else "Missing parameters")

        if has_parameters and len(data["parameters"]) > 0:
            first_param = data["parameters"][0]
            required_fields = ["code", "name", "menu_path", "default_value"]
            has_required_fields = all(field in first_param for field in required_fields)
            result["checks"]["required_fields"] = (has_required_fields, "All required fields present" if has_required_fields else "Missing required fields")

    def _validate_hardware(self, data, result):
        """Validate hardware.json structure"""
        has_metadata = "metadata" in data
        result["checks"]["metadata"] = (has_metadata, "metadata section present" if has_metadata else "Missing metadata")

        has_boards = "boards" in data and isinstance(data["boards"], list)
        result["checks"]["boards"] = (has_boards, f"{len(data.get('boards', []))} boards" if has_boards else "Missing boards")

        if has_boards and len(data["boards"]) > 0:
            first_board = data["boards"][0]
            required_fields = ["name", "location", "function"]
            has_required_fields = all(field in first_board for field in required_fields)
            result["checks"]["required_fields"] = (has_required_fields, "All required fields present" if has_required_fields else "Missing required fields")

    def _validate_contacts(self, data, result):
        """Validate contacts.json structure"""
        has_metadata = "metadata" in data
        result["checks"]["metadata"] = (has_metadata, "metadata section present" if has_metadata else "Missing metadata")

        has_contacts = "contacts" in data and isinstance(data["contacts"], list)
        result["checks"]["contacts"] = (has_contacts, f"{len(data.get('contacts', []))} contacts" if has_contacts else "Missing contacts")

        if has_contacts and len(data["contacts"]) > 0:
            first_contact = data["contacts"][0]
            required_fields = ["code", "name", "location"]
            has_required_fields = all(field in first_contact for field in required_fields)
            result["checks"]["required_fields"] = (has_required_fields, "All required fields present" if has_required_fields else "Missing required fields")

    def _validate_connectors(self, data, result):
        """Validate connectors.json structure"""
        has_metadata = "metadata" in data
        result["checks"]["metadata"] = (has_metadata, "metadata section present" if has_metadata else "Missing metadata")

        has_connectors = "connectors" in data and isinstance(data["connectors"], list)
        result["checks"]["connectors"] = (has_connectors, f"{len(data.get('connectors', []))} connectors" if has_connectors else "Missing connectors")

        if has_connectors and len(data["connectors"]) > 0:
            first_conn = data["connectors"][0]
            required_fields = ["code", "board", "purpose"]
            has_required_fields = all(field in first_conn for field in required_fields)
            result["checks"]["required_fields"] = (has_required_fields, "All required fields present" if has_required_fields else "Missing required fields")

    def _validate_quirks(self, data, result):
        """Validate quirks.json structure"""
        has_metadata = "metadata" in data
        result["checks"]["metadata"] = (has_metadata, "metadata section present" if has_metadata else "Missing metadata")

        has_issues = "known_issues" in data and isinstance(data["known_issues"], list)
        result["checks"]["known_issues"] = (has_issues, f"{len(data.get('known_issues', []))} known issues" if has_issues else "Missing known_issues")

    def main(self):
        print("="*80)
        print("LIFTEC POC - DATA VALIDATION TOOL")
        print("="*80)
        print(f"\nValidating data in: {self.data_dir}\n")

        # List of files to validate
        files_to_validate = [
            "error_codes.json",
            "parameters.json",
            "hardware.json",
            "contacts.json",
            "connectors.json",
            "quirks.json"
        ]

        # Validate each file
        for filename in files_to_validate:
            result = self.validate_json_file(filename)
            self.validation_results[filename] = result

        # Print summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)

        valid_files = sum(1 for r in self.validation_results.values() if r["valid_json"])
        total_files = len(self.validation_results)

        print(f"\nFiles validated: {valid_files}/{total_files}")

        if self.total_errors == 0:
            print("✅ No errors found!")
        else:
            print(f"❌ Total errors: {self.total_errors}")

        print("\n" + "="*80)
        print("STATUS BY FILE")
        print("="*80)

        for filename, result in self.validation_results.items():
            if result["valid_json"]:
                status = "✅ PASS"
            elif result["exists"]:
                status = "⚠️  PARTIAL"
            else:
                status = "❌ FAIL"

            print(f"{status} - {filename}")

        print("\n" + "="*80)
        print("NEXT STEPS")
        print("="*80)
        print("1. Review extracted raw data in: extracted_raw/")
        print("2. For each JSON file, populate with actual data from PDF")
        print("3. Verify cross-references (e.g., error codes link to contacts)")
        print("4. Re-run this validation")
        print("5. Once all green ✅, ready for AI integration!")

        return self.total_errors == 0

def main():
    validator = DataValidator(DATA_DIR)
    success = validator.main()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
