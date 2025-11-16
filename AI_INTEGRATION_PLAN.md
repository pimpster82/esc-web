# Phase 2: AI Integration Plan

## Overview

Transform our 270 extracted data entries into an intelligent diagnostic system using Claude API.

---

## Architecture: 4-Layer Knowledge System

```
LAYER 1: UNIVERSAL LOGIC
├─ How elevators work (general principles)
├─ Common mechanical/electrical issues
└─ Diagnostic reasoning patterns

LAYER 2: HANDBOOK DATA (OUR EXTRACTED DATA)
├─ 26 Error codes with descriptions + causes
├─ 93 Parameters with context
├─ 151 Component/abbreviation definitions
└─ Technical specifications from manual

LAYER 3: VIA-SPECIFIC QUIRKS
├─ Known problematic components
├─ Common failure patterns for this model
├─ Workarounds and tips
└─ (Can be populated with field experience)

LAYER 4: FIELD LEARNING (Feedback Loop)
├─ Cases resolved successfully
├─ Confidence scores by diagnosis type
├─ Common misdiagnoses and corrections
└─ (Learns from actual technician feedback)
```

---

## Implementation Strategy

### Step 1: Create System Prompt
Build Claude's instructions that tell it:
- How to use the 4-layer knowledge system
- When to cite Layer 2 data (handbook)
- How to express confidence levels
- When to ask for more information

### Step 2: Create Query Interface
Build a Python interface that:
- Takes technician questions in German or English
- Formats context with relevant data from JSON files
- Passes query + context to Claude API
- Returns structured diagnostic response

### Step 3: Test with Sample Queries
Test the system with:
- "F01 02 error, what does it mean?"
- "How to configure P0001?"
- "What is XTSS connector?"
- "Elevator won't open doors"
- etc.

### Step 4: Implement Feedback Loop
Add ability to:
- Capture whether diagnosis was correct
- Update confidence scores
- Store successful case patterns
- Learn from corrections

---

## Components to Build

### 1. `ai_diagnostics.py` - Main Query Interface
```
Usage:
  diagnosis = DiagnosticSystem()
  response = diagnosis.query("F01 02 was found - what's the issue?")
  print(response.explanation)
  print(response.confidence)
  print(response.next_steps)
```

### 2. `system_prompt.py` - Claude Instructions
Defines how Claude should:
- Interpret error codes
- Explain parameters
- Reference components
- Structure responses
- Handle uncertainty

### 3. `knowledge_loader.py` - Load JSON Data
Reads and indexes:
- error_codes.json
- parameters.json
- abbreviations.json
- Creates searchable knowledge base

### 4. `test_queries.py` - Sample Diagnostics
Test suite with:
- Real error code questions
- Parameter configuration queries
- Component identification
- Complex multi-symptom cases

---

## System Prompt Structure

**Core Instruction:**
```
You are an expert elevator technician assistant for Via Series elevators.
You have access to the official Via Series manual data:
- 26 error codes with complete descriptions and causes
- 93 parameters across different system sections
- 151 component/connector definitions

When answering questions:
1. Always cite which manual section you're referencing
2. Show confidence level (high/medium/low)
3. Provide practical next diagnostic steps
4. Never guess - ask for clarification if uncertain
5. Use German technical terms when appropriate
```

**Data Context:**
```
ERROR CODES (F-codes):
[26 codes provided as JSON]

PARAMETERS (P-codes):
[93 parameters provided as JSON]

ABBREVIATIONS:
[151 codes provided as JSON]
```

---

## Implementation Steps

### Phase 2a: Setup (30 min)
- [ ] Create `ai_diagnostics.py`
- [ ] Create `system_prompt.py`
- [ ] Create `knowledge_loader.py`
- [ ] Test basic API connection

### Phase 2b: Core Functionality (1-2 hours)
- [ ] Query parsing (German/English)
- [ ] Data retrieval from JSON files
- [ ] Claude API integration
- [ ] Response formatting

### Phase 2c: Testing (1-2 hours)
- [ ] Test with 10 sample queries
- [ ] Verify accuracy against manual
- [ ] Check response quality
- [ ] Validate confidence scores

### Phase 2d: Feedback Loop (1 hour)
- [ ] Capture user confirmation
- [ ] Update confidence metrics
- [ ] Store successful cases
- [ ] Create learning dashboard

---

## Example Query Flow

**User asks:** "F01 02 occurred - what do I check?"

**System processes:**
1. Parses: Error code = "F01 02"
2. Looks up in error_codes.json
3. Finds: "Sicherheitskreis geöffnet" + full cause text
4. Retrieves related components: "1H", "3C" from cause
5. Looks up: 1H, 3C in abbreviations.json
6. Queries Claude with:
   - System prompt (expert instructions)
   - Error definition + causes
   - Component descriptions
   - Related parameters that might affect it

**Claude responds:**
```
F01 02 - SAFETY CIRCUIT OPEN

From Manual:
Sicherheitskreis geöffnet (Safety circuit opened)

Likely Causes:
1. Contacts between points 1H and 3C are open
2. Wiring break in safety circuit
3. Sensor malfunction

Check These Components First:
- 1H: [definition from abbreviations]
- 3C: [definition from abbreviations]
- XTSS: [connector definition]

Next Diagnostic Steps:
1. Visually inspect wiring between 1H and 3C
2. Check XTSS connector for loose pins
3. Test continuity with multimeter
4. Check P0xxx parameters affecting circuit

Confidence: HIGH (from manual data)
```

---

## Files to Create

```
scripts/
├── ai_diagnostics.py       (Main interface)
├── system_prompt.py        (Claude instructions)
├── knowledge_loader.py     (JSON indexing)
├── test_queries.py         (Sample tests)
└── feedback_handler.py     (Learning system)

data/via/v74/
├── error_codes.json        (already exists)
├── parameters.json         (already exists)
├── abbreviations.json      (already exists)
└── feedback_log.json       (new - store learning)
```

---

## Success Criteria for Phase 2

✅ System can answer error code questions
✅ System can explain parameters
✅ System can identify components
✅ System cites manual sources
✅ System expresses uncertainty appropriately
✅ All queries return structured JSON response
✅ Can process German and English questions

---

## Timeline

- **Phase 2a (Setup):** 30 min
- **Phase 2b (Core):** 1-2 hours
- **Phase 2c (Testing):** 1-2 hours
- **Phase 2d (Feedback):** 1 hour

**Total Phase 2: ~4-5 hours**

Then:
- **Phase 3 (Optimization):** Tweak prompts, improve accuracy
- **Phase 4 (Deployment):** Package as service/CLI tool

---

## API Requirements

Need:
- Claude API key (from Anthropic)
- Python claude SDK (`pip install anthropic`)
- Our 270 extracted data entries (✅ ready)

---

## Next Action

Ready to start? We can:

**Option A:** Build it now (I'll code the full system)
**Option B:** Plan it out more (design phase first)
**Option C:** Start with one component (e.g., just knowledge_loader.py)

What would you prefer?
