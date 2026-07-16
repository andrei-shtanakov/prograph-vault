---
title: OpenProse -> Libretto full ecosystem rename
type: adr
status: accepted
owner: Andrei
updated: 2026-07-16
---

# TL;DR

- Decision proposal: rename the whole language/ecosystem from `OpenProse` to `Libretto`, not only the repository.
- New canonical surfaces: `libretto` repo/package/CLI, `.libretto` source files, `.libretto/runs` state, and `libretto.*` contract namespaces.
- Old `openprose.*` artifacts remain historical facts and should stay verifiable by consumers.
- The GitHub repo/local directory rename should happen after the core repo passes under the new name.
- Upstream `prose/` remains provenance/upstream context and is not part of the rename target.

# ADR: OpenProse -> Libretto full ecosystem rename

## Context

The workspace currently contains `open-prose/` as the downstream/spec-as-VM language repo and a separate `prose/` checkout as upstream `openprose/prose` reference. The local downstream has become active enough that a repo-only rename would be misleading: docs, CLI, file extensions, state paths, contracts, tests, and downstream consumers already encode the old name.

Important existing consumers:

- `atp-platform` vendors open-prose contracts and fixtures under `method/contract/openprose/` and implements `atp/evaluators/openprose_receipts/`.
- The KB has active notes for the open-prose contracts handoff and response.
- Workspace registry/devtools and sibling repo instructions mention `../open-prose/`.

## Decision

Adopt `Libretto` as the full identity.

| Surface | Old | New | Compatibility posture |
|---|---|---|---|
| Repository | `open-prose` | `libretto` | Rename after core PR is green |
| Brand | `OpenProse` | `Libretto` | Keep old name in provenance/history |
| CLI | `prose` | `libretto` | Deprecated alias during transition |
| Source extension | `.prose` | `.libretto` | Legacy read/import support |
| Responsibility extension | `.prose.md` | `.libretto.md` | Additive; local downstream has no current `*.prose.md` files |
| VM spec | `prose.md` | `libretto.md` | Legacy pointer only if needed |
| State dir | `.prose/runs` | `.libretto/runs` | Migration/import path required |
| Tool package | `openprose-tools` | `libretto-tools` | Wrapper only during transition |
| Import package | `openprose_tools` | `libretto_tools` | Wrapper only during transition |
| Receipt contract | `openprose.receipt.v1` | `libretto.receipt.v1` | Consumers dual-read |
| Run manifest | `openprose.run.v1` | `libretto.run.v1` | Consumers dual-read |
| Compile IR | `openprose.compile-ir.v1` | `libretto.compile-ir.v1` | Consumers dual-read |
| Statement IDs | `openprose.statement-id.v1` | `libretto.statement-id.v1` | Consumers dual-read |

## Consequences

- This is a breaking rename with a compatibility bridge, not a cosmetic rename.
- `atp-platform` must be updated before old contract names can be considered deprecated.
- Historical KB/status/fleet records should not be mass rewritten; active registry and handoff docs should be updated deliberately.
- The sibling upstream `prose/` checkout should stay named `prose`.

## Migration order

1. Record ADR and inventory in `_cowork_output/` and KB.
2. Rename core repo internals on a branch: package, brand, CLI, extensions, state paths, contracts, docs, examples, tests.
3. Add compatibility aliases/readers for `prose`, `.prose`, `.prose/runs`, and `openprose.*`.
4. Update `atp-platform` to read both `openprose.*` and `libretto.*`.
5. Update active KB registry/notes, root registry, devtools/workspace, prograph docs, and sibling `CLAUDE.md` path lists.
6. Rename GitHub repo and local directory.
7. Remove old aliases later only by a follow-up ADR.

## Linked draft artifacts

- Draft ADR: `all_ai_orchestrators/_cowork_output/decisions/2026-07-16-adr-openprose-to-libretto.md`
- Inventory: `all_ai_orchestrators/_cowork_output/integration/2026-07-16-libretto-rename-inventory.md`
- Reusable runbook: `all_ai_orchestrators/_cowork_output/plans/2026-07-16-libretto-migration-runbook.md`

## Acceptance record

Accepted: 2026-07-16
Approver: Andrei

Confirmed decisions:

- Full ecosystem rename `OpenProse` -> `Libretto`.
- `prose` remains a deprecated alias during transition.
- `.prose` remains legacy-readable; new files use `.libretto`.
- `.prose/runs` is not rewritten in place; `.libretto/runs` is the new default.
- `openprose.*` contracts remain historical-valid; new artifacts use `libretto.*`.
