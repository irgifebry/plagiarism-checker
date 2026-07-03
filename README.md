# Plagiarism Checker & AI Detector
Open-source tool untuk deteksi plagiarisme dan AI-generated text.

🌐 **Live demo:** [https://irgifebry.github.io/plagiarism-checker/](https://irgifebry.github.io/plagiarism-checker/)

## Features
- **Plagiarism Detection**: Scraping real-time via Google & ddgr.
- **AI Detection**: Berbasis statistik (TTR, Burstiness, Hapax Ratio).
- **Format Support**: DOCX, PDF, TXT.
- **Agent-Ready**: Dirancang untuk dijalankan otomatis oleh AI Agent.

## Quick Installation

```bash
# 1. Clone Repository
git clone https://github.com/irgifebry/plagiarism-checker.git
cd plagiarism-checker

# 2. Setup Venv
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

## Usage

```bash
# Extract text
python3 scripts/extract_text.py <file.docx|.pdf|.txt> > temp.txt

# Analyze
python3 scripts/analyze.py < temp.txt
```

---

# Integration Guide for AI Agents

## Table of Contents

1. [Hermes Agent](#hermes-agent)
2. [Claude Code](#claude-code)
3. [Cursor Editor](#cursor-editor)
4. [Windsurf](#windsurf)
5. [Amazon Q](#amazon-q)
6. [OpenCode](#opencode)
7. [Generic Agent](#generic-agent)

---

## Hermes Agent

### Setup

```bash
cd ~/.hermes/skills/
sudo rm -rf plagiarism-checker || true
mkdir -p plagiarism-checker
cd plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git .

python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y

hermes status --show-skills
```

### Usage

```bash
skill_view(name='plagiarism-checker')
source venv/bin/activate
python3 scripts/analyze.py < document.txt
```

---

## Claude Code

### Setup

```bash
mkdir -p ~/.claude-code/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.claude-code/tools/plagiarism-checker

python3 -m venv ~/.claude-code/tools/plagiarism-checker/venv
source ~/.claude-code/tools/plagiarism-checker/venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

### Usage

> "Run plagiarism check on proposal.docx"

---

## Cursor Editor

### Setup

```bash
mkdir -p ~/.cursor/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.cursor/tools/plagiarism-checker
pip install --user pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

### Usage

```
Cmd+K → "Check document.docx for plagiarism using ~/.cursor/tools/plagiarism-checker/scripts/analyze.py"
```

---

## Windsurf

### Setup

```bash
mkdir -p ~/.windsurf/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.windsurf/tools/plagiarism-checker

cd ~/.windsurf/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

---

## Amazon Q

### Setup

```bash
mkdir -p ~/.aws/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.aws/tools/plagiarism-checker

cd ~/.aws/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

---

## OpenCode

### Setup

```bash
opencode tools install plagiarism-checker --url https://github.com/irgifebry/plagiarism-checker --path ~/.opencode/tools/plagiarism-checker
cd ~/.opencode/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

---

## Generic Agent (Custom Integration)

### REST API Wrapper

```python
from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.post("/check")
async def check_plagiarism(file_path: str):
    extract = subprocess.check_output(f"python3 scripts/extract_text.py {file_path}", shell=True).decode()
    result = subprocess.run("python3 scripts/analyze.py", input=extract, capture_output=True, shell=True, text=True)
    return {"report": result.stdout}
```

---

## Troubleshooting

### ddgr Not Found
```bash
sudo apt install ddgr
```

### ModuleNotFoundError
```bash
source venv/bin/activate
pip install --upgrade pymupdf python-docx requests beautifulsoup4
```

---

## License
MIT
