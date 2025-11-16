# LIFTEC LOGICAL ARCHITECTURE
## Building the System: Knowledge Layers, Data Types, and Training Process

---

## 1. KNOWLEDGE LAYER STRUCTURE

Think of it like **nested knowledge domains**:

```
┌─────────────────────────────────────────────────────────┐
│ LAYER 4: FIELD LEARNING (Feedback Loop)                 │
│ ↑ Patterns emerge from real usage                        │
├─────────────────────────────────────────────────────────┤
│ LAYER 3: MODEL QUIRKS (Via CAB Board, etc.)              │
│ ↑ Known issues specific to this model                    │
├─────────────────────────────────────────────────────────┤
│ LAYER 2: MANUFACTURER HANDBOOK (Definitive)              │
│ ↑ Static truth from documentation                        │
├─────────────────────────────────────────────────────────┤
│ LAYER 1: UNIVERSAL LOGIC (How elevators work)            │
│ ↑ Applies to ALL elevators, all brands                   │
└─────────────────────────────────────────────────────────┘
```

**Key principle:** Each layer is **independent** but can be **queried together**.

---

## 2. THREE DATA TYPES (Different Treatment)

### A) STATIC TRUTH (Never changes)
- Error code definitions
- Parameter specifications
- Physical locations
- Safety information

**Treatment:** JSON lookup tables, fast search

### B) STRUCTURED PATTERNS (Extracted from manual)
- Diagnostic flowcharts
- Signal chains
- Component interactions
- Step-by-step procedures

**Treatment:** Template structures that AI fills in

### C) LEARNED PATTERNS (From feedback)
- Which diagnoses were correct
- Frequency of causes
- Edge cases discovered
- Performance metrics

**Treatment:** Database records, statistical analysis

---

## 3. TRAINING PROCESS (How to Build Knowledge)

### Phase 1: Seed with Handbook (Week 1-2)

```
VIA Manual (PDF) → Extract Data
  ├─ Error codes → error_codes.db
  ├─ Parameters → parameters.db
  ├─ Hardware → hardware.db
  └─ Procedures → procedures.db

+ Manual Knowledge (Known issues)
  ├─ CAB Board problems (40% of door issues)
  ├─ Software bugs (v74DEEN issues)
  └─ Hardware weaknesses
  → via_quirks.db
```

**Result:** System can answer any handbook question immediately.

### Phase 2: Teach Problem-Solving Logic (Week 2-3)

```
Create decision trees:
  "Lift won't start?"
    ├─ Display shows A-code?
    │   ├─ Which A-code? → Look up meaning
    │   └─ Check what A-code blocks
    ├─ No A-code?
    │   ├─ Sicherheitskreis?
    │   └─ Spannung?
    └─ Check LED status

Create diagnosis templates:
  "Door won't open"
    ├─ Is it constant or sporadic?
    │   ├─ Constant → Check mechanisch/elektrisch
    │   └─ Sporadic → Check elektronisch
    ├─ What's the LED status?
    └─ Narrow down with more questions
```

**Result:** System can guide through troubleshooting systematically.

### Phase 3: Learn from Feedback (Week 3+, ongoing)

```
Each technician interaction:
  Problem described → Diagnosis given → User confirms/corrects

Store:
  {
    symptom: "Tür öffnet sporadisch",
    diagnosis_suggested: "CAB Board",
    was_correct: true,
    actual_cause: "CAB Board",
    time_spent: 35,
    lift_id: "AT-1234"
  }

Analyze patterns:
  "Sporadisch + CAB LED = Board" → 92% accuracy (was 90%)
  "Never seen this before" → Flag for review
  "This always leads to..." → Add to quirks
```

**Result:** System gets smarter with every real case.

---

## 4. AI DECISION POINTS (Where AI Helps)

The AI model should handle **only what data can't**:

| Task | Why AI Needed | What It Uses |
|------|---------------|--------------|
| **Generate explanation** | Different levels/contexts | Static data + context |
| **Connect patterns** | Cross-reference knowledge | All layers + logic |
| **Ask follow-up questions** | Conditional reasoning | Decision trees + feedback |
| **Explain unfamiliar symptoms** | Reasoning about unknowns | Universal logic + handbook |
| **Prioritize next steps** | Probability-based | Learned patterns + quirks |

**Important:** AI should **cite its source**:
- "According to handbook (Layer 2)..."
- "This is a known Via issue (Layer 3)..."
- "Based on previous cases (Layer 4)..."
- "By elevator logic (Layer 1)..."

---

## 5. SCALABILITY FRAMEWORK (For Multiple Models Later)

### Current (Via only):
```
database/
├── via/
│   ├── error_codes.json
│   ├── parameters.json
│   ├── hardware.json
│   ├── quirks.json
│   └── procedures.json
└── feedback/
    └── via_cases.json
```

### Future (Add EcoGo, Schindler, etc.):
```
database/
├── manufacturers/
│   ├── macpuarsa/
│   │   ├── via/
│   │   │   ├── v73/
│   │   │   ├── v74/
│   │   │   └── v75/
│   │   └── ecogo/
│   │       ├── v2.3/
│   │       └── v2.4/
│   ├── schindler/
│   ├── otis/
│   └── ...
├── universal/
│   ├── elevator_principles.json
│   ├── safety_circuits.json
│   └── common_problems.json
└── feedback/
    ├── via_cases.json
    ├── ecogo_cases.json
    └── ...
```

**Key:** Universal knowledge is **shared**, manufacturer-specific is **isolated**.

---

## 6. SYSTEM COMPONENTS (What to Build)

### Data Layer
- Structured databases (not free text)
- Each knowledge layer separate
- Queryable, versioned, traceable

### Logic Layer
- Decision trees (IF/THEN rules)
- Diagnostic flowcharts
- Probability mappings

### AI Integration Layer
- Takes query + context
- Returns explanation + sources + confidence
- Formats for technician consumption

### Feedback Collection & Analysis
- Captures what was correct/wrong
- Updates probabilities
- Flags new patterns
- Measures system accuracy

---

## 7. SYSTEM PERFORMANCE CONSIDERATIONS

For this to work well **even with multiple models**, you need:

### A) Separation of Concerns
- Via knowledge doesn't contaminate EcoGo knowledge
- Universal knowledge applies everywhere
- Feedback tagged by model (so learnings don't mix)

### B) Versioning
- Track which handbook version
- Track which model version
- Track feedback source/date

### C) Confidence Scoring
- "Based on X feedback cases" (N=15, confidence 92%)
- "Not enough data on this yet" (N=2, confidence 40%)
- "Handbook says X, but field shows Y" (contradiction flag)

### D) Edge Case Handling
- "Unusual combination, similar to..."
- "Never seen exactly this, but..."
- When to defer to human expert

---

## 8. RECOMMENDED TECH STACK (For Solid Growth)

### Knowledge Storage:
- **PostgreSQL** or **SQLite** (structured, queryable)
- **JSON files** for config/lookup tables (fast, simple)
- **Vector database** (pgvector, Weaviate) for semantic search later

### Logic/Rules:
- **Decision trees** stored as JSON/YAML
- **Probability tables** for diagnosis weighting
- **Pattern matching** using regex/fuzzy search

### AI Integration:
- **Claude/GPT API** for explanations & follow-ups
- **Prompt engineering** to cite sources consistently
- **System context** (which knowledge layer to use)

### Feedback System:
- **Simple database** to record outcomes
- **Analysis scripts** to compute statistics
- **Dashboard** to see improvement over time

---

## 9. TRAINING ROADMAP

### Month 1: Foundation
1. Extract Via manual completely → Database
2. Add Via quirks layer
3. Build basic QA (answer handbook questions)
4. Test with 20 sample questions

### Month 2: Logic
1. Create diagnostic flowcharts (decision trees)
2. Add AI explanations
3. Test with 10 real diagnostic scenarios
4. Measure diagnosis accuracy

### Month 3: Learning
1. Deploy feedback collection
2. Run with 50+ real technicians
3. Analyze patterns
4. Update probabilities
5. Document learnings

### Month 4: Scale
1. Add EcoGo (parallel structure)
2. Add universal layer (shared knowledge)
3. Test with mixed queries
4. Optimize performance

---

## 10. KEY QUESTIONS TO DECIDE NOW

1. **Data source:** Do you have Via manual in digital form (PDF, or already extracted)?
2. **AI model:** Claude, OpenAI, open-source? (Different trade-offs)
3. **Deployment:** Cloud API, local server, or hybrid?
4. **Storage:** Database or JSON files to start?
5. **Feedback infrastructure:** How will technicians submit feedback? (App, form, email?)
6. **Version control:** How do you track changes to knowledge?

---

## SUMMARY

This logical structure ensures:
- ✅ Clean separation (doesn't get messy when adding models)
- ✅ Scalable (adding Via v74 or EcoGo is additive, not changing)
- ✅ Measurable (can track improvement)
- ✅ Maintainable (each piece independently upgradeable)

---

**Next steps:**
1. Define **data schema** specifically
2. Plan **AI integration strategy** in detail
3. Design **feedback loop mechanics**
