---
title: atp-platform — activity journal
type: journal
source: kb-save
project: atp-platform
updated: 2026-07-12
---

# atp-platform — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 19:14 — decision: RD-007 LearningEvent design drafted (PR #248)

- docs/2026-07-12-rd-007-learning-event-design.md: LearningEvent is
  observational; graduation only via human-reviewed PR; federated
  producer-owned append-only stores + one schema + evidence_refs; governed
  paths across atp/robin-runtime/vault with CODEOWNERS as v1 ACCEPTANCE;
  first slice = Robin regression loop (gap -> event -> graduation PR ->
  regression gate). Producer=robin-runtime, graduation owner=atp (provenance).
  Schema path: method/contract/learning-event-v1.schema.json. M2 deferred:
  conformance-CI, no-runtime-writes scanner.
- Recon: no silent-write anti-pattern exists today; RD-007 formalizes the
  informal discipline. Note: local main typecheck currently broken by
  in-flight litellm dependency work (pyrefly hook skipped for docs commit).
- Links: https://github.com/andrei-shtanakov/atp-platform/pull/248

## 2026-07-12 19:29 — change: RD-007 M1a..M1c shipped (three PRs)

- M1a = atp #249: learning-event-v1.schema.json (observational-only, ULID ids,
  content provenance, vendored EvidenceRef v1 incl gate-verdict) + 20 contract
  tests + .github/CODEOWNERS (governed paths, v1 acceptance).
- M1b = robin-runtime #9: selfreview emits conformant events to
  var/learning_events.jsonl (content-addressed source.id; zero-breakage
  adapter); vendored schema pin; CODEOWNERS; drive-by fix of a
  calendar-dependent test red on master.
- M1c = vault PR (this one): CODEOWNERS for authored/** + RD-007
  evidence_rules -> board flips verified once atp #249 merges.

## 2026-07-12 19:37 — status: contracts-v1 COMPLETE — all RD items on live masters

- M1a (atp #249) + M1b (robin-runtime #9) + M1c (vault #20) merged. Live
  board with all five project snapshots (Maestro/arbiter/steward/
  spec-runner/atp-platform): RD-000..RD-007 implemented/verified,
  RD-007 verified. The contracts roadmap is fully closed, every status
  evidence-derived, zero manual ticks.
- Remaining threads (not roadmap items): RD-007 M2 (conformance-CI,
  no-runtime-writes scanner), Maestro handoff M-1..M-3 live gates in
  orchestrate, L2 routing-stats series, owner's in-flight litellm work in
  atp (main does not typecheck without it).
