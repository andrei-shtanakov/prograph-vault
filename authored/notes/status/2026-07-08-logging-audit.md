---
title: Logging/observability audit and unification plan
type: note
status: living
owner: Andrei
updated: 2026-07-08
---

# ATP — logging audit and unification plan

**Date:** 2026-07-08 · **Repos inspected:** 14
> Companion to `status/2026-07-08-1228-status.md`; feeds `ecosystem-roadmap.md` §Observability.

## Bottom line

The instinct that logging is inconsistent is only half right. Good news: **a unified standard already
exists and works end-to-end** — `observability-contract/v1` (an OpenTelemetry-compatible JSON schema)
plus a shared emitter, `obs.py` (canonical in spec-runner) with a Rust port `obs.rs`. Logs are written
to `<logs_dir>/<ULID>/<service>-<pid>.jsonl`, and `dispatcher` reads them via that same contract. So
"bringing it to consistency" isn't a from-scratch job — it's **catching the rest up to the already-adopted
standard** and fixing a couple of divergences.

Bad news: only 3 core repos actually follow the standard, one more (atp-platform) logs structurally but
in its **own** format, and the most active new service (proctor) plus all the young periphery are either
on bare `logging`, `print()`, or no logging at all.

## Current state by repo

| Repo | Logging approach | On contract v1? | Comment |
|---|---|---|---|
| **spec-runner** | `obs.py` (structlog→JSON) — **source of truth** | ✅ | Canonical. 333 lines, actively developed |
| **arbiter** | Rust `tracing`/`log` + `obs.rs`; vendored `obs.py` in orchestrator | ✅ | Emits `service.name=arbiter` |
| **Maestro** | vendored `obs.py` | ✅ (but the copy is stale) | see Divergence 1 |
| **atp-platform** | its own `atp-core/logging.py` (structlog: `correlation_id`, `version`, `hostname`) | ⚠️ **own format** | Structural, but NOT the contract's fields. `atp` is in the service enum, but the shape differs |
| **proctor** | bare `logging.getLogger(__name__)` (25 modules) | ❌ | **Main gap**: `proctor-a` is in the enum and dispatcher expects its logs in contract format, but it doesn't write them |
| **dispatcher** | doesn't log itself — it's a **consumer** of logs | n/a | Parses `SeverityNumber/Text`, `Body`, `Attributes.pipeline_id`, `Resource.service.name` |
| **deployer** | no logging, ~13 `print()` calls | ❌ | Gap |
| **prograph** | no logging (Rust — no `tracing`; Python — no `logging`) | ❌ | A gap for a production tool |
| **robin-runtime** | none (M0 skeleton, 7 `print()`) | ❌ | Early days, but should be built in now |
| **steward** | none (spec-only repo) | n/a | Almost no code |
| **spec-runner-vscode** | `console.*` (TS, client) | n/a | Client-side logging, fine |
| **open-prose / robin-toolkit / prograph-vault** | docs-only | n/a | No code |

> Aside: `print()` in the CLI repos (atp-platform ~705, spec-runner ~343, arbiter ~307) is mostly
> Typer/Rich UX output and tests, not debug litter. But operational events that go through `print`
> bypass the structured sink and never reach dispatcher — worth migrating to the logger over time.

## Contract v1 format (target)

One JSON record per line (`.jsonl`), OTel fields:
`Timestamp`, `ts_iso`, `SeverityText` (DEBUG/INFO/WARN/ERROR/FATAL), `SeverityNumber` (1–24), `TraceId`,
`SpanId`, `TraceFlags`, `Body`, `Resource.service.name` (enum: `maestro|spec-runner|arbiter|atp|proctor-a`),
`Attributes` (required `event` in `foo.bar` style, `pipeline_id` as a ULID; optional `task_id`, `module`,
`error{type,message,stack,caused_by}`). The schema is canonical and byte-identical in Maestro and arbiter.

## Explicit divergences (what to fix)

**1. Vendored `obs.py` has drifted from the source.** Three copies, three different md5s:
- `spec-runner/src/spec_runner/obs.py` — **333 lines** (canon, ahead: added `_StderrProxy`, `sys`, `cast`).
- `Maestro/maestro/_vendor/obs.py` — 283 lines, marked "Vendored from spec-runner@fa6b106…".
- `arbiter/orchestrator/_vendor/obs.py` — 282 lines.

The Maestro/arbiter copies are **~50 lines behind canon** (≈98–99 diverged diff lines). The header itself
says "Do not edit locally. To update: re-copy and bump marker" — but the re-copy hasn't happened in a
while. Risk: divergent sink/secret-redaction behavior between the orchestrator and spec-runner.

**2. atp-platform logs structurally but not to the contract.** `atp-core/logging.py` builds its own field
set (`correlation_id`, `version`, `hostname`) instead of the contract's OTel fields. `atp` is listed in the
service enum — so the intent to be compatible exists, but the shape doesn't match. dispatcher can't
correctly parse its logs as they stand.

**3. proctor — the most active service, with no contract-compliant logs.** 250 commits, `proctor-a` is in
the enum, dispatcher is ready to read it — but proctor logs via bare stdlib `logging`, no JSON sink, no
contract fields. Monitoring proctor through dispatcher effectively doesn't work yet.

**4. Periphery with no logging:** deployer, prograph, robin-runtime.

## Unification plan (by priority)

**P1. Pull `obs.py` out of vendoring into a shared package.** Root cause is copy-paste. Extract the
canonical `obs.py` into an installable package (e.g. `atp-obs`/`orchestra-obs`, or export it from
spec-runner as `spec_runner.obs`) and depend on it instead of `_vendor/`. This removes divergence #1
permanently.
_Quick patch until then:_ re-copy the canon into Maestro and arbiter, bump the commit marker.

**P2. Move proctor onto the contract.** Wire up the `obs` emitter, write `service.name=proctor-a`
(already in the enum), format `<logs_dir>/<ULID>/proctor-a-<pid>.jsonl`. This turns on proctor monitoring
in dispatcher (and incidentally closes the `data/state.db` vs logs tail from the status report — see
`status/2026-07-08-1228-status.md` misalignment 2).

**P3. Bring atp-platform to the contract.** Either add a structlog processor to `atp-core/logging.py`
that renders the contract's OTel fields (can be a second sink), or reuse `obs.py`. Keep `correlation_id`
as `Attributes.task_id` or an extra field.

**P4. Add logging to the periphery:** prograph (Rust `tracing` + Python via the shared `obs`), deployer,
robin-runtime (build in `obs` from M1).

**P5. Lock it in with CI discipline.** Add a check "`obs.py` copy == canon" (while vendoring is still
alive) and validate a log sample against `log-schema.json`. `prograph` already detects contracts/drift —
this can hang off its indexing.

**P6. Gradually push operational `print()` calls into the structured logger** (keep Rich/Typer only for
user-facing CLI output).

### Target picture
One `obs` package (Python) + `obs.rs` (Rust) → every service writes `.jsonl` per
`observability-contract/v1` with its own `service.name` → dispatcher/prograph read it uniformly. The
standard is already chosen — what's left is rolling it out and no longer copy-pasting the emitter.
