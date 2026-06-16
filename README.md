# pythonAssessment

This repository contains `pythonAssessment.py`, a script to perform basic text analysis on a news article. It implements the functions required by the assessment:

- `count_specific_word(text, search_word) -> int`
- `identify_most_common_word(text) -> Optional[str]`
- `calculate_average_word_length(text) -> float`
- `count_paragraphs(text) -> int`
- `count_sentences(text) -> int`

Usage examples:

```bash
python3 pythonAssessment.py --file article_assessment.txt --word pie
python3 pythonAssessment.py --test
```

The script also sets a module-level variable `article_text` containing the loaded article string, which can be imported when used as a module.

If you need a different output format for an autograder, tell me the exact expected lines and I'll adapt the script.
