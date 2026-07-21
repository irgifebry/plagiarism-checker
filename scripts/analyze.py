#!/usr/bin/env python3
"""Advanced plagiarism + AI detection with concurrent async search and flexible scoring."""
import sys
import statistics
import re
import asyncio
from collections import Counter
from urllib.parse import quote_plus
from duckduckgo_search import DDGS

STOPWORDS = set([
    'yang', 'di', 'dan', 'dari', 'untuk', 'pada', 'dengan', 'itu', 'adalah',
    'ini', 'sebagai', 'tersebut', 'oleh', 'dalam', 'untuk', 'adanya', 'karena',
    'itu', 'juga', 'ada', 'telah', 'akan', 'lebih', 'atau', 'sudah', 'sangat',
    'the', 'is', 'are', 'was', 'and', 'of', 'to', 'in', 'that', 'for', 'on',
    'with', 'as', 'by', 'an', 'be', 'this', 'which', 'or', 'from', 'at',
])

# Flexible AI detection thresholds.
# 'metric': ( (strong_threshold, strong_penalty), (weak_threshold, weak_penalty), is_lower_bad )
AI_THRESHOLDS = {
    'ttr': ((0.40, 25), (0.45, 10), True),
    'ngram_div': ((0.50, 25), (0.60, 10), True),
    'burstiness': ((50, 25), (80, 10), True),
    'hapax_ratio': ((0.35, 25), (0.45, 10), True),
}

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
        if not words: continue
        unique_ratio = len(set(w.lower() for w in words)) / len(words)
        score = len(words) * unique_ratio
        scored.append((score, s))
    scored.sort(reverse=True)
    return [s for _, s in scored[:n]]


async def search_web(query):
    """Async search the web using DuckDuckGo and return top 3 results."""
    try:
        results = await DDGS().atext(query, max_results=3)
        return {'query': query, 'results': [{'title': r['title'], 'url': r['href'], 'snippet': r['body']} for r in results]}
    except Exception:
        return {'query': query, 'results': []}


def text_similarity_ratio(text_a, text_b):
    """Simple word-overlap ratio between two texts."""
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    overlap = words_a & words_b
    return len(overlap) / min(len(words_a), len(words_b))


async def plagiarism_check(text):
    """Concurrent plagiarism check using an async search engine."""
    key_sentences = extract_key_sentences(text, n=15)
    if not key_sentences:
        return 0, []

    print(f">> Checking plagiarism ({len(key_sentences)} queries concurrently)...", file=sys.stderr)

    tasks = [search_web(s[:250]) for s in key_sentences]
    search_results = await asyncio.gather(*tasks)

    sources = []
    hits = 0
    for res in search_results:
        if res['results']:
            top_hit_similarity = text_similarity_ratio(res['query'], res['results'][0]['snippet'])
            if top_hit_similarity > 0.3:
                hits += 1
                sources.append({
                    'query': res['query'][:80],
                    'engine': 'DuckDuckGo',
                    'results': res['results'],
                })

    score = hits / len(key_sentences)
    return score, sources


def calculate_ai_metrics(text):
    words = get_clean_words(text)
    if not words:
        return None

    ttr = len(set(words)) / len(words)
    trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]
    ngram_div = len(set(trigrams)) / len(trigrams) if trigrams else 0
    sentences = [s for s in re.split(r'[.!?]+', text) if len(s.split()) > 3]
    lengths = [len(s.split()) for s in sentences]
    burstiness = statistics.variance(lengths) if len(lengths) > 1 else 0
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
    """Calculate AI score based on a flexible threshold configuration."""
    if not metrics:
        return 0

    score = 0
    for metric, config in AI_THRESHOLDS.items():
        (strong_thresh, strong_penalty), (weak_thresh, weak_penalty), lower_is_bad = config
        value = metrics.get(metric, 0)

        if lower_is_bad:
            if value < strong_thresh:
                score += strong_penalty
            elif value < weak_thresh:
                score += weak_penalty
        else: # Higher is bad
            if value > strong_thresh:
                score += strong_penalty
            elif value > weak_thresh:
                score += weak_penalty

    return min(score, 100)


def format_sources(sources):
    lines = []
    for s in sources:
        lines.append(f"- Query: _{s['query']}_")
        lines.append(f"  Engine: {s['engine']}")
        for r in s['results']:
            title = r.get('title', '?')
            url = r.get('url', '?')
            lines.append(f"  - [{title}]({url})")
        lines.append("")
    return "\n".join(lines)


async def main():
    text = sys.stdin.read()
    words_raw = text.split()
    total_words = len(words_raw)

    print(">> Analyzing AI indicators...", file=sys.stderr)
    metrics = calculate_ai_metrics(text)
    score = ai_score(metrics)

    plag_score, sources = await plagiarism_check(text)

    print("# Document Analysis Report (V6 - Flexible Scoring)")
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
    print("| Metric | AI Flag (Strong) | AI Flag (Weak) |")
    print("|--------|------------------|----------------|")
    for name, config in AI_THRESHOLDS.items():
        (strong, _), (weak, _), lower_is_bad = config
        op = "<" if lower_is_bad else ">"
        print(f"| {name.replace('_', ' ').title()} | {op} {strong:.2f} | {op} {weak:.2f} |")


if __name__ == '__main__':
    asyncio.run(main())
