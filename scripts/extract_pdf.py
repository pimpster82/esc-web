#!/usr/bin/env python3
"""
Extract Via Manual PDF → Structured JSON
LIFTEC POC - Data Extraction Tool
"""

import pdfplumber
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
PDF_PATH = "../manuals/Handbuch VIA MTIPIEPVS_308_DE.pdf"  # Updated with actual file
OUTPUT_DIR = "../data/via/v74"
RAW_EXTRACT_DIR = "../extracted_raw"

# Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RAW_EXTRACT_DIR, exist_ok=True)

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf = None
        self.extraction_log = []

    def open_pdf(self):
        """Open PDF and verify it's searchable"""
        try:
            self.pdf = pdfplumber.open(self.pdf_path)
            num_pages = len(self.pdf.pages)
            print(f"✅ PDF opened successfully: {num_pages} pages")
            self.log(f"PDF opened: {num_pages} pages")
            return True
        except FileNotFoundError:
            print(f"❌ PDF not found: {self.pdf_path}")
            return False
        except Exception as e:
            print(f"❌ Error opening PDF: {e}")
            return False

    def extract_all_tables(self):
        """Extract all tables from PDF with page references"""
        print("\n" + "="*80)
        print("EXTRACTING TABLES FROM PDF")
        print("="*80)

        tables_by_page = {}

        for page_num, page in enumerate(self.pdf.pages, 1):
            tables = page.extract_tables()

            if tables:
                print(f"\n📄 Page {page_num}: Found {len(tables)} table(s)")
                tables_by_page[page_num] = tables

                for table_idx, table in enumerate(tables):
                    print(f"  Table {table_idx}: {len(table)} rows × {len(table[0])} columns")

                    # Show first 3 rows as preview
                    for row_idx, row in enumerate(table[:3]):
                        print(f"    Row {row_idx}: {row[:2]}...")  # Show first 2 cells

                # Save raw table to JSON for inspection
                with open(f"{RAW_EXTRACT_DIR}/page_{page_num:02d}_tables.json", 'w', encoding='utf-8') as f:
                    json.dump(tables, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Total tables found: {sum(len(t) for t in tables_by_page.values())}")
        self.log(f"Extracted {sum(len(t) for t in tables_by_page.values())} tables from {len(tables_by_page)} pages")

        return tables_by_page

    def extract_all_text(self):
        """Extract text from each page"""
        print("\n" + "="*80)
        print("EXTRACTING TEXT FROM PDF")
        print("="*80)

        text_by_page = {}

        for page_num, page in enumerate(self.pdf.pages, 1):
            text = page.extract_text()

            if text:
                text_by_page[page_num] = text

                # Save to file
                with open(f"{RAW_EXTRACT_DIR}/page_{page_num:02d}_text.txt", 'w', encoding='utf-8') as f:
                    f.write(f"=== PAGE {page_num} ===\n\n")
                    f.write(text)

                # Show preview
                preview = text[:150].replace('\n', ' ')
                print(f"Page {page_num}: {len(text)} characters - {preview}...")

        print(f"\n✅ Extracted text from {len(text_by_page)} pages")
        self.log(f"Extracted text from {len(text_by_page)} pages")

        return text_by_page

    def close_pdf(self):
        """Close PDF"""
        if self.pdf:
            self.pdf.close()
            print("✅ PDF closed")

    def log(self, message):
        """Add to extraction log"""
        timestamp = datetime.now().isoformat()
        self.extraction_log.append(f"[{timestamp}] {message}")

    def save_log(self):
        """Save extraction log"""
        log_path = f"{OUTPUT_DIR}/extraction_log.txt"
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.extraction_log))
        print(f"\n✅ Extraction log saved: {log_path}")

def main():
    print("="*80)
    print("LIFTEC POC - PDF EXTRACTION TOOL")
    print("="*80)

    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"\n⚠️  PDF not found at: {PDF_PATH}")
        print("\nPlease:")
        print("1. Place your Via manual PDF in: manuals/")
        print("2. Update PDF_PATH in this script")
        print("3. Run again")
        return False

    # Initialize extractor
    extractor = PDFExtractor(PDF_PATH)

    # Open PDF
    if not extractor.open_pdf():
        return False

    # Extract tables
    tables = extractor.extract_all_tables()

    # Extract text
    text = extractor.extract_all_text()

    # Close PDF
    extractor.close_pdf()

    # Save log
    extractor.save_log()

    # Summary
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)
    print(f"Tables extracted: {sum(len(t) for t in tables.values())}")
    print(f"Pages with text: {len(text)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Raw data directory: {RAW_EXTRACT_DIR}")
    print("\n✅ Extraction complete!")
    print("\nNext steps:")
    print("1. Review extracted data in extracted_raw/")
    print("2. Run: python organize_json.py")
    print("3. Run: python validate_data.py")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
