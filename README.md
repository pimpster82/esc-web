# ESC - ELEVATOR SERVICE COMPANION (POC)
## Knowledge Assistant for MacPuarsa Via Elevators

**Status:** Extraction Complete ✅ (Ready for data population)
**Model:** MacPuarsa Via (all versions)
**Timeline:** 4 weeks
**Current Phase:** Phase 1 - Data Population (⏳ In Progress)

---

## 📚 DOCUMENTATION (Start Here)

### 🎯 Project Overview (5 min read)
**File:** [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)
- What this project does
- 4 knowledge layers explained
- Complete roadmap & timeline
- Validation checklist

**👉 Start here if:** You're new to the project

---

### 🏗️ System Architecture (15 min read)
**File:** [`LOGICAL_ARCHITECTURE.md`](LOGICAL_ARCHITECTURE.md)
- How knowledge is organized
- Data types (static, structured, learned)
- Training process (3 phases)
- AI decision points
- Scalability framework

**👉 Start here if:** You want to understand the design

---

### 📋 Data Extraction Guide (20 min read)
**File:** [`DATA_EXTRACTION_GUIDE.md`](DATA_EXTRACTION_GUIDE.md)
- What data exists in the manual
- 7 data types to extract
- How to validate extracted data
- Week-by-week timeline
- Quality assurance checklist

**👉 Start here if:** You want to know what to extract

---

### ⚡ Quick Start (10 min read)
**File:** [`EXTRACTION_QUICKSTART.md`](EXTRACTION_QUICKSTART.md)
- Setup in 5 minutes
- 3-step extraction pipeline
- Sample commands & expected output
- Troubleshooting guide
- Validation examples

**👉 Start here if:** You want to start extracting NOW

---

### ✅ Extraction Complete Status (15 min read)
**File:** [`EXTRACTION_COMPLETE.md`](EXTRACTION_COMPLETE.md)
- Extraction results summary (565 tables, 155 pages extracted)
- Template creation status (6 JSON templates ready)
- Data population checklist (what needs manual work)
- Time estimates per template (6-10 hours total)
- Next steps and validation plan

**👉 Start here if:** Extraction is done, time to populate templates

---

### 🔧 Technical Details (30 min read)
**File:** [`EXTRACTION_WORKFLOW_PDF.md`](EXTRACTION_WORKFLOW_PDF.md)
- PDF extraction methods (3 approaches)
- Code examples for each step
- Detailed organization of JSON files
- Enrichment with field knowledge
- Python scripts explained line-by-line

**👉 Start here if:** You need detailed technical implementation

---

## 🐍 PYTHON SCRIPTS

All scripts are in `/scripts/` directory.

### `extract_pdf.py` - Extract PDF
**What it does:**
- Opens Via manual PDF
- Extracts all tables
- Extracts all text by page
- Saves raw data to `extracted_raw/`

**Time to run:** ~30 seconds
**Command:** `python scripts/extract_pdf.py`
**Output:** `extracted_raw/*.json` and `extracted_raw/*.txt`

---

### `organize_json.py` - Create Templates
**What it does:**
- Creates JSON file templates
- Includes metadata
- Shows expected structure
- Provides 1 example for each type

**Time to run:** ~5 seconds
**Command:** `python scripts/organize_json.py`
**Output:** `data/via/v74/*.json` (6 files)

---

### `validate_data.py` - Validate JSON
**What it does:**
- Checks all JSON files are valid
- Verifies required fields present
- Counts entries
- Reports any errors

**Time to run:** ~5 seconds
**Command:** `python scripts/validate_data.py`
**Output:** Validation report in console

---

## 📊 DATA FILES

All data goes to `/data/via/v74/` directory.

### `error_codes.json`
**Contains:** F-codes and A-codes
**Example:** F03 55 (Türkreis öffnet nicht)
**Fields:** code, family, number, description_de, affected_contacts, manual_page

---

### `parameters.json`
**Contains:** All P-parameters
**Example:** P0005 (Temperature threshold)
**Fields:** code, name, menu_path, default_value, range, unit, related_errors

---

### `hardware.json`
**Contains:** Boards (SMQ, CAB, Door Operator, etc.)
**Example:** CAB Board location, function, connectors, LED groups
**Fields:** name, location, function, connectors, led_groups, failure_modes

---

### `contacts.json`
**Contains:** Safety contacts (7H, 8H, 1H, 2H, etc.)
**Example:** 7H (Shaft door contact)
**Fields:** code, name, location, monitors, normal_state, smd_led_group, connector, failure_consequences

---

### `connectors.json`
**Contains:** Wiring connectors (XSSH2, XFOT, XSM1, etc.)
**Example:** XSSH2 with 4 pins
**Fields:** code, board, purpose, pins[], common_issues

---

### `quirks.json`
**Contains:** Known Via issues
**Example:** CAB Board problem (40% of door failures)
**Fields:** component, problem, symptoms, affected_codes, frequency, detection_method, solution

---

## 🚀 QUICK START (TL;DR)

```bash
# 1. Install dependencies (one time)
pip install pdfplumber jsonschema pandas

# 2. Extract from PDF
cd scripts
python extract_pdf.py

# 3. Create templates
python organize_json.py

# 4. Manually populate JSON files with data from PDF
# (Use extracted_raw/ files as reference)
# This takes 2-3 hours

# 5. Validate
python validate_data.py

# 6. Check everything is valid
# If all green ✅, you're done!
```

**Total time:** ~5-10 hours (mostly manual data entry)

---

## 📈 IMPLEMENTATION PHASES

### Phase 1: Data Extraction (Week 1-2) ← YOU ARE HERE
- [x] Setup Python environment
- [x] Extract data from PDF (565 tables, 155 pages)
- [x] Create JSON templates (6 files ready)
- [ ] Populate JSON files (6-10 hours manual work)
- [ ] Validate all data
- [ ] Commit to git

**Status:** Extraction complete ✅ | Templates created ✅ | **Now:** Population in progress ⏳

---

### Phase 2: AI Integration (Week 2-3)
- [ ] Design system prompt
- [ ] Test with sample questions
- [ ] Implement feedback collection
- [ ] Measure accuracy

**Status:** Strategy planned, document TBD

---

### Phase 3: Feedback Loop (Week 3-4)
- [ ] Deploy with test technicians
- [ ] Collect feedback
- [ ] Analyze improvements
- [ ] Update probabilities

**Status:** Schema ready, document TBD

---

### Phase 4: Scale (Post-POC)
- [ ] Add EcoGo model
- [ ] Add other manufacturers
- [ ] Automated deployment
- [ ] Performance monitoring

**Status:** Architecture ready

---

## 🎯 SUCCESS CRITERIA

**Week 2:** Knowledge base complete & validated
**Week 3:** AI integration working, tested with 10 questions
**Week 4:** Feedback loop tested with 5-10 technicians
**After:** Ready to add EcoGo & scale

---

## 📁 DIRECTORY STRUCTURE

```
ESC/
├── README.md                                    ← You are here
├── PROJECT_SUMMARY.md                           ← Overview & roadmap
├── LOGICAL_ARCHITECTURE.md                      ← System design
├── DATA_EXTRACTION_GUIDE.md                      ← What to extract
├── EXTRACTION_WORKFLOW_PDF.md                    ← How to extract
├── EXTRACTION_QUICKSTART.md                      ← Quick reference
│
├── scripts/
│   ├── extract_pdf.py                           ← Extract from PDF
│   ├── organize_json.py                         ← Create templates
│   └── validate_data.py                         ← Validate JSON
│
├── data/
│   └── via/
│       └── v74/
│           ├── error_codes.json                 ← F & A codes
│           ├── parameters.json                  ← P-parameters
│           ├── hardware.json                    ← Boards & components
│           ├── contacts.json                    ← Safety contacts
│           ├── connectors.json                  ← Wiring
│           ├── quirks.json                      ← Known issues
│           └── extraction_manifest.json         ← What was extracted
│
├── extracted_raw/                               ← Temporary files
│   ├── page_01_tables.json
│   ├── page_01_text.txt
│   └── ...
│
├── manuals/                                     ← Put PDF here
│   └── VIASerie_Kurzanleitung_v74.pdf
│
└── (Other old files)
    ├── aufzug-assistent-instructions.md
    ├── liftec-companion-workflow.md
    ├── liftec-interactive-mentor.md
    └── liftec-learning-guide.md
```

---

## 🔍 WHAT EACH DOCUMENT EXPLAINS

| Document | Focus | Best For |
|----------|-------|----------|
| PROJECT_SUMMARY.md | Overview, timeline, checklist | Getting oriented, planning |
| LOGICAL_ARCHITECTURE.md | System design, 4 layers | Understanding the approach |
| DATA_EXTRACTION_GUIDE.md | What data exists, methodology | Learning what to extract |
| EXTRACTION_WORKFLOW_PDF.md | Technical implementation, code | Actually extracting |
| EXTRACTION_QUICKSTART.md | Commands & quick reference | Running the scripts |

---

## ✅ YOUR NEXT STEPS

1. **Read** `PROJECT_SUMMARY.md` (5 min)
2. **Understand** `LOGICAL_ARCHITECTURE.md` (15 min)
3. **Follow** `EXTRACTION_QUICKSTART.md` (10 min to run scripts)
4. **Extract** data from your PDF (2-3 hours)
5. **Validate** using `validate_data.py` (1 min)
6. **Come back** when you hit AI integration phase

---

## 🤔 QUESTIONS?

**"What should I read first?"**
→ `PROJECT_SUMMARY.md`

**"How do I understand the architecture?"**
→ `LOGICAL_ARCHITECTURE.md`

**"How do I run the extraction?"**
→ `EXTRACTION_QUICKSTART.md`

**"I need detailed technical info"**
→ `EXTRACTION_WORKFLOW_PDF.md`

**"What data needs to be extracted?"**
→ `DATA_EXTRACTION_GUIDE.md`

---

## 📞 SUPPORT

All documents include:
- Step-by-step instructions
- Example outputs
- Troubleshooting sections
- Code samples
- Validation checklists

Everything you need is in the documentation.

---

## 📝 VERSION INFO

**Project:** LIFTEC Elevator Companion (POC)
**Version:** 1.0 - Setup Phase
**Created:** 2025-11-16
**Model:** MacPuarsa Via
**Status:** Ready for data extraction

---

**Let's build this! 🚀**

Start with: [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)
