---
title: Documentation coherence audit — Maestro & arbiter (2026-05-23)
type: note
status: archived
owner: Andrei
updated: 2026-05-23
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# Documentation coherence audit — Maestro & arbiter (2026-05-23)

> Trigger: "there was work in Maestro and arbiter today, check the documentation".
> Mode: read-only over the repositories; edits made only to cowork artifacts (`COWORK_CONTEXT.md`, this report).

## TL;DR

1. Today **R-06b M4** was closed — the ATP→arbiter feedback loop. arbiter gained a 6th MCP tool `report_benchmark`, a `benchmark_runs` table, and the protocolVersion was raised **1.0.0 → 1.1.0**. In parallel, Maestro underwent a breaking refactor **Zadacha → Workstream** (v0.4.0).
2. **The main drift is the arbiter documentation.** Today only `Cargo.toml` and the contract schema were touched in the arbiter repo; README / CLAUDE.md / TODO.md / arbiter-spec.md still describe "5 tools" and know nothing about `report_benchmark`, `benchmark_runs`, or protocol 1.1.0.
3. **Maestro is well documented** (TODO, CHANGELOG, design specs, contract schema). The rename was carried through both code and docs; residual `zadacha` occurrences are only in the migration code (which is correct) and in historical analytical artifacts.
4. **Two positive findings — coherence holds:** the contract schema `report_benchmark-v1.schema.json` is byte-for-byte identical in both repos, and the vendored Maestro client does version negotiation against protocol 1.1.0. There is no compatibility break.
5. **The root `COWORK_CONTEXT.md` was updated** as part of this task (6 tools, R-06b/R-07 statuses, Maestro 0.4.0, protocol 1.1.0). Actions remain on the repository owner's side (see below).

## What changed today (git, 2026-05-23)

| Repo | Key commits | Substance |
|------|------------------|-------|
| arbiter | `e4b02a0`, `89cd305`, `aa72b40`, `aa38b37`, `7aeb6b1`, `151004b`, `cb5da64` | `benchmark_runs` table → `report_benchmark` handler → expose tool + protocol 1.1.0 → contract test → INVALID_PARAMS → input validation → schema-path fix |
| Maestro | `3066ded` (#19), `17eb295` (#20), `5edb359` (#21), `f1a64ea` | R-06b M4 arbiter wiring + Copilot follow-ups; then rename Zadacha→Workstream (v0.4.0) |

## Findings

| # | Where | Severity | What is wrong | Confirmation |
|---|-----|----------|------------|---------------|
| 1 | `arbiter/TODO.md:10` | 🔴 High | "(5 tools)", no `report_benchmark`; no record of closing R-06b M4 | code: `arbiter-mcp/src/server.rs:146,475` |
| 2 | `arbiter/README.md` (ASCII diagram ~:60-69 + prose `:253`) | 🔴 High | Lists 5 tools; no `report_benchmark`, protocol 1.1.0, `benchmark_runs` | code: `server.rs:418` (`"protocolVersion":"1.1.0"`) |
| 3 | `arbiter/CLAUDE.md`, `arbiter/arbiter-spec.md:22` | 🔴 High | Spec: "2 required tools: route_task, report_outcome"; `report_benchmark` and `benchmark_runs` not described | grep |
| 4 | root `COWORK_CONTEXT.md` (5 tools, R-06b pending, Maestro 0.2.0) | 🔴 High → ✅ fixed | Registry 2 weeks stale | fixed in this task |
| 5 | `Maestro/CHANGELOG.md:44`, `TODO.md:101` | 🟠 Med | Pin on arbiter `7aeb6b1`, but `151004b` (input validation) and `cb5da64` (schema path) landed after it — the recommended SHA does not include the hardening | `git log 7aeb6b1..HEAD` |
| 6 | `_cowork_output/decisions/2026-04-25-r06b-design.md:3` | 🟡 Low | Header "Status: draft, awaiting review", although §8 = Resolved/Recommended and the feature is already in code | self |
| 7 | `Maestro/_cowork_output/01..08-*.md` | 🟡 Low | Historical analysis references `Zadacha/ZadachaConfig/create_zadacha()` — the symbols no longer exist in code | grep |
| 8 | `Maestro/TODO.md:101` | 🟡 Low | Reference to commit `05cd04e` — it exists as an object but is not in the master line (probably before the squash-merge) | `git cat-file` |

> Note: `maestro/database.py:486-515` and `tests/test_database.py:1760` with the word `zadacha` are **migration code** (`ALTER TABLE ... RENAME`). Correct, no need to touch.

## What is in sync (verified, no action needed)

| Aspect | Status | Evidence |
|--------|--------|----------------|
| Contract `report_benchmark-v1.schema.json` | ✅ identical | `diff Maestro/_cowork_output/benchmark-contract/… arbiter/arbiter-mcp/tests/contract/…` → identical |
| Version compatibility of protocol 1.1.0 | ✅ negotiation present | `Maestro/maestro/coordination/arbiter_client.py:59,529,542` (`ARBITER_PROTOCOL_VERSION`, `MIN_ARBITER_PROTOCOL`, `_parse_version`) |
| Maestro R-06b M4 in docs | ✅ documented | `Maestro/TODO.md:99-101`, `CHANGELOG.md:21-47` |
| Maestro rename in docs | ✅ carried through | `CHANGELOG.md`, `README.md`, `CLAUDE.md`, `pyproject.toml` (v0.4.0) |

## Edits made (cowork artifacts)

`COWORK_CONTEXT.md`:
- update date `2026-05-08 → 2026-05-23`;
- registry: Maestro `0.2.0 → 0.4.0 (Workstream API)`; arbiter — "protocol 1.1.0", "R-06b M4 ✅";
- ASCII map: Maestro `v0.4.0`; benchmark block `M1–M4 ✅` + `report_benchmark → arbiter (benchmark_runs)`; arbiter box `MCP tools (6)` + `report_benchmark` + lines `Protocol: MCP 1.1.0` and `Table: + benchmark_runs`;
- section "Maestro ↔ Arbiter": "Tools (6)" + bullet `report_benchmark` + a note about version negotiation and schema sync;
- section "Maestro ↔ ATP": status `🟢 M1–M4 ✅, M5 pending`; M2/M3/M4 spelled out with SHAs, noted that the arbiter docs are not updated;
- roadmap: `R-06b M2/M3/M4 ✅`, `R-06b M5 pending`, `R-07 🟢 unblocked`, a new line about `report_benchmark (MCP 1.1.0)`.

## Recommended actions

**arbiter (repository, read-only for cowork — owner needed):**
- Update `README.md` (diagram + prose list), `CLAUDE.md`, `TODO.md`, `arbiter-spec.md`: the 6th tool `report_benchmark`, the `benchmark_runs` table, protocolVersion 1.1.0, a note that R-06b M4 is closed.
- Add to `arbiter-spec.md` acceptance criteria for `report_benchmark` (happy / duplicate-idempotency / validation-reject) — the tests already exist (`server.rs:1086`, contract test), but the spec does not describe them.

**Maestro (repository):**
- Bump the recommended arbiter SHA from `7aeb6b1` to `cb5da64` (or HEAD) in `CHANGELOG.md:44` and `TODO.md:101` — the current pin does not include the input-validation hardening `151004b`.
- Fix the reference to commit `05cd04e` in `TODO.md:101` to the real merged SHA `3066ded`.
- (Optional) Mark `_cowork_output/01..08-*.md` as historical or run the rename `Zadacha→Workstream` over the symbols, if these docs are used as a live reference.

**cowork artifacts (I can do this myself on your go-ahead):**
- Move the header of `decisions/2026-04-25-r06b-design.md` from `draft → Implemented (2026-05-23)`.
