# Push ESC Python System to GitHub

## Schritt 1: Neues Repository auf GitHub erstellen

1. Gehe zu: https://github.com/new
2. Repository Name: `esc` oder `esc-ai` oder `elevator-service-companion`
3. Beschreibung: "AI-powered elevator diagnostic system using Claude"
4. Make it Public (optional - für Tests)
5. Click "Create repository"

## Schritt 2: Remote hinzufügen und pushen

```bash
cd /mnt/c/daniel_ai_playground/ESC

# Ersetze USERNAME und REPONAME mit deinen Werten
git remote add origin git@github.com:USERNAME/REPONAME.git
git branch -M main
git push -u origin main
```

## Beispiel (wenn Username = "pimpster82" und Repo = "esc"):

```bash
git remote add origin git@github.com:pimpster82/esc.git
git branch -M main
git push -u origin main
```

## Überprüfe ob es funktioniert:

```bash
git remote -v
# Sollte zeigen:
# origin	git@github.com:pimpster82/esc.git (fetch)
# origin	git@github.com:pimpster82/esc.git (push)
```

## Was wird gepusht:

```
scripts/
├── knowledge_loader.py    ✅ 270 data entries
├── system_prompt.py       ✅ Claude instructions
├── ai_diagnostics.py      ✅ Main diagnostic system
└── ... (andere scripts)

test_ai_simple.py         ✅ Interactive tester
AI_INTEGRATION_PLAN.md    ✅ Original plan
PYTHON_AI_SYSTEM_READY.md ✅ Documentation
data/via/v74/            ✅ JSON data files
```

## Danach kannst du testen mit:

```bash
# Clone it
git clone git@github.com:USERNAME/esc.git

# Setup
export ANTHROPIC_API_KEY="sk-ant-..."
pip install anthropic

# Test
python test_ai_simple.py
```

Lass mich wissen wenn du dein Repository erstellt hast - dann kann ich den Rest pushen!
