---
title: ADR: Unified Ecosystem KB on prograph-vault
type: adr
status: accepted
owner: Andrei
updated: 2026-07-05
---

# ADR: Unified Ecosystem KB on prograph-vault (git-controlled)

> Date: 2026-07-05 · Status: **Proposed** → Accepted (KB is live) · Role: TPM/architect
> Related: [[project-repo-topology-decision]], prograph/prograph-vault, [[project-spec-governance-layer]] (steward),
> dispatcher (monitoring), COWORK_CONTEXT.md (registry)

## TL;DR

1. **Problem:** coordination through the root (`_cowork_output/` + `COWORK_CONTEXT.md` + per-repo
   CLAUDE.md) has turned into a mess with no rules. BUT we cannot build a new repo — **there are
   already 2-3 overlapping stores**, and a new one would become a 4th fragment.
2. **Decision:** promote **prograph-vault** to a unified **Ecosystem KB** (give it git). It already
   has the skeleton: `contracts/`, `projects/`, `mcp_patterns/`, `claude-kb/`, Obsidian + a connected MCP.
3. **The key is not the repo, but the three rules that were missing:** information architecture (what
   goes where), SSOT boundaries (who is the owner, so nothing gets duplicated), lifecycle (when to archive).
4. **The main structural principle — `authored/` vs `derived/`:** people own rules/ADRs/
   templates; prograph/tools write into derived (graph, contract snapshots, digests) — do not touch
   these by hand.
5. **SSOT invariant (against duplication, the theme of the whole day):** the KB **references**
   contracts but **does not own** them — authority remains in the producing repo. Repo-local rules
   live in the repo's CLAUDE.md; the KB holds only cross-cutting knowledge.

## Context: three existing stores

| Store | What it holds | Problem |
|---|---|---|
| `_cowork_output/` (root git) | ADRs, plans, roadmap, status, contracts, devtools, spec drafts, `.pptx`, `заметки.txt` | a mess of ~20 categories mixed together |
| `prograph-vault/` (no git) | `contracts/`, `projects/`, `mcp_patterns/`, `claude-kb/digests/`, `index.md` | already a KB, but not versioned, mixed authored/derived |
| `COWORK_CONTEXT.md` (root) | project registry + integration map | kept separate from the rest of the knowledge |

## Decision: information architecture

prograph-vault is restructured (the name can be changed later to `ecosystem-kb`/`commons` — for now
"vault" hints at prograph ownership, whereas the role has become ecosystem-wide):

```
prograph-vault/                      # = Ecosystem KB (git init)
├── CLAUDE.md                        # rules of the KB itself (naming, lifecycle, authored/derived)
├── index.md
├── authored/                        # PEOPLE own — git-review mandatory
│   ├── rules/                       # 🆕 cross-cutting: code-style, gui, tui, library-usage
│   │   ├── code-style.md
│   │   ├── gui.md · tui.md
│   │   └── libraries.md
│   ├── decisions/                   # ADRs (cross-repo) — from _cowork_output/decisions
│   ├── templates/                   # 🆕 spec templates, steward profiles (lite/team), scaffolds
│   ├── skills/                      # project-specific skills (or pointers to Cowork skills)
│   ├── notes/                       # plans, intentions, cross-cutting TODO
│   └── registry/                    # COWORK_CONTEXT (registry + integration map)
└── derived/                         # TOOLS write — do NOT touch by hand
    ├── graph/                       # prograph output (structure, deps, MCP calls)
    ├── contracts/                   # contract SNAPSHOTS for search (not the authority!)
    ├── projects/                    # auto-facts per repo (prograph)
    └── digests/                     # claude-kb/digests (auto)
```

## SSOT boundaries (anti-duplication)

| Type of knowledge | Owner (SSOT) | Role of the KB |
|---|---|---|
| Inter-repo contract | **producing repo** (vendored inward) | `derived/contracts/` — snapshot/index for search, NOT the authority |
| Repo-local rules | **repo's CLAUDE.md** | none; CLAUDE.md references `authored/rules/`, does not copy |
| Cross-cutting rules (style/gui/tui/lib) | **KB `authored/rules/`** | owns |
| Code change history | **repo's git** | none; `authored/decisions/` holds the cross-repo *why* (ADRs) |
| Project registry | **KB `authored/registry/`** (COWORK_CONTEXT moves in) | owns; the root keeps a pointer |
| Runtime skills | **the Cowork skills mechanism** (`.claude/skills`, plugins) | `authored/skills/` — sources/docs/pointers |
| Repo structure/drift | **prograph** (auto) | `derived/graph/` |
| Transient session drafts | **`_cowork_output/`** (dev-scratch) | canon is *graduated* into the KB |

## Lifecycle and naming (the missing piece)

- **Naming:** `YYYY-MM-DD-<kebab>.md` for dated items; thematic ones use stable names.
- **ADR/doc states:** `Proposed → Accepted → Superseded|Archived`. Superseded references the
  replacement.
- **Archiving:** obsolete → `authored/**/archive/` with a **date + why** marker (do not delete —
  the history of decisions is valuable). The curation skill (Stage 2) does this on a cadence.
- **Graduation:** a draft is born in `_cowork_output/`; once it becomes canon, it moves into the KB
  under git-review. Runtime never reads `_cowork_output/` (the rule already exists).
- **Freshness:** the registry and `derived/` are re-audited on a schedule (the same freshness audit
  that used to be done by hand).

## Migration (from 3 stores → KB)

| From | To |
|---|---|
| `_cowork_output/decisions/*` | `authored/decisions/` |
| `_cowork_output/{roadmap,status,plans}` | `authored/notes/` (or `decisions/` for ADRs) |
| `_cowork_output/contracts/` | `derived/contracts/` (snapshots) |
| `_cowork_output/devtools/` | `authored/skills/` or a separate tools path (pointer) |
| session spec drafts (C1/C2/C4/WS-002) | **into the owning repos** (placement rule); reusable profiles → `authored/templates/` |
| `prograph-vault/contracts,projects,mcp_patterns` | reclassification: snapshots → `derived/`, hand-authored → `authored/` |
| `COWORK_CONTEXT.md` (root) | `authored/registry/`, with a pointer at the root |
| `заметки.txt`, `.pptx` | `authored/notes/` or archive |

After migration, `_cowork_output/` is only transient dev-scratch.

## Stage 2 / Stage 3 (within this frame)

- **Stage 2 (curation/search)** — not a bespoke agent, but an assembly of what exists: Obsidian-MCP
  (search over the vault), prograph (populating `derived/`), a curation skill (archival/link-fix — the
  `consolidate-memory` pattern + freshness audit). Delineate from steward (spec-governance) and
  dispatcher (monitoring) so nothing gets duplicated.
- **Stage 3 (living governance)** — rules from `authored/rules/` become CI checks (like
  `gate-check`); drift is auto-detected (prograph) → surfaced (dispatcher) → fixed (the curation
  agent: PR + auto-sync of the registry). Convergence of KB + steward + prograph + dispatcher into a
  single ecosystem-governance. Automates the manual TPM role.

## Risks

1. **Junk drawer 2.0** — without adherence to `authored/derived` and the SSOT table, the KB becomes a
   mess again. IA and lifecycle are not optional.
2. **Authored↔derived leak** — prograph accidentally overwrites authored. Mitigation: a hard directory
   boundary, prograph writes only into `derived/`.
3. **The name `prograph-vault`** hints at prograph ownership, though the role is ecosystem-wide —
   consider renaming (`ecosystem-kb`), but that breaks prograph's references — a separate step.
4. **Contract duplication** again — strictly: the KB holds snapshots, authority stays in the producing
   repo.

## Recommended actions

- **[KB]** `git init` in prograph-vault; add the KB `CLAUDE.md` (naming/lifecycle/authored-derived
  rules); create the `authored/` + `derived/` skeleton.
- **[migration]** Move things per the table; reduce `_cowork_output` to dev-scratch.
- **[COWORK_CONTEXT]** Add the KB as a project (role "ecosystem knowledge base"); the registry moves
  into `authored/registry/`, with a pointer at the root.
- **[SSOT]** In each repo's CLAUDE.md — a reference to `authored/rules/` instead of copies of
  cross-cutting rules.
- **[Stage 2]** Set up the curation skill (freshness/archival) on top of Obsidian-MCP + prograph.
- **[later]** Decide on renaming vault → ecosystem-kb.
