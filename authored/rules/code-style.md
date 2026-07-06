---
title: Code style (cross-cutting)
type: rule
status: accepted
owner: Andrei
updated: 2026-07-05
---

# Code style rules (cross-cutting)

> SSOT for all repos. A repo's CLAUDE.md **references** this, it does not copy. Repo-specifics go in the repo's CLAUDE.md.
> Based on the actual ecosystem toolchain (scan 2026-07-05).

## Python

- **Version:** new repos — `>=3.12`. Exception: `spec-runner` stays on `>=3.10` (consumer
  compatibility). Do not use 3.11+-only APIs (`datetime.UTC`, `enum.StrEnum`, `typing.Self`) in
  code that spec-runner imports.
- **Formatter/linter:** ruff. **`line-length = 100`** — canon. ⚠️ *Divergence:* one repo is on 88 —
  bring it to 100. Rules: `E, F, W, I, UP, B, C4, SIM`; `E501` ignored for deliberate long lines.
- **Typing:** annotations **required everywhere**, strict mode. ⚠️ *Divergence:* repos split between
  `pyrefly` and `mypy` — target: converge on one (recommendation — pyrefly, as in Maestro). Until
  convergence — each repo pins its choice in CLAUDE.md.
- **Data models:** `pydantic` for validated/serializable boundaries; `dataclass` for internal
  simple structures (like `SpecMeta`, `ExecutorConfig`).
- **Logging:** through the `get_logger("...")` wrapper over `structlog`. ⚠️ Do not use
  `logging.getLogger` directly in new code (there are 15 legacy occurrences — migrate on touch).
- **Async:** `anyio` for structured concurrency (like proctor's microkernel); bare `asyncio` is
  acceptable, but do not mix paradigms in a single module.
- **Environment/dependencies:** `uv` (`uv sync`, `uv run`). No `pip install` in prod.

## Tests

- `pytest`. Mark E2E/subprocess with `@pytest.mark.slow`; unit tests **mock** CLI/subprocesses.
- Refactoring invariant: **existing tests stay green without edits** (if behavior changes —
  the test changes too, deliberately).
- Golden/contract tests on the seams between repos (`tasks.md`, `project.yaml`, SpecMeta formats).

## Cross-repo conventions

- **agent-id:** `<harness>@<model>` (e.g. `claude@claude-opus-4-8`) for `generated_by`/`approved_by`.
- **Contracts are vendored inward** into the consumer repo as a pinned copy (marker + re-copy + pinned
  version; see `maestro/_vendor/obs.py`, `maestro/spec_runner.py`). **Do not** reference outward into
  `_cowork_output/`. Contract authority lives in the producer repo.
- **`source_prompt_version`** and content hashes — `sha256:<hex>`, not manual counters.

## Enforcement (Stage 3)

These rules → CI checks (ruff/typecheck gate) + `gate-check` linter on the seams. prograph catches drift.
