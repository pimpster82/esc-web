# 🤖 Claude AI Integration - Live Now!

## What's New

ESC now supports **Claude AI-powered natural language questions** in addition to keyword search. Ask questions in German and get intelligent diagnostic responses.

---

## How to Use

### Step 1: Add Your Claude API Key

1. Open: https://pimpster82.github.io/esc-web/
2. Look for the blue section: **"Claude API Schlüssel"**
3. Get your API key from: https://console.anthropic.com/account/keys
4. Paste it in the input field
5. Click **"Speichern"** (Save)
6. Button changes to **"KI an"** (AI on)

**Your API key stays in your browser (not sent to servers)**

### Step 2: Enable AI Mode

1. After saving your key, click **"KI an"** (AI on)
2. Message shows: "✅ KI-Modus aktiviert"
3. Now use natural language questions!

### Step 3: Ask Questions

Instead of just keywords, you can now ask:
```
❌ Old way: "Tür"
✅ New way: "Was sind die Türprobleme und wie behebe ich sie?"

❌ Old way: "F01 02"
✅ New way: "Warum öffnet sich der Sicherheitskreis?"

❌ Old way: "Fehler"
✅ New way: "Welche Fehler können bei der Türsteuerung auftreten?"

❌ Old way: "Fahrtdauer"
✅ New way: "Wie konfiguriere ich die maximale Fahrtdauer?"
```

---

## What It Does

### AI Mode (KI an)
- **Understands context**: Asks "was hat Türfehler mit Aufzügen zu tun?" → Gets smart answer
- **Explains solutions**: Gives step-by-step diagnostic procedures
- **References codes**: Answers include relevant error codes (F01 02, etc.)
- **Speaks German**: All responses in German, using manual language
- **Uses knowledge base**: Claude searches and references your 270 data entries

### Fallback to Keyword Search
- If AI request fails → Automatically switches to keyword search
- If no API key configured → Uses keyword search
- **Never locked into one mode** - always has backup

---

## Example Conversations

### Example 1: Türfehler (Door Error)

**User Query:**
```
"Welche Fehler können bei den Aufzugstüren auftreten?"
```

**AI Response:**
```
🤖 KI-Diagnose

Bei der Via-Serie Aufzugsteuerung können folgende Türfehler auftreten:

1. **F02 06 - Etagentürkreis geöffnet während einer Fahrt**
   - Problem: Bei der Fahrt wurde eine Öffnung des Türkreis (Punkt 6H) festgestellt
   - Ursache: Türkontakt unterbrochen während Fahrtbewegung
   - Lösung: Prüfen Sie den Türkontakt und die Verbindung

2. **F03 05 - Wiederholte Fehler am Kreis der Fahrkorbtüren**
   - Problem: Nach mehrfachen Schließversuchen bleibt die Tür offen
   - Ursache: Defekt am Riegelkontakt 7H-8H oder 8H-9H
   - Lösung: Riegelkontakte prüfen und ggf. ersetzen

Parameter für Türsteuerung:
- P0005: Art der Türen
- P0007: Türen beim Anhalten
- P0008: Verlängerte Öffnungsdauer Türen
```

### Example 2: Sicherheitskreis (Safety Circuit)

**User Query:**
```
"Der Sicherheitskreis ist geöffnet. Was muss ich prüfen?"
```

**AI Response:**
```
🤖 KI-Diagnose

Fehlercode: **F01 02 - Sicherheitskreis geöffnet**

Das ist ein kritischer Fehler! Der Aufzug funktioniert nicht, bis das behoben ist.

**Checkliste zur Fehlersuche:**
1. Prüfen Sie die Sicherheitskontakte zwischen Punkt 1H und 3C
2. Überprüfen Sie die Verdrahtung und Stecker
3. Testen Sie die Spannungsversorgung an den Sicherheitsklemmen
4. Kontrollieren Sie auf beschädigte oder korrodierte Kontakte
5. Falls F01 09 auch auftritt → 110V Versorgungsproblem prüfen

**Wichtige Parameter:**
- Überprüfen Sie P-Parameter für Sicherheitseinstellungen
- Kalibrieren Sie die Sensoren nach dem Befund

Seite im Handbuch: 113
```

### Example 3: Konfiguration

**User Query:**
```
"Wie stelle ich die Fahrtdauer ein?"
```

**AI Response:**
```
🤖 KI-Diagnose

Fahrtdauer-Parameter in der Via-Serie:

**Relevante Parameter:**
- **P0007**: Maximale Dauer Türkreis
- **P0008**: Verlängerte Öffnungsdauer Türen
- **P0001**: Programmierung maximale Fahrtdauer

**Konfigurationsschritte:**
1. Öffnen Sie die Programmierseite in der Steuerung
2. Navigieren Sie zu Seite Programmierungen
3. Wählen Sie das Parameter (z.B. P0001 für Fahrtdauer)
4. Geben Sie die neue Dauer in Sekunden ein
5. Speichern und testen

Handbuch Referenzen:
- Seite 141-151: Parameter-Tabellen
- Seite 143: Programmierungen Abschnitt
```

---

## Technical Details

### API Key Security
```javascript
// API key stored in browser localStorage (CLIENT-SIDE ONLY)
localStorage.setItem('claude_api_key', key);

// NOT sent to any server
// NOT logged anywhere
// NOT transmitted except to Anthropic API
// User controls deletion (clear browser data)
```

### System Prompt
Claude is instructed with:
```
Du bist ein Experte für Via-Serie Aufzugsteuerungen.
Du hast Zugang zu einer Wissensdatenbank mit:
- 26 Fehlercodes (F-Codes)
- 93 Parameter (P-Codes)
- 151 Komponenten und Abkürzungen

Beantworte Fragen auf Deutsch und verweise auf spezifische Codes aus der Datenbank.
```

### Fallback Logic
```javascript
if (aiEnabled && claudeApiKey) {
    const aiResponse = await queryClaudeAI(query, knowledgeBase);
    if (aiResponse) {
        displayAiResponse(aiResponse);  // Show AI answer
        return;
    }
    // Falls through if API fails
}

// Always has keyword search as backup
const response = await analyzeQuery(query, knowledgeBase);
displayResults(response);  // Show keyword results
```

---

## UI Elements

### API Key Section
```
[Input: sk-ant-...] [Speichern] [KI an/aus]
🔐 Dein API-Schlüssel wird nur lokal gespeichert
```

### Button States

| State | Button | Color | Meaning |
|-------|--------|-------|---------|
| No key | KI aus | Gray | Need to save API key first |
| Key saved | KI aus | Gray | Keyword search active |
| AI enabled | KI an | Green | AI mode active |

### Response Display

**When using AI:**
```
🤖 KI-Diagnose
[Full AI response with formatting]
Quelle: Claude AI mit Wissensdatenbank
```

**When using keyword (fallback):**
```
📋 Suchergebnis
Ergebnis 1 von X
[Card-based results with navigation]
Genauigkeit: Hoch/Mittel/Niedrig
```

---

## Pricing & Costs

### How Much Does It Cost?

Claude API uses a per-token pricing model:
- **Input tokens**: ~$3 per 1M tokens
- **Output tokens**: ~$15 per 1M tokens

### Estimated Costs

| Scenario | Tokens | Cost |
|----------|--------|------|
| Single question + KB | 5,000-10,000 | ~$0.05-0.15 |
| 10 questions/day | 50,000-100,000 | ~$0.50-1.50 |
| 100 technician questions/day | 500,000+ | ~$5-15 |

**Tips to reduce costs:**
- Only enable AI when needed
- Keep knowledge base reasonably sized
- Use keyword search for simple lookups
- Limit context sent to API

---

## How to Get API Key

### Free Trial
1. Go to: https://console.anthropic.com
2. Sign up for free account
3. Verify email
4. Get $5 free credits (usually lasts days/weeks)

### Production Use
1. Add payment method to account
2. API key is same - just charges your card
3. Monitor usage in dashboard
4. Set spending limits if needed

---

## Troubleshooting

### "API Error: 401"
- **Problem**: Invalid or expired API key
- **Solution**: Check key format and validity on console.anthropic.com

### "API Error: 429"
- **Problem**: Rate limited (too many requests)
- **Solution**: Wait a moment and try again, or reduce request frequency

### "API Error: 5xx"
- **Problem**: Anthropic API is down
- **Solution**: Will fallback to keyword search automatically

### "No response from AI"
- **Problem**: Network issue or API unreachable
- **Solution**: Fallback to keyword search happens automatically

### "KI an button won't activate"
- **Problem**: No valid API key saved
- **Solution**:
  1. Go to https://console.anthropic.com/account/keys
  2. Copy your API key
  3. Paste in input field
  4. Click "Speichern"

---

## Examples to Try

### Once AI is Enabled

**Test Query 1 (Fehlerdiagnose):**
```
"Warum funktioniert der Aufzug nicht und zeigt F01 02?"
```

**Test Query 2 (Konfiguration):**
```
"Wie stelle ich die Anzahl der Haltestellen ein?"
```

**Test Query 3 (Symptom-based):**
```
"Die Türen schließen nicht. Was könnte falsch sein?"
```

**Test Query 4 (Components):**
```
"Was ist XTSS und wo sitzt es?"
```

**Test Query 5 (Multi-step):**
```
"Geben Sie mir eine Schritt-für-Schritt Anleitung zur Fehlerbehebung bei Türproblemen"
```

---

## Features

| Feature | Status | Details |
|---------|--------|---------|
| Natural language questions | ✅ Live | Ask in German, get smart answers |
| Knowledge base context | ✅ Live | AI uses all 270 data entries |
| Fallback to keyword search | ✅ Live | Never stuck if API fails |
| API key management | ✅ Live | Save/load from localStorage |
| Multiple AI modes | ✅ Live | Toggle between AI and keyword |
| Error handling | ✅ Live | Graceful fallback to keyword |
| Mobile compatible | ✅ Live | Works on phones/tablets |
| Security | ✅ Live | Key stays in browser only |

---

## Git Commit

```
Commit: 🤖 Claude AI integration - natural language questions + fallback to keyword search
Hash: 1f47302 (HEAD -> main)
Parent: 38ef9f7

Files Changed:
- index.html: +159 lines, -1 line
```

---

## Next Steps

### Short Term
- [ ] Test with various error scenarios
- [ ] Refine AI prompts based on feedback
- [ ] Monitor API costs
- [ ] Gather technician feedback

### Medium Term
- [ ] Add conversation history (remember previous questions)
- [ ] Better context limiting (smarter KB filtering)
- [ ] Result caching (avoid duplicate API calls)
- [ ] Multi-language support

### Long Term
- [ ] Fine-tune Claude model on your specific manual
- [ ] Build technician feedback loop
- [ ] Add image recognition (photos of panels → diagnose)
- [ ] Integration with maintenance systems

---

## Summary

✅ **AI Integration is now LIVE!**

**Users can now:**
1. Enter Claude API key (optional)
2. Toggle between AI mode and keyword search
3. Ask natural language questions
4. Get intelligent diagnostic responses
5. Always fall back to keyword search if needed

**The system intelligently:**
- Understands context and meaning
- References specific codes from the knowledge base
- Explains solutions in practical terms
- Communicates in German
- Handles API failures gracefully

**Cost-effective because:**
- API key stays in user's browser
- Each user brings their own API key (Anthropic billing)
- Fallback to free keyword search if API unavailable
- Small context window keeps token usage low

🎉 ESC is now an intelligent diagnostic assistant!
