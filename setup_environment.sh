#!/bin/bash
# ESC - Elevator Service Companion
# Python Environment Setup Script

echo "========================================================================"
echo "ESC - PYTHON ENVIRONMENT SETUP"
echo "========================================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Project directory: $PROJECT_DIR"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ Found: $PYTHON_VERSION${NC}"
echo ""

# Check pip
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed${NC}"
    echo "Installing pip3..."
    python3 -m ensurepip --upgrade
fi

PIP_VERSION=$(pip3 --version)
echo -e "${GREEN}✅ Found: $PIP_VERSION${NC}"
echo ""

# Create virtual environment (optional but recommended)
echo "Creating Python virtual environment..."
if [ ! -d "$PROJECT_DIR/venv" ]; then
    python3 -m venv "$PROJECT_DIR/venv"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$PROJECT_DIR/venv/bin/activate"
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

# Install requirements
echo "Installing required packages..."
echo "Installing: pdfplumber, jsonschema, pandas, openpyxl"
echo ""

pip3 install -r "$PROJECT_DIR/requirements.txt"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All packages installed successfully!${NC}"
else
    echo ""
    echo -e "${RED}❌ Some packages failed to install${NC}"
    exit 1
fi

# Verify installation
echo ""
echo "Verifying installation..."
echo "---"

python3 -c "import pdfplumber; print(f'✅ pdfplumber: {pdfplumber.__version__}')" 2>/dev/null || echo -e "${RED}❌ pdfplumber failed${NC}"
python3 -c "import jsonschema; print(f'✅ jsonschema: {jsonschema.__version__}')" 2>/dev/null || echo -e "${RED}❌ jsonschema failed${NC}"
python3 -c "import pandas; print(f'✅ pandas: {pandas.__version__}')" 2>/dev/null || echo -e "${RED}❌ pandas failed${NC}"
python3 -c "import openpyxl; print(f'✅ openpyxl: {openpyxl.__version__}')" 2>/dev/null || echo -e "${RED}❌ openpyxl failed${NC}"

echo "---"
echo ""

# Create directories
echo "Creating project directories..."
mkdir -p "$PROJECT_DIR/manuals"
mkdir -p "$PROJECT_DIR/extracted_raw"
mkdir -p "$PROJECT_DIR/data/via/v74"
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Final message
echo "========================================================================"
echo -e "${GREEN}SETUP COMPLETE!${NC}"
echo "========================================================================"
echo ""
echo "To activate the environment in the future, run:"
echo -e "${YELLOW}source $PROJECT_DIR/venv/bin/activate${NC}"
echo ""
echo "To deactivate, run:"
echo -e "${YELLOW}deactivate${NC}"
echo ""
echo "Next steps:"
echo "1. Place Via manual PDF in: manuals/"
echo "2. Run extraction: cd scripts && python3 extract_pdf.py"
echo "3. Populate JSON files with data"
echo "4. Validate: python3 validate_data.py"
echo ""
echo "========================================================================"
