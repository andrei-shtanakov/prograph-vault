<!-- prograph:generated -->

---
indexed_at: "2026-05-27T12:45:37Z"
kind: python
name: atp-sdk
parent: atp-platform
prograph: project
root: ./atp-platform/packages/atp-sdk
snapshot: 48
---

# atp-sdk

> Python SDK for the [ATP (Agent Test Platform)](https://github.com/andrei-shtanakov/atp-platform) benchmark platform.

## Manifest

- declared package: `atp-platform-sdk` version `2.0.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `CONFIG_DIR` (const) — `atp_sdk/auth.py:21`
- `CONFIG_FILE` (const) — `atp_sdk/auth.py:22`
- `load_token` (function) — `atp_sdk/auth.py:25`
- `save_token` (function) — `atp_sdk/auth.py:45`
- `login` (function) — `atp_sdk/auth.py:69`
- `logger` (const) — `atp_sdk/benchmark.py:14`
- `BenchmarkRun` (class) — `atp_sdk/benchmark.py:17`
- `logger` (const) — `atp_sdk/client.py:18`
- `AsyncATPClient` (class) — `atp_sdk/client.py:21`
- `RunStatus` (class) — `atp_sdk/models.py:8`
- `LeaderboardEntry` (class) — `atp_sdk/models.py:19`
- `BenchmarkInfo` (class) — `atp_sdk/models.py:28`
- `RunInfo` (class) — `atp_sdk/models.py:40`
- `logger` (const) — `atp_sdk/retry.py:13`
- `RETRYABLE_STATUS_CODES` (const) — `atp_sdk/retry.py:15`
- `retry_request` (function) — `atp_sdk/retry.py:49`
- `logger` (const) — `atp_sdk/sync.py:21`
- `ATPClient` (class) — `atp_sdk/sync.py:27`

## Modules

_7 files, 18 public symbols, 0 internal imports._

- `atp_sdk/__init__.py` (python)
- `atp_sdk/auth.py` (python)
- `atp_sdk/benchmark.py` (python)
- `atp_sdk/client.py` (python)
- `atp_sdk/models.py` (python)
- `atp_sdk/retry.py` (python)
- `atp_sdk/sync.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

- ← [[Maestro]] · `package_dep` · `atp-platform-sdk`
- ← [[atp-platform]] · `package_dep` · `atp-platform-sdk`

## Recent changes (last 5)

- snapshot 43 (2026-05-27T10:51:48Z): project added (added)

## Drift findings

_None._
