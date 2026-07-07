<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: python
name: spec-runner-test
prograph: project
root: ./spec-runner-test
snapshot: 1
---

# spec-runner-test

## Manifest

- declared package: `textkit` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `pytest_sessionfinish` (function) — `conftest.py:14`
- `main` (function) — `src/textkit/cli.py:11`
- `is_palindrome` (function) — `src/textkit/utils/palindrome.py:6`
- `primes_up_to` (function) — `src/textkit/utils/primes.py:6`
- `reverse_words` (function) — `src/textkit/utils/reverse_words.py:6`
- `to_roman` (function) — `src/textkit/utils/roman.py:24`
- `from_roman` (function) — `src/textkit/utils/roman.py:35`
- `slugify` (function) — `src/textkit/utils/slugify.py:10`
- `count` (function) — `src/textkit/utils/wordcount.py:6`
- `test_is_palindrome_normal` (function) — `tests/test_palindrome.py:8`
- `test_is_palindrome_non_palindrome` (function) — `tests/test_palindrome.py:13`
- `test_is_palindrome_empty` (function) — `tests/test_palindrome.py:18`
- `test_is_palindrome_whitespace_only` (function) — `tests/test_palindrome.py:23`
- `test_primes_up_to_normal` (function) — `tests/test_primes.py:8`
- `test_primes_up_to_inclusive_bound` (function) — `tests/test_primes.py:13`
- `test_primes_up_to_below_two_empty` (function) — `tests/test_primes.py:18`
- `test_reverse_words_normal` (function) — `tests/test_reverse_words.py:8`
- `test_reverse_words_empty` (function) — `tests/test_reverse_words.py:13`
- `test_reverse_words_whitespace_only` (function) — `tests/test_reverse_words.py:18`
- `test_to_roman_normal` (function) — `tests/test_roman.py:10`
- `test_from_roman_normal` (function) — `tests/test_roman.py:19`
- `test_round_trip` (function) — `tests/test_roman.py:26`
- `test_to_roman_zero_raises` (function) — `tests/test_roman.py:32`
- `test_to_roman_4000_raises` (function) — `tests/test_roman.py:38`
- `test_from_roman_invalid_symbol_raises` (function) — `tests/test_roman.py:44`
- `test_from_roman_malformed_raises` (function) — `tests/test_roman.py:50`
- `test_from_roman_empty_raises` (function) — `tests/test_roman.py:56`
- `test_slugify_normal` (function) — `tests/test_slugify.py:8`
- `test_slugify_collapses_runs` (function) — `tests/test_slugify.py:13`
- `test_slugify_empty` (function) — `tests/test_slugify.py:18`
- `test_slugify_all_punctuation` (function) — `tests/test_slugify.py:23`
- `test_count_normal` (function) — `tests/test_wordcount.py:8`
- `test_count_single_line` (function) — `tests/test_wordcount.py:14`
- `test_count_empty` (function) — `tests/test_wordcount.py:19`

## Modules

_16 files, 34 public symbols, 6 internal imports._

- `conftest.py` (python)
- `src/textkit/__init__.py` (python)
- `src/textkit/cli.py` (python)
- `src/textkit/utils/__init__.py` (python)
- `src/textkit/utils/palindrome.py` (python)
- `src/textkit/utils/primes.py` (python)
- `src/textkit/utils/reverse_words.py` (python)
- `src/textkit/utils/roman.py` (python)
- `src/textkit/utils/slugify.py` (python)
- `src/textkit/utils/wordcount.py` (python)
- `tests/test_palindrome.py` (python)
- `tests/test_primes.py` (python)
- `tests/test_reverse_words.py` (python)
- `tests/test_roman.py` (python)
- `tests/test_slugify.py` (python)
- `tests/test_wordcount.py` (python)

## Inbound references

_None._

## Outbound references

- to [[spec-runner-tasks]]:
  - `tests/test_palindrome.py:5` → `utils.palindrome::is_palindrome`
  - `tests/test_primes.py:5` → `utils.primes::primes_up_to`
  - `tests/test_reverse_words.py:5` → `utils.reverse_words::reverse_words`
  - `tests/test_roman.py:7` → `utils.roman::from_roman`
  - `tests/test_roman.py:7` → `utils.roman::to_roman`
  - `tests/test_slugify.py:5` → `utils.slugify::slugify`
  - `tests/test_wordcount.py:5` → `utils.wordcount::count`

## Outbound edges

_None._

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
