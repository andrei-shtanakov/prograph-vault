---
title: Libretto rename inventory
type: note
status: proposed
owner: Andrei
updated: 2026-07-16
---

# TL;DR

- Inventory confirms this is a cross-repo ecosystem rename, not a local repo rename.
- Primary high-risk surfaces are `open-prose` core files and `atp-platform` vendored contracts/checker code.
- KB and workspace active references were updated after the core repo decision was accepted.
- The upstream `prose/` checkout is explicitly out of scope for mass rename.

# Libretto rename inventory

This note mirrors the dev inventory in `_cowork_output/integration/2026-07-16-libretto-rename-inventory.md` and records the KB-facing facts.

## Summary counts

| Pattern family | Main hits |
|---|---|
| `open-prose|OpenProse|openprose` | `open-prose` 134 files, `atp-platform` 49, `prograph-vault` 35, `_cowork_output` 24, upstream `prose` 342 |
| `.prose`, `prose.md`, `prose run`, `openprose.*` | `open-prose` 119 files, `atp-platform` 39, `prograph-vault` 7, upstream `prose` 147 |
| Core source files | `open-prose` has 121 `*.prose` files, 0 `*.prose.md`, 1 `prose.md` |
| ATP vendored fixtures | `atp-platform/method/contract/fixtures/openprose` has 51 files |

## KB-relevant update targets

| Target | Action |
|---|---|
| `authored/registry/registry.md` | Updated active registry from `open-prose` to `libretto` after repo rename landed |
| `authored/notes/2026-07-16-libretto-contracts-offer.md` | Supersedes the old OpenProse-named handoff with Libretto canonical names |
| `authored/notes/2026-07-16-libretto-contracts-response.md` | Records accepted downstream response under Libretto canonical names |
| `authored/notes/2026-07-16-register-prose-upstream-clone.md` | Preserve old provenance; clarify `open-prose` is becoming `libretto` |
| `authored/notes/status/*` | Do not mass rewrite historical status facts |
| `derived/**` | Do not manually edit unless owned by the generating tool/process |

## Boundary rules

- The KB owns the cross-cutting decision and registry view.
- Contract authority remains in the producing repo; consumers vendor pinned copies.
- Runtime code must not read `_cowork_output`.
- Upstream `prose/` is a separate project/provenance context.

## Next handoffs

| Repo | Handoff |
|---|---|
| `libretto` | Core rename merged to `main` with aliases |
| `atp-platform` | Dual-read `openprose.*` and `libretto.*`; rename checker surface |
| `devtools` | Workspace references updated after local directory rename |
| `prograph` | Tracked project docs updated after registry update |
| Neighbor repos | `CLAUDE.md` sibling lists updated from `../open-prose/` to `../libretto/` |
