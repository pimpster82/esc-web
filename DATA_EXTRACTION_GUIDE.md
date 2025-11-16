# DATA EXTRACTION & ORGANIZATION GUIDE
## How to Extract Via Manual and Build Knowledge Base

---

## OVERVIEW: Three Extraction Levels

```
LEVEL 1: FACTUAL EXTRACTION (High confidence, mechanical)
├─ Error codes with definitions
├─ Parameter lists
├─ Component locations
└─ LED meanings
→ Straightforward data mining from manual

LEVEL 2: RELATIONAL EXTRACTION (Medium confidence, requires analysis)
├─ Which codes are related?
├─ What affects what?
├─ Signal flow connections
└─ Cause-effect chains
→ Requires reading & understanding manual

LEVEL 3: KNOWLEDGE SYNTHESIS (Lower confidence, requires expertise)
├─ Known problem frequencies (CAB Board 40%)
├─ Typical troubleshooting sequences
├─ Edge cases and exceptions
└─ Safety considerations
→ Requires domain expertise + manual + field knowledge
```

---

## PART 1: WHAT DATA TO EXTRACT

### 1.1 ERROR CODES (F-Codes)

**Source:** Via Manual, pages with error code tables

**What to extract:**

```
For EACH F-code:
├─ Code (e.g., "F03 55")
├─ Family (e.g., "03")
├─ Number (e.g., "55")
├─ Description (German from manual)
├─ English translation (if not in manual)
├─ Affected components (e.g., "7H, 8H")
├─ Related parameters (e.g., "P0005")
├─ Manual page reference
├─ Typical cause(s)
│  ├─ Mechanical
│  ├─ Electrical
│  └─ Electronic/Software
└─ Suggested first check
```

**Example:**

```
F03 55
├─ Family: 03 (Door System)
├─ Description: "Öffnet den Türkreis nicht beim der ersten Fahrt nach dem Einschalten oder von INS auf NORM"
├─ Translation: "Does not open door circuit on first drive after power-on or switching from INS to NORM"
├─ Affected components: 7H (shaft door), 8H (cabin door)
├─ Related parameters: P0014 (door timing)
├─ Manual page: 7
├─ Typical causes:
│  ├─ CAB Board defect (40% - sporadisch)
│  ├─ Mechanical blockage (35% - konstant)
│  ├─ Door Operator failure (15% - no sound)
│  └─ Contact defect 7H/8H (10% - moves but doesn't register)
└─ First check: Is problem constant or sporadic?
```

### 1.2 A-CODES (Prevent Start Codes)

**Source:** Via Manual, A-code table

**What to extract:**

```
For EACH A-code:
├─ Code (e.g., "A07")
├─ Description
├─ What it blocks (prevents start)
├─ Trigger condition
├─ Normal causes
├─ How to clear it
└─ Related safety contact
```

**Example:**

```
A07
├─ Description: "Fotozelle unterbrochen"
├─ Blocks: Lift cannot close doors/start
├─ Trigger: XFOT1 input open
├─ Normal causes:
│  ├─ Person/object in door
│  ├─ Fotozelle verstellt
│  ├─ Fotozelle verschmutzt
│  └─ CAB Board not communicating
├─ Clear when: Trigger gone, then reset
└─ Related contact: XFOT1 on CAB Board
```

### 1.3 PARAMETERS (P-Codes)

**Source:** Via Manual, Setup/Prog section

**What to extract:**

```
For EACH Parameter:
├─ Code (e.g., "P0005")
├─ Name
├─ Function/Description
├─ Menu path (Setup → Prog → ?)
├─ Default value
├─ Possible range
├─ Unit of measurement
├─ Related error codes
├─ When to change it
└─ Common adjustment values
```

**Example:**

```
P0005
├─ Name: "Temperature Threshold - Machine Room"
├─ Function: "Maximum allowed machine room temperature before F12 46 triggers"
├─ Menu path: Setup → Prog → PProt → P0005
├─ Default value: 60°C
├─ Range: 40°C to 80°C
├─ Unit: °C
├─ Related errors: F12 46, A03
├─ When to change: Frequent false alarms, unequal sensor
├─ Common adjustments: 65-70°C (if sensor miscalibrated)
```

### 1.4 HARDWARE COMPONENTS & LOCATIONS

**Source:** Via Manual, hardware diagrams, board photos

**What to extract:**

```
For EACH Component:
├─ Name (e.g., "CAB Board")
├─ Location in system
│  ├─ Physical location (Kabine, Schrank, Schacht)
│  ├─ Mounting details
│  └─ How to access
├─ Function/Purpose
├─ Connections
│  ├─ Input connectors
│  ├─ Output connectors
│  └─ Power requirements
├─ LED indicators
│  ├─ LED group name
│  ├─ What each LED means
│  ├─ Normal state (ON/OFF/Blinking)
│  └─ Error state
├─ Common failure modes
└─ Replacement procedure notes
```

**Example:**

```
CAB Board (Cabin Control Board)
├─ Location:
│  ├─ Physical: Inside cabin (usually ceiling/wall)
│  ├─ Access: Open cabin panel
│  └─ Recognition: Platine with 3 LED groups
├─ Function: Processes door commands, communicates via CAN bus
├─ Connections:
│  ├─ XFOT1 (Fotocell)
│  ├─ XCABUS (CAN communication to SMQ)
│  ├─ XOP1/XOP2 (Door Operator)
│  └─ 24V power
├─ LED Groups (Group F):
│  ├─ LED 1: MAC BUS OP (communication)
│  │  ├─ Normal: Blinking regularly
│  │  └─ Error: Not blinking or irregular
│  ├─ LED 2: MAC BUS EXT (cabin buttons)
│  └─ LED 3: CAN BUS SM (sensor communication)
├─ Failure modes:
│  ├─ Sporadische Türprobleme
│  ├─ A07 error (false photocell signal)
│  └─ Door doesn't respond to commands
└─ Replacement notes: 30-45 min, requires re-commissioning
```

### 1.5 SAFETY CONTACTS (1H-9H, nC, nS)

**Source:** Via Manual, safety circuit diagrams

**What to extract:**

```
For EACH Contact:
├─ Contact designation (e.g., "7H")
├─ Full name
├─ Physical location
├─ What it monitors
├─ Normal state (open/closed when safe)
├─ LED indicator on SMQ Board
├─ Connector location (e.g., XSSH2)
├─ Failure consequences
└─ How to verify/test
```

**Example:**

```
7H - Schachttür Kontakt
├─ Full name: Shaft Door Contact
├─ Location: At each shaft door entrance
├─ Monitors: Whether shaft door is closed
├─ Normal state: CLOSED when safe (7H conducts)
├─ SMQ LED: Group D, LED 7H
│  ├─ ON (lit) = Contact closed = Door OK
│  └─ OFF (dark) = Contact open = Door open!
├─ Connector: XSSH2 pin 7H
├─ Failure consequences:
│  ├─ If stuck OPEN → Lift won't start (A-code or 7H LED off)
│  ├─ If stuck CLOSED → Lift can't detect open door (safety issue)
│  └─ If intermittent → Sporadic start failures
└─ Test procedure:
   ├─ Open door physically → LED should go OFF
   ├─ Close door physically → LED should go ON
   ├─ If not → Contact or wiring problem
```

### 1.6 CONNECTORS & WIRING

**Source:** Via Manual, wiring diagrams

**What to extract:**

```
For EACH Connector:
├─ Connector code (e.g., "XSSH2")
├─ Board it connects to
├─ Pins/connections
│  ├─ Pin number
│  ├─ Signal name
│  ├─ Source
│  └─ Destination
├─ Voltage levels
├─ Wire colors (if specified)
└─ Common issues
```

**Example:**

```
XSSH2 - Safety Contact Connector (SMQ Board)
├─ Board: SMQ (Hauptsteuerung)
├─ Pins:
│  ├─ Pin 1: 7H (Shaft door) - Input 110V
│  ├─ Pin 2: 8H (Cabin door) - Input 110V
│  ├─ Pin 3: 9H (Door lock) - Input 110V
│  ├─ Pin 4: GND
│  └─ Pin 5: GND
├─ Voltage: 110V AC (safety circuit)
├─ Common issues:
│  ├─ Loose connector → Intermittent failures
│  ├─ Oxidized pins → High resistance
│  └─ Wrong pin → Component not detected
```

### 1.7 CONSOLE NAVIGATION

**Source:** Via Manual, console guide section

**What to extract:**

```
For key procedures:
├─ Goal (what to do)
├─ Starting point (where you are)
├─ Step-by-step path
│  ├─ Which button/menu
│  ├─ Expected display response
│  └─ Timeout/wait times
├─ Common mistakes
└─ Exit/cancel method
```

**Example:**

```
PROCEDURE: Read Error Codes
├─ Goal: See list of stored errors
├─ Starting point: Normal operation (display shows position)
├─ Steps:
│  1. Press FUN → Display: "Function Menu"
│  2. Press ERROR (or Taste 3) → Display: "Error List"
│  3. Use ▲▼ to scroll → Shows errors one by one
│  4. Press ERROR & hold → Shows date/time of error
│  5. Press BACK → Return to normal display
├─ Display format:
│  ├─ Line 1: "01 F 03" (Error #1, F-family, code 03)
│  ├─ Line 2: "01 c 55" (Same, showing full code F03 55)
│  ├─ Line 3: "F 15 11" (Date: Nov 15)
│  └─ Line 4: "H 14 30" (Time: 14:30)
├─ Common mistakes:
│  ├─ Using wrong button
│  ├─ Not understanding 2-line display format
│  └─ Missing hold action for details
└─ Exit: Press BACK or SETUP
```

---

## PART 2: HOW TO EXTRACT (Methodology)

### Step 1: Prepare the Manual

**If you have PDF:**
- Use PDF extraction tool (PDFMiner, pdfplumber, or Adobe)
- Extract text preserving structure
- Manually verify extracted tables
- Note page numbers for reference

**If you have physical manual:**
- Scan pages to PDF
- OCR to text
- Manually correct OCR errors
- Add page references

**If data already exists (spreadsheets):**
- Export as CSV
- Validate all fields present
- Add missing metadata

### Step 2: Create Extraction Template

For each data type, use a structured form:

**Error Code Template:**
```
CODE: F03 55
FAMILY: 03
NUMBER: 55
DESCRIPTION_DE: [copy from manual]
DESCRIPTION_EN: [translate or find]
AFFECTED_CONTACTS: [list]
RELATED_PARAMETERS: [list]
MANUAL_PAGE: [number]
MECHANICAL_CAUSE: [yes/no/typical]
ELECTRICAL_CAUSE: [yes/no/typical]
ELECTRONIC_CAUSE: [yes/no/typical]
FREQUENCY_VIA: [estimate or feedback]
FIRST_CHECK: [key diagnostic step]
NOTES: [any special info]
STATUS: [extracted/verified/complete]
```

### Step 3: Source Control & Versioning

```
data/
├── via/
│   ├── v74/                          ← Version specific!
│   │   ├── error_codes_F03.csv
│   │   ├── error_codes_F12.csv
│   │   ├── error_codes_A_codes.csv
│   │   ├── parameters.csv
│   │   ├── hardware.csv
│   │   ├── contacts.csv
│   │   ├── connectors.csv
│   │   └── console_procedures.csv
│   ├── v75/                          ← Different version if exists
│   └── extraction_manifest.json      ← What was extracted when
│
└── extraction_manifest.json
    {
      "manual_version": "VIASerie_v74",
      "manual_pages_total": 17,
      "extraction_date": "2025-11-16",
      "extracted_by": "Daniel",
      "completeness": {
        "error_codes": "100% (87 codes)",
        "parameters": "100% (42 params)",
        "hardware": "95% (2 boards TBD)",
        "contacts": "100% (all safety contacts)",
        "connectors": "85% (need wiring detail)"
      },
      "validation_status": "in_progress",
      "notes": "CAB Board details extracted, need LED mapping verification"
    }
```

### Step 4: Data Validation Checklist

For each extracted item, verify:

- [ ] All codes actually exist in manual (no invented codes)
- [ ] Descriptions match manual exactly (or note translation)
- [ ] Page references are correct
- [ ] Related items are actually related
- [ ] No duplicate entries
- [ ] All required fields populated
- [ ] No sensitive/dangerous information removed
- [ ] Cross-references check out

**Validation Example:**

```
F03 55 extraction:
✓ Code exists in manual page 7
✓ Description matches "Öffnet den Türkreis nicht..."
✓ Related contacts 7H, 8H verified in safety diagram
✓ Related parameter P0014 checked (exists, timing parameter)
✓ Not a duplicate (no other F03 55)
✓ All fields populated except frequency (will come from feedback)
✓ No dangerous info (all safety-relevant)
✓ Cross-check: F03 56 (similar code) also extracted
```

---

## PART 3: WHAT TO DO WITH EXTRACTED DATA

### Layer 1: Static Truth (Database/JSON)

**File structure:**
```
via/v74/error_codes.json
{
  "F-codes": [
    {
      "code": "F03 55",
      "family": "03",
      "number": "55",
      "description_de": "Öffnet den Türkreis nicht...",
      "description_en": "Does not open door circuit...",
      "affected_contacts": ["7H", "8H"],
      "related_parameters": ["P0014"],
      "manual_page": 7,
      "extracted_date": "2025-11-16",
      "validation_status": "verified"
    }
  ]
}
```

**Advantages:**
- Fast lookup by code
- Queryable (SQL or JSON)
- Version controlled
- Easy to update

### Layer 2: Model Quirks (Structured Knowledge)

**File structure:**
```
via/v74/quirks.json
{
  "known_issues": [
    {
      "component": "CAB Board",
      "problem": "Bus signal processing failure",
      "symptoms": ["sporadisch Türprobleme", "A07 false positive"],
      "error_codes": ["F03 55", "F03 56", "A07"],
      "frequency_via": 0.40,
      "frequency_note": "40% of door failures on Via (from field data)",
      "detection_method": "LED irregular + sporadic symptom",
      "solution": "Replace CAB Board",
      "solution_difficulty": "medium",
      "solution_duration_minutes": 35,
      "source": "manual_quirks + field_feedback",
      "confidence": "high"
    }
  ]
}
```

### Layer 3: Diagnostic Flows (Decision Trees)

**File structure:**
```
via/v74/diagnostic_flows.json
{
  "door_wont_open": {
    "name": "Tür öffnet nicht",
    "entry_symptoms": ["Türe bewegt sich nicht", "Türe reagiert nicht"],
    "first_question": "Ist das Problem konstant oder sporadisch?",
    "branches": [
      {
        "condition": "sporadisch",
        "confidence": 0.40,
        "suspect": "CAB Board",
        "next_check": "CAB Board LED Status (Group F)",
        "led_indicator": "MAC BUS OP LED irregular"
      },
      {
        "condition": "konstant",
        "confidence": 0.35,
        "suspect": "Mechanik blockiert",
        "next_check": "Von Hand bewegen",
        "next_question": "Lässt sich die Tür von Hand bewegen?"
      }
    ]
  }
}
```

---

## PART 4: ORGANIZATION BY PURPOSE

### For QA System (Quick Lookup)

```
Organize by:
- Code (F03 55, A07, P0005)
- Category (Door, Temperature, Safety)
- Severity (critical, high, medium)

Access pattern: "What does this code mean?"
→ Fast, indexed by code

Database:
- error_codes TABLE (indexed by code)
- parameters TABLE (indexed by parameter_id)
- contacts TABLE (indexed by contact_name)
```

### For Diagnostic System (Decision Making)

```
Organize by:
- Symptom (won't start, temperature alarm, door issues)
- Decision branches (constant vs sporadic, LED status)
- Probability ranking

Access pattern: "What should I check next?"
→ Conditional logic, decision trees

Database:
- diagnostic_flows TABLE (indexed by symptom)
- decision_branches TABLE (conditions + next_steps)
- probability_rankings TABLE (cause frequency)
```

### For Learning System (Feedback)

```
Organize by:
- Lift ID + timestamp
- Suspected cause vs actual cause
- Accuracy metrics

Access pattern: "How often is this diagnosis correct?"
→ Statistics, pattern analysis

Database:
- feedback_cases TABLE (symptoms + diagnosis + outcome)
- accuracy_metrics TABLE (cause → success_rate)
- new_patterns TABLE (unexpected combinations)
```

---

## PART 5: EXTRACTION CHECKLIST & TIMELINE

### Week 1: Error Codes & Parameters

**Monday-Tuesday:**
- [ ] Extract all F-codes (pages 7-9)
- [ ] Extract all A-codes (page 6)
- [ ] Create error_codes.json
- [ ] Validate 100% accuracy
- [ ] Add manual page references

**Wednesday-Thursday:**
- [ ] Extract all parameters (pages 13-14)
- [ ] Create parameters.json
- [ ] Link parameters to error codes
- [ ] Document menu paths
- [ ] Validate all fields

**Friday:**
- [ ] Spot-check random entries
- [ ] Verify cross-references
- [ ] Create extraction_manifest.json
- [ ] Commit to version control

### Week 2: Hardware & Components

**Monday-Tuesday:**
- [ ] Extract board locations (page 10)
- [ ] Extract LED meanings (page 10-11)
- [ ] Create hardware.json
- [ ] Document connectors (page 11-12)
- [ ] Create connectors.json

**Wednesday-Thursday:**
- [ ] Extract safety contacts (pages 3-4, diagrams)
- [ ] Create contacts.json
- [ ] Map contacts to LEDs
- [ ] Document signal paths
- [ ] Verify against wiring diagrams

**Friday:**
- [ ] Validate all component locations
- [ ] Verify LED mappings
- [ ] Check connector pin assignments
- [ ] Create reference diagrams

### Week 3: Knowledge Synthesis

**Monday-Tuesday:**
- [ ] Document Via known issues → quirks.json
- [ ] Add CAB Board problem details
- [ ] Add software bugs (v74DEEN)
- [ ] Add frequency estimates
- [ ] Note source (manual + field knowledge)

**Wednesday-Thursday:**
- [ ] Create diagnostic flowcharts → diagnostic_flows.json
- [ ] Map symptoms to decision trees
- [ ] Add confidence levels
- [ ] Link to error codes
- [ ] Document special cases

**Friday:**
- [ ] Review all extracted data
- [ ] Test with 10 sample questions
- [ ] Document any gaps
- [ ] Plan feedback loop integration

---

## PART 6: QUALITY ASSURANCE

### Accuracy Verification

For each data type, spot-check against manual:

```
CHECKLIST: Error Code F03 55
□ Code exactly matches manual
□ Description matches word-for-word
□ Affected contacts listed (7H, 8H)
□ Manual page reference correct (7)
□ Related parameters correct (P0014 exists)
□ Translation is accurate
□ No invented information
□ Status field updated
□ Date extracted noted

RESULT: ✓ PASS / ✗ FAIL
```

### Completeness Verification

```
CHECKLIST: All F-codes extracted
□ Manual page 7 scanned for all codes
□ Manual page 8 scanned for all codes
□ Manual page 9 scanned for all codes
□ No codes mentioned elsewhere missed
□ Total count matches manual
□ Spot-check 5 random entries

RESULT: ✓ PASS / ✗ FAIL
```

### Consistency Verification

```
CHECKLIST: Cross-references valid
□ Code F03 55 references 7H → 7H exists in contacts
□ Code F03 55 references P0014 → P0014 exists in parameters
□ LED 7H in Group D → verified in diagram
□ Connector XSSH2 → board location verified
□ Parameter menu path valid → tested on console

RESULT: ✓ PASS / ✗ FAIL
```

---

## PART 7: TOOLS & AUTOMATION

### For Data Extraction

**Python libraries:**
```python
# PDF extraction
import pdfplumber
with pdfplumber.open("VIASerie_Manual.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        text = page.extract_text()

# Data validation
import jsonschema
schema = {
    "type": "object",
    "properties": {
        "code": {"type": "string"},
        "description_de": {"type": "string"},
        "manual_page": {"type": "integer"}
    },
    "required": ["code", "description_de"]
}
jsonschema.validate(error_code, schema)

# Version control
import json
with open('error_codes.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### For Data Organization

```python
# Create searchable database
import sqlite3
conn = sqlite3.connect('via_knowledge.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE error_codes (
    code TEXT PRIMARY KEY,
    family TEXT,
    number TEXT,
    description_de TEXT,
    manual_page INTEGER,
    validation_status TEXT,
    extracted_date TEXT
)
''')

cursor.execute('''
INSERT INTO error_codes
VALUES (?, ?, ?, ?, ?, ?, ?)
''', ('F03 55', '03', '55', 'Türkreis öffnet nicht...', 7, 'verified', '2025-11-16'))

conn.commit()
```

### For Validation

```python
# Validation script
def validate_error_code(code_data, manual_reference):
    checks = {
        'code_exists': code_data['code'] in manual_reference,
        'description_matches': code_data['description_de'] in manual_reference,
        'page_reference_correct': manual_reference['page'] == code_data['manual_page'],
        'all_required_fields': all(field in code_data for field in REQUIRED_FIELDS)
    }
    return all(checks.values()), checks

# Run validation
results = validate_error_code(extracted_code, manual_data)
if not results[0]:
    print(f"Failed checks: {results[1]}")
```

---

## SUMMARY: Extraction Output

**After completing this process, you'll have:**

✅ `error_codes.json` - All F and A codes with definitions
✅ `parameters.json` - All P-codes with functions and ranges
✅ `hardware.json` - All boards, locations, and functions
✅ `contacts.json` - All safety contacts and meanings
✅ `connectors.json` - All wiring and pin assignments
✅ `quirks.json` - Known Via issues and frequencies
✅ `diagnostic_flows.json` - Decision trees for troubleshooting
✅ `console_procedures.json` - Step-by-step how-to guides
✅ `extraction_manifest.json` - What was extracted, when, status

**Ready for:** AI integration, feedback loop, testing with real cases

---

## NEXT STEPS

1. Inventory what manual documentation you have
2. Decide: Extract manually or use OCR?
3. Assign person/timeline for extraction
4. Set up version control (Git)
5. Plan validation process
6. Create first database schema
