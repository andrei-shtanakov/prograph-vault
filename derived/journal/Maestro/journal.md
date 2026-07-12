---
title: Maestro — activity journal
type: journal
source: kb-save
project: Maestro
updated: 2026-07-12
---

# Maestro — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 11:44 — change: WS-006 handoff M-1..M-4 implemented (PRs #72, #73)

- M-4 (PR #72, CI green, review addressed): EvidenceRef kind=gate-verdict —
  pipeline_id+gate_id+sha, pre-adoption additive; null-hole in ALL kinds'
  allOf branches closed (Copilot finding); inline WorkCorrelation copy synced.
- M-1..M-3 (PR #73, pending review): opt-in gates: config; ex-ante/ex-post
  guards shelling to steward risk-classify; fail-closed; NEEDS_REVIEW routing
  with SHA-bound operator-approval marker; verdict-records JSONL in
  logs/<ULID>/; advisory channel for host-enforced gates; READY->NEEDS_REVIEW
  edge added to workstream state machine; preflight gates-* checks.
- Links: maestro/gates.py, contracts/observability/evidence-ref.schema.json,
  https://github.com/andrei-shtanakov/Maestro/pull/72,
  https://github.com/andrei-shtanakov/Maestro/pull/73

## 2026-07-12 12:33 — result: gates live e2e passed (real steward x real GateKeeper)

- Both handoff PRs merged (#72, #73 -> master eedd7bf). Live e2e on real
  components: allow (docs scope) -> block (contracts scope, ecosystem-contract
  /critical via consumer registry) -> operator re-queue approval -> SHA
  invalidation on new commit -> ex-post scope_violation block. 25 verdict
  records in gate_verdicts.jsonl, every one round-trips into EvidenceRef
  kind=gate-verdict (schema-validated). maestro validate catches
  gates-steward-missing live.
- Observed: ex-ante docs/** classifies medium (unknown), not low — per-repo
  Maestro section of risk-model.yaml lacks a docs rule and name-based generic
  rules are excluded from ex-ante by design. Candidate data tweak in steward.
