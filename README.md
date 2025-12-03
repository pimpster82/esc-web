# 🛗 ESC - Elevator Service Companion

AI-gestütztes Diagnose-System für Via-Series Aufzugstechniker.

## Features

- 🤖 **Claude AI Integration** - Intelligente Diagnosen mit natürlicher Sprache
- 📚 **Umfangreiche Wissensdatenbank** - 271 Einträge (26 Fehlercodes, 93 Parameter, 151 Komponenten)
- 🇩🇪 **Deutsche Benutzeroberfläche** - Vollständig auf Deutsch
- 📊 **Feedback-System** - Verbesserung durch Nutzer-Feedback
- ⚡ **Offline-Modus** - Fallback auf Stichwortsuche

## Tech Stack

- **Frontend**: Pure HTML/CSS/JavaScript
- **Backend**: Python Flask + Claude AI API
- **Deployment**: Railway (empfohlen)

## 🚀 Deployment auf Railway

### Voraussetzungen

1. [Railway Account](https://railway.app/) erstellen
2. [Claude API Key](https://console.anthropic.com/) besorgen

### Deployment-Schritte

1. **Repository auf Railway deployen**:
   - Gehe zu [railway.app/new](https://railway.app/new)
   - Wähle "Deploy from GitHub repo"
   - Wähle dieses Repository aus
   - Railway erkennt automatisch die Python-App

2. **Environment Variables konfigurieren**:
   - Gehe zu deinem Railway-Projekt
   - Klicke auf "Variables"
   - Füge hinzu:
     ```
     ANTHROPIC_API_KEY=dein-api-key-hier
     ```

3. **Deployment starten**:
   - Railway deployed automatisch
   - Nach dem Deployment bekommst du eine URL (z.B. `https://dein-projekt.railway.app`)

4. **Testen**:
   - Öffne die Railway-URL in deinem Browser
   - Du solltest die ESC-Oberfläche sehen
   - Der Status-Badge sollte grün sein: "✅ 271 Einträge geladen | AI bereit"

### Railway CLI (Optional)

```bash
# Railway CLI installieren
npm install -g @railway/cli

# Einloggen
railway login

# Projekt verknüpfen
railway link

# Environment Variable setzen
railway variables set ANTHROPIC_API_KEY=dein-key-hier

# Logs anschauen
railway logs
```

## 💻 Lokale Entwicklung

### Setup

```bash
# Repository klonen
git clone https://github.com/pimpster82/esc-web.git
cd esc-web

# Python Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Environment Variables konfigurieren
cp .env.example .env
# .env editieren und ANTHROPIC_API_KEY eintragen
```

### Server starten

```bash
# Mit gunicorn (Produktions-Modus)
gunicorn web_api:app

# Oder direkt mit Python (Development-Modus)
python3 web_api.py

# Server läuft auf http://localhost:8080
```

### Lokal testen

1. Browser öffnen: `http://localhost:8080`
2. Beispiel-Frage stellen: "Was ist SMQ?"
3. Feedback geben: Antwort bewerten (Ja/Nein/Unsicher)

## 📁 Projektstruktur

```
esc-web/
├── index.html           # Frontend SPA
├── knowledge.json       # Wissensdatenbank (271 Einträge)
├── web_api.py          # Flask Backend + Claude Integration
├── requirements.txt    # Python Dependencies
├── Procfile           # Railway/Heroku Konfiguration
├── railway.toml       # Railway-spezifische Config
├── runtime.txt        # Python Version
├── .env.example       # Beispiel für Environment Variables
├── .gitignore         # Git Ignore Regeln
└── README.md          # Diese Datei
```

## 🔧 API Endpoints

### `GET /api/knowledge-summary`
Gibt eine Zusammenfassung der Wissensdatenbank zurück.

**Response**:
```json
{
  "success": true,
  "summary": {
    "total": 271,
    "error_codes": 26,
    "parameters": 93,
    "components": 151
  }
}
```

### `POST /api/query`
Verarbeitet eine Diagnose-Anfrage mit Claude AI.

**Request**:
```json
{
  "question": "Was ist SMQ?",
  "use_history": true
}
```

**Response**:
```json
{
  "success": true,
  "diagnosis": "SMQ ist die Safety Monitoring and Control Board...",
  "confidence": "HIGH",
  "codes_referenced": ["SMQ"],
  "manual_pages": ["113", "141"]
}
```

### `POST /api/feedback`
Speichert Nutzer-Feedback.

**Request**:
```json
{
  "query": "Was ist SMQ?",
  "response": "SMQ ist...",
  "feedback": "correct",
  "confidence": "HIGH",
  "notes": "Sehr hilfreich"
}
```

**Response**:
```json
{
  "success": true
}
```

### `GET /health`
Health Check Endpoint für Railway.

**Response**:
```json
{
  "status": "healthy",
  "knowledge_loaded": true,
  "entries": 271
}
```

## 📚 Wissensdatenbank

Die `knowledge.json` enthält:

- **26 Fehlercodes** (F01 02 bis F11 13)
  - Beispiel: `F01 02` - Sicherheitskreis geöffnet
  - Beispiel: `F10 01` - Maximale Fahrtdauer überschritten

- **93 Parameter** (P0001-P0015 pro Kategorie)
  - Beispiel: `P0001` - Anzahl Haltestellen
  - Beispiel: `P0007` - Nenngeschwindigkeit

- **151 Hardware-Komponenten**
  - Beispiel: `SMQ` - Safety Monitoring and Control Board
  - Beispiel: `XTSS` - Sicherheitskreis-Spannungsanschluss

Alle Einträge mit deutschen Beschreibungen und Handbuch-Referenzen.

## 🔐 Sicherheit

- API-Key wird über Environment Variables verwaltet
- `.env` Datei ist in `.gitignore` und wird nicht committed
- CORS ist aktiviert für Frontend-API-Kommunikation
- Feedback wird lokal in `feedback.json` gespeichert (nicht in Git)

## 🐛 Troubleshooting

### "API nicht verfügbar" Fehler

**Problem**: Frontend zeigt "⚠️ Offline Modus - nur Stichwortsuche"

**Lösung**:
1. Überprüfe, ob der Backend-Server läuft
2. Prüfe Railway Logs: `railway logs`
3. Stelle sicher, dass `ANTHROPIC_API_KEY` gesetzt ist
4. Teste Health Endpoint: `curl https://deine-url.railway.app/health`

### "Claude API error" Fehler

**Problem**: Claude AI Anfragen schlagen fehl

**Lösung**:
1. Überprüfe API Key Gültigkeit auf [console.anthropic.com](https://console.anthropic.com/)
2. Prüfe Claude API Credits/Limits
3. Schaue in Railway Logs nach detaillierten Fehlermeldungen

### Railway Deployment schlägt fehl

**Problem**: Build oder Start schlägt fehl

**Lösung**:
1. Prüfe `railway logs` für Details
2. Stelle sicher, dass `requirements.txt` korrekt ist
3. Prüfe Python Version in `runtime.txt`
4. Verifiziere `Procfile` Syntax

## 📝 Lizenz

Dieses Projekt ist für interne Verwendung bestimmt.

## 👥 Support

Bei Fragen oder Problemen:
1. Railway Logs prüfen: `railway logs`
2. Issue auf GitHub erstellen
3. API Health Check durchführen: `/health` Endpoint

## 🚀 Nächste Schritte

Nach dem Deployment:
1. ✅ URL testen und sicherstellen, dass AI funktioniert
2. 📝 Erste Diagnose-Anfrage stellen
3. 💾 Feedback geben um System zu verbessern
4. 🔧 Bei Bedarf weitere Einträge zur `knowledge.json` hinzufügen

---

**Made with ❤️ for Via Series Elevator Technicians**
