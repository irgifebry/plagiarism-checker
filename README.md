# Plagiarism Checker & AI Detector

Open‑source tool for detecting plagiarism and AI‑generated text in DOCX, PDF, and TXT files. Works completely offline, requires no API keys, and is ready to be used by AI agents (Hermes, Claude Code, Cursor, Windsurf, Amazon Q, OpenCode) or directly from the command line.

---  

## Table of Contents
- [Features](#features)  
- [Supported File Types](#supported-file-types)  
- [Installation (Manual)](#installation-manual)  
- [Command‑Line Usage](#command-line-usage)  
- [Programmatic API](#programmatic-api)  
- [Agent Integration](#agent-integration)  
- [Quick‑Start Examples](#quick-start-examples)  
- [Troubleshooting](#troubleshooting)  

---  

## Features
- **Plagiarism detection** – extracts sentences, searches via DuckDuckGo's API and estimates similarity.  
- **AI‑generated text detection** – uses statistical metrics:  
  - Type‑Token Ratio (TTR)  
  - N‑gram diversity (3‑grams)  
  - Sentence‑length variance  
  - Hapax legomena ratio  
  - Approximate Flesch Reading Ease  
- **Multiple formats** – handles `.docx`, `.pdf`, `.txt`.  
- **Zero dependencies beyond pip packages** – no external services, no registration.  
- **Agent‑friendly** – designed to be invoked autonomously by AI agents.  

---  

## Supported File Types
| Format | Extension | Notes |
|--------|-----------|-------|
| Microsoft Word | `.docx` | Extracts text from paragraphs; ignores images/objects. |
| PDF | `.pdf` | Uses PyMuPDF (`fitz`) for text extraction. |
| Plain Text | `.txt` | UTF‑8 assumed; falls back to `latin‑1` on error. |

---  

## Installation (Manual)
> **All steps are explicit.**

```bash
# 1. Clone the repository
git clone https://github.com/irgifebry/plagiarism-checker.git
cd plagiarism-checker

# 2. Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate   # .\\venv\\Scripts\\activate on Windows PowerShell

# 3. Install required Python packages
pip install pymupdf python-docx duckduckgo-search

```

> After activation, your shell prompt should show `(venv)`. All subsequent `python` and `pip` commands refer to this isolated environment.

---  

## Command‑Line Usage
1. **Extract text** from a document:  
   ```bash
   python3 scripts/extract_text.py path/to/file.docx > extracted.txt
   ```
   Works for `.pdf` and `.txt` as well.

2. **Analyze the extracted text** (produces a Markdown report on stdout):  
   ```bash
   python3 scripts/analyze.py < extracted.txt
   ```

The report includes:
- Plagiarism score (percentage)  
- AI‑detection metrics (TTR, N‑gram diversity, sentence‑length variance, hapax ratio, FRE)  
- List of matching sentences with source URLs/snippets  

---  

## Programmatic API
You can call the detector directly from Python without touching the CLI.

```python
import subprocess, json, pathlib

def extract_text(file_path: str) -> str:
    """Return plain text from DOCX/PDF/TXT."""
    return subprocess.check_output(
        ["python3", "scripts/extract_text.py", file_path],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()

def analyze_text(text: str) -> dict:
    """Run the analyzer on raw text and return a JSON dict."""
    result = subprocess.run(
        ["python3", "scripts/analyze.py"],
        input=text,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)

# Example usage
if __name__ == "__main__":
    txt = extract_text("sample.docx")
    report = analyze_text(txt)
    print(json.dumps(report, indent=2))
```

The returned JSON has the same fields as the Markdown report (you can pretty‑print or further process it).

---  

## Agent Integration
Below are ready‑to‑copy snippets for each supported agent. Adjust paths if you store the repository elsewhere.

### Hermes Agent
```bash
# Install the skill (once)
cd ~/.hermes/skills
rm -rf plagiarism-checker || true
mkdir -p plagiarism-checker
cd plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git .
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx duckduckgo-search
hermes status --show-skills   # verify

# Usage
skill_view(name='plagiarism-checker')
source ~/venv/plagiarism-checker/bin/activate
python3 scripts/analyze.py < /path/to/file.docx
```

### Claude Code
```bash
mkdir -p ~/.claude-code/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.claude-code/tools/plagiarism-checker
python3 -m venv ~/.claude-code/tools/plagiarism-checker/venv
source ~/.claude-code/tools/plagiarism-checker/venv/bin/activate
pip install pymupdf python-docx duckduckgo-search

# In Claude Code chat:
#   “Run plagiarism check on proposal.docx”
```

### Cursor
```bash
mkdir -p ~/.cursor/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.cursor/tools/plagiarism-checker
pip install --user pymupdf python-docx requests beautifulsoup4

# Add a custom command (e.g., in Settings → Commands):
#   cmd: python3 ~/.cursor/tools/plagiarism-checker/scripts/analyze.py
#   args: $(cat ~/.cursor/tools/plagiarism-checker/scripts/extract_text.py "$FILE")
```

### Windsurf
```bash
mkdir -p ~/.windsurf/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.windsurf/tools/plagiarism-checker
cd ~/.windsurf/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx duckduckgo-search

# Optional: expose as MCP server (see docs/windsurf-mcp.json)
```

### Amazon Q
```bash
mkdir -p ~/.aws/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.aws/tools/plagiarism-checker
cd ~/.aws/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx duckduckgo-search

# Create a wrapper script:
cat > ~/.aws/tools/plagiarism-checker/run.sh <<'EOF'
#!/usr/bin/env bash
cd "$HOME/.aws/tools/plagiarism-checker"
source venv/bin/activate
python3 scripts/analyze.py "$1"
EOF
chmod +x ~/.aws/tools/plagiarism-checker/run.sh
# Then in Amazon Q:  /path/to/run.sh document.docx
```

### OpenCode
```bash
opencode tools install plagiarism-checker \
  --url https://github.com/irgifebry/plagiarism-checker.git \
  --path ~/.opencode/tools/plagiarism-checker
cd ~/.opencode/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx duckduckgo-search
# Use via the OpenCode CLI: `opencode run "plagiarism-checker document.docx"`
```

### Custom Agent / Generic Python
See the **Programmatic API** section above; import `extract_text` and `analyze_text` functions into your agent’s codebase.

---  

## Quick‑Start Examples
```bash
# 1. Extract text from a PDF
python3 scripts/extract_text.py lecture.pdf > lecture.txt

# 2. Analyze for plagiarism & AI content
python3 scripts/analyze.py < lecture.txt
```
Output (truncated):
```
## Plagiarism Score
- Overall similarity: 7%
- Matching chunks: 2 / 15

## AI‑Generated Text Detection
- TTR: 0.62
- N‑gram diversity: 0.55
- Sentence‑length variance: 92
- Hapax ratio: 0.38
- FRE: 51

## Highlighted Matches
> “The quick brown fox jumps over the lazy dog.” – matches https://example.com/paper.pdf (73%)
```

---  

## Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError: No module named 'fitz'` | `pymupdf` not installed or broken | `pip install --upgrade pymupdf` (may need system packages: `sudo apt install python3-pip libfreetype6-dev`) |
| Permission denied when running scripts | Virtual env not activated | Run `source venv/bin/activate` (Linux/macOS) or `.\venv\Scripts\activate` (Windows) |
| Rate‑limit / HTTP 429 from search | Too many requests in short time | Increase `DELAY` constant in `scripts/analyze.py` (default 3 s) to 5‑10 s |
| “Protected View” warning in Word | DOCX opened in Protected View | Click **Enable Editing** – does not affect analysis |
| No output / empty report | Input text empty after extraction | Verify file is not image‑only PDF; run `pdfinfo` or try another file |
| ImportError in custom script | Wrong working directory | Ensure you run scripts from repository root or use absolute paths to `scripts/…` |

---  



---  
