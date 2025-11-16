"""
Enhance Knowledge Base - Integrate hardware and connectors into abbreviations
Merges hardware.json and connectors.json into the main abbreviations.json
"""

import json
from pathlib import Path


def enhance_abbreviations():
    """Merge hardware and connectors data into abbreviations"""

    data_dir = Path("../data/via/v74")

    print("📚 Enhancing Knowledge Base...")
    print("=" * 60)

    # Load existing abbreviations
    abbrev_file = data_dir / "abbreviations.json"
    with open(abbrev_file, 'r', encoding='utf-8') as f:
        abbrev_data = json.load(f)

    existing_abbrevs = abbrev_data.get('abbreviations', [])
    existing_codes = {a.get('code'): a for a in existing_abbrevs}

    print(f"📌 Existing abbreviations: {len(existing_abbrevs)}")

    # Load hardware.json
    hardware_file = data_dir / "hardware.json"
    if hardware_file.exists():
        with open(hardware_file, 'r', encoding='utf-8') as f:
            hardware_data = json.load(f)

        boards = hardware_data.get('boards', [])
        print(f"🖥️  Hardware boards found: {len(boards)}")

        for board in boards:
            name = board.get('name', '')
            # Try to extract code from name (e.g., "SMQ Board" -> "SMQ")
            code = name.split()[0] if name else None

            if code and code not in existing_codes:
                # Create abbreviation entry for hardware
                entry = {
                    "code": code,
                    "description_de": f"{name} - {board.get('function', 'Hardware component')}",
                    "location": board.get('location', ''),
                    "connectors": board.get('connectors', []),
                    "type": "hardware",
                    "extraction_status": board.get('extraction_status', 'merged')
                }
                existing_abbrevs.append(entry)
                existing_codes[code] = entry
                print(f"  ✅ Added: {code} - {name}")
            elif code:
                print(f"  ⏭️  Already exists: {code}")

    # Load connectors.json
    connectors_file = data_dir / "connectors.json"
    if connectors_file.exists():
        with open(connectors_file, 'r', encoding='utf-8') as f:
            connectors_data = json.load(f)

        connectors = connectors_data.get('connectors', [])
        print(f"\n🔌 Connectors found: {len(connectors)}")

        for connector in connectors:
            code = connector.get('code', '')
            if code and code not in existing_codes:
                # Create abbreviation entry for connector
                entry = {
                    "code": code,
                    "description_de": connector.get('description_de', connector.get('description', '')),
                    "type": "connector",
                    "board": connector.get('board', ''),
                    "pins": connector.get('pins', ''),
                    "extraction_status": connector.get('extraction_status', 'merged')
                }
                existing_abbrevs.append(entry)
                existing_codes[code] = entry
                print(f"  ✅ Added: {code}")
            elif code:
                print(f"  ⏭️  Already exists: {code}")

    # Update abbreviations.json
    abbrev_data['abbreviations'] = existing_abbrevs
    abbrev_data['metadata'] = {
        "total_entries": len(existing_abbrevs),
        "includes": ["original_abbreviations", "hardware_boards", "connectors"],
        "last_enhanced": "2025-11-16",
        "manual_version": "VIASerie_v74"
    }

    with open(abbrev_file, 'w', encoding='utf-8') as f:
        json.dump(abbrev_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"✅ Knowledge Base Enhanced!")
    print(f"📊 Total abbreviations now: {len(existing_abbrevs)}")
    print(f"💾 Saved to: {abbrev_file}")

    return existing_abbrevs


def verify_smq():
    """Verify SMQ is now findable"""
    data_dir = Path("../data/via/v74")
    abbrev_file = data_dir / "abbreviations.json"

    with open(abbrev_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    abbreviations = data.get('abbreviations', [])

    print("\n" + "=" * 60)
    print("🔍 Verification: Looking for SMQ...")
    print("=" * 60)

    smq = None
    for abbrev in abbreviations:
        if abbrev.get('code') == 'SMQ':
            smq = abbrev
            break

    if smq:
        print("\n✅ SMQ FOUND!")
        print(f"  Code: {smq.get('code')}")
        print(f"  Description: {smq.get('description_de')}")
        if smq.get('location'):
            print(f"  Location: {smq.get('location')}")
        if smq.get('function'):
            print(f"  Function: {smq.get('function')}")
        if smq.get('connectors'):
            print(f"  Connectors: {', '.join(smq.get('connectors'))}")
        return True
    else:
        print("\n❌ SMQ still not found")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting Knowledge Base Enhancement\n")

    # Enhance knowledge base
    enhance_abbreviations()

    # Verify SMQ
    verify_smq()

    print("\n✅ Done!")
