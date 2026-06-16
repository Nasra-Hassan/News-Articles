#!/usr/bin/env python3
"""pythonAssessment.py

Performs text analysis on a news article (or any text file).

Features:
- Count occurrences of a specific word
- Identify the most common word (optionally excluding stopwords)
- Calculate average word length
- Count paragraphs
- Count sentences

Usage examples:
  python3 pythonAssessment.py --file article.txt --word pie
  python3 pythonAssessment.py --file article.txt --exclude-stopwords --top 20
  python3 pythonAssessment.py --test
"""
from collections import Counter
import argparse
import re
import sys
from typing import List, Optional, Tuple


STOPWORDS = {
    'the', 'and', 'a', 'an', 'to', 'of', 'in', 'for', 'on', 'with', 'is', 'was',
    'were', 'that', 'by', 'as', 'at', 'from', 'it', 'this', 'these', 'those', 'be',
    'are', 'or', 'which', 'their', 'has', 'have', 'had', 'but', 'not', 'will'
}


def load_text(file_path: Optional[str]) -> str:
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    try:
        with open('article.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''


def get_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def get_sentences(text: str) -> List[str]:
    raw = text.strip()
    if not raw:
        return []
    parts = re.split(r'(?<=[.!?])\s+', raw)
    return [s.strip() for s in parts if s.strip()]


def get_words(text: str) -> List[str]:
    return re.findall(r"\b[A-Za-z0-9']+\b", text)


def count_word_occurrences(target: str, words: List[str]) -> int:
    t = target.lower()
    return sum(1 for w in words if w.lower() == t)


def most_common_word(words: List[str], exclude_stopwords: bool = False) -> Tuple[Optional[str], int]:
    if not words:
        return None, 0
    counts = Counter(w.lower() for w in words)
    if exclude_stopwords:
        for s in STOPWORDS:
            counts.pop(s, None)
    if not counts:
        return None, 0
    word, cnt = counts.most_common(1)[0]
    return word, cnt


def average_word_length(words: List[str]) -> float:
    if not words:
        return 0.0
    total = sum(len(w) for w in words)
    return total / len(words)


def analyze_text(text: str, target: Optional[str] = None, exclude_stopwords: bool = False) -> dict:
    paragraphs = get_paragraphs(text)
    sentences = get_sentences(text)
    words = get_words(text)
    result = {
        'paragraphs': len(paragraphs),
        'sentences': len(sentences),
        'words': len(words),
        'average_word_length': average_word_length(words),
    }
    if target:
        result['target_count'] = count_word_occurrences(target, words)
    mcw, mcc = most_common_word(words, exclude_stopwords=exclude_stopwords)
    result['most_common_word'] = mcw
    result['most_common_count'] = mcc
    result['top_counts'] = Counter(w.lower() for w in words)
    return result


def print_results(results: dict, target: Optional[str], top: int) -> None:
    if target:
        print(f"Occurrences of '{target}': {results.get('target_count', 0)}")
    mcw = results['most_common_word'] or '(none)'
    print(f"Most common word: {mcw} ({results['most_common_count']})")
    print(f"Average word length: {results['average_word_length']:.2f}")
    print(f"Paragraphs: {results['paragraphs']}")
    print(f"Sentences: {results['sentences']}")
    print(f"Total words: {results['words']}")
    print(f"Top {top} words:")
    for i, (w, c) in enumerate(results['top_counts'].most_common(top), start=1):
        print(f"  {i}. {w} — {c}")


def main() -> None:
    parser = argparse.ArgumentParser(description='News article text analysis')
    parser.add_argument('--file', '-f', help='Path to article file')
    parser.add_argument('--word', '-w', help='Specific word to count')
    parser.add_argument('--exclude-stopwords', action='store_true', help='Exclude common stopwords when finding most common word')
    parser.add_argument('--top', '-t', type=int, default=10, help='Show top N most common words')
    parser.add_argument('--test', action='store_true', help='Run built-in self-test example')
    args = parser.parse_args()

    if args.test:
        sample = (
            "President signs new bill into law. The law will affect many communities. "
            "In related news, experts say the change could be significant.\n\n"
            "This is the second paragraph of the article. It contains several sentences."
        )
        text = sample
    else:
        text = load_text(args.file)

    results = analyze_text(text, target=args.word, exclude_stopwords=args.exclude_stopwords)
    print_results(results, args.word, args.top)


if __name__ == '__main__':
    main()
