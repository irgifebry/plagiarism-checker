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
git clone https://github.com/irgifebry/plagiarism-checker.git
cd plagiarism-checker
```

## Installation via NPX (Recommended)
```bash
npx plagiarism-checker <path/to/file.docx|.pdf|.txt>
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

### Auto-Install (Skill Native)

```bash
cd ~/.hermes/skills/
sudo rm -rf plagiarism-checker || true
mkdir -p plagiarism-checker
cd plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git .

# Setup venv
python3 -m venv ~/venv/plagiarism-checker
source ~/venv/plagiarism-checker/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y

# Verifikasi
hermes status --show-skills
```

### Usage

```bash
# Call via skill_view
skill_view(name='plagiarism-checker')

# Run analysis
source ~/venv/plagiarism-checker/bin/activate
python3 ~/.hermes/skills/plagiarism-checker/scripts/analyze.py < document.txt
```

---

## Claude Code

### Setup

```bash
mkdir -p ~/.claude-code/tools
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.claude-code/tools/plagiarism-checker

python3 -m venv ~/.claude-code/tools/plagiarism-checker/venv
source ~/.claude-code/tools/plagiarism-checker/venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y

chmod +x ~/.claude-code/tools/plagiarism-checker/scripts/*.py
```

### Usage via Prompt

> "Run plagiarism check on proposal.docx using plagiarism-checker tool"

Claude Code akan:
1. Mendeteksi tool
2. Menjalankan extraction + analysis
3. Output report

---

## Cursor Editor

### Setup

```bash
mkdir -p ~/.cursor/tools
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.cursor/tools/plagiarism-checker

pip install --user pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

### Configure Rules

Buat file `~/.cursor/rules/plagiarism-check.md`:

```markdown
# Plagiarism Check Rules

When user asks to check plagiarism:
1. Run: `python3 ~/.cursor/tools/plagiarism-checker/scripts/extract_text.py <file>`
2. Pipe to: `python3 ~/.cursor/tools/plagiarism-checker/scripts/analyze.py`
3. Display Markdown report
```

### Usage

```
Cmd+K (Ctrl+K) → "Check this document for plagiarism: document.docx"
```

---

## Windsurf

### Setup

```bash
mkdir -p ~/.windsurf/tools
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.windsurf/tools/plagiarism-checker

cd ~/.windsurf/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### Configure as MCP

```json
// ~/.windsurf/mcp-config.json
{
  "mcpServers": {
    "plagiarism-checker": {
      "command": "python3",
      "args": ["/home/irgi/.windsurf/tools/plagiarism-checker/scripts/analyze.py"]
    }
  }
}
```

---

## Amazon Q

### Setup

```bash
mkdir -p ~/.aws/tools
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.aws/tools/plagiarism-checker

cd ~/.aws/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### Custom Command Wrapper

```bash
# ~/.aws/tools/plagiarism-checker/run.sh
#!/bin/bash
cd /home/irgi/.aws/tools/plagiarism-checker
source venv/bin/activate
python3 scripts/analyze.py < "$1"
```

### Lambda Integration (Optional)

```python
import subprocess, json

def lambda_handler(event, context):
    file_path = event['file_path']
    extract = subprocess.check_output(
        f"python3 scripts/extract_text.py {file_path}", shell=True
    ).decode()
    result = subprocess.run(
        "python3 scripts/analyze.py", input=extract,
        capture_output=True, text=True
    )
    return {'statusCode': 200, 'body': json.dumps(result.stdout)}
```

---

## OpenCode

### Setup

```bash
opencode tools install plagiarism-checker \
  --url https://github.com/irgifebry/plagiarism-checker \
  --path ~/.opencode/tools/plagiarism-checker
```

### Manual

```bash
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.opencode/tools/plagiarism-checker
python3 -m venv ~/.opencode/tools/plagiarism-checker/venv
source ~/.opencode/tools/plagiarism-checker/venv/bin/activate
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
    extract = subprocess.check_output(
        f"python3 scripts/extract_text.py {file_path}", shell=True
    ).decode()
    result = subprocess.run(
        "python3 scripts/analyze.py", input=extract,
        capture_output=True, shell=True
    )
    return {"report": result.stdout}

# uvicorn server:app --host 0.0.0.0 --port 8000
```

### Docker Integration

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y git poppler-utils ddgr
RUN git clone https://github.com/irgifebry/plagiarism-checker.git /app
WORKDIR /app
RUN pip install pymupdf python-docx requests beautifulsoup4
CMD ["python3", "scripts/analyze.py"]
```

```bash
docker run -v ./document.docx:/app/document.docx plagiarism-checker \
  python3 scripts/extract_text.py /app/document.docx | python3 scripts/analyze.py
```

---

## Comparison

| Agent            | Complexity | Auto-Discovery | CLI | Web UI |
|------------------|------------|----------------|-----|--------|
| Hermes           | Easy       | Yes            | Yes | Yes    |
| Claude Code      | Medium     | Yes            | Yes | No     |
| Cursor           | Medium     | No             | Yes | No     |
| Windsurf         | Hard       | No             | Yes | No     |
| Amazon Q         | Medium     | Yes (AWS)      | Yes | Yes    |
| OpenCode         | Medium     | Yes            | Yes | No     |

---

## Troubleshooting

### ddgr Not Found
```bash
sudo apt install ddgr
# or
brew install ddgr  # macOS
```

### ModuleNotFoundError: No module named 'fitz'
```bash
source venv/bin/activate
pip install --upgrade pymupdf
```

### Google Rate Limit
Edit `scripts/analyze.py`:
```python
DELAY = 5  # Increase from 3 to 5 seconds
```

### Empty Results
- Check file encoding: `file document.docx`
- Ensure text is not image-based (OCR not supported yet)
- Run with verbose: `python3 scripts/analyze.py -v < file`

---

## License
MIT
