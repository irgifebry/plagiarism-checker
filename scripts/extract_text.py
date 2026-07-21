#!/usr/bin/env python3
"""Extract clean text from DOCX, PDF, or TXT files."""
import sys
import os
from pathlib import Path

def extract_docx(path):
    from docx import Document
    doc = Document(path)
    return '\n'.join(p.text.strip() for p in doc.paragraphs if p.text.strip())

def extract_pdf(path):
    import fitz
    doc = fitz.open(path)
    return '\n'.join(page.get_text() for page in doc)

def extract_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_text.py <file.docx|file.pdf|file.txt>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    ext = Path(path).suffix.lower()
    
    extractors = {
        '.docx': extract_docx,
        '.pdf': extract_pdf,
        '.txt': extract_txt,
    }
    
    if ext not in extractors:
        print(f"Unsupported format: {ext}", file=sys.stderr)
        sys.exit(1)
    
    text = extractors[ext](path)
    print(text)

if __name__ == '__main__':
    main()
