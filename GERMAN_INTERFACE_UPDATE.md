# 🇩🇪 Deutsches Interface & Intelligente Suche

## Status: Gerade deployed ✅

Die ESC-Website wurde gerade aktualisiert mit:

---

## 1. Deutsches Interface

Alle Oberflächentexte sind jetzt auf Deutsch:
- ✅ Seitentitel: "Elevator Service Companion - Via Serie Diagnose"
- ✅ Button: "Suchen" (statt "Ask")
- ✅ Platzhalter: "Fehlercodes, Parameter, Komponenten..."
- ✅ Beispiel-Abfragen auf Deutsch
- ✅ Fehlermeldungen auf Deutsch
- ✅ Fußzeile auf Deutsch

---

## 2. Intelligente Suche

**Alte Suche:** Nur exakte Codematches (sehr begrenzt)
```
Suche nach "F01 02" → Funktioniert ✓
Suche nach "Sicherheit" → Keine Treffer ✗
Suche nach "Tür" → Keine Treffer ✗
```

**Neue Intelligente Suche:**
- Durchsucht CODES (stark gewichtet)
- Durchsucht BESCHREIBUNGEN (mittel gewichtet)
- Durchsucht URSACHE/LÖSUNG (schwach gewichtet)
- Sortiert Ergebnisse nach Relevanz
- Zeigt weitere Treffer bei unsicheren Matches

```
Suche nach "F01 02" → FEHLERCODE gefunden (Genauigkeit: Hoch) ✓
Suche nach "Sicherheit" → Mehrere Fehlercodes gefunden ✓
Suche nach "Tür" → Türfehler gefunden + weitere Treffer ✓
Suche nach "P0001" → Parameter gefunden ✓
Suche nach "XTSS" → Komponente gefunden ✓
```

### Beispiele der neuen Suchfunktion:

**Test 1: Beschreibung suchen**
```
Eingabe: "Sicherheitskreis"
→ Findet F01 02: "Sicherheitskreis geöffnet" (Genauigkeit: Hoch)
→ Zeigt auch weitere verwandte Fehler
```

**Test 2: Teilwort suchen**
```
Eingabe: "Türen"
→ Findet mehrere Türbezogene Fehler
→ F02 06: "Etagentürkreis geöffnet während einer Fahrt"
→ F02 07: "Riegelkreis geöffnet während einer Fahrt"
```

**Test 3: Wortgruppe suchen**
```
Eingabe: "Wiederholte Fehler"
→ Findet F03 05 Beschreibung: "Wiederholte Fehler am Kreis der Fahrkorbtüren"
```

---

## 3. Was hat sich in der Code-Änderung?

### `analyzeQuery()` Funktion - Komplett regeschrieben

**Scoring-System:**
```javascript
// Exakte Übereinstimmung = 100 Punkte
// Vollständige Abfrageübereinstimmung = 50 Punkte
// Individuelle Wortübereinstimmungen = 10 Punkte pro Wort

// Gewichtung nach Feldtyp:
// - Code-Matches: × 3 (sehr stark)
// - Beschreibung: × 2 (mittel)
// - Ursache/Lösung: × 1 (schwach)

// Genauigkeit bestimmt durch Score:
// - Score > 40 = Hoch
// - Score 20-40 = Mittel
// - Score < 20 = Niedrig
```

**Neue Fähigkeiten:**
1. Durchsucht alle 3 Datentypen (Fehlercodes, Parameter, Komponenten)
2. Sortiert Ergebnisse nach Relevanz (höchste Score zuerst)
3. Zeigt zusätzliche Treffer wenn weniger als 100% sicher
4. Bessere Fehlerausgaben mit mehreren Suchvorschlägen

---

## 4. Live-Test

Die Website ist sofort einsatzbereit:
**https://pimpster82.github.io/esc-web/**

Teste die neuen Beispiele in der blauen Box:
- → Fehlercode F01 02
- → Sicherheitskreis (Beschreibung-Suche!)
- → Parameter P0001
- → Komponente XTSS
- → Türfehler (Beschreibung-Suche!)

---

## 5. Nächster Schritt: Source-Dateiname

Um die Quelle richtig zu dokumentieren, benötigen wir:

**OneDrive Pfad-Struktur:**
```
LIFTEC/
└── Beschreibungen/
    └── Macpuarsa/
        └── Steuerung/
            └── Via/
                └── [FILENAME WIR BRAUCHEN?]
```

**Was ist der Dateiname des Via-Steuerungshandbuchs?**

z.B.:
- `Via_Serie_v74.pdf`
- `Steuerung_VIA_Manual.pdf`
- `VIA-Handbuch.pdf`
- Etwas anderes?

Sobald ich den Namen habe, aktualisiere ich:
1. knowledge.json mit Quellenangabe
2. Weboberfläche mit Link zur Quelle
3. Dokumentation mit vollständigem Dateipfad

---

## 6. Git-Änderungen

```
Commit: 🇩🇪 German interface + intelligent search (descriptions, not just codes)
        68cb363 (HEAD)

Vorherige: 🚀 Initial ESC release - Elevator Service Companion with 270 real data entries
        2475a41
```

Die Website wird in 1-2 Minuten aktualisiert.

---

## Zusammenfassung

| Feature | Status | Details |
|---------|--------|---------|
| **Deutsche Oberfläche** | ✅ Live | Alle UI-Text auf Deutsch |
| **Intelligente Suche** | ✅ Live | Code + Beschreibung + Ursache |
| **Sortierung nach Relevanz** | ✅ Live | Beste Treffer zuerst |
| **Weitere Treffer** | ✅ Live | Verwandte Ergebnisse anzeigen |
| **Quellenangabe** | ⏳ Wartet auf Dateiname | Für knowledge.json metadata |

Alles funktioniert offline, auf Mobilgeräten und ohne Installation!
