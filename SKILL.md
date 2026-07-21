---
name: plagiarism-checker
description: Check documents (DOCX, PDF, TXT) for plagiarism & AI detection using n-gram diversity, TTR, variance, and web search via ddgr.
compatibility: Python 3.10+, pymupdf, python-docx, ddgr
---

# Plagiarism Checker & AI Detector

Analyzes academic documents for two things:
1. **Plagiarism** — detects similarity with online sources via `ddgr`.
2. **AI-generated** — detects AI-written text via statistical text analysis (TTR, N-gram Diversity, Sentence Burstiness/Variance, Hapax Legomena ratio).

## Workflow

1. `scripts/extract_text.py <file>` → extract clean text to stdout
2. `scripts/analyze.py < <text>` → output Markdown report
3. Report is displayed to the user

## Manual Setup

```bash
python3 -m venv ~/venv/plagiarism-checker
source ~/venv/plagiarism-checker/bin/activate
pip install pymupdf python-docx requests beautifulsoup4
sudo apt install ddgr -y
```

## Manual Usage

```bash
VENV=~/venv/plagiarism-checker/bin

# 1. Extract
$VENV/python3 scripts/extract_text.py proposal.docx > /tmp/text.txt

# 2. Analyze
$VENV/python3 scripts/analyze.py </tmp/text.txt
```

## Scripts

- `scripts/extract_text.py` — Extract clean text from DOCX/PDF/TXT
- `scripts/analyze.py` — Complete analysis + Markdown report

## AI Detection Algorithm

- **TTR (Type-Token Ratio)** — ratio of unique words vs total words. AI text tends to be <0.45
- **N-gram Diversity** — unique 3-grams vs total 3-grams. AI tends to be <0.6
- **Sentence Length Variance** — variation in sentence length. AI tends to be <80 (too uniform)
- **Flesch Reading Ease (estimate)** — readability score. AI often in 30-50 range

## Plagiarism Check

- Split text into chunks of ~500 words
- Extract the 1 most unique sentence per chunk
- Search via ddgr (DuckDuckGo CLI)
- Similarity score based on match results

## Pitfalls

1. **Duplicate skill path**: If the skill appears in two paths (`plagiarism-checker` and `software-development/plagiarism-checker`), Hermes will fail to load with "Ambiguous skill name". Remove one. The correct one is in `software-development/plagiarism-checker`.
2. **Module not found**: Ensure the venv is active and all dependencies are installed.
3. **Google rate limit**: If Google scraping is blocked (403/captcha), increase `DELAY` in `analyze.py` to 5-10 seconds.
4. **100% plagiarism score**: Doesn't mean 100% copy-paste. Short/common sentences (titles, technical terms) will always match. Focus on matching long sentences.
5. **DOCX "Protected View"**: After generating DOCX, the user must click "Enable Editing" in Word. This is normal.

## Limitations

- No access to Turnitin/iThenticate (requires official institutional portal).
- AI detection is statistically based; accuracy is not 100%.
- Dependent on ddgr/Google connectivity and rate limits.
- **Agent-Driven Workflow:** This check is designed for AI Agents to run autonomously.
- **Scope Warning:** Only checks public web data (Google/DuckDuckGo). Misses paid journals and local campus repositories.