---
title: arbiter — activity journal
type: journal
source: kb-save
project: arbiter
updated: 2026-07-12
---

# arbiter — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 12:45 — decision: RD-006 Capability/Authority split design drafted (PR #49)

- docs/2026-07-12-authority-split-design.md: arbiter owns Capability decision +
  Authority enforcement contract; steward owns policy data (vendored pinned copy,
  agents-catalog pattern). role x phase allowlist (decompose|implement|review|
  benchmark x authoring|execution|merge|pr), wire = constraints.authority_context
  (kept out of the 22-dim vector), pipeline capability->authority->scoring,
  exact harness@model + harness@* only, all-denied = REJECT with
  authority_no_authorized_candidates + audit payload. Tools/escalation = v2.
- M1..M5 plan + contracts/capability promotion; OQ-1..3 open for owner review.
- Links: https://github.com/andrei-shtanakov/arbiter/pull/49

## 2026-07-12 13:06 — change: RD-006 M1 shipped as PR #50 (authority enforcement + both contracts)

- arbiter-core/src/authority.rs (pure engine, fail-closed), wire
  constraints.authority_context (excluded from feature vector), route_task
  step 3b (capability -> authority -> scoring), REJECT
  authority_no_authorized_candidates + audit at metadata.authority,
  load_authority with sha256 provenance + hot-reload, contracts/authority/ +
  contracts/capability/ with live-output tests, conformance script (+7 tests).
- Design refinement: retired-model check applies to exact pins only
  (wildcards covered by routable requirement; catalog CI owns live retired refs).
- 15/15 cargo targets, 107 pytest, clippy clean.
- Links: https://github.com/andrei-shtanakov/arbiter/pull/50

## 2026-07-12 14:38 — result: RD-006 M2..M5 complete; authority ACTIVE

- M1+review merged (#50/#51). M2 = steward #9 (profiles/authority.yaml SSOT).
  M4 = Maestro #74 (authority_context on every route call) — deliberately
  BEFORE M3: activating deny without the context would reject all routing.
  M3 = arbiter #52 (ACTIVE vendored config/authority.toml @ steward SSOT
  45eddb3d…, AUTHORITY_PINNED_SHA CI gate, live fail-closed e2e proof:
  context-less route_task = reject/authority_no_authorized_candidates).
- M5 = vault PR (this one): RD-006 evidence_rules -> board flips verified.
