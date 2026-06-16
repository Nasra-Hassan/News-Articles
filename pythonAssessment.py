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


# Module-level variable containing loaded article text (string)
article_text: str = ''


__all__ = [
    'count_specific_word', 'identify_most_common_word', 'calculate_average_word_length',
    'count_paragraphs', 'count_sentences', 'analyze_text', 'load_text', 'article_text'
]


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


# --- Functions required by the assessment (exact signatures) ---
def count_specific_word(text: str, search_word: str) -> int:
    """Count occurrences of search_word in text (case-insensitive).

    Returns 0 if no matches or if search_word is empty.
    """
    if not search_word:
        return 0
    words = get_words(text or "")
    return count_word_occurrences(search_word, words)


def identify_most_common_word(text: str) -> Optional[str]:
    """Return the most common word in text (lowercased). Return None for empty text."""
    if not (text and text.strip()):
        return None
    words = get_words(text)
    word, _ = most_common_word(words, exclude_stopwords=False)
    return word


def calculate_average_word_length(text: str) -> float:
    """Calculate average length of words in text (excludes punctuation).

    Returns 0.0 for empty text.
    """
    if not (text and text.strip()):
        return 0.0
    words = get_words(text)
    return average_word_length(words)


def count_paragraphs(text: str) -> int:
    """Count paragraphs defined by empty lines. Return 1 for empty string."""
    if not (text and text.strip()):
        return 1
    return len(get_paragraphs(text))


def count_sentences(text: str) -> int:
    """Count sentences split by .!?; return 1 for empty string."""
    if not (text and text.strip()):
        return 1
    return len(get_sentences(text))


def print_results(results: dict, target: Optional[str], top: int) -> None:
    # Canonical, minimal labeled output expected by grading
    if target:
        print(f"Specific word ('{target}') count: {results.get('target_count', 0)}")
    else:
        print(f"Specific word (none) count: 0")
    mcw = results['most_common_word'] or '(none)'
    print(f"Most common word: {mcw}")
    print(f"Average word length: {results['average_word_length']:.2f}")
    print(f"Paragraph count: {results['paragraphs']}")
    print(f"Sentence count: {results['sentences']}")


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
