# ESC - Elevator Service Companion
## AI Diagnostic System - Complete Project Structure

---

## 📋 Project Overview

**ESC** (Elevator Service Companion) is an intelligent AI-powered diagnostic system for elevator service and maintenance. It provides technicians with instant access to diagnostic information, error codes, component details, and troubleshooting procedures using Claude AI with a comprehensive knowledge base.

### Key Features
- Multi-language support (German, English)
- REST API and Web UI interfaces
- Interactive CLI validation tool
- Hierarchical knowledge base (universal + manufacturer-specific)
- Feedback/validation system with statistics
- Real-time conversation history for context-aware responses

---

## 📁 Directory Structure

```
ESC/
├── data/                           # Core knowledge base and validation data
│   ├── general/                    # Universal elevator knowledge (all manufacturers)
│   │   ├── knowledge/              # JSON knowledge base files
│   │   ├── practical_guides/       # Step-by-step procedures and guides
│   │   └── images/                 # General reference images
│   │       ├── components/         # Component diagrams and photos
│   │       ├── diagrams/           # System diagrams
│   │       └── procedures/         # Procedural illustrations
│   │
│   ├── manufacturers/              # Manufacturer-specific knowledge
│   │   └── macpuarsa/              # Macpuarsa manufacturer
│   │       └── via/                # VIA elevator model line
│   │           └── v74/            # Version 74 specific data
│   │               ├── knowledge/  # V74-specific error codes, parameters
│   │               ├── specific_guides/  # V74-specific procedures
│   │               └── images/     # V74-specific diagrams
│   │                   ├── assemblies/
│   │                   ├── components/
│   │                   ├── procedures/
│   │                   └── schematics/
│   │
│   ├── lookups/                    # Reference lookup files (abbreviations, codes)
│   └── validation/                 # Validation and feedback system
│       ├── feedback.json           # User feedback records
│       └── stats.json              # Validation statistics
│
├── scripts/                        # Python backend system
│   ├── ai_diagnostics.py          # Main diagnostic engine (Claude AI integration)
│   ├── knowledge_loader.py        # Load and manage knowledge base
│   ├── validation_manager.py      # Feedback/validation system
│   ├── validate_cli.py            # Interactive CLI validation tool
│   ├── extract_pdf.py             # PDF extraction utility
│   ├── test_ai_simple.py          # Testing and debugging script
│   └── __pycache__/               # Python bytecode cache
│
├── web/                           # Frontend web interface
│   └── index.html                 # Main web UI (React/Vanilla JS)
│                                   # Features:
│                                   # - Query input box
│                                   # - Response display with formatting
│                                   # - Feedback buttons (Correct/Incorrect/Unsure)
│                                   # - History management
│                                   # - Knowledge summary display
│
├── manuals/                       # Original PDF manuals
│   ├── Handbuch VIA MTIPIEPVS_308_DE.pdf
│   └── MTELIEPSCM_404_DE.pdf
│
├── venv/                          # Python virtual environment
│
├── web_api.py                     # Flask REST API server
│
├── test_ai_simple.py              # Standalone test script
│
├── setup_environment.sh           # Environment setup script
│
├── requirements.txt               # Python dependencies
│
└── INDEX.md                       # This file - Project documentation

```

---

## 🔧 Core Components

### 1. Backend System (Python)

#### **ai_diagnostics.py** - Diagnostic Engine
- Main AI interface using Claude API
- Processes natural language queries
- Returns structured diagnostic responses with:
  - `diagnosis` - Detailed diagnostic answer
  - `confidence` - Confidence level (HIGH/MEDIUM/LOW)
  - `codes_referenced` - Related error/component codes
  - `manual_pages` - Page references from manuals
  - `next_steps` - Recommended actions
- Maintains conversation history for context

#### **knowledge_loader.py** - Knowledge Base Manager
- Loads hierarchical knowledge structure
- Searches across general and manufacturer-specific data
- Key methods:
  - `load_knowledge()` - Load all knowledge files
  - `search_components()` - Search by component name
  - `search_codes()` - Search error codes
  - `get_knowledge_summary()` - Overview of loaded data
  - `get_context()` - Prepare knowledge for Claude

#### **validation_manager.py** - Feedback System
- Stores user feedback on AI responses
- Tracks accuracy statistics
- Methods:
  - `add_feedback()` - Record feedback (correct/incorrect/unsure)
  - `get_stats()` - Return validation statistics
  - `get_feedback()` - Query feedback records
  - `export_csv()` - Export for analysis
- Storage: JSON files in `data/validation/`

#### **validate_cli.py** - Interactive CLI Tool
- Command-line interface for testing and validation
- Interactive query → response → feedback workflow
- Features:
  - Real-time statistics display
  - Session summaries
  - History management
  - Notes for feedback entries

### 2. Web Interface

#### **web/index.html** - Main UI
- Responsive web interface for ESC system
- Key sections:
  - Header with project info
  - Query input area
  - Response display (formatted diagnosis)
  - **Feedback section** with:
    - ✓ Correct button (green)
    - ✗ Incorrect button (red)
    - ? Unsure button (yellow)
    - Notes textarea
    - Submit button
  - Knowledge summary panel
  - History management controls

### 3. API Layer

#### **web_api.py** - Flask REST Server
Provides REST endpoints:

**Diagnostic Endpoints:**
- `POST /api/query` - Submit diagnostic query
  - Input: `{question, use_history}`
  - Output: `{diagnosis, confidence, codes_referenced, manual_pages, next_steps}`
- `POST /api/clear-history` - Reset conversation history
- `GET /api/knowledge-summary` - Get loaded knowledge overview

**Feedback/Validation Endpoints:**
- `POST /api/feedback` - Submit feedback on responses
  - Input: `{query, response, feedback, confidence, notes}`
  - Values: feedback ∈ {correct, incorrect, unsure}
- `GET /api/validation/summary` - Get validation statistics
- `GET /api/validation/feedback` - Query feedback records
  - Params: `limit`, `type` (filter by feedback type)
- `GET /api/validation/export` - Export feedback as CSV

**Server Details:**
- Port: 5000 (configurable via `PORT` env var)
- Host: 0.0.0.0 (accessible from localhost and network)
- Debug mode: Configurable via `DEBUG` env var

---

## 📊 Knowledge Base Structure

### General Knowledge (`data/general/`)
Universal information applicable to all elevator types:
- Component specifications and functions
- Common error codes and solutions
- Safety procedures and regulations
- Standard troubleshooting workflows
- General maintenance procedures

### Manufacturer-Specific Knowledge (`data/manufacturers/`)
Detailed information for specific elevator models:

```
manufacturers/
└── macpuarsa/              # Manufacturer name
    └── via/                # Model line (VIA = elevator series)
        └── v74/            # Specific version
            ├── knowledge/  # Version-specific error codes, parameters
            ├── specific_guides/  # Model-specific procedures
            └── images/     # Schematics, assemblies, diagrams
```

**How to add new manufacturers:**
1. Create directory: `data/manufacturers/[MANUFACTURER]/[MODEL]/[VERSION]/`
2. Add knowledge files to `knowledge/` subdirectory
3. Add guides to `specific_guides/` subdirectory
4. System automatically detects and loads on startup

---

## 🚀 Running the System

### Option 1: Web Interface (Recommended)
```bash
python3 web_api.py
# Open http://localhost:5000 in browser
```

### Option 2: CLI Tool
```bash
cd scripts
python3 validate_cli.py
# Interactive command-line interface
```

### Option 3: Python API Direct Usage
```python
from ai_diagnostics import DiagnosticSystem

diagnostic = DiagnosticSystem()
response = diagnostic.query("F01 02 error code")
print(response.diagnosis)
print(f"Confidence: {response.confidence}")
```

---

## 📝 Validation & Feedback System

### How It Works
1. **User asks question** → System provides diagnosis
2. **User provides feedback** via UI buttons:
   - ✓ Correct - Response was accurate and helpful
   - ✗ Incorrect - Response was inaccurate or misleading
   - ? Unsure - Response needs clarification
3. **Optional notes** - User can add details about feedback
4. **Data is stored** - JSON records for analysis

### Accessing Feedback
- **Web UI**: Shows stats at top of page
- **API**: `GET /api/validation/summary`
- **Export**: `GET /api/validation/export` (CSV format)
- **Raw data**: `data/validation/feedback.json`

### Feedback Statistics
- Total validations: Count of all feedback records
- Accuracy: (correct / (correct + incorrect)) × 100%
- Last updated: Timestamp of most recent feedback

---

## 🔌 API Usage Examples

### Query for Diagnosis
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "F01 02 error"}'
```

Response:
```json
{
  "success": true,
  "diagnosis": "Sicherheitskreis geöffnet - Safety circuit open",
  "confidence": "HIGH",
  "codes_referenced": ["F01 02"],
  "manual_pages": [45, 46],
  "next_steps": ["Check connections", "Review safety circuit"]
}
```

### Submit Feedback
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "query": "F01 02 error",
    "response": "Sicherheitskreis geöffnet",
    "feedback": "correct",
    "confidence": "HIGH",
    "notes": "Accurate and helpful"
  }'
```

### Get Validation Summary
```bash
curl http://localhost:5000/api/validation/summary
```

Response:
```json
{
  "success": true,
  "summary": {
    "total_validations": 4,
    "correct": 3,
    "incorrect": 0,
    "unsure": 1,
    "accuracy": 100.0,
    "recent_feedback": [...]
  }
}
```

---

## 🛠️ Maintenance & Development

### Adding New Knowledge
1. Create/edit JSON files in appropriate `knowledge/` directory
2. Follow existing schema and structure
3. System auto-loads on next startup

### Testing
```bash
cd scripts
python3 test_ai_simple.py
# Or use validate_cli.py for interactive testing
```

### Debugging
- Set `DEBUG=true` environment variable
- Check Flask logs in terminal
- Use browser console for frontend issues
- Check `data/validation/feedback.json` for validation records

### Environment Variables
- `PORT` - API server port (default: 5000)
- `DEBUG` - Enable Flask debug mode (default: False)
- `ANTHROPIC_API_KEY` - Claude API key (required)

---

## 📚 Knowledge Base File Format

### Knowledge Files (knowledge/*.json)
```json
{
  "category": "error_codes",
  "items": [
    {
      "code": "F01 02",
      "description": "Sicherheitskreis geöffnet",
      "english": "Safety circuit open",
      "possible_causes": ["...", "..."],
      "solutions": ["...", "..."],
      "component": "Safety Circuit",
      "priority": "HIGH"
    }
  ]
}
```

### Practical Guides (practical_guides/*.json)
```json
{
  "title": "Guide title",
  "category": "maintenance",
  "steps": [
    {"step": 1, "action": "Description", "notes": "Additional info"},
    {"step": 2, "action": "Next action", "notes": "..."}
  ],
  "safety_warnings": ["..."],
  "estimated_time": "30 minutes",
  "tools_needed": ["..."]
}
```

---

## ✅ Validation/Feedback Files

### feedback.json
```json
[
  {
    "id": 1,
    "timestamp": "2025-11-16T23:54:37.077525",
    "query": "F01 02",
    "response": "Sicherheitskreis geöffnet - Safety circuit open",
    "feedback": "correct",
    "confidence": "HIGH",
    "notes": "Correct description and cause"
  }
]
```

### stats.json
```json
{
  "total_validations": 4,
  "correct": 3,
  "incorrect": 0,
  "unsure": 1,
  "accuracy": 100.0,
  "last_updated": "2025-11-16T23:58:37.479689"
}
```

---

## 🗑️ Cleanup & Files to Ignore

### Temporary/Development Files (Not Needed)
- `extracted_raw/` - Temporary PDF extraction cache (deleted)
- `__pycache__/` - Python bytecode (auto-generated)
- `.git/` - Version control (internal use)
- `venv/` - Python virtual environment (can rebuild)

### Documentation Files (Archived)
The following markdown files from previous development phases are archived but not actively maintained:
- `*_PLAN.md`, `*_GUIDE.md`, `*COMPLETE*.md` - Development notes
- These contain historical information about setup and development

### Files to Keep
- All files in `data/` directory
- All files in `scripts/` directory
- All files in `web/` directory
- Core configuration files (`requirements.txt`, `setup_environment.sh`)
- API and server files (`web_api.py`)

---

## 🔗 Related Files

- **Main README**: `README.md` - User-facing documentation
- **API Reference**: See web_api.py docstrings for endpoint details
- **Dependencies**: `requirements.txt` - Python packages needed

---

## 📞 Support & Issues

For issues or questions:
1. Check `data/validation/feedback.json` for previous similar queries
2. Review knowledge base in `data/` directory
3. Test using CLI: `python3 scripts/validate_cli.py`
4. Check API directly: `curl http://localhost:5000/api/knowledge-summary`

---

**Last Updated**: 2025-11-17
**System Status**: Production Ready
**Version**: 1.0 (Complete with Validation System)
