# Plagiarism Checker & AI Detector
Open-source tool for detecting plagiarism and AI-generated text.

## Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/irgifebry/plagiarism-checker.git
cd plagiarism-checker

# 2. Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install required packages
pip install pymupdf python-docx requests beautifulsoup4

# 4. Install ddgr (for plagiarism search)
sudo apt install ddgr -y
```

## Usage

```bash
# Extract text from a document
python3 scripts/extract_text.py <file_path> > extracted.txt

# Analyze the extracted text
python3 scripts/analyze.py < extracted.txt
```

## Integration Guide for AI Agents

### Hermes Agent
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

### Claude Code
```bash
mkdir -p ~/.claude-code/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.claude-code/tools/plagiarism-checker

python3 -m venv ~/.claude-code/tools/plagiarism-checker/venv
source ~/.claude-code/tools/plagiarism-checker/venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

### Cursor
```bash
mkdir -p ~/.cursor/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.cursor/tools/plagiarism-checker

pip install --user pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

### Windsurf
```bash
mkdir -p ~/.windsurf/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.windsurf/tools/plagiarism-checker

cd ~/.windsurf/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### Amazon Q
```bash
mkdir -p ~/.aws/tools/plagiarism-checker
git clone https://github.com/irgifebry/plagiarism-checker.git ~/.aws/tools/plagiarism-checker

cd ~/.aws/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

### OpenCode
```bash
opencode tools install plagiarism-checker \
  --url https://github.com/irgifebry/plagiarism-checker \
  --path ~/.opencode/tools/plagiarism-checker
cd ~/.opencode/tools/plagiarism-checker
python3 -m venv venv
source venv/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr
```

## Troubleshooting

### ddgr not found
```bash
sudo apt install ddgr
```

### Module not found
```bash
source venv/bin/activate
pip install --upgrade pymupdf python-docx requests beautifulsoup4
```

## Usage Example

```bash
# Extract text from a DOCX file
python3 scripts/extract_text.py proposal.docx > extracted.txt

# Analyze the extracted text
python3 scripts/analyze.py < extracted.txt
```

The generated Markdown report includes:
- Plagiarism score
- AI detection metrics (TTR, Burstiness, N-gram Diversity, Hapax Ratio)
- Highlighted matching sentences