---
title: "ADR-ECO-006: Cross-repo requests are GitHub issues in the target repo (inbox), never plan items"
type: adr
status: accepted
owner: Andrei
updated: 2026-07-29
---

# ADR-ECO-006: Cross-repo issue inbox

> **CANON.** Accepted 2026-07-29 after the Stage 1 pilot executed end to end on live
> data (see *Verification*). The review draft lived in `_cowork_output/`; this copy
> supersedes it. `_cowork_output/` is one machine's dev scratch and does not travel with
> a clone — cite this path, not that one.

**Status:** Accepted (2026-07-29, Andrei) · **Proposed:** 2026-07-28
**Deciders:** Andrei (sole owner of the ecosystem today)
**Scope:** how a repo asks a *neighbouring* repo for work — the delivery channel, its
identity, who may accept, and how the request meets the existing plan graph. **Not** a
new plan format and **not** a change to plan semantics: ADR-ECO-005 stands untouched.
**Related:** [[2026-07-27-adr-eco-005-plan-fields-two-plane-model]] (this decision adds
the state *before* its operational plane; see §D6 for the split from its D8),
[[repo-boundaries]], `authored/rules/git-workflow.md`,
`devtools/check-plan-fields.py` (the `@blocked_by` graph this plugs into),
`devtools/Makefile` (`make morning`), `github-checker/github_checker/models.py`
(`Issue.labels`, already parsed),
`prograph-vault/authored/skills/install-skills.sh` (the existing skill distributor),
`ai-orchestrators-workspace/workspace-manifest.toml` (SSOT of fleet composition).

**Fleet scope is always derived, never a literal count.** Every "all repos" statement
below means *the unique `git_dir` values in `workspace-manifest.toml`* — 15 as of
2026-07-28 (`arbiter, atp-platform, deployer, devtools, dispatcher, github-checker,
libretto, maestro, proctor, prograph, prograph-vault, research-bench, robin-runtime,
spec-runner, steward`). Tooling must read the manifest; a hardcoded number is a bug.

---

## Root cause (thesis first)

A cross-repo dependency is already expressible — but **only from the waiting side**.
`arbiter/TODO.md:48` and `:60` both carry `@blocked_by:atp-platform#benchmark-2`, and
`atp-platform/TODO.md` has no such item. `devtools/check-plan-fields.py` reports this as
a *dangling blocker*, which is precisely correct and precisely useless: it tells the
**waiter** that nobody planned their work. It cannot tell the **target**, because
nothing was ever delivered there.

So today's outbound channel is a handoff note in `prograph-vault/authored/notes/` or a
draft in `_cowork_output/`. Both live **outside the receiving repo**. An agent working
inside `maestro/` — scope-fenced to `maestro/` by [[repo-boundaries]] — never opens
them. The note is written, and the request is never seen.

```
today:                            missing:
arbiter/TODO.md                   atp-platform
  @blocked_by:atp#benchmark-2  ──X──>  (never notified)
        │
        └─> vault note  ──────────X──>  (never read from inside the repo)
```

The gap is not expressiveness. It is that a **pull-claim has no push counterpart**. The
mechanism to carry it already exists and is completely unused: **0 open issues across all
15 manifest repos**, enumerated and verified via `gh issue list` on 2026-07-28 — while
`github-checker` already fetches `repos/{r}/issues?state=open` and its `Issue` model
already carries `labels`.

The fix is one channel — a labelled GitHub issue in the target repo — with a single
structural line that lets it meet the plan graph, and **no new plan semantics whatsoever**.

---

## Decision

### D1 — An `inbox` issue is a request, not a plan item

An open issue labelled `inbox` in repo R is a **cross-repo request addressed to R that
is not yet part of anyone's plan**. It is the state *before* ADR-ECO-005's operational
plane, not a third plane.

The two plan ontologies are unchanged: operational (`repo/TODO.md`, owner-declared) and
governance (`authored/roadmaps/*.yaml`, engine-computed). An `inbox` issue is neither. It
carries no status of its own beyond open/closed and **is never an input to status
computation**.

Triggers (the three cases this channel exists for):
1. tagging a neighbouring repo for work it must do,
2. a proposal — including a proposal merely to *investigate* something,
3. a fault surfaced while interacting with that repo.

### D2 — Acceptance is derived, not stored

There is no "accepted" field, label, or state anywhere. Acceptance is the intersection of
two facts that already exist:

| Issue | Slug in target `TODO.md` | Meaning |
|---|---|---|
| open | absent | **not accepted** — awaiting an owner decision |
| open | present | accepted, in progress |
| closed, reason `completed` | (was present) | done |
| closed, reason `not planned` | never appeared | declined |

Decline uses GitHub's native close reason — `gh issue close --reason "not planned"`, whose
only values are `completed | not planned`. It is **not** a `wontfix` label: a second label
would contradict D3 and put lifecycle state in two places.

Note this reason is **for human readers only**. No tool in this decision reads closed
issues: `github-checker` fetches `state=open`, and `make inbox` filters `--state open`.
Consequently `github_checker.models.Issue` needs **no new field** for it.

Nothing is synchronised, so nothing can drift. This is the same discipline as
ADR-ECO-005's D6: the joint view is a **derived projection**, never a store.

### D3 — Body contract: `slug:` + `from:`, everything else prose

```
slug: benchmark-2
from: arbiter#crossover-gate

Нужен прогон второго task_type тремя агентами — без второй точки
crossover-гейт в arbiter остаётся непроверяемым.
Готово, когда в benchmark_runs есть rank_score для второго suite_id.
```

- **`slug:` (required)** — the proposed name of the item in the *target's* `TODO.md`.
- **`from:` (required)** — the sending repo; `#slug` optional (a fault report may have no
  originating plan item).
- **Prose** — what is needed and by what observable condition it is done.

The mechanism defines **exactly one** label, `inbox` — it is the sole label any tool here
reads or writes. Repos remain free to add their own labels; those carry no meaning for
this contract. In particular, **no label encodes lifecycle state** (see D2: acceptance is
derived, decline is a close reason).

The trigger kind (tag / proposal / fault) is **not** machine-encoded: it is legible from
the prose, and a separate taxonomy would be a third field ontology of exactly the kind
ADR-ECO-005 exists to collapse.

Why this and not free prose: without `slug:`, the request and the plan item it becomes
are linked only in someone's head, the dangling-blocker warning stays mute, and the
sensor cannot distinguish *delivered* from *read* — reproducing the exact defect of
handoff notes.

### D4 — `slug:` requests a name; it does not assign one

The sender proposes the slug. The **owner of the target repo** decides: accept as
proposed, accept under a different slug, or decline (close, reason `not planned`).

**Renaming protocol (load-bearing).** `slug:` in the issue body is the *only* join between
the issue and the plan graph (D2). Accepting under a different name therefore requires the
target owner to **edit `slug:` in the issue body** to the name they actually used — the
issue lives in their repo, so this is their edit to make — after which the sender amends
their own `@blocked_by`. Without this step the derived acceptance check would compare a
stale slug against the new item and report **not accepted forever**.

This is the D2-of-ADR-ECO-005 trust rule applied to delivery: an owner-declared *inbound*
item that auto-materialised in a neighbour's plan would let any repo write into another
repo's plan — the same trust inversion that forbids upward evidence edges.

### D5 — Filing an issue in a neighbouring repo does not breach repo boundaries

[[repo-boundaries]] forbids **editing a neighbour's files**. An issue edits nothing. This
decision makes explicit what that rule already implies: filing an `inbox` issue is the
*sanctioned* form of "stop, do not edit, record a handoff" — merely addressed to the repo
that must act, instead of to a shared scratch directory.

The PR-only mandate is untouched: repo **content** still changes only through PRs.

### D6 — `inbox` is disjoint from ADR-ECO-005's D8 diagnostic issues

ADR-ECO-005 D8 also uses GitHub issues. The two must never be conflated:

| | **D8 diagnostics** (ADR-ECO-005) | **`inbox`** (this ADR) |
|---|---|---|
| Author | fleet sensor reconciler (machine) | human / agent |
| Home | `ai-orchestrators-workspace` (umbrella) | the **target** repo |
| Identity | fingerprint `code+subject+related+rule_id` | free; `slug:` in body |
| Lifecycle | auto-open / auto-close / reopen on recurrence | opened and closed by people |
| Semantics | **sensor state** — an observation | **intent** — a request |
| Mutator | reconciler, label-scoped, own authority | ordinary repo participants |

They share no repo, no label, and no authority. D8's reconciler is defined to touch only
issues bearing *its* label and ownership marker, so the disjointness holds by
construction; this table makes it explicit rather than incidental.

### D7 — One versioned skill source, distributed by the existing installer; a rule per repo

The skill's **source of truth** is `prograph-vault/authored/skills/repo-inbox/`, alongside
the `kb-*` skills, and it is distributed by the **already existing**
`prograph-vault/authored/skills/install-skills.sh` — adding `repo-inbox` to its `SKILLS`
array is the whole integration. No new distribution infrastructure is built.

The skill resolves the current repo with `gh repo view --json nameWithOwner`. Two
operations:

- **check** — `gh issue list -R <owner/repo> --label inbox --state open`, then grep each
  `slug:` against the local `TODO.md`, matching **checkbox lines only**; report *not
  accepted* and *accepted, in progress* separately.
- **file** — assemble the D3 body and `gh issue create -R <target> --label inbox`.

**This is a GitHub coordinate, not plan identity — the distinction is load-bearing.**
The plan-fields contract is explicit that a *canonical repo name* is the
workspace-manifest key and that `remote_origin` is diagnostic only, so that a rename or
case change cannot mint a new identity (`authored/contracts/plan-fields/v1/README.md`,
*Identity & provenance*). Nothing in this decision touches that: an `inbox` issue is never
a plan node, produces no `todo://` URI, and contributes no `node_id`. What `gh -R` needs
is the GitHub API's own addressing, which a manifest key cannot express.

The one place the two planes meet is `inbox.py` mapping a repo GitHub just named to a
checkout on this disk. That lookup goes through the shared `plan_fields.fleet.canonical_name`
— the same function `check-plan-fields.py:117` already uses to build its on-disk index
before reconciling against the manifest — so the inbox view follows the package's
established pattern rather than inventing a second one. A rename that desynchronises the
two degrades **visibly**: the issue renders as *«не проверить — репо не склонирован
здесь»* rather than silently reading as not accepted.

What lands **in** each repo is a **rule, not code** — one byte-identical block appended to
its `CLAUDE.md` (the fleet-uniformity rule of 2026-07-19: fleet-wide callers are amended
everywhere at once, never per-repo):

```markdown
## Входящие запросы (inbox)

В начале работы проверь входящие: `gh issue list --label inbox --state open`.
Issue с лейблом `inbox` — запрос от соседнего репо, ещё **не** пункт плана.
Принять = завести пункт в `TODO.md` с указанным `slug:`; принял под другим
именем — поправь `slug:` в теле issue.
Отказать = `gh issue close --reason "not planned"`.
Нужна работа в соседнем репо — не редактируй его: заведи там issue
(`slug:` + `from:` + проза).
```

Rationale. An earlier draft of this ADR placed the skill in `~/.claude/skills/` on the
claim that the fleet has no distribution mechanism. **That claim was false** — the
installer exists and already serves ten targets from `targets.txt`. With the mechanism
real, the vault-sourced option dominates on every axis at identical cost: the source is
versioned and reviewable, re-running `--from-config` makes drift unrepresentable, and the
contract stops being single-user. The record is corrected here rather than silently
rewritten, because the earlier decision rested on the false premise.

Two properties of the installer must be understood, not assumed:

- It **gitignores what it installs** (`ensure_gitignore`) unless `--track` is passed. So
  distributed skills are *not* versioned inside the target repo either; a fresh clone on
  another machine gets the `CLAUDE.md` rule but no skill until the installer is re-run.
  What the installer buys is a **single reviewed source plus a sync command** — not
  travel-with-the-clone. Choosing `--track` for `repo-inbox` is deliberately left open
  until the pilot shows whether in-repo visibility matters.
- Its `targets.txt` lists **ten** repos while the manifest declares fifteen `git_dir`s —
  `deployer`, `research-bench`, `devtools`, `github-checker` receive no skills at all
  today. That gap is **pre-existing and out of scope here**; it is recorded as a
  consequence (below) rather than fixed in passing.

The rule in `CLAUDE.md` degrades gracefully regardless: an agent with no skill installed
reads the rule and runs `gh` by hand.

The block is Russian while this ADR is English: it is quoted verbatim as the artifact, and
the fleet's `CLAUDE.md`/`TODO.md` corpus is Russian-first.

### D8 — Morning ritual stays offline-fast; the fleet report gains a section

`make morning` is today `repos.sh fetch && repos.sh status` — pure git, seconds, offline.
It gains a third step, `make inbox`, implemented as **one** fleet-wide query rather than
14 per-repo walks:

```
gh search issues --owner andrei-shtanakov --label inbox --state open \
  --json repository,number,title,body
```

`body` is **required, not optional**: without it there is no `slug:`, and D2's acceptance
cannot be derived — the ritual would list requests without saying which ones still need a
decision, which is the only thing worth showing in the morning. (`gh search issues`
supports `body` among its `--json` fields; verified 2026-07-28.)

The acceptance check runs **locally**: `make inbox` executes from `devtools/`, which
already operates over the parent workspace and reads sibling `TODO.md` files — exactly
what `check-plan-fields.py` does. For each issue: parse `slug:` from the body, resolve
`repository` to its workspace directory, grep that repo's `TODO.md`.

**Directory resolution must be canonical-name-aware.** GitHub returns the canonical repo
name while the on-disk directory may differ (`maestro` vs the legacy `Maestro/` checkout,
resolvable only on case-insensitive APFS). `check-plan-fields.py` already solves this with
its `by_name` map; `make inbox` reuses that approach rather than assuming
`repository == dirname`.

**Graceful degradation is mandatory**: no `gh`, unauthenticated, or no network → print the
reason and **exit 0**. `make morning` must never fail offline; the daily ritual is the one
thing that must not regress, or it stops being run.

Rejected: folding `github-checker snapshot` into `morning`. It walks every manifest repo over the
network for PRs + issues + alerts and needs `uv` — turning a two-second offline ritual
into a network sweep.

`fleet_report.py` additionally grows an inbox section, filtered on the **already-parsed**
`Issue.labels` field. **Zero changes to `github-checker`.** Note the asymmetry: the
snapshot carries no issue **body**, so the fleet report can only *list* inbox issues, not
compute acceptance. That is the correct division — the report is a fleet-wide artifact
delivered by PR to the vault and cannot depend on one machine's working copies, whereas
`make inbox` legitimately can.

`make inbox` hardcodes `--owner andrei-shtanakov` for the search and does not read the
manifest to enumerate repos; it is a local convenience alias and claims no ownership of
fleet composition (which stays with `ai-orchestrators-workspace` per ADR-ECO-005 D9). The
first repo outside that owner breaks it visibly rather than silently.

Its **directory** resolution walks the workspace for `*/.git` — the same autodiscovery
`repos.sh` uses — rather than the manifest. This is deliberate and the distinction is not
pedantic: the manifest declares which repos *should* exist, but this lookup answers a
different question — "GitHub named a repo; is it checked out here, and what does its
`TODO.md` say?" Resolving through the manifest would make a clone that is present but
unlisted invisible, for no benefit; a manifest repo with no clone here is already reported
as unresolvable. Naming still goes through the shared `canonical_name`, so the lookup is
host-independent where it matters.

### D9 — Ownership

| Artifact | Semantic owner | Physical home |
|---|---|---|
| The `inbox` contract (D1–D6) | steward / governance | `prograph-vault/authored/` |
| `inbox` issue content | the two repos party to it | GitHub issues in the target repo |
| Acceptance decision | **target repo owner** — exclusively | `<repo>/TODO.md` |
| `repo-inbox` skill source | prograph-vault (KB skills) | `prograph-vault/authored/skills/repo-inbox/` |
| Skill distribution | prograph-vault | `install-skills.sh` + `targets.txt` |
| `make inbox`, fleet-report section | devtools | `devtools/` (PR) |
| Per-repo rule block | fleet-wide, byte-identical | each `<repo>/CLAUDE.md` (PR) |

---

## Rollout

> **Stage 1 complete 2026-07-29.** The pilot ran on `arbiter`, `atp-platform` and
> `devtools`; every step below was executed and its result is recorded under
> *Verification*. Stage 3 — the remaining manifest repos — is **not** authorised yet and
> is gated on the reliability follow-ups (`devtools#19`, `prograph-vault#45`) landing.

**Staged: 3 repos first, the remaining 12 only after the mechanism is shown to work.**
The rule block is a PR per repo with Copilot review and human merge — fifteen of those on
an unproven design is the wrong order of spending. Stage 3's repo list is **computed from
the manifest minus the pilot**, never typed out.

**Stage 1 — pilot (`arbiter`, `atp-platform`, `devtools`).** These three are exactly the
verification scenario's participants.

1. `gh label create inbox` on the three repos. (This is also where it emerges whether any
   repo has issues disabled — never checked, since the fleet has 0 issues ever.)
2. prograph-vault PR: `authored/skills/repo-inbox/` (check + file) and `repo-inbox` added
   to the `SKILLS` array in `install-skills.sh`; install into the pilot repos.
3. devtools PR: `make inbox`, `morning: fetch && status && inbox`, README row.
4. `CLAUDE.md` rule block — one PR per pilot repo.

**Stage 2 — verification on live data** (see below). Gate for Stage 3.

**Stage 3 — fleet.** `gh label create inbox` on the remaining manifest repos; the
byte-identical rule block by PR; the `fleet_report.py` inbox section. Whether `repo-inbox`
is also added to `targets.txt` (and whether it ships `--track`) is decided here, informed
by the pilot — not assumed now.

**Deferred, explicitly not in this iteration:**

- **Auto-proposing issues from dangling blockers.** `check-plan-fields.py` could detect a
  `@blocked_by` whose slug exists in neither the target's `TODO.md` nor an open `inbox`
  issue, and print a ready-to-run command. Attractive — it converts a mute warning into
  an action — but it covers **one of the three triggers**, modifies a checker owned
  elsewhere, and raises a spam question best answered by observing real traffic first.
- **`.github/ISSUE_TEMPLATE`** — 14 copies of the format and guaranteed drift; the skill
  writes the body.
- Any change to plan parsers, robin, or dispatcher. This decision requires none.

---

## Verification — executed 2026-07-29, not synthetic

The pilot ran against a **live dangling blocker that had been open for months**, not a
fixture: `arbiter/TODO.md:48` and `:60` both carried
`@blocked_by:atp-platform#benchmark-2` while `atp-platform` tracked no such item.

### Artefacts

| What | Where |
|---|---|
| The request | `atp-platform#279` (label `inbox`) |
| Fleet tooling | `devtools#16`, `#17` (`inbox.py`, `make inbox`, wired into `make morning`) |
| The skill | `prograph-vault#44` (`authored/skills/repo-inbox/`) |
| Acceptance | `atp-platform#280` |
| The waiting side following the accepted name | `arbiter#61` |
| The rule in three `CLAUDE.md` | `arbiter#62`, `atp-platform#281`, `devtools#18` |
| Reliability follow-ups | `devtools#19`, `prograph-vault#45` |

Rule-block identity across the three pilot repos, hashed rather than eyeballed —
`sha1 4b89409ffca8ec2eebb039eb9115fa59b97d3def` in all three.

### Observed results

| Step | Observed |
|---|---|
| Before delivery | `make plan-check` warned on **both** arbiter lines: *"'benchmark-2' not found in atp-platform/TODO.md"* |
| Request filed | `make inbox` → `Входящие (inbox): 1, из них не принято 1` — `atp-platform#279 НЕ ПРИНЯТ, от arbiter#crossover-gate` |
| Morning ritual | `make morning` printed the same section after the status table |
| Skill, inside `atp-platform` | `gh repo view` resolved the repo; the body rendered with `slug:` on its own line; the checkbox-anchored grep reported **НЕ ПРИНЯТ** |
| Accepted under a **different** slug (`second-task-type-sweep`) | shared `plan-fields` scraper saw exactly one open item with that `@id` |
| **Rename trap, before applying D4** | `make inbox` still said **НЕ ПРИНЯТ** although the work was accepted — the issue body still named the old slug |
| D4 applied (issue body edited) | `make inbox` → `не принято 0`, `#279 принят` |
| **Load-bearing** | `make plan-check` warns for **neither** arbiter line |

### Two behaviours the pilot confirmed rather than assumed

**Prose does not count.** `atp-platform/TODO.md` had contained the string `benchmark-2`
in an indented prose paragraph the whole time. Both the shared scraper and the skill's
checkbox-anchored grep refused to treat it as acceptance. D1's "an issue becomes a plan
item only when an *item* carries the slug" is therefore enforced by the tooling, not
merely asserted here.

**The rename trap is real.** Between accepting under a new name and editing the issue
body, the fleet view reported **not accepted** for work that *was* accepted. Without D4's
renaming protocol that state is permanent, exactly as D4 predicted. This is the strongest
evidence that D4 is load-bearing rather than ceremony.

---

## Consequences & non-goals

- **Non-goal:** a third plan plane. An `inbox` issue is never a plan item (D1).
- **Non-goal:** replacing `TODO.md`, or moving cross-repo work out of it.
- **Non-goal:** abolishing handoff notes. A vault note remains the home of **why** —
  narrative, decision, session context. An issue is an addressed **what**. They cross-link.
  What changes: a cross-repo *task* recorded **only** as a note now counts as undelivered.
- **Cost:** a label per manifest repo; one `CLAUDE.md` PR per repo (staged); a devtools PR;
  a prograph-vault PR.
- **Known limitation — slug matching is a substring test.** Acceptance asks whether the
  slug occurs in the raw text of a checkbox item, so "the slug is present" is weaker than
  it reads: `benchmark-2` also matches an item mentioning `benchmark-20`. What counts as
  an *item* is not in question — that comes from the shared `plan-fields` package
  (`scrape_items`), which ADR-ECO-005 PF-7 made the single implementation; only the
  match **within** an item is loose. **Not fixed here** — tightening it is the package's
  call under ADR-ECO-005 D9, and a private stricter rule in `inbox.py` or `repo-inbox`
  would recreate the divergence that ADR removes. Recorded so acceptance is not mistaken
  for a proof.
- **Known boundary — a fresh clone has no skill.** `install-skills.sh` gitignores what it
  installs unless `--track`, so on another machine only the `CLAUDE.md` rule is present
  until the installer is re-run (the agent then runs `gh` by hand).
- **Known boundary — hardcoded owner** in `make inbox`'s search (D8).
- **Pre-existing gap, surfaced not fixed:** `targets.txt` covers ten repos against the
  manifest's fifteen — `deployer`, `research-bench`, `devtools`, `github-checker` receive
  no distributed skills at all. Reconciling the installer's target list with the manifest
  is its own change, owned by prograph-vault.
- **Open question:** whether an `inbox` issue that is accepted should be auto-closed on
  item closure, or closed by hand. Deferred deliberately — decide after observing whether
  stale accepted issues actually accumulate.
