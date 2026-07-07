<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: python
name: spec-runner-tasks
prograph: project
root: ./spec-runner-tasks
snapshot: 1
---

# spec-runner-tasks

## Manifest

- declared package: `textkit` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `main` (function) — `src/textkit/cli.py:131`
- `encode` (function) — `src/textkit/utils/base64_codec.py:6`
- `decode` (function) — `src/textkit/utils/base64_codec.py:11`
- `factorization_string` (function) — `src/textkit/utils/factorization_string.py:6`
- `fib` (function) — `src/textkit/utils/fibonacci.py:4`
- `gcd` (function) — `src/textkit/utils/gcd_lcm.py:4`
- `lcm` (function) — `src/textkit/utils/gcd_lcm.py:11`
- `is_palindrome` (function) — `src/textkit/utils/palindrome.py:4`
- `prime_factors` (function) — `src/textkit/utils/prime_factors.py:8`
- `primes_up_to` (function) — `src/textkit/utils/primes.py:4`
- `reverse_words` (function) — `src/textkit/utils/reverse_words.py:4`
- `to_roman` (function) — `src/textkit/utils/roman.py:22`
- `from_roman` (function) — `src/textkit/utils/roman.py:33`
- `roman_add` (function) — `src/textkit/utils/roman_add.py:6`
- `rot13` (function) — `src/textkit/utils/rot13.py:11`
- `shout` (function) — `src/textkit/utils/shout.py:1`
- `slug_table` (function) — `src/textkit/utils/slug_table.py:10`
- `slugify` (function) — `src/textkit/utils/slugify.py:8`
- `convert` (function) — `src/textkit/utils/temperature.py:24`
- `titlecase` (function) — `src/textkit/utils/titlecase.py:4`
- `unique_slugify` (function) — `src/textkit/utils/unique_slugify.py:6`
- `count` (function) — `src/textkit/utils/wordcount.py:4`
- `test_encode_ascii` (function) — `tests/test_base64_codec.py:6`
- `test_round_trip_unicode` (function) — `tests/test_base64_codec.py:11`
- `test_empty_encode` (function) — `tests/test_base64_codec.py:16`
- `test_empty_round_trip` (function) — `tests/test_base64_codec.py:21`
- `test_slugify_str_result` (function) — `tests/test_cli.py:13`
- `test_palindrome_bool_true` (function) — `tests/test_cli.py:19`
- `test_palindrome_bool_false` (function) — `tests/test_cli.py:25`
- `test_primes_list_space_joined` (function) — `tests/test_cli.py:31`
- `test_wordcount_dict_lines` (function) — `tests/test_cli.py:37`
- `test_roman_to_nested` (function) — `tests/test_cli.py:44`
- `test_roman_from_nested` (function) — `tests/test_cli.py:50`
- `test_base64_encode_decode_roundtrip` (function) — `tests/test_cli.py:56`
- `test_gcd_two_int_args` (function) — `tests/test_cli.py:64`
- `test_temperature_float_args` (function) — `tests/test_cli.py:70`
- `test_unique_slugify_nargs` (function) — `tests/test_cli.py:76`
- `test_slug_table_multiline_str_result` (function) — `tests/test_cli.py:82`
- `test_roman_add_two_string_args` (function) — `tests/test_cli.py:91`
- `test_value_error_to_stderr_exit_2` (function) — `tests/test_cli.py:97`
- `test_missing_command_exits` (function) — `tests/test_cli.py:105`
- `test_normal_case` (function) — `tests/test_factorization_string.py:8`
- `test_prime_input_renders_without_exponent` (function) — `tests/test_factorization_string.py:13`
- `test_smallest_valid_input` (function) — `tests/test_factorization_string.py:18`
- `test_prime_power` (function) — `tests/test_factorization_string.py:23`
- `test_large_residual_prime` (function) — `tests/test_factorization_string.py:28`
- `test_multiple_factors_render_in_ascending_order` (function) — `tests/test_factorization_string.py:33`
- `test_below_two_raises` (function) — `tests/test_factorization_string.py:38`
- `test_fibonacci_normal_case` (function) — `tests/test_fibonacci.py:8`
- `test_fibonacci_larger_n` (function) — `tests/test_fibonacci.py:13`
- `test_fibonacci_zero_is_empty` (function) — `tests/test_fibonacci.py:18`
- `test_fibonacci_one_is_seed` (function) — `tests/test_fibonacci.py:23`
- `test_fibonacci_two` (function) — `tests/test_fibonacci.py:28`
- `test_fibonacci_negative_raises` (function) — `tests/test_fibonacci.py:33`
- `test_gcd_normal_case` (function) — `tests/test_gcd_lcm.py:6`
- `test_gcd_coprime` (function) — `tests/test_gcd_lcm.py:11`
- `test_gcd_with_zero` (function) — `tests/test_gcd_lcm.py:16`
- `test_gcd_both_zero` (function) — `tests/test_gcd_lcm.py:22`
- `test_lcm_normal_case` (function) — `tests/test_gcd_lcm.py:27`
- `test_lcm_left_zero` (function) — `tests/test_gcd_lcm.py:32`
- `test_lcm_right_zero` (function) — `tests/test_gcd_lcm.py:37`
- `test_is_palindrome_normal_case` (function) — `tests/test_palindrome.py:6`
- `test_is_palindrome_empty_string` (function) — `tests/test_palindrome.py:11`
- `test_is_palindrome_non_palindrome` (function) — `tests/test_palindrome.py:16`
- `test_normal_case` (function) — `tests/test_prime_factors.py:8`
- `test_prime_input_is_its_own_factor` (function) — `tests/test_prime_factors.py:13`
- `test_smallest_valid_input` (function) — `tests/test_prime_factors.py:18`
- `test_prime_power` (function) — `tests/test_prime_factors.py:23`
- `test_large_residual_prime` (function) — `tests/test_prime_factors.py:28`
- `test_below_two_raises` (function) — `tests/test_prime_factors.py:33`
- `test_primes_normal_case` (function) — `tests/test_primes.py:6`
- `test_primes_includes_n_when_prime` (function) — `tests/test_primes.py:11`
- `test_primes_at_two` (function) — `tests/test_primes.py:16`
- `test_primes_one_is_empty` (function) — `tests/test_primes.py:21`
- `test_primes_negative_is_empty` (function) — `tests/test_primes.py:26`
- `test_reverse_words_normal_case` (function) — `tests/test_reverse_words.py:6`
- `test_reverse_words_empty_string` (function) — `tests/test_reverse_words.py:11`
- `test_reverse_words_whitespace_only` (function) — `tests/test_reverse_words.py:16`
- `test_reverse_words_single_word` (function) — `tests/test_reverse_words.py:21`
- `test_reverse_words_strips_outer_whitespace` (function) — `tests/test_reverse_words.py:26`
- `test_reverse_words_nonspace_separators` (function) — `tests/test_reverse_words.py:31`
- `test_to_roman_normal_case` (function) — `tests/test_roman.py:8`
- `test_from_roman_normal_case` (function) — `tests/test_roman.py:13`
- `test_round_trip_boundaries` (function) — `tests/test_roman.py:18`
- `test_from_roman_accepts_lowercase_and_whitespace` (function) — `tests/test_roman.py:26`
- `test_to_roman_below_range` (function) — `tests/test_roman.py:31`
- `test_to_roman_above_range` (function) — `tests/test_roman.py:37`
- `test_from_roman_rejects_non_canonical` (function) — `tests/test_roman.py:43`
- `test_from_roman_rejects_unknown_chars` (function) — `tests/test_roman.py:49`
- `test_from_roman_rejects_empty` (function) — `tests/test_roman.py:55`
- `test_roman_add_normal_case` (function) — `tests/test_roman_add.py:8`
- `test_roman_add_subtractive_result` (function) — `tests/test_roman_add.py:13`
- `test_roman_add_overflow_raises` (function) — `tests/test_roman_add.py:18`
- `test_roman_add_invalid_input_propagates` (function) — `tests/test_roman_add.py:24`
- `test_roman_add_empty_input_propagates` (function) — `tests/test_roman_add.py:30`
- `test_rot13_normal_case` (function) — `tests/test_rot13.py:6`
- `test_rot13_empty_string` (function) — `tests/test_rot13.py:11`
- `test_rot13_round_trip` (function) — `tests/test_rot13.py:16`
- `test_rot13_leaves_non_letters_unchanged` (function) — `tests/test_rot13.py:22`
- `test_rot13_wraps_around_alphabet` (function) — `tests/test_rot13.py:27`
- `TestShout` (class) — `tests/test_shout.py:10`
- `test_version_exposed` (function) — `tests/test_skeleton.py:6`
- `test_multi_row_table_is_aligned` (function) — `tests/test_slug_table.py:6`
- `test_column_widths_size_to_longest_entry` (function) — `tests/test_slug_table.py:18`
- `test_empty_list_is_header_only` (function) — `tests/test_slug_table.py:28`
- `test_no_trailing_newline` (function) — `tests/test_slug_table.py:33`
- `test_normal_case` (function) — `tests/test_slugify.py:6`
- `test_collapses_runs_of_non_alphanumerics` (function) — `tests/test_slugify.py:11`
- `test_empty_string` (function) — `tests/test_slugify.py:16`
- `test_all_punctuation` (function) — `tests/test_slugify.py:21`
- `test_celsius_to_fahrenheit` (function) — `tests/test_temperature.py:8`
- `test_celsius_to_kelvin` (function) — `tests/test_temperature.py:13`
- `test_fahrenheit_to_celsius` (function) — `tests/test_temperature.py:18`
- `test_kelvin_to_fahrenheit` (function) — `tests/test_temperature.py:23`
- `test_units_are_case_insensitive` (function) — `tests/test_temperature.py:28`
- `test_same_unit_returns_value_unchanged` (function) — `tests/test_temperature.py:33`
- `test_unknown_target_unit_raises` (function) — `tests/test_temperature.py:38`
- `test_unknown_source_unit_raises` (function) — `tests/test_temperature.py:44`
- `test_titlecase_normal_case` (function) — `tests/test_titlecase.py:6`
- `test_titlecase_empty_string` (function) — `tests/test_titlecase.py:11`
- `test_titlecase_whitespace_only` (function) — `tests/test_titlecase.py:16`
- `test_titlecase_single_word` (function) — `tests/test_titlecase.py:21`
- `test_titlecase_collapses_internal_whitespace` (function) — `tests/test_titlecase.py:26`
- `test_titlecase_strips_outer_whitespace` (function) — `tests/test_titlecase.py:31`
- `test_collision_appends_suffix` (function) — `tests/test_unique_slugify.py:6`
- `test_empty_list` (function) — `tests/test_unique_slugify.py:11`
- `test_no_collision_preserves_slugs` (function) — `tests/test_unique_slugify.py:16`
- `test_manufactured_collision_is_skipped` (function) — `tests/test_unique_slugify.py:21`
- `test_three_way_collision` (function) — `tests/test_unique_slugify.py:26`
- `test_count_normal_case` (function) — `tests/test_wordcount.py:6`
- `test_count_single_line` (function) — `tests/test_wordcount.py:12`
- `test_count_empty_string` (function) — `tests/test_wordcount.py:17`

## Modules

_41 files, 132 public symbols, 43 internal imports._

- `src/textkit/__init__.py` (python)
- `src/textkit/cli.py` (python)
- `src/textkit/utils/__init__.py` (python)
- `src/textkit/utils/base64_codec.py` (python)
- `src/textkit/utils/factorization_string.py` (python)
- `src/textkit/utils/fibonacci.py` (python)
- `src/textkit/utils/gcd_lcm.py` (python)
- `src/textkit/utils/palindrome.py` (python)
- `src/textkit/utils/prime_factors.py` (python)
- `src/textkit/utils/primes.py` (python)
- `src/textkit/utils/reverse_words.py` (python)
- `src/textkit/utils/roman.py` (python)
- `src/textkit/utils/roman_add.py` (python)
- `src/textkit/utils/rot13.py` (python)
- `src/textkit/utils/shout.py` (python)
- `src/textkit/utils/slug_table.py` (python)
- `src/textkit/utils/slugify.py` (python)
- `src/textkit/utils/temperature.py` (python)
- `src/textkit/utils/titlecase.py` (python)
- `src/textkit/utils/unique_slugify.py` (python)
- `src/textkit/utils/wordcount.py` (python)
- `tests/test_base64_codec.py` (python)
- `tests/test_cli.py` (python)
- `tests/test_factorization_string.py` (python)
- `tests/test_fibonacci.py` (python)
- `tests/test_gcd_lcm.py` (python)
- `tests/test_palindrome.py` (python)
- `tests/test_prime_factors.py` (python)
- `tests/test_primes.py` (python)
- `tests/test_reverse_words.py` (python)
- `tests/test_roman.py` (python)
- `tests/test_roman_add.py` (python)
- `tests/test_rot13.py` (python)
- `tests/test_shout.py` (python)
- `tests/test_skeleton.py` (python)
- `tests/test_slug_table.py` (python)
- `tests/test_slugify.py` (python)
- `tests/test_temperature.py` (python)
- `tests/test_titlecase.py` (python)
- `tests/test_unique_slugify.py` (python)
- `tests/test_wordcount.py` (python)

## Inbound references

- from [[spec-runner-test]]:
  - `tests/test_palindrome.py:5` → `utils.palindrome::is_palindrome`
  - `tests/test_primes.py:5` → `utils.primes::primes_up_to`
  - `tests/test_reverse_words.py:5` → `utils.reverse_words::reverse_words`
  - `tests/test_roman.py:7` → `utils.roman::from_roman`
  - `tests/test_roman.py:7` → `utils.roman::to_roman`
  - `tests/test_slugify.py:5` → `utils.slugify::slugify`
  - `tests/test_wordcount.py:5` → `utils.wordcount::count`

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
