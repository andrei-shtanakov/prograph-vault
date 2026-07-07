<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: python
name: robin-runtime
prograph: project
root: ./robin-runtime
snapshot: 1
---

# robin-runtime

> Implementation home for Robin, the AI chief of staff for the AI-Orchestrators ecosystem. Governed by [`../prograph-vault/ROBIN-SPEC.local.md`](../prograph-vault/ROBIN-SPEC.local.md); identity is…

## Manifest

- declared package: `robin-runtime` version `0.0.1`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `ask` (function) — `src/robin/agent.py:38`
- `build_prompt` (function) — `src/robin/agent.py:56`
- `load_config` (function) — `src/robin/config.py:37`
- `TEXT_SUFFIXES` (const) — `src/robin/kb.py:15`
- `SKIP_DIRS` (const) — `src/robin/kb.py:16`
- `MAX_FILE_BYTES` (const) — `src/robin/kb.py:21`
- `SCAFFOLDING_FILES` (const) — `src/robin/kb.py:24`
- `SCAFFOLDING_DIRS` (const) — `src/robin/kb.py:25`
- `Kb` (class) — `src/robin/kb.py:37`
- `test_grounding_ranks_authoritative_and_excludes_scaffolding` (function) — `tests/test_agent.py:13`
- `test_build_prompt_includes_sources_and_question` (function) — `tests/test_agent.py:30`
- `test_search_finds_agents_catalog_ssot` (function) — `tests/test_kb.py:12`
- `test_cowork_output_is_never_read` (function) — `tests/test_kb.py:24`

## Modules

_6 files, 13 public symbols, 3 internal imports._

- `src/robin/__init__.py` (python)
- `src/robin/agent.py` (python)
- `src/robin/config.py` (python)
- `src/robin/kb.py` (python)
- `tests/test_agent.py` (python)
- `tests/test_kb.py` (python)

## Inbound references

_None._

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
