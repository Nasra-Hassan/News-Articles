#!/usr/bin/env python3
"""pythonAssessment.py

Text analysis utilities for a news article assessment.

Features:
- Count occurrences of a specific word
- Identify most common word (optionally excluding stopwords)
- Calculate average word length
- Count paragraphs
- Count sentences

Usage:
  python3 pythonAssessment.py --file article.txt --word the
  python3 pythonAssessment.py --test
"""
from collections import Counter
import re
import argparse
import sys


def _words(text):
    return re.findall(r"\b[\w']+\b", text.lower())


def count_specific_word(text, word):
    words = _words(text)
    return sum(1 for w in words if w == word.lower())


def most_common_word(text, exclude_stopwords=False):
    words = _words(text)
    if not words:
        return None, 0
    stopwords = {
        'the','and','a','an','to','of','in','for','on','with','is','was','were','that','by','as','at','from','it'
    }
    c = Counter(words)
    if exclude_stopwords:
        for s in stopwords:
            c.pop(s, None)
    if not c:
        return None, 0
    word, count = c.most_common(1)[0]
    return word, count


def average_word_length(text):
    words = _words(text)
    if not words:
        return 0.0
    total_chars = sum(len(w) for w in words)
    return total_chars / len(words)


def count_paragraphs(text):
    parts = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    return len(parts)


def count_sentences(text):
    # Split on sentence enders followed by whitespace; simple but effective for this task
    parts = [s for s in re.split(r'(?<=[\.!?])\s+', text) if s.strip()]
    return len(parts)


def analyze(text, specific_word=None, exclude_stopwords=False):
    results = {}
    results['specific_word'] = (specific_word, count_specific_word(text, specific_word)) if specific_word else None
    results['most_common'] = most_common_word(text, exclude_stopwords=exclude_stopwords)
    results['average_word_length'] = average_word_length(text)
    results['paragraphs'] = count_paragraphs(text)
    results['sentences'] = count_sentences(text)
    return results


def _print_results(results):
    if results['specific_word']:
        w, c = results['specific_word']
        print(f"Count of '{w}': {c}")
    mc_word, mc_count = results['most_common']
    print(f"Most common word: {mc_word} ({mc_count})")
    print(f"Average word length: {results['average_word_length']:.2f}")
    print(f"Paragraphs: {results['paragraphs']}")
    print(f"Sentences: {results['sentences']}")


def main():
    parser = argparse.ArgumentParser(description='News article text analysis')
    parser.add_argument('--file', '-f', help='Path to article file (defaults to stdin)')
    parser.add_argument('--word', '-w', help='Specific word to count')
    parser.add_argument('--exclude-stopwords', action='store_true', help='Exclude common stopwords when finding most common word')
    parser.add_argument('--test', action='store_true', help='Run built-in self-test example')
    args = parser.parse_args()

    if args.test:
        sample = (
            "President signs new bill into law. The law will affect many communities. "
            "In related news, experts say the change could be significant.\n\n" 
            "This is the second paragraph of the article. It contains several sentences."
        )
        results = analyze(sample, specific_word=args.word, exclude_stopwords=args.exclude_stopwords)
        _print_results(results)
        return

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print('Error reading file:', e)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    results = analyze(text, specific_word=args.word, exclude_stopwords=args.exclude_stopwords)
    _print_results(results)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""pythonAssessment.py

Performs text analysis on a news article (or any text file).

Features:
- Count occurrences of a specific word
- Identify the most common word
- Calculate average word length
- Count paragraphs
- Count sentences

Usage examples:
  python3 pythonAssessment.py --file article.txt --word the
  python3 pythonAssessment.py --word economy

If `--file` omitted, the script will attempt to read `article.txt` in
the current directory; if that is missing it uses a small default text.
"""
import argparse
import re
from collections import Counter
from typing import List

DEFAULT_ARTICLE = (
    """
Tech startup researchers published a short analysis of recent trends.

The team focused on natural language processing applications for news
analysis and described common tasks such as counting words, identifying
most frequent tokens, and measuring sentence statistics. The project
aims to provide reproducible scripts for educational assessments.

Researchers noted that accurate sentence splitting and tokenization
remain important for downstream metrics.
"""
)


def load_text(file_path: str | None) -> str:
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    try:
        with open("article.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return DEFAULT_ARTICLE


def get_paragraphs(text: str) -> List[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paragraphs


def get_sentences(text: str) -> List[str]:
    raw = text.strip()
    if not raw:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', raw)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def get_words(text: str) -> List[str]:
    words = re.findall(r"\b[A-Za-z0-9']+\b", text)
    return words


def count_word_occurrences(target: str, words: List[str]) -> int:
    target_l = target.lower()
    return sum(1 for w in words if w.lower() == target_l)


def most_common_word(words: List[str]) -> tuple[str, int] | tuple[None, int]:
    if not words:
        return (None, 0)
    counts = Counter(w.lower() for w in words)
    word, cnt = counts.most_common(1)[0]
    return (word, cnt)


def average_word_length(words: List[str]) -> float:
    if not words:
        return 0.0
    total = sum(len(w) for w in words)
    return total / len(words)


def analyze_text(text: str, target_word: str | None = None) -> dict:
    paragraphs = get_paragraphs(text)
    sentences = get_sentences(text)
    words = get_words(text)
    word_counts = {}
    if target_word:
        word_counts["target_count"] = count_word_occurrences(target_word, words)
    most_common, most_count = most_common_word(words)
    return {
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "words": len(words),
        "most_common_word": most_common,
        "most_common_count": most_count,
        "average_word_length": average_word_length(words),
        **word_counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="News article text analysis")
    parser.add_argument("--file", "-f", help="Path to article text file")
    parser.add_argument("--word", "-w", help="Specific word to count (case-insensitive)")
    parser.add_argument("--top", "-t", type=int, default=10, help="Show top N most common words")
    args = parser.parse_args()

    text = load_text(args.file)
    results = analyze_text(text, args.word)

    print(f"Paragraphs: {results['paragraphs']}")
    print(f"Sentences: {results['sentences']}")
    print(f"Total words: {results['words']}")
    if args.word:
        print(f"Occurrences of '{args.word}': {results.get('target_count', 0)}")
    mcw = results['most_common_word'] or "(none)"
    print(f"Most common word: {mcw} ({results['most_common_count']})")
    print(f"Average word length: {results['average_word_length']:.2f}")

    # show top N words
    words = get_words(text)
    counts = Counter(w.lower() for w in words)
    print(f"Top {args.top} words:")
    for i, (w, c) in enumerate(counts.most_common(args.top), start=1):
        print(f"  {i}. {w} — {c}")


if __name__ == "__main__":
    main()
