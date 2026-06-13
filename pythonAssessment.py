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
