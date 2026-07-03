#!/usr/bin/env python3
"""Advanced plagiarism + AI detection with Google scraping (rate-limited)."""
import sys
import subprocess
import statistics
import time
import re
from collections import Counter
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None

STOPWORDS = set([
    'yang', 'di', 'dan', 'dari', 'untuk', 'pada', 'dengan', 'itu', 'adalah',
    'ini', 'sebagai', 'tersebut', 'oleh', 'dalam', 'untuk', 'adanya', 'karena',
    'itu', 'juga', 'ada', 'telah', 'akan', 'lebih', 'atau', 'sudah', 'sangat',
    'the', 'is', 'are', 'was', 'and', 'of', 'to', 'in', 'that', 'for', 'on',
    'with', 'as', 'by', 'an', 'be', 'this', 'which', 'or', 'from', 'at',
])

# Rate limit: seconds between Google requests
DELAY = 3.0


def get_clean_words(text):
    words = [w.strip(".,!?:;\"'()[]{}1234567890").lower() for w in text.split()]
    return [w for w in words if w and len(w) > 1 and w not in STOPWORDS]


def extract_key_sentences(text, n=8):
    """Pick the N most 'unique' sentences for search queries."""
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.split()) >= 12]
    # Prefer longer, content-rich sentences
    scored = []
    for s in sentences:
        words = s.split()
        # Score by word count and unique words
        unique_ratio = len(set(w.lower() for w in words)) / len(words)
        score = len(words) * unique_ratio
        scored.append((score, s))
    scored.sort(reverse=True)
    return [s for _, s in scored[:n]]


def google_scrape(query):
    """Scrape Google search results for a query. Returns list of (title, url, snippet)."""
    if not requests or not BeautifulSoup:
        return []
    try:
        url = f"https://www.google.com/search?q={quote_plus(query)}&hl=en"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/128.0',
            'Accept-Language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        for g in soup.select('div.g'):
            title_el = g.select_one('h3')
            link_el = g.select_one('a[href]')
            snippet_el = g.select_one('.VwiC3b, .IsZvec, span.st')
            if title_el and link_el:
                results.append({
                    'title': title_el.get_text(strip=True),
                    'url': link_el['href'],
                    'snippet': snippet_el.get_text(strip=True) if snippet_el else '',
                })
        return results[:5]
    except Exception:
        return []


def ddgr_search(query):
    """Search via ddgr CLI. Returns list of dicts."""
    try:
        res = subprocess.run(
            ['ddgr', '--json', '--np', '5', query],
            capture_output=True, text=True, timeout=15
        )
        import json
        data = json.loads(res.stdout) if res.stdout.strip().startswith('[') else []
        return data
    except Exception:
        return []


def text_similarity_ratio(text_a, text_b):
    """Simple word-overlap ratio between two texts."""
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    overlap = words_a & words_b
    return len(overlap) / min(len(words_a), len(words_b))


def plagiarism_check(text):
    """Multi-engine plagiarism check with rate limiting."""
    sentences = extract_key_sentences(text, n=6)
    sources = []
    hits = 0

    for i, sentence in enumerate(sentences):
        query = sentence[:120]  # Google limit ~128 chars effective
        print(f"  [{i+1}/{len(sentences)}] Searching: {query[:60]}...", file=sys.stderr)

        # Try ddgr first
        ddgr_results = ddgr_search(query)
        if ddgr_results:
            hits += 1
            sources.append({
                'query': query[:80],
                'engine': 'ddgr',
                'results': ddgr_results[:3],
            })
            time.sleep(DELAY)
            continue

        # Fallback: Google scraping (rate limited)
        if requests and BeautifulSoup:
            g_results = google_scrape(query)
            if g_results:
                hits += 1
                sources.append({
                    'query': query[:80],
                    'engine': 'google',
                    'results': g_results[:3],
                })

        time.sleep(DELAY)

    score = hits / len(sentences) if sentences else 0
    return score, sources


def calculate_ai_metrics(text):
    words = get_clean_words(text)
    if not words:
        return None

    # TTR (filtered)
    ttr = len(set(words)) / len(words)

    # N-gram diversity (3-grams)
    trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]
    ngram_div = len(set(trigrams)) / len(trigrams) if trigrams else 0

    # Sentence burstiness
    sentences = [s for s in re.split(r'[.!?]+', text) if len(s.split()) > 3]
    lengths = [len(s.split()) for s in sentences]
    burstiness = statistics.variance(lengths) if len(lengths) > 1 else 0

    # Vocabulary richness (hapax legomena ratio)
    freq = Counter(words)
    hapax = sum(1 for w in freq if freq[w] == 1)
    hapax_ratio = hapax / len(freq) if freq else 0

    return {
        'ttr': ttr,
        'ngram_div': ngram_div,
        'burstiness': burstiness,
        'hapax_ratio': hapax_ratio,
    }


def ai_score(metrics):
    if not metrics:
        return 0
    score = 0
    # TTR < 0.40 suggests AI
    if metrics['ttr'] < 0.40:
        score += 25
    elif metrics['ttr'] < 0.45:
        score += 10
    # N-gram diversity < 0.50 suggests AI
    if metrics['ngram_div'] < 0.50:
        score += 25
    elif metrics['ngram_div'] < 0.60:
        score += 10
    # Burstiness < 50 suggests AI (too flat)
    if metrics['burstiness'] < 50:
        score += 25
    elif metrics['burstiness'] < 80:
        score += 10
    # Hapax ratio < 0.35 suggests limited vocab
    if metrics['hapax_ratio'] < 0.35:
        score += 25
    elif metrics['hapax_ratio'] < 0.45:
        score += 10
    return min(score, 100)


def format_sources(sources):
    lines = []
    for s in sources:
        lines.append(f"- Query: _{s['query']}_")
        lines.append(f"  Engine: {s['engine']}")
        for r in s['results']:
            title = r.get('title', r.get('title', '?'))
            url = r.get('url', r.get('url', '?'))
            lines.append(f"  - [{title}]({url})")
        lines.append("")
    return "\n".join(lines)


def main():
    text = sys.stdin.read()
    words_raw = text.split()
    total_words = len(words_raw)

    print(">> Analyzing AI indicators...", file=sys.stderr)
    metrics = calculate_ai_metrics(text)
    score = ai_score(metrics)

    print(">> Checking plagiarism (multi-engine, rate-limited)...", file=sys.stderr)
    plag_score, sources = plagiarism_check(text)

    print("# Document Analysis Report (V3 - Google + ddgr)")
    print(f"- **Total Words:** {total_words}")
    print(f"- **AI Score (Estimated):** {score}%")
    print(f"- **Plagiarism Score:** {plag_score * 100:.0f}%")

    if sources:
        print(f"\n## Similarity Sources ({len(sources)} queries)")
        print(format_sources(sources))

    if metrics:
        print("\n## AI Metrics Detail")
        print(f"- TTR (Excl. Stopwords): {metrics['ttr']:.3f}")
        print(f"- N-gram Diversity: {metrics['ngram_div']:.3f}")
        print(f"- Burstiness (Variance): {metrics['burstiness']:.2f}")
        print(f"- Hapax Legomena Ratio: {metrics['hapax_ratio']:.3f}")

    print("\n## Threshold Reference")
    print("| Metric | AI Flag | Human |")
    print("|--------|---------|-------|")
    print("| TTR | < 0.40 | >= 0.45 |")
    print("| N-gram Diversity | < 0.50 | >= 0.60 |")
    print("| Burstiness | < 50 | >= 80 |")
    print("| Hapax Ratio | < 0.35 | >= 0.45 |")


if __name__ == '__main__':
    main()
