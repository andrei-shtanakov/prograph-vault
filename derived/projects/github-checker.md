<!-- prograph:generated -->

---
indexed_at: "2026-07-10T17:42:43Z"
kind: python
name: github-checker
prograph: project
root: ./github-checker
snapshot: 6
---

# github-checker

> TUI-дашборд состояния нескольких GitHub-репозиториев: открытые PRы (с пометкой dependabot), ветки, security alerts и статус Copilot-ревью.

## Manifest

- declared package: `github-checker` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `COLUMNS` (const) — `github_checker/app.py:21`
- `GITHUB_URL` (const) — `github_checker/app.py:22`
- `rules_cell` (function) — `github_checker/app.py:35`
- `repo_row` (function) — `github_checker/app.py:47`
- `local_line` (function) — `github_checker/app.py:67`
- `details_text` (function) — `github_checker/app.py:83`
- `details_content` (function) — `github_checker/app.py:113`
- `AddRepoScreen` (class) — `github_checker/app.py:126`
- `SetPathScreen` (class) — `github_checker/app.py:154`
- `ConfirmScreen` (class) — `github_checker/app.py:187`
- `GithubCheckerApp` (class) — `github_checker/app.py:211`
- `default_config_path` (function) — `github_checker/config.py:12`
- `resolve_config_path` (function) — `github_checker/config.py:18`
- `load_config` (function) — `github_checker/config.py:38`
- `save_config` (function) — `github_checker/config.py:48`
- `add_repo` (function) — `github_checker/config.py:55`
- `remove_repo` (function) — `github_checker/config.py:68`
- `set_path` (function) — `github_checker/config.py:78`
- `DEPENDABOT_LOGIN` (const) — `github_checker/github.py:23`
- `COPILOT_LOGIN` (const) — `github_checker/github.py:24`
- `parse_pull` (function) — `github_checker/github.py:27`
- `parse_issues` (function) — `github_checker/github.py:39`
- `parse_branches` (function) — `github_checker/github.py:53`
- `copilot_state` (function) — `github_checker/github.py:58`
- `count_copilot_comments` (function) — `github_checker/github.py:66`
- `parse_ruleset_info` (function) — `github_checker/github.py:71`
- `format_bypass_actor` (function) — `github_checker/github.py:81`
- `parse_ruleset_details` (function) — `github_checker/github.py:99`
- `MAX_CONCURRENCY` (const) — `github_checker/github.py:114`
- `GhError` (class) — `github_checker/github.py:118`
- `fetch_repo` (function) — `github_checker/github.py:156`
- `fetch_all` (function) — `github_checker/github.py:241`
- `gh_ready` (function) — `github_checker/github.py:248`
- `list_rulesets` (function) — `github_checker/github.py:277`
- `get_ruleset` (function) — `github_checker/github.py:283`
- `set_ruleset_enforcement` (function) — `github_checker/github.py:288`
- `delete_ruleset` (function) — `github_checker/github.py:297`
- `build_ruleset_copy` (function) — `github_checker/github.py:302`
- `copy_ruleset` (function) — `github_checker/github.py:307`
- `LocalGitError` (class) — `github_checker/localgit.py:9`
- `local_status` (function) — `github_checker/localgit.py:29`
- `is_git_repo` (function) — `github_checker/localgit.py:65`
- `remote_url` (function) — `github_checker/localgit.py:76`
- `fetch` (function) — `github_checker/localgit.py:84`
- `pull_ff_only` (function) — `github_checker/localgit.py:89`
- `main` (function) — `github_checker/main.py:47`
- `REPO_RE` (const) — `github_checker/models.py:9`
- `RepoRef` (class) — `github_checker/models.py:12`
- `Config` (class) — `github_checker/models.py:26`
- `Branch` (class) — `github_checker/models.py:40`
- `CopilotReview` (class) — `github_checker/models.py:46`
- `PullRequest` (class) — `github_checker/models.py:53`
- `Issue` (class) — `github_checker/models.py:64`
- `RulesetInfo` (class) — `github_checker/models.py:73`
- `RulesetDetails` (class) — `github_checker/models.py:82`
- `LocalStatus` (class) — `github_checker/models.py:95`
- `RepoState` (class) — `github_checker/models.py:105`
- `protection_details_text` (function) — `github_checker/protection.py:31`
- `RepoPickerScreen` (class) — `github_checker/protection.py:50`
- `ProtectionScreen` (class) — `github_checker/protection.py:75`
- `parse_github_remote` (function) — `github_checker/snapshot.py:27`
- `RepoSnapshot` (class) — `github_checker/snapshot.py:33`
- `WorkspaceSnapshot` (class) — `github_checker/snapshot.py:42`
- `discover` (function) — `github_checker/snapshot.py:52`
- `build_snapshot` (function) — `github_checker/snapshot.py:57`
- `PULLS` (const) — `tests/fixtures.py:5`
- `BRANCHES` (const) — `tests/fixtures.py:20`
- `REVIEWS_WITH_COPILOT` (const) — `tests/fixtures.py:25`
- `REVIEWS_NO_COPILOT` (const) — `tests/fixtures.py:33`
- `REVIEW_COMMENTS` (const) — `tests/fixtures.py:37`
- `ISSUES` (const) — `tests/fixtures.py:43`
- `ALERTS` (const) — `tests/fixtures.py:59`
- `RULESETS_LIST` (const) — `tests/fixtures.py:64`
- `RULESET_DETAILS` (const) — `tests/fixtures.py:86`
- `STATE` (const) — `tests/test_app.py:27`
- `test_repo_row_normal` (function) — `tests/test_app.py:52`
- `test_repo_row_error` (function) — `tests/test_app.py:65`
- `test_repo_row_caps_at_100` (function) — `tests/test_app.py:70`
- `test_details_text` (function) — `tests/test_app.py:79`
- `test_details_text_error` (function) — `tests/test_app.py:86`
- `test_details_text_includes_link` (function) — `tests/test_app.py:91`
- `test_details_content_has_link_span` (function) — `tests/test_app.py:95`
- `test_local_line_variants` (function) — `tests/test_app.py:102`
- `test_details_text_shows_local_block` (function) — `tests/test_app.py:114`
- `test_rules_cell_variants` (function) — `tests/test_app.py:227`
- `test_repo_row_rules_column` (function) — `tests/test_app.py:236`
- `test_default_config_path_respects_xdg` (function) — `tests/test_config.py:18`
- `test_resolve_config_path_explicit_wins` (function) — `tests/test_config.py:25`
- `test_resolve_config_path_migrates_legacy` (function) — `tests/test_config.py:30`
- `test_resolve_config_path_existing_target_not_overwritten` (function) — `tests/test_config.py:44`
- `test_load_missing_creates_empty` (function) — `tests/test_config.py:58`
- `test_load_missing_creates_parent_dirs` (function) — `tests/test_config.py:65`
- `test_save_load_roundtrip` (function) — `tests/test_config.py:72`
- `test_save_load_roundtrip_with_path` (function) — `tests/test_config.py:81`
- `test_add_repo` (function) — `tests/test_config.py:89`
- `test_add_repo_preserves_existing_path` (function) — `tests/test_config.py:97`
- `test_add_repo_duplicate_noop` (function) — `tests/test_config.py:104`
- `test_add_repo_invalid_raises` (function) — `tests/test_config.py:110`
- `test_remove_repo` (function) — `tests/test_config.py:117`
- `test_set_path_sets_and_clears` (function) — `tests/test_config.py:125`
- `test_set_path_unknown_name_is_noop` (function) — `tests/test_config.py:142`
- `RESPONSES` (const) — `tests/test_fetch.py:19`
- `test_gh_ready_missing_binary` (function) — `tests/test_fetch.py:98`
- `FakeProc` (class) — `tests/test_fetch.py:107`
- `test_local_status_missing_path` (function) — `tests/test_localgit.py:34`
- `test_local_status_non_git_dir` (function) — `tests/test_localgit.py:40`
- `test_local_status_no_upstream` (function) — `tests/test_localgit.py:45`
- `test_local_status_dirty` (function) — `tests/test_localgit.py:56`
- `test_local_status_ahead_of_upstream` (function) — `tests/test_localgit.py:63`
- `test_fetch_unreachable_remote_raises` (function) — `tests/test_localgit.py:78`
- `test_pull_ff_only_succeeds` (function) — `tests/test_localgit.py:86`
- `test_git_binary_missing` (function) — `tests/test_localgit.py:98`
- `test_is_git_repo_true_for_clone` (function) — `tests/test_localgit.py:113`
- `test_is_git_repo_false_for_plain_dir` (function) — `tests/test_localgit.py:119`
- `test_is_git_repo_false_for_missing_path` (function) — `tests/test_localgit.py:123`
- `test_pull_ff_only_divergence_raises` (function) — `tests/test_localgit.py:127`
- `test_main_exits_on_corrupt_config` (function) — `tests/test_main.py:8`
- `test_main_exits_when_gh_not_ready` (function) — `tests/test_main.py:23`
- `test_config_coerces_string_repos` (function) — `tests/test_models.py:15`
- `test_config_accepts_repo_ref_with_path` (function) — `tests/test_models.py:22`
- `test_config_rejects_bad_repo` (function) — `tests/test_models.py:27`
- `test_repo_ref_rejects_bad_name` (function) — `tests/test_models.py:32`
- `test_repo_state_defaults` (function) — `tests/test_models.py:37`
- `test_local_status_holds_desync` (function) — `tests/test_models.py:46`
- `test_pull_request_optional_copilot` (function) — `tests/test_models.py:52`
- `test_parse_pull_regular` (function) — `tests/test_parsers.py:21`
- `test_parse_pull_dependabot` (function) — `tests/test_parsers.py:29`
- `test_parse_branches` (function) — `tests/test_parsers.py:33`
- `test_copilot_state_found` (function) — `tests/test_parsers.py:38`
- `test_copilot_state_absent` (function) — `tests/test_parsers.py:42`
- `test_count_copilot_comments` (function) — `tests/test_parsers.py:46`
- `test_parse_ruleset_info` (function) — `tests/test_parsers.py:50`
- `test_parse_ruleset_details` (function) — `tests/test_parsers.py:58`
- `test_format_bypass_actor_variants` (function) — `tests/test_parsers.py:71`
- `DETAILS` (const) — `tests/test_protection.py:13`
- `INFO` (const) — `tests/test_protection.py:24`
- `test_protection_details_text` (function) — `tests/test_protection.py:27`
- `test_protection_details_text_empty_lists` (function) — `tests/test_protection.py:39`
- `test_build_ruleset_copy_strips_service_fields` (function) — `tests/test_rulesets_ops.py:28`
- `test_discover_finds_only_git_dirs` (function) — `tests/test_snapshot.py:40`

## Modules

_21 files, 140 public symbols, 88 internal imports._

- `github_checker/__init__.py` (python)
- `github_checker/app.py` (python)
- `github_checker/config.py` (python)
- `github_checker/github.py` (python)
- `github_checker/localgit.py` (python)
- `github_checker/main.py` (python)
- `github_checker/models.py` (python)
- `github_checker/protection.py` (python)
- `github_checker/snapshot.py` (python)
- `tests/conftest.py` (python)
- `tests/fixtures.py` (python)
- `tests/test_app.py` (python)
- `tests/test_config.py` (python)
- `tests/test_fetch.py` (python)
- `tests/test_localgit.py` (python)
- `tests/test_main.py` (python)
- `tests/test_models.py` (python)
- `tests/test_parsers.py` (python)
- `tests/test_protection.py` (python)
- `tests/test_rulesets_ops.py` (python)
- `tests/test_snapshot.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 2 (2026-07-10T10:08:54Z): project added (added)

## Drift findings

_None._
