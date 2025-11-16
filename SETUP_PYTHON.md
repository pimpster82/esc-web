# ESC - Python Environment Setup Guide

## System Information

```
Python: 3.12.3 ✅
pip: 24.0 ✅
Location: /usr/bin/python3
```

Your system is ready, but we need to work around a permissions issue.

---

## OPTION 1: Install Packages to User Home (Recommended)

This is the safest approach - no system access needed.

### Step 1: Install required packages

```bash
cd /mnt/c/daniel_ai_playground/ESC

pip3 install --user pdfplumber jsonschema pandas openpyxl
```

This will install to your user home directory (~/.local/lib/python3.12/site-packages)

### Step 2: Verify installation

```bash
python3 -c "import pdfplumber; print('✅ pdfplumber ready')"
python3 -c "import jsonschema; print('✅ jsonschema ready')"
python3 -c "import pandas; print('✅ pandas ready')"
python3 -c "import openpyxl; print('✅ openpyxl ready')"
```

Expected output:
```
✅ pdfplumber ready
✅ jsonschema ready
✅ pandas ready
✅ openpyxl ready
```

### Step 3: Run scripts

```bash
cd scripts
python3 extract_pdf.py
```

---

## OPTION 2: Use Python Virtual Environment (If venv is available)

If you have access to python3-venv (or get sudo), you can create an isolated environment:

```bash
# Create virtual environment
python3 -m venv /mnt/c/daniel_ai_playground/ESC/venv

# Activate it
source /mnt/c/daniel_ai_playground/ESC/venv/bin/activate

# Install packages
pip install pdfplumber jsonschema pandas openpyxl

# Run scripts (venv will be active in this terminal)
cd scripts
python3 extract_pdf.py
```

To use the venv in future sessions:
```bash
source /mnt/c/daniel_ai_playground/ESC/venv/bin/activate
```

---

## OPTION 3: Install System-Wide (Requires sudo)

If you have sudo access:

```bash
sudo apt-get install python3-venv python3-full
sudo python3 -m pip install pdfplumber jsonschema pandas openpyxl
```

Then you can create a virtual environment as in Option 2.

---

## What Each Package Does

| Package | Purpose | Used By |
|---------|---------|---------|
| **pdfplumber** | Extract tables & text from PDF | extract_pdf.py |
| **jsonschema** | Validate JSON file structure | validate_data.py |
| **pandas** | Data processing & CSV handling | organize_json.py |
| **openpyxl** | Excel file support (optional) | Future use |

---

## Recommended Setup (For ESC POC)

### Quick Setup (5 minutes)

```bash
# Just install to user directory
pip3 install --user pdfplumber jsonschema pandas

# Then run extraction
cd /mnt/c/daniel_ai_playground/ESC/scripts
python3 extract_pdf.py
```

### Full Setup (With virtual environment, if venv available)

```bash
# Create isolated environment
python3 -m venv ~/esc-venv

# Activate
source ~/esc-venv/bin/activate

# Install packages
pip install pdfplumber jsonschema pandas openpyxl

# Then run scripts
cd /mnt/c/daniel_ai_playground/ESC/scripts
python3 extract_pdf.py
```

---

## Verification Checklist

After installation, verify everything works:

```bash
# Check Python
python3 --version
# Expected: Python 3.12.3 or similar

# Check pip
pip3 --version
# Expected: pip 24.0 or similar

# Check packages
python3 -c "import pdfplumber, jsonschema, pandas; print('✅ All ready')"
# Expected: ✅ All ready

# Test scripts are accessible
ls -la /mnt/c/daniel_ai_playground/ESC/scripts/
# Expected: extract_pdf.py, organize_json.py, validate_data.py
```

---

## Directory Structure

After setup, your project should look like:

```
ESC/
├── README.md
├── claude.md
├── requirements.txt
├── SETUP_PYTHON.md           ← You are reading this
├── setup_environment.sh
├── scripts/
│   ├── extract_pdf.py
│   ├── organize_json.py
│   └── validate_data.py
├── data/
│   └── via/v74/
│       ├── error_codes.json
│       ├── parameters.json
│       ├── hardware.json
│       ├── contacts.json
│       ├── connectors.json
│       └── quirks.json
├── manuals/                   ← Put PDF here
└── extracted_raw/             ← Will be created
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pdfplumber'"

**Solution:**
```bash
# Try installing with --user flag
pip3 install --user pdfplumber

# Or use python3 -m pip
python3 -m pip install --user pdfplumber
```

### "Permission denied" when installing

**Solution:** Use `--user` flag (installs to home directory):
```bash
pip3 install --user pdfplumber jsonschema pandas
```

### "pip3: command not found"

**Solution:** Use python module:
```bash
python3 -m pip install --user pdfplumber jsonschema pandas
```

### Virtual environment won't activate

**Solution:** Check if python3-venv is installed:
```bash
python3 -m venv --help
# If this fails, venv is not available
# Use Option 1 instead (--user flag)
```

---

## Quick Start Commands

### One-liner to install everything:
```bash
python3 -m pip install --user pdfplumber jsonschema pandas openpyxl && echo "✅ Setup complete"
```

### One-liner to verify:
```bash
python3 -c "import pdfplumber, jsonschema, pandas; print('✅ All packages ready')"
```

### One-liner to run extraction:
```bash
cd /mnt/c/daniel_ai_playground/ESC/scripts && python3 extract_pdf.py
```

---

## Next Steps After Setup

1. **Verify installation** (run the verification checklist above)
2. **Place PDF** in `manuals/` directory
3. **Run extraction:**
   ```bash
   cd scripts
   python3 extract_pdf.py
   ```
4. **Create templates:**
   ```bash
   python3 organize_json.py
   ```
5. **Populate data** (manual work, 2-3 hours)
6. **Validate:**
   ```bash
   python3 validate_data.py
   ```

---

## Help & Support

If you encounter issues:

1. **Check Python version:** `python3 --version` (should be 3.7+)
2. **Check pip:** `pip3 --version` (should work)
3. **Try alternative install:** `python3 -m pip install --user pdfplumber`
4. **Check internet:** Packages need to download from PyPI
5. **Review error message:** Usually tells you what's wrong

---

## After Setup is Complete

Once packages are installed, you can:

✅ Run extraction scripts
✅ Validate JSON data
✅ Process PDF files
✅ Prepare for AI integration

See: `EXTRACTION_QUICKSTART.md` for next steps

---

*Last updated: 2025-11-16*
*ESC POC v1.0*
