---
title: "ADR: Contract authority must not live in _cowork_output/"
type: adr
status: accepted
owner: Andrei
updated: 2026-07-10
---

# ADR: Contract authority must not live in `_cowork_output/`

**Status:** Accepted (2026-07-10) · **Surfaced by:** /robin-init onboarding dry-run (M0)

## Context

The onboarding checklist (`authored/skills/onboarding/roles/developer.yaml`, step
`key-contracts`) asks a newcomer where the observability contract's *authority* lives. Reading
the snapshot `derived/contracts/https---all_ai_orchestrators-observability-contract-v1.md`
(owner `[[Maestro]]`), the recorded source path is:

```
_cowork_output/observability-contract/log-schema.json
```

This contradicts two established rules:

- **KB constitution §4 / `authored/README.md`:** contract *authority* lives in the **producing
  repo**; `derived/contracts/` holds only a search **snapshot**, not the source of truth.
- **Ecosystem rule (root `CLAUDE.md`, ADR-ECO-003 line):** `_cowork_output/` is dev-scratch —
  *"users and teams that install the projects do not have it"*; runtime never reads it, and
  canon is **vendored into the owning repo**, not referenced out into scratch.

So the observability contract's SSOT currently points into an **ephemeral** folder. When
`_cowork_output/` is cleaned (it "exists only on this machine and for a while"), the authority
path dangles — the snapshot in the KB would outlive its own source of truth.

(Related but distinct: `derived/contracts/obs-v1.md` is a **prograph test fixture**
`tests/fixtures/monorepo_mcp/…`, owner `[[prograph]]`, and must not be confused with the
ecosystem contract. The onboarding checklist was corrected to stop citing it.)

## Decision (accepted 2026-07-10)

The observability contract's authoritative schema MUST live in the **producing repo (Maestro)**
— e.g. `Maestro/<path>/log-schema.json` under version control — and `derived/contracts/` MUST
snapshot **that** path. No `derived/` contract snapshot may record its source as a
`_cowork_output/**` path.

Generalization: **contract authority MUST resolve to a producing repo, never to
`_cowork_output/`.** A snapshot whose `Owners`/source resolves into `_cowork_output/` is a
drift defect and MUST be re-pointed at the graduated in-repo copy.

## Consequences

- Move/confirm `log-schema.json` into Maestro; re-run prograph so the snapshot's source path
  updates to the in-repo location.
- Add a check (prograph or a gate) that flags any `derived/contracts/*` whose source resolves
  into `_cowork_output/`.
- Onboarding step `key-contracts` then teaches a durable authority path, not a scratch one.

## Notes

Ratified and executed 2026-07-10 (maintainer review):

- Maestro PR `feature/graduate-contracts`: `_cowork_output/observability-contract/` →
  `Maestro/contracts/observability/`; `_cowork_output/benchmark-contract/` →
  `Maestro/contracts/benchmark/`; live references updated (test SCHEMA_PATH,
  docs/debugging.md, benchmark README raw-URL).
- obs.py docstring pointer fixed in sync across spec-runner (source), Maestro and
  arbiter vendored copies (drift check stays clean).
- devtools PR `fix/drift-checker-contract-path`: benchmark compare path updated.
- `derived/contracts/…observability-contract-v1.md` source path updates on the next
  `prograph index` run (derived/ is tool-written — not hand-edited here).
- Outstanding from Consequences: the automated check flagging `derived/contracts/*`
  sources resolving into `_cowork_output/` (prograph or gate-check) — not yet built.
