# Integration Guide for AI Agents

Total 6 halaman panduan instalasi untuk berbagai AI Agent:

---

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
# Link skill dari GitHub
git clone https://github.com/irgi/plagiarism-checker.git ~/.hermes/skills/plagiarism-checker

# Setup venv
python3 -m venv ~/venv/plagiarism-checker
source ~/venv/plagiarism-checker/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y

# Verifikasi skill loaded
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

### Auto-Run via Cron

```yaml
# ~/.hermes/cron/plagiarism-check.yaml
name: plagiarism-check
prompt: "Check proposal.docx for plagiarism"
deliver: "telegram"
enabled_toolsets: ["terminal"]
```

---

## Claude Code

### Setup

```bash
# Install globally
mkdir -p ~/.claude-code/tools
git clone https://github.com/irgi/plagiarism-checker.git ~/.claude-code/tools/plagiarism-checker

# Install dependencies
python3 -m venv ~/.claude-code/tools/plagiarism-checker/venv
source ~/.claude-code/tools/plagiarism-checker/venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y

# Make executable
chmod +x ~/.claude-code/tools/plagiarism-checker/scripts/*.py
```

### Usage via Prompt

> "Run plagiarism check on proposal.docx using plagiarism-checker tool"

Claude Code will:
1. Detect the tool
2. Run extraction + analysis
3. Output report

### Custom Tool Definition

```json
{
  "name": "plagiarism-check",
  "description": "Check documents for plagiarism and AI detection",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_path": { "type": "string" }
    },
    "required": ["file_path"]
  },
  "handler": "/home/irgi/.claude-code/tools/plagiarism-checker/scripts/run_check.py"
}
```

---

## Cursor Editor

### Setup Custom Tool

```bash
# Install dependencies
sudo apt install python3-pip
sudo apt install ddgr
pip install pymupdf python-docx requests beautifulsoup4

# Clone tool
git clone https://github.com/irgi/plagiarism-checker.git ~/.cursor/tools/plagiarism-checker
```

### Configure in .cursor/rules/plagiarism-check.md

```markdown
# Plagiarism Check Rules

When user asks to check plagiarism:
1. Run: `python3 ~/.cursor/tools/plagiarism-checker/scripts/extract_text.py <file>`
2. Pipe to: `python3 ~/.cursor/tools/plagiarism-checker/scripts/analyze.py`
3. Display Markdown report
```

### Usage

Press `Cmd+K` (or `Ctrl+K`) → Type:
```
Check this document for plagiarism: document.docx
```

---

## Windsurf

### Setup

```bash
# Create tools directory
mkdir -p ~/.windsurf/tools

# Clone repository
git clone https://github.com/irgi/plagiarism-checker.git ~/.windsurf/tools/plagiarism-checker

# Install dependencies
cd ~/.windsurf/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### Configure as MCP (Model Context Protocol)

```json
// ~/.windsurf/mcp-config.json
{
  "mcpServers": {
    "plagiarism-checker": {
      "command": "python3",
      "args": [
        "/home/irgi/.windsurf/tools/plagiarism-checker/scripts/mcp-server.py"
      ]
    }
  }
}
```

### Usage

> "Analyze document.txt for plagiarism using MCP tool"

---

## Amazon Q

### Setup via AWS Tools

```bash
# Install AWS CLI tools
pip install aws-cli

# Install plagiarism-checker
git clone https://github.com/irgi/plagiarism-checker.git ~/.aws/tools/plagiarism-checker
cd ~/.aws/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### Configure as Custom Command

```bash
# ~/.aws/tools/plagiarism-checker/run.sh
#!/bin/bash
cd /home/irgi/.aws/tools/plagiarism-checker
source venv/bin/activate
python3 scripts/analyze.py < "$1"
```

### Usage in Amazon Q

> "Run plagiarism check on src/document.pdf"

### Lambda Integration (Optional)

```python
# Lambda function wrapper
import subprocess
import json

def lambda_handler(event, context):
    file_path = event['file_path']
    
    # Extract text
    extract_cmd = f"python3 scripts/extract_text.py {file_path}"
    extracted = subprocess.check_output(extract_cmd, shell=True).decode()
    
    # Analyze
    result = subprocess.run(
        "python3 scripts/analyze.py",
        input=extracted,
        capture_output=True,
        text=True
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(result.stdout)
    }
```

---

## OpenCode

### Setup

```bash
# Install via OpenCode CLI
opencode tools install plagiarism-checker \
  --url https://github.com/irgi/plagiarism-checker \
  --path ~/.opencode/tools/plagiarism-checker
```

### If Manual Setup Required

```bash
git clone https://github.com/irgi/plagiarism-checker.git ~/.opencode/tools/plagiarism-checker
python3 -m venv ~/.opencode/tools/plagiarism-checker/venv
source ~/.opencode/tools/plagiarism-checker/venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### Usage

```bash
# Via OpenCode CLI
opencode run "check_plagiarism document.docx"
```

---

## Generic Agent (Custom Integration)

### REST API Wrapper

```python
# FastAPI wrapper for any agent
from fastapi import FastAPI
import subprocess
import tempfile

app = FastAPI()

@app.post("/check")
async def check_plagiarism(file_path: str):
    # Extract
    extract_cmd = f"python3 scripts/extract_text.py {file_path}"
    extracted = subprocess.check_output(extract_cmd, shell=True).decode()
    
    # Analyze
    result = subprocess.run(
        "python3 scripts/analyze.py",
        input=extracted,
        capture_output=True,
        shell=True
    )
    
    return {"report": result.stdout}

# Run: uvicorn server:app --host 0.0.0.0 --port 8000
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    poppler-utils \
    ddgr

# Clone and setup
RUN git clone https://github.com/irgi/plagiarism-checker.git /app
WORKDIR /app
RUN pip install pymupdf python-docx requests beautifulsoup4

# Expose
CMD ["python3", "scripts/analyze.py"]
```

Usage:
```bash
docker run -v ./document.docx:/app/document.docx plagiarism-checker python3 scripts/analyze.py /app/document.docx
```

### WebSocket Real-Time Agent Integration

```python
# WebSocket handler for real-time streaming
import asyncio
import websockets
import subprocess

async def handle_ws(websocket, path):
    async for message in websocket:
        # Parse file path
        async for line in stream_analysis(message):
            await websocket.send(line)

async def stream_analysis(file_path):
    process = subprocess.Popen(
        f"python3 scripts/extract_text.py {file_path} | python3 scripts/analyze.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    for line in iter(process.stdout.readline, ''):
        yield line
```

---

## Quick Comparison

| Agent            | Setup Complexity | Auto-Discovery | CLI Access | Web UI |
|------------------|------------------|----------------|------------|--------|
| Hermes           | ★☆☆ Easy        | ✅             | ✅         | ✅     |
| Claude Code      | ★★☆ Medium      | ✅             | ✅         | ❌     |
| Cursor           | ★★☆ Medium      | ❌             | ✅         | ❌     |
| Windsurf         | ★★★ Hard        | ❌             | ✅         | ❌     |
| Amazon Q         | ★★★ Hard        | ✓ (AWS)        | ✅         | ✅     |
| OpenCode         | ★★☆ Medium      | ✅             | ✅         | ❌     |

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
python3 -m venv venv
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
- Ensure text is not image-based (OCR not supported)
- Run with verbose: `python3 scripts/analyze.py -v < file`

---

## Support

- **GitHub Issues**: https://github.com/irgi/plagiarism-checker/issues
- **Documentation**: https://plagiarism-checker.org
- **License**: MIT