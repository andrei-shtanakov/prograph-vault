# Ecosystem KB — rules (CLAUDE.md)

> Unified knowledge base of a multi-project ecosystem (promoted from prograph-vault, ADR 2026-07-05).
> This file is the **KB constitution**. All agents and humans follow it when reading/writing.

## 0.0. Orientation for Claude Code (operational)

> Read this before searching for or changing anything. Below is the actual state; the rules further
> down (§0+) are the target canon.

- **This is an Obsidian knowledge vault, not a code project.** There is no build/test/lint here — do
  not look for `package.json`/`pyproject.toml`/CI. "Verification" means consistency of frontmatter,
  links, and the `authored`/`derived` boundary — not `pytest`/`ruff`. The format is Markdown + YAML
  frontmatter (§7) and Obsidian `[[wiki-links]]`.
- **The main invariant before any write:** `authored/**` is written ONLY by humans (via git-review);
  `derived/**` is written ONLY by tools (prograph/digest skills) and is **regenerable** — manual
  edits there will be lost. Details in §1–§2, `authored/README.md`, `derived/README.md`.
- **The §3 map is now largely realized (migration complete, 2026-07-08).** What exists now:
  `authored/{rules,skills,decisions,notes,registry,roadmaps,contracts}`,
  `derived/{contracts,projects,digests,journal}`.
  Still NOT created: `authored/templates`, `derived/graph` (the prograph→graph promoter skill exists
  but graph output may be empty). Legacy dirs at the root (`contracts/`, `projects/`, `mcp_patterns/`,
  `claude-kb/`) are leftovers awaiting reclassification (mostly empty). When creating a missing
  `authored/*` subfolder, follow §3/§8 — do not invent a new structure. The migration checklist lives
  in `index.md` (all items closed as of 2026-07-08).
- **How work happens here:**
  - Curation/search/archival/graduation — the `kb-curator` skill
    (`authored/skills/kb-curator/SKILL.md`); it writes only to `authored/**`, other repos are read-only.
  - Knowledge search — Obsidian-MCP (`obsidian_simple_search`/`obsidian_complex_search`) + reading
    files; return paths + quotes, not a recollection from memory.
  - From sibling projects (atp-platform, Maestro, …) the **`kb-*` skills** reach into this KB over
    the filesystem (no Obsidian): `kb-load` (warm up a work area), `kb-search` (targeted lookup),
    `kb-session` (read-only start orientation) — all read-only, unrestricted; `kb-save` writes a
    per-project journal to `derived/journal/<project>/` (see §3/§4, ADR 2026-07-06). Sources live in
    `authored/skills/`; `authored/skills/install-skills.sh` distributes them into the sub-projects.
  - `derived/**` is populated by **prograph** (not kb-curator), except `derived/journal/` (kb-save).
  - Edits to `authored/**` — as a PR set under human review; do not auto-merge substantive changes.
- **Reading entry points:** `index.md` (navigation + migration status), this `CLAUDE.md` (rules),
  `authored/README.md` and `derived/README.md` (subfolder guardrails).

## 0. Purpose

The KB stores **cross-cutting knowledge of the ecosystem**: rules, ADRs, contracts (snapshots),
templates, skill-pointers, notes/plans, project registry. The KB is the **source of truth for
cross-cutting knowledge**; it does **not** duplicate what repos own (see §4).

## 1. Golden rules (invariants)

1. **`authored/` is written by HUMANS (via git-review). `derived/` is written by TOOLS.** Never mix.
2. **The KB references contracts but does not own them.** Authority lives in the producing repo.
3. **Repo-local rules live in the repo's CLAUDE.md.** The KB holds only cross-cutting knowledge; the
   repo's CLAUDE.md *references* `authored/rules/`, it does not copy them.
4. **Canon is born in `_cowork_output/` (dev-scratch) and graduated into the KB.** Runtime never reads
   `_cowork_output/`.
5. **Nothing is deleted — it is archived** with a date + reason. The history of decisions is valuable.

## 2. authored/ vs derived/

| | `authored/` | `derived/` |
|---|---|---|
| Written by | humans (PR + review) | prograph and other tools (auto) |
| Editable by hand | yes | **no** (will be overwritten) |
| Examples | rules, decisions (ADR), templates, notes, registry | graph, contract snapshots, project facts, journal, digests |
| Git-review | required | committed by the tool, review optional |

**For tools:** prograph writes **only** to `derived/`. Writing to `authored/` from automation is
forbidden (the directory boundary is hard). A second automated writer is allowed under `derived/`:
the `kb-save` skill owns `derived/journal/` (append-only, not regenerable — ADR 2026-07-06).
A third writer is the fleet agent (`devtools/fleet_report.py`): it owns `derived/fleet/` —
dated fleet-state reports (append-only, not regenerable, delivered by PR only, never direct
commits — `authored/decisions/2026-07-10-adr-fleet-agent-role.md`, proposed).
A fourth writer is the dispatcher publisher (`dispatcher publish-snapshot`): it owns
`derived/snapshots/` — per-host workspace sync snapshots (`<host>.json`, github-checker
snapshot contract v1), each overwritten in place (regenerable: latest state per host, no
history), committed directly by the scheduled tool — dispatcher Gate 1 Design DESIGN-203,
2026-07-14. Since 2026-08-26 (inbox #98) the publisher delivers to the unprotected
`derived-snapshots` **branch**, never to `master`: `derived/snapshots/` is a regenerable
read-model, not authority, so its machine writer gets no bypass of the `master` rulesets.
Consequently a local `master` checkout deliberately does **not** contain the live machine
read-model — readers fetch the branch explicitly
(`git show origin/derived-snapshots:derived/snapshots/<host>.json` or a dedicated service
worktree, never by switching the main KB checkout) and degrade to `unknown`/`stale` when
the branch is absent. Consumer-side adaptation is tracked in dispatcher#199.

## 3. Directory map (what goes where)

```
authored/
  rules/        cross-cutting: code-style.md, gui.md, tui.md, libraries.md
  decisions/    ADRs (cross-repo), YYYY-MM-DD-<kebab>.md
  templates/    spec templates, steward profiles (lite/team), scaffolds
  skills/       project-specific skills: sources/docs OR pointers to Cowork skills
  notes/        plans, intentions, cross-cutting TODOs
  registry/     COWORK_CONTEXT (registry + integration map)
  roadmaps/     machine-readable governance intent (*.yaml; computed status, never manual ticks)
  contracts/    AUTHORITY for cross-cutting contracts owned by no repo (<name>/v<N>/); see §4
derived/
  graph/        prograph output (structure, deps, MCP calls)
  contracts/    contract SNAPSHOTS for search (not authority)
  projects/     auto-facts per repo (prograph)
  journal/      <project>/journal.md — per-project activity log (kb-save; append-only)
  fleet/        dated fleet-state reports (fleet agent via PR; append-only)
  snapshots/    <host>.json — per-host sync snapshots (dispatcher publisher; overwritten;
                live copy on the derived-snapshots branch, not master — see §2)
  digests/      claude-kb/digests (auto)
```

## 4. SSOT boundaries (against duplication)

| Knowledge | Owner (SSOT) | KB role |
|---|---|---|
| Inter-repo contract (has a producing repo) | producing repo | `derived/contracts/` — snapshot/index, NOT authority |
| Cross-cutting contract (**no** producing repo) | **KB `authored/contracts/`** | owns; consumers vendor a pinned copy inward |
| Governance roadmap (intent) | **KB `authored/roadmaps/`** | owns; status is computed from evidence, never ticked by hand |
| Repo-local rules | the repo's CLAUDE.md | none; the repo references `authored/rules/` |
| Cross-cutting rules | **KB `authored/rules/`** | owns |
| Code history | the repo's git | none; `authored/decisions/` = cross-repo *why* |
| Project registry | **KB `authored/registry/`** | owns; the root is a pointer |
| Runtime skills | the Cowork skills mechanism | `authored/skills/` — sources/pointers |
| Project activity log | **KB `derived/journal/`** (kb-save) | owns; append-only, not authoritative |
| Structure/drift | prograph (auto) | `derived/graph/` |
| Transient drafts | `_cowork_output/` | canon graduated here |

Mnemonic rule: **if a specific repo owns it — the KB only references it. The KB owns only what
belongs to no repo.**

## 5. Naming

- Dated: `YYYY-MM-DD-<kebab>.md` (ADRs, notes, statuses).
- Stable thematic: `<kebab>.md` (rules, templates).
- ADR: `authored/decisions/YYYY-MM-DD-adr-<slug>.md`.

## 6. Lifecycle

- **ADR/doc states:** `Proposed → Accepted → Superseded | Archived`. Superseded/Archived — a link to
  the replacement + reason.
- **Archival:** obsolete → `authored/**/archive/` with a YAML mark `archived: YYYY-MM-DD` +
  `reason:`. Do not delete.
- **Graduation:** a draft in `_cowork_output/` → once it becomes canon, it moves into the KB under
  git-review.
- **Freshness:** `registry/` and `derived/` are re-audited on a schedule (curation skill, Stage 2).

## 7. Document frontmatter (minimum)

```yaml
---
title: <short>
type: rule | adr | template | note | contract | contract-snapshot | registry | roadmap
status: proposed | accepted | superseded | archived | living   # for authored
owner: <who maintains it>     # for authored
source: <derived tool>        # for derived
updated: YYYY-MM-DD
---
```

## 8. How to add

- **A rule (cross-cutting):** `authored/rules/<topic>.md`, `type: rule`, PR + review. If the rule is
  repo-local — it goes into the repo's CLAUDE.md, not here.
- **An ADR:** `authored/decisions/YYYY-MM-DD-adr-<slug>.md`, `status: proposed`.
- **A template/profile:** `authored/templates/`. Steward profiles `lite`/`team` go here (SSOT of
  profiles).
- **A contract:** if a repo produces it, authority stays there and the KB only carries a snapshot in
  `derived/contracts/` (by a tool). If the contract spans the ecosystem and **no repo owns it**
  (e.g. plan-fields), the KB is the authority: `authored/contracts/<name>/v<N>/`, `type: contract`,
  PR + review; consumers vendor a pinned copy inward and never read this directory at run time
  ([[2026-07-27-adr-eco-005-plan-fields-two-plane-model]], D11).

## 9. Tools and agents

- **Search:** Obsidian-MCP over the vault (the KB is Obsidian-compatible); from sibling projects, the
  filesystem-based `kb-search`/`kb-load` skills.
- **Populating `derived/`:** prograph (structure/facts/contracts/digests); `kb-save` (journal only).
- **kb-* skills:** sources in `authored/skills/` (`kb-load`, `kb-save`, `kb-search`, `kb-session`,
  `kb-utils/kb-env.sh`); `install-skills.sh` distributes them into ecosystem sub-projects
  (`targets.txt`). `kb-curator` stays KB-side.
- **Curation (Stage 2):** an archival/freshness/link-fix skill (the `consolidate-memory` pattern).
- **Enforcement (Stage 3):** rules in `authored/rules/` → CI checks (à la `gate-check`); drift →
  prograph → dispatcher → auto-PR.

## 10. Relationships

- **steward** — consumer of `authored/templates/` (gate profiles) and `authored/rules/`.
- **prograph** — writer of `derived/`.
- **dispatcher** — reader for status dashboards.
- **COWORK_CONTEXT** — moves into `authored/registry/`; a pointer remains at the root.

## Repo scope & boundaries

- **Этот репо:** `prograph-vault` — git-корень `all_ai_orchestrators/prograph-vault/`, remote `git@github.com:andrei-shtanakov/prograph-vault.git`.
- **Соседи (READ-ONLY reference):** все остальные подпроекты воркспейса — их код не
  редактировать. Состав флота — `ai-orchestrators-workspace/workspace-manifest.toml`
  (SSOT); рукописные списки соседей в CLAUDE.md не ведём — они дрейфуют.
- **Канон имени репо = имя каталога после обычного `git clone`** (`maestro`, `libretto`).
- Нужна правка у соседа → **стоп**: запиши handoff в `authored/notes/`
  (кросс-проектное) или `../_cowork_output/` (черновик), не трогай его файлы.
- Кросс-репные контракты — **вендорить пиненой копией внутрь**, не ссылаться наружу.
- Полное правило (SSOT): `authored/rules/repo-boundaries.md`.

## Git workflow (у репо есть remote)

- Ветка `<type>/<slug>` → push → `gh pr create`. **Прямые коммиты в `master`
  запрещены**, как и локальный мерж ветки в `master` в обход PR.
- После открытия PR — прочитать ревью **GitHub Copilot**: валидные замечания исправлять
  новыми коммитами в ту же ветку; невалидные — ответить с обоснованием, **не применять
  вслепую**; итерировать, пока не останется открытых замечаний. Ревью не всегда
  запрашивается само — если его нет, запросить явно:
  `gh api -X POST repos/<owner>/<repo>/pulls/<n>/requested_reviewers -f 'reviewers[]=copilot-pull-request-reviewer[bot]'`.
- **Не мержить.** Мерж делает пользователь.
- После мержа пользователем: `git switch master && git pull --ff-only`, затем удалить
  влитую ветку в **обеих половинах**: локально `git branch -d <ветка>` (после squash-мержа
  `-d` откажется — сверить, что `git diff master <ветка>` пуст, и удалить
  `git branch -D <ветка>`) и на origin
  `git push origin --delete <ветка>`, если GitHub не удалил сам; затем `git fetch --prune`.
- Никогда не делать force-push в общие ветки; не трогать другие репо (см. scope выше).
- Полное правило (SSOT): `authored/rules/git-workflow.md`.

## Входящие запросы (inbox)

В начале работы проверь входящие: `gh issue list --label inbox --state open`.
Issue с лейблом `inbox` — запрос от соседнего репо, ещё **не** пункт плана.
Принять = завести пункт в `TODO.md` с указанным `slug:`; принял под другим
именем — поправь `slug:` в теле issue.
Отказать = `gh issue close --reason "not planned"`.
Нужна работа в соседнем репо — не редактируй его: заведи там issue
(`slug:` + `from:` + проза). Правило: ADR-ECO-006 — канон в `ecosystem-kb`
(каталог `prograph-vault/` в корне воркспейса),
`authored/decisions/2026-07-28-adr-eco-006-cross-repo-issue-inbox.md`.

Исходящее ожидание — вторая половина того же ритуала: «ждём соседа» существует
**только** как чекбокс `TODO.md` с `@blocked_by:todo://<repo>/<id>` (переходно —
`<repo>#<номер>`); память сессий, заметки и handoff-доки — лишь зеркало. Находка
PF-BLOCKER-STALE по этому репо = «ожидание доставлено — действуй или переставь тег».
Правило (SSOT): `authored/rules/cross-repo-waits.md`.

## `../_cowork_output/` — dev-only

Координационный dev-scratch воркспейса; у пользователей и клонов проекта его НЕТ.
Shipped/runtime-код никогда не читает и не резолвит пути под ним; кросс-репные
контракты вендорятся пиненой копией внутрь, не ссылкой наружу. Ссылаться на него
могут только dev-тулинг самого воркспейса и документация. Канонические факты живут
в репо-владельце (пример: SSOT agents-catalog — `atp-platform/method/agents-catalog.toml`,
ADR-ECO-003). Полное правило (SSOT): `authored/rules/cowork-output.md`.
