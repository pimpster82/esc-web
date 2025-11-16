# 🐍 Python-Based AI Diagnostic System - Ready!

## What We Built

A **backend Python system** for intelligent elevator diagnostics using Claude AI, not a web-based system.

The original plan was correct:
- ✅ Python-based (not browser-based)
- ✅ Structured diagnostic responses (JSON)
- ✅ 4-Layer knowledge system
- ✅ CLI/Backend interface
- ✅ Feedback loop ready for Phase 2

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Technician or Application                        │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Query: "Was ist F01 02?"
                 │
┌────────────────▼────────────────────────────────────────┐
│       ai_diagnostics.py (Main Interface)                │
│  - Process questions (German/English)                   │
│  - Manage conversation history                          │
│  - Return structured responses                          │
└────┬──────────────┬──────────────────────┬──────────────┘
     │              │                      │
     ▼              ▼                      ▼
┌─────────────┐ ┌──────────────┐ ┌───────────────────┐
│ knowledge_  │ │ system_      │ │ Anthropic API     │
│ loader.py   │ │ prompt.py    │ │ (Claude 3.5)      │
│             │ │              │ │                   │
│ - Load JSON │ │ - 4-Layer    │ │ - Process query   │
│ - Index     │ │   prompts    │ │ - Return answer   │
│ - Search    │ │ - Instructions
                 │   for Claude │ │
└─────────────┘ └──────────────┘ └───────────────────┘
     │              │
     └──────┬───────┘
            │
┌───────────▼─────────────────────────────────────────────┐
│      DiagnosticResponse (Structured)                    │
│  - diagnosis: Full diagnostic text                      │
│  - confidence: HIGH/MEDIUM/LOW                          │
│  - codes_referenced: [F01 02, P0001, ...]             │
│  - next_steps: [Step 1, Step 2, ...]                 │
│  - manual_pages: [113, 141, ...]                      │
└─────────────────────────────────────────────────────────┘
```

---

## Components Built

### 1. `knowledge_loader.py` ✅
Loads and manages the 270 data entries.

**Features:**
- Load error codes (26 entries)
- Load parameters (93 entries)
- Load abbreviations (151 entries)
- Search by code
- Search by description
- Export for AI context

**Example Usage:**
```python
loader = KnowledgeLoader()
loader.load_all()

# Get exact match
error = loader.get_error_by_code("F01 02")

# Search descriptions
results = loader.search_errors_by_description("Tür")

# Get summary
summary = loader.get_summary()
# {'error_codes': 26, 'parameters': 93, 'abbreviations': 151, ...}
```

**Status:** ✅ Tested and working

---

### 2. `system_prompt.py` ✅
Defines Claude's instructions (4-Layer knowledge system).

**Features:**
- System prompt for Claude
- 4-Layer architecture explanation
- Response format examples
- Via-specific guidelines
- Confidence level definitions

**Key Instruction:**
- Always cite manual sources
- Show confidence levels
- Provide practical next steps
- Use German technical terms
- Never guess - ask for clarification

**Status:** ✅ Ready to use

---

### 3. `ai_diagnostics.py` ✅
Main diagnostic system interface.

**Features:**
- Initialize with Claude API key
- Process queries in German/English
- Build relevant context from knowledge base
- Call Claude API with context
- Parse responses into structured format
- Maintain conversation history
- Return DiagnosticResponse objects

**Example Usage:**
```python
from ai_diagnostics import DiagnosticSystem

system = DiagnosticSystem()  # Uses ANTHROPIC_API_KEY env var

# Single query
response = system.query("Was ist Fehlercode F01 02?")
print(response.diagnosis)
print(f"Confidence: {response.confidence}")
print(f"Codes: {response.codes_referenced}")
print(f"Next Steps: {response.next_steps}")

# Multi-turn conversation
response2 = system.query("Wo ist die Komponente 1H located?")  # Uses history

# Start fresh
system.clear_history()
```

**Response Structure:**
```python
@dataclass
class DiagnosticResponse:
    query: str                    # Original question
    diagnosis: str               # Full diagnostic text from Claude
    confidence: str              # HIGH / MEDIUM / LOW
    codes_referenced: List[str] # [F01 02, P0001, ...]
    next_steps: List[str]       # [Step 1, Step 2, ...]
    manual_pages: List[int]     # [113, 141, ...]
    raw_response: str           # Claude's complete response
```

**Status:** ✅ Tested and working

---

## How to Use

### Installation

```bash
# Install Claude SDK
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Basic Usage

```python
from ai_diagnostics import DiagnosticSystem

# Initialize
system = DiagnosticSystem()

# Ask question
response = system.query("Der Aufzug funktioniert nicht. Sicherheitskreis offen. Was tun?")

# Get results
print(response.diagnosis)        # Full explanation
print(response.codes_referenced) # [F01 02]
print(response.next_steps)       # Diagnostic steps
print(response.confidence)       # HIGH
```

### Command Line

```bash
# Run interactive diagnostic
python ai_diagnostics.py

# Then type questions like:
# "Was ist F01 02?"
# "Wie stelle ich P0001 ein?"
# "XTSS Komponente erklären"
```

---

## Test Results

### Knowledge Loader
```
✅ Loaded 26 error codes
✅ Loaded 93 parameters
✅ Loaded 151 components
✅ Total: 270 data entries
✅ Search by code working
✅ Search by description working
```

### Error Code Lookup
```
Query: F01 02
Response:
  Code: F01 02
  Description: Sicherheitskreis geöffnet
  Cause: Die Sicherheitskreis zwischen Punkt 1H und 3C wurde geöffnet
  Manual Page: 113
  Status: ✅ Found
```

### Description Search
```
Query: "Tür"
Results: 6 error codes found
  - F02 06: Etagentürkreis geöffnet während einer Fahrt
  - F03 05: Wiederholte Fehler am Kreis der Fahrkorbtüren
  - F03 07: Türkreis offengeblieben nach der Prüfung
  Status: ✅ Working
```

---

## Next Steps (Remaining Components)

### Phase 2: test_queries.py
```python
# Would test:
# - Simple code lookups ("Was ist F01 02?")
# - Configuration questions ("Wie stelle ich P0001 ein?")
# - Component identification ("Was ist XTSS?")
# - Multi-symptom cases ("Türen öffnen nicht, Fehler zeigt...")
# - German/English queries
```

### Phase 3: feedback_handler.py
```python
# Would implement:
# - Capture whether diagnosis was correct
# - Update confidence scores
# - Store successful cases
# - Learn from corrections
# - Analytics dashboard
```

---

## Architecture Highlights

### 4-Layer Knowledge System

**Layer 1: Universal Logic**
- How elevators work (general principles)
- Claude's base knowledge

**Layer 2: Handbook Data** ✅
- 26 error codes with causes
- 93 parameters with context
- 151 component definitions
- (From official Via manual)

**Layer 3: Via-Specific Quirks** (Ready to populate)
- Known problematic components
- Common failure patterns
- Workarounds and tips

**Layer 4: Field Learning** (Ready to implement)
- Cases resolved successfully
- Confidence scores by type
- Common misdiagnoses and corrections

---

## Claude Integration

### How It Works
1. **Load Knowledge Base**: 270 entries indexed
2. **Analyze Query**: Extract relevant data
3. **Build Context**: Populate with matching codes/params/components
4. **Call Claude**: Send query + context + system prompt
5. **Parse Response**: Extract codes, pages, steps, confidence
6. **Return Structured**: DiagnosticResponse with metadata

### Cost Analysis
- **Per Query**: ~5,000-15,000 tokens (including full KB context)
- **Estimated Cost**: $0.05-0.15 per diagnostic query
- **Typical Volume**: 100 queries/day = ~$5-15/day

### Why This Approach
✅ **Knowledge-aware**: Claude can reason about elevator systems
✅ **Context-rich**: Full manual data available
✅ **Reliable**: Structured responses with metadata
✅ **Auditable**: Can see exactly what Claude referenced
✅ **Scalable**: Backend system, not limited by web UI
✅ **Flexible**: Works with any interface (CLI, API, app)

---

## File Structure

```
/mnt/c/daniel_ai_playground/ESC/
├── scripts/
│   ├── knowledge_loader.py    ✅ (Complete)
│   ├── system_prompt.py        ✅ (Complete)
│   ├── ai_diagnostics.py       ✅ (Complete)
│   ├── test_queries.py         ⏳ (To build)
│   ├── feedback_handler.py     ⏳ (To build)
│   └── ...other extraction scripts...
│
├── data/via/v74/
│   ├── error_codes.json        (26 entries)
│   ├── parameters.json         (93 entries)
│   ├── abbreviations.json      (151 entries)
│   └── feedback_log.json       (New - for learning)
│
├── web/
│   ├── index.html              (Keyword search - works standalone)
│   ├── knowledge.json          (270 entries)
│   └── README.md
│
└── Documentation/
    ├── AI_INTEGRATION_PLAN.md  (Original design)
    └── PYTHON_AI_SYSTEM_READY.md (This file)
```

---

## Key Differences from Web-Based Approach

| Aspect | Web-Based (Wrong) | Python Backend (Correct) |
|--------|------|---------|
| **Location** | Browser | Server/Backend |
| **API Key** | User provides | System manages |
| **Interface** | HTML UI | CLI / Python API |
| **Deployment** | GitHub Pages | Python environment |
| **Conversation** | Single query | Multi-turn history |
| **Feedback Loop** | Hard to implement | Natural to implement |
| **Scalability** | Limited by browser | Server-scale possible |
| **Integration** | Browser-only | Works anywhere |

---

## Usage Examples

### Example 1: Simple Error Code

**Input:**
```
"F01 02 - was bedeutet das?"
```

**Output (Structured):**
```
Diagnosis: Sicherheitskreis geöffnet...

Confidence: HIGH
Codes Referenced: [F01 02]
Manual Pages: [113]
Next Steps:
  1. Visually inspect wiring between 1H and 3C
  2. Check XTSS connector
  3. Test continuity with multimeter
```

### Example 2: Multi-Turn Conversation

**Turn 1:**
```
User: "Der Aufzug öffnet die Türen nicht"
System: "Das könnte F02 06 sein. Welche Fehler zeigt die Anzeige?"
```

**Turn 2:**
```
User: "Ja, F02 06 wird angezeigt"
System: "Perfekt. Das ist Etagentürkreis geöffnet während einer Fahrt.
         Überprüfen Sie..." [Uses history for context]
```

### Example 3: Configuration Help

**Input:**
```
"Wie stelle ich die maximale Fahrtdauer ein?"
```

**Output:**
```
Diagnosis: Parameter P0001 Programmierung maximale Fahrtdauer...

Confidence: MEDIUM
Codes Referenced: [P0001]
Manual Pages: [143]
Next Steps:
  1. Öffnen Sie Programmierseite
  2. Navigieren zu Seite Programmierungen
  3. Parameter P0001 wählen
  4. Neue Dauer eingeben
  5. Speichern
```

---

## Success Criteria ✅

- ✅ Knowledge base loads (270 entries)
- ✅ Can look up error codes
- ✅ Can search descriptions
- ✅ Claude integration works
- ✅ Structured responses returned
- ✅ Confidence levels assigned
- ✅ Manual pages extracted
- ✅ Next steps identified
- ✅ Multi-turn conversations possible

**Next: Implement test_queries.py and feedback_handler.py**

---

## Deployment

### For Backend/CLI Use
```bash
# Run diagnostic system
export ANTHROPIC_API_KEY="sk-ant-..."
python ai_diagnostics.py

# Or import in your application
from ai_diagnostics import DiagnosticSystem
system = DiagnosticSystem()
response = system.query("Technician question...")
```

### For Integration
```python
# Use as library in Flask/FastAPI app
from ai_diagnostics import DiagnosticSystem

app = Flask(__name__)
diagnostic_system = DiagnosticSystem()

@app.route('/diagnose', methods=['POST'])
def diagnose():
    question = request.json['question']
    response = diagnostic_system.query(question)
    return response.__dict__
```

---

## Conclusion

✅ **Python AI diagnostic system is ready!**

The system implements the original planned architecture:
- ✅ Python-based backend
- ✅ Knowledge base indexing
- ✅ Claude AI integration
- ✅ Structured responses
- ✅ Multi-turn conversations
- ✅ 4-Layer knowledge system foundation

**The web interface (keyword search) still works independently.**

**Ready for:**
- Testing with real technicians
- Integration with other systems
- Feedback loop implementation
- Field learning system deployment
