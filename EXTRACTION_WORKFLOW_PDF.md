# PDF EXTRACTION WORKFLOW
## From Via Manual PDF → Structured Knowledge Base

---

## PHASE 0: PREPARATION (30 minutes)

### Step 1: Identify Manual File

**Questions:**
- [ ] Which Via manual version? (v73, v74, v75?)
- [ ] How many pages total?
- [ ] Is it searchable PDF (text extractable) or image-based (scanned)?
- [ ] Where is the file located?

**Check if searchable:**
```bash
# Use pdftotext to test
pdftotext VIASerie_Kurzanleitung.pdf test.txt
# If this creates text, it's searchable
# If it creates garbage, it's image-based (needs OCR)
```

### Step 2: Set Up Workspace

```
project/
├── manuals/
│   ├── VIASerie_Kurzanleitung_v74.pdf
│   └── VIASerie_Handbuch_komplett_v74.pdf
├── extracted_raw/
│   ├── error_codes_raw.txt
│   ├── parameters_raw.txt
│   └── hardware_raw.txt
├── data/
│   ├── via/
│   │   └── v74/
│   │       ├── error_codes.json
│   │       ├── parameters.json
│   │       ├── hardware.json
│   │       ├── contacts.json
│   │       ├── connectors.json
│   │       └── quirks.json
│   └── extraction_manifest.json
└── scripts/
    ├── extract_pdf.py
    ├── validate_data.py
    └── organize_json.py
```

### Step 3: Install Tools

```bash
# For PDF extraction
pip install pdfplumber

# For data validation
pip install jsonschema

# For spreadsheet → JSON
pip install pandas

# Optional: For better table extraction
pip install camelot-py
```

---

## PHASE 1: RAPID EXTRACTION (2-3 hours)

### Method 1: Table-Based (Fastest for structured data)

**Best for:** Error codes, parameters, contacts (all table format in manual)

**Step 1: Extract all tables from PDF**

```python
import pdfplumber
import json

pdf_path = "VIASerie_Kurzanleitung_v74.pdf"

extracted_data = {
    "error_codes": [],
    "a_codes": [],
    "parameters": [],
    "contacts": []
}

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        tables = page.extract_tables()

        if tables:
            print(f"Page {page_num}: Found {len(tables)} table(s)")

            for table_num, table in enumerate(tables):
                # Save raw table
                print(f"  Table {table_num}:")
                for row in table[:3]:  # Print first 3 rows
                    print(f"    {row}")

# Output: All tables extracted with page numbers
```

**Output will show:** Which page has which table

**Step 2: Convert tables to JSON**

```python
import pandas as pd
import json

# For each table that looks like error codes:
error_code_table = [
    ['Code', 'Family', 'Number', 'Description'],
    ['F03 55', '03', '55', 'Türkreis öffnet nicht...'],
    ['F03 56', '03', '56', 'MPC Zusatzkontakt...'],
]

# Convert to JSON
error_codes = []
for row in error_code_table[1:]:  # Skip header
    error_codes.append({
        "code": row[0],
        "family": row[1],
        "number": row[2],
        "description_de": row[3],
        "manual_page": 7  # Add manually
    })

with open('data/via/v74/error_codes.json', 'w', encoding='utf-8') as f:
    json.dump(error_codes, f, ensure_ascii=False, indent=2)
```

### Method 2: Text-Based (For unstructured content)

**Best for:** Component descriptions, procedures, hardware locations

**Step 1: Extract text by page**

```python
import pdfplumber

pdf_path = "VIASerie_Kurzanleitung_v74.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")

    # Save each page as text for manual review
    for page_num, page in enumerate(pdf.pages, 1):
        text = page.extract_text()

        # Save to file
        with open(f'extracted_raw/page_{page_num:02d}.txt', 'w', encoding='utf-8') as f:
            f.write(f"=== PAGE {page_num} ===\n")
            f.write(text)

        # Also print first 500 chars to console
        print(f"Page {page_num}:")
        print(text[:500])
        print("-" * 80)
```

**Output:** Separate text file for each page (easy to search & verify)

**Step 2: Parse text to extract specific sections**

```python
def extract_hardware_section(text):
    """Extract CAB Board info from text"""
    if "CAB Board" in text or "CAB-Board" in text:
        # Find section boundaries
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if "CAB Board" in line:
                # Extract next 10 lines (adjust as needed)
                section = '\n'.join(lines[i:i+10])
                return section
    return None

# Use on extracted text
for page_num in range(1, 18):  # All 17 pages
    with open(f'extracted_raw/page_{page_num:02d}.txt', 'r') as f:
        text = f.read()

    hardware_info = extract_hardware_section(text)
    if hardware_info:
        print(f"Found on page {page_num}:")
        print(hardware_info)
```

### Method 3: Hybrid (Recommended)

**Step 1: Extract tables (structured)**

```python
# Run extraction script for tables
# Output: error_codes.json, parameters.json, contacts.json
```

**Step 2: Extract text (unstructured)**

```python
# Run extraction script for text
# Output: page_01.txt, page_02.txt, ... page_17.txt
```

**Step 3: Manual review + cleanup**

```
For each JSON file:
├─ Open in text editor
├─ Check first 5 entries
├─ Verify format consistency
├─ Fix any OCR errors
└─ Save clean version

For text files:
├─ Search for key sections (CAB Board, LED meanings, etc.)
├─ Copy relevant parts to structured format
├─ Verify against manual
└─ Delete temporary files
```

---

## PHASE 2: STRUCTURED ORGANIZATION (1-2 hours)

### Step 1: Create Error Codes JSON

```python
# Input: error_codes table extracted from PDF

error_codes_data = {
    "metadata": {
        "manual_version": "VIASerie_v74",
        "manual_pages": "7-9",
        "extraction_date": "2025-11-16",
        "total_codes": 0
    },
    "f_codes": [],
    "a_codes": []
}

# F-CODES (from pages 7-9)
f_codes = [
    {
        "code": "F03 55",
        "family": "03",
        "number": "55",
        "description_de": "Öffnet den Türkreis nicht beim der ersten Fahrt nach dem Einschalten oder von INS auf NORM",
        "family_name": "Türsystem",
        "manual_page": 7,
        "extraction_status": "verified",
        "notes": "Betroffene Kontakte: 7H, 8H"
    },
    {
        "code": "F03 56",
        "family": "03",
        "number": "56",
        "description_de": "MPC Zusatzkontakt offen",
        "family_name": "Türsystem",
        "manual_page": 7,
        "extraction_status": "verified",
        "notes": ""
    }
    # ... more codes
]

# A-CODES (from page 6)
a_codes = [
    {
        "code": "A07",
        "description_de": "Fotozelle unterbrochen",
        "manual_page": 6,
        "extraction_status": "verified"
    }
    # ... more codes
]

error_codes_data["f_codes"] = f_codes
error_codes_data["a_codes"] = a_codes
error_codes_data["metadata"]["total_codes"] = len(f_codes) + len(a_codes)

# Save
with open('data/via/v74/error_codes.json', 'w', encoding='utf-8') as f:
    json.dump(error_codes_data, f, ensure_ascii=False, indent=2)
```

**Verification:**
```bash
# Check JSON validity
python -m json.tool data/via/v74/error_codes.json > /dev/null && echo "✓ Valid JSON"

# Count entries
python -c "import json; f=open('data/via/v74/error_codes.json'); d=json.load(f); print(f\"F-codes: {len(d['f_codes'])}\nA-codes: {len(d['a_codes'])}\")"
```

### Step 2: Create Parameters JSON

```python
# Input: Parameters table (pages 13-14)

parameters_data = {
    "metadata": {
        "manual_version": "VIASerie_v74",
        "manual_pages": "13-14",
        "extraction_date": "2025-11-16",
        "total_parameters": 0
    },
    "parameters": [
        {
            "code": "P0005",
            "name": "Temperatur-Schwelle Maschinenraum",
            "name_en": "Machine Room Temperature Threshold",
            "function": "Maximale Temperatur bevor F12 46 ausgelöst wird",
            "menu_path": "Setup → Prog → PProt → P0005",
            "default_value": "60",
            "range_min": "40",
            "range_max": "80",
            "unit": "°C",
            "related_errors": ["F12 46", "A03"],
            "manual_page": 13,
            "extraction_status": "verified",
            "field_notes": "Häufig zu niedrig kalibriert → Falschauslösung"
        }
        # ... more parameters
    ]
}

# Save and verify
with open('data/via/v74/parameters.json', 'w', encoding='utf-8') as f:
    json.dump(parameters_data, f, ensure_ascii=False, indent=2)
```

### Step 3: Create Hardware JSON

```python
# Input: Hardware descriptions (pages 10-12)

hardware_data = {
    "metadata": {
        "manual_version": "VIASerie_v74",
        "manual_pages": "10-12",
        "extraction_date": "2025-11-16"
    },
    "boards": [
        {
            "name": "SMQ Board",
            "name_de": "Steuerplatinenmodul",
            "location": "Schaltschrank (Maschinenraum)",
            "function": "Hauptsteuerung, Sicherheitskreis-Verarbeitung",
            "connectors": ["XSSC", "XSSH2", "XSM1", "XSM2", "XFOT"],
            "led_groups": [
                {
                    "group": "A",
                    "leds": ["K.O.", "OK", "MODE"],
                    "purpose": "Grundstatus"
                },
                {
                    "group": "D",
                    "leds": ["1H", "2H", "7H", "8H", "9H", "3C"],
                    "purpose": "Sicherheitskreis-Kontakte"
                }
            ],
            "manual_page": 10,
            "extraction_status": "verified"
        },
        {
            "name": "CAB Board",
            "name_de": "Fahrkorbsteuerung",
            "location": "Fahrkabine (Decke/Wand)",
            "function": "Türsteuerung, CAN-Bus Kommunikation",
            "connectors": ["XFOT1", "XCABUS", "XOP1", "XOP2"],
            "led_groups": [
                {
                    "group": "F",
                    "leds": ["MAC BUS OP", "MAC BUS EXT", "CAN BUS SM"],
                    "purpose": "Kommunikation"
                }
            ],
            "common_failures": "Bus-Signal-Verarbeitung fehlerhaft (sporadische Türprobleme)",
            "failure_frequency_via": 0.40,
            "manual_page": 11,
            "extraction_status": "verified"
        }
        # ... more boards
    ]
}

with open('data/via/v74/hardware.json', 'w', encoding='utf-8') as f:
    json.dump(hardware_data, f, ensure_ascii=False, indent=2)
```

### Step 4: Create Contacts JSON

```python
# Input: Safety circuit diagram (pages 3-4)

contacts_data = {
    "metadata": {
        "manual_version": "VIASerie_v74",
        "extraction_date": "2025-11-16"
    },
    "contacts": [
        {
            "code": "7H",
            "name": "Schachttür Kontakt",
            "name_en": "Shaft Door Contact",
            "location": "An jeder Schachttür",
            "monitors": "Ob Schachttür geschlossen",
            "normal_state": "GESCHLOSSEN (wenn sicher)",
            "smd_led_group": "D",
            "smd_led_number": "7",
            "connector": "XSSH2",
            "pin": "1",
            "voltage": "110V AC",
            "failure_consequences": [
                "Offen → Lift startet nicht (Sicherheitskreis unterbrochen)",
                "Hängt → Sporadic failures"
            ],
            "test_procedure": "Tür öffnen → LED OFF, Tür zu → LED ON",
            "manual_page": "3-4",
            "extraction_status": "verified"
        }
        # ... more contacts
    ]
}

with open('data/via/v74/contacts.json', 'w', encoding='utf-8') as f:
    json.dump(contacts_data, f, ensure_ascii=False, indent=2)
```

### Step 5: Create Connectors JSON

```python
# Input: Wiring diagram (page 12)

connectors_data = {
    "metadata": {
        "manual_version": "VIASerie_v74",
        "manual_page": 12,
        "extraction_date": "2025-11-16"
    },
    "connectors": [
        {
            "code": "XSSH2",
            "board": "SMQ",
            "name": "Safety Contact Connector",
            "purpose": "Türkontakte und Sicherheitskontakte",
            "pins": [
                {
                    "pin": 1,
                    "signal": "7H",
                    "signal_name": "Schachttür",
                    "voltage": "110V AC"
                },
                {
                    "pin": 2,
                    "signal": "8H",
                    "signal_name": "Kabinentür",
                    "voltage": "110V AC"
                },
                {
                    "pin": 3,
                    "signal": "9H",
                    "signal_name": "Türverriegelung",
                    "voltage": "110V AC"
                },
                {
                    "pin": 4,
                    "signal": "GND",
                    "signal_name": "Masse",
                    "voltage": "0V"
                }
            ],
            "common_issues": ["Loose connector", "Oxidized pins", "High resistance"],
            "extraction_status": "verified"
        }
        # ... more connectors
    ]
}

with open('data/via/v74/connectors.json', 'w', encoding='utf-8') as f:
    json.dump(connectors_data, f, ensure_ascii=False, indent=2)
```

---

## PHASE 3: MANUAL REVIEW & VERIFICATION (1 hour)

### Verification Script

```python
import json
import os

def verify_extraction(data_dir="data/via/v74"):
    """Verify all extracted data"""

    print("=" * 80)
    print("EXTRACTION VERIFICATION REPORT")
    print("=" * 80)

    files_to_check = [
        'error_codes.json',
        'parameters.json',
        'hardware.json',
        'contacts.json',
        'connectors.json'
    ]

    for filename in files_to_check:
        filepath = os.path.join(data_dir, filename)

        if not os.path.exists(filepath):
            print(f"❌ {filename}: NOT FOUND")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)

                # Count entries
                if 'f_codes' in data:
                    f_count = len(data['f_codes'])
                    a_count = len(data['a_codes'])
                    print(f"✅ {filename}: {f_count} F-codes + {a_count} A-codes")
                elif 'parameters' in data:
                    count = len(data['parameters'])
                    print(f"✅ {filename}: {count} parameters")
                elif 'boards' in data:
                    count = len(data['boards'])
                    print(f"✅ {filename}: {count} boards")
                elif 'contacts' in data:
                    count = len(data['contacts'])
                    print(f"✅ {filename}: {count} contacts")
                elif 'connectors' in data:
                    count = len(data['connectors'])
                    print(f"✅ {filename}: {count} connectors")
                else:
                    print(f"⚠️  {filename}: Unknown structure")

            except json.JSONDecodeError as e:
                print(f"❌ {filename}: INVALID JSON - {e}")

    print("=" * 80)

# Run verification
verify_extraction()
```

**Run verification:**
```bash
python scripts/verify_extraction.py
```

**Expected output:**
```
================================================================================
EXTRACTION VERIFICATION REPORT
================================================================================
✅ error_codes.json: 87 F-codes + 12 A-codes
✅ parameters.json: 42 parameters
✅ hardware.json: 8 boards
✅ contacts.json: 15 contacts
✅ connectors.json: 6 connectors
================================================================================
```

### Manual Spot-Check

**Check 5 random entries from each file:**

```
error_codes.json - F03 55:
  ✓ Code matches manual page 7
  ✓ Description matches
  ✓ Affected contacts (7H, 8H) noted
  → PASS

parameters.json - P0005:
  ✓ Default value 60°C correct
  ✓ Range 40-80 correct
  ✓ Menu path verified
  → PASS

hardware.json - CAB Board:
  ✓ Location "Fahrkabine" correct
  ✓ Connectors listed
  ✓ LED groups match manual
  → PASS
```

---

## PHASE 4: ENRICHMENT (1-2 hours)

### Add Manual Knowledge (Not in PDF)

```python
import json

# Load error_codes
with open('data/via/v74/error_codes.json', 'r') as f:
    data = json.load(f)

# Add field knowledge to specific codes
for code in data['f_codes']:
    if code['code'] == 'F03 55':
        code['typical_causes'] = [
            {
                "cause": "CAB Board Bus-Signal defekt",
                "frequency": 0.40,
                "indicator": "sporadisch",
                "via_specific": True
            },
            {
                "cause": "Mechanik blockiert",
                "frequency": 0.35,
                "indicator": "konstant"
            },
            {
                "cause": "Door Operator defekt",
                "frequency": 0.15,
                "indicator": "Motor läuft nicht"
            },
            {
                "cause": "Kontakte 7H/8H verstellt",
                "frequency": 0.10,
                "indicator": "Tür bewegt sich, aber kein Signal"
            }
        ]
        code['first_check'] = "Ist das Problem sporadisch oder konstant?"

# Save enriched data
with open('data/via/v74/error_codes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Enriched error_codes.json with field knowledge")
```

### Create Quirks Database

```python
# Create via/v74/quirks.json

quirks_data = {
    "metadata": {
        "manual_version": "VIASerie_v74",
        "source": "manual + field_knowledge",
        "extraction_date": "2025-11-16"
    },
    "known_issues": [
        {
            "component": "CAB Board",
            "problem": "Bus-Signal-Verarbeitung fehlerhaft",
            "symptoms": [
                "Türen öffnen/schließen manchmal nicht (sporadisch)",
                "A07 Falschmeldung (Fotozelle OK aber Fehler)",
                "Tür reagiert zeitweise nicht auf Befehle"
            ],
            "affected_codes": ["F03 55", "F03 56", "A07"],
            "frequency_via": 0.40,
            "frequency_note": "~40% aller Türprobleme bei Via",
            "detection_method": "Sporadisch + CAB LED unregelmäßig",
            "solution": "CAB Board austauschen",
            "solution_difficulty": "medium",
            "solution_time_minutes": 35
        },
        {
            "component": "Software v74DEEN",
            "problem": "Türen zucken, unstabile Bewegungen",
            "symptoms": ["Türe öffnet ruckartig", "A07 intermittierend"],
            "affected_codes": ["A07", "F03"],
            "frequency_via": 0.05,
            "frequency_note": "Bekannter Bug in dieser Version",
            "solution": "Software Update auf v75+",
            "solution_difficulty": "medium",
            "solution_time_minutes": 20
        }
    ]
}

with open('data/via/v74/quirks.json', 'w', encoding='utf-8') as f:
    json.dump(quirks_data, f, ensure_ascii=False, indent=2)

print("✅ Created quirks.json with known issues")
```

---

## PHASE 5: CREATE MANIFEST (15 minutes)

```python
import json
from datetime import datetime

manifest = {
    "project": "LIFTEC POC",
    "manual_version": "VIASerie_v74",
    "extraction_date": datetime.now().isoformat(),
    "extracted_by": "Daniel",
    "files_extracted": {
        "error_codes.json": {
            "f_codes": 87,
            "a_codes": 12,
            "status": "verified",
            "completeness": "100%"
        },
        "parameters.json": {
            "parameters": 42,
            "status": "verified",
            "completeness": "100%"
        },
        "hardware.json": {
            "boards": 8,
            "status": "verified",
            "completeness": "95%"
        },
        "contacts.json": {
            "contacts": 15,
            "status": "verified",
            "completeness": "100%"
        },
        "connectors.json": {
            "connectors": 6,
            "status": "verified",
            "completeness": "85%"
        },
        "quirks.json": {
            "known_issues": 5,
            "status": "in_progress",
            "completeness": "60%",
            "notes": "More field knowledge to add"
        }
    },
    "next_steps": [
        "Test QA system with sample questions",
        "Create diagnostic flowcharts",
        "Add feedback loop integration",
        "Test with real technician"
    ]
}

with open('data/extraction_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("✅ Created extraction_manifest.json")
```

---

## QUICK REFERENCE: Command Line Workflow

```bash
# 1. Extract tables from PDF
python scripts/extract_pdf.py

# 2. Verify JSON validity
python -m json.tool data/via/v74/*.json

# 3. Count entries
for file in data/via/v74/*.json; do
    echo "$(basename $file): $(python -c "import json; print(len(json.load(open('$file'))))")"
done

# 4. Run verification report
python scripts/verify_extraction.py

# 5. Create manifest
python scripts/create_manifest.py

# 6. Commit to git
git add data/via/v74/
git commit -m "Extract Via v74 manual - error codes, parameters, hardware"
git tag extraction-v74-2025-11-16
```

---

## TIME ESTIMATES

| Phase | Task | Time |
|-------|------|------|
| 0 | Prepare workspace & tools | 30 min |
| 1 | Extract tables from PDF | 30 min |
| 1 | Convert tables to JSON | 30 min |
| 1 | Extract text sections | 30 min |
| 2 | Create error_codes.json | 20 min |
| 2 | Create parameters.json | 15 min |
| 2 | Create hardware.json | 15 min |
| 2 | Create contacts.json | 15 min |
| 2 | Create connectors.json | 15 min |
| 3 | Manual review & verification | 60 min |
| 4 | Add field knowledge & quirks | 60 min |
| 5 | Create manifest | 15 min |
| **TOTAL** | | **~5.5 hours** |

---

## SUCCESS CRITERIA

After completing this workflow:

✅ All tables extracted from PDF
✅ All data in valid JSON format
✅ All files pass JSON validation
✅ Manual spot-check: 5/5 samples correct
✅ Extraction manifest created & filed
✅ Ready for AI integration testing

---

## NEXT: AI Integration

Once extraction is complete, you'll have:
- ✅ Structured knowledge base (JSON files)
- ✅ Fast lookup capability
- ✅ Version control setup
- ✅ Manifest of what's been done

Then we can move to:
1. **AI Integration** - How the model uses this data
2. **Prompt Engineering** - What to tell the AI
3. **Testing** - Verify it answers questions correctly
