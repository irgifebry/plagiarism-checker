# Plagiarism Checker & AI Detector
Open-source tool untuk deteksi plagiarisme dan AI-generated text.

## Features
- **Plagiarism Detection**: Scraping real-time via Google & ddgr.
- **AI Detection**: Berbasis statistik (TTR, Burstiness, Hapax Ratio).
- **Format Support**: DOCX, PDF, TXT.
- **Agent-Ready**: Dirancang untuk dijalankan otomatis oleh AI Agent.

## Quick Installation

```bash
# 1. Setup Venv
python3 -m venv ~/venv/plagiarism-checker
source ~/venv/plagiarism-checker/bin/activate

# 2. Install Dependencies
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y

# 3. Clone Repository
git clone https://github.com/irgi/plagiarism-checker.git
cd plagiarism-checker
```

## AI Agent Integration Guide

### 1. Hermes Agent
Tambahkan ke folder `~/.hermes/skills/`:
```bash
ln -s /path/to/plagiarism-checker ~/.hermes/skills/plagiarism-checker
```

### 2. Claude Code / OpenCode
Tambahkan `plagiarism-checker` ke dalam directory proyek `.agents/skills/` dan panggil lewat prompt:
> "Run plagiarism check on proposal.docx"

### 3. Custom Agent (Generic)
Integrasikan script sebagai tool:
```bash
# Tool definition
- name: check_plagiarism
  command: /home/irgi/venv/plagiarism-checker/bin/python3 /path/to/analyze.py < extracted_text.txt
```

## Dependencies
- Python 3.10+
- `pymupdf` (PDF processing)
- `python-docx` (DOCX processing)
- `ddgr` (Search CLI)
