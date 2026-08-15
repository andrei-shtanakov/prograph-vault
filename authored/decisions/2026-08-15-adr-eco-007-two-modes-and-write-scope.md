---
title: "ADR-ECO-007: Two operating modes and write_scope — repository authority is declared by the run, not by the filesystem"
type: adr
status: proposed
owner: Andrei
updated: 2026-08-15
---

# ADR-ECO-007: Two modes and `write_scope`

**Status:** Proposed (2026-08-15, Andrei) · **Deciders:** Andrei (sole owner of the
ecosystem today)

**Scope:** what the agent fleet is allowed to change, and under which of two operating
modes; the shared vocabulary every checkpoint decision is expressed in; who merges in
each mode. **Not in scope:** the commit / PR / issue granularity table (a separate rule
in `authored/rules/`, split off deliberately — see *Non-goals*), the triage engine, the
`AgentJob` contract, Dependabot risk policy, and the product-delivery lifecycle stages.
Each of those is its own change.

**Related:** [[2026-07-18-adr-eco-004-governance-plane]] (D7 defines `agent_merge` and
its invariants I1–I4; its *Deferred* list is what gates D3 below),
[[2026-07-28-adr-eco-006-cross-repo-issue-inbox]] (D5 — the sanctioned cross-repo
request channel that D2 here generalises),
[[2026-07-27-adr-eco-005-plan-fields-two-plane-model]] (canonical repo identity),
[[repo-boundaries]], `authored/rules/git-workflow.md`, `impresario/docs/semantics.md`
(the FSM D4 aligns with), `steward/TODO.md:235` (the open `agent_merge` item).

---

## Root cause (thesis first)

Both governing rules draw their fence by **topology** — where a directory sits on this
disk — and neither names the thing that actually decides the question: **which
repository is the current run authorised to change.**

- `repo-boundaries.md:14` — «Правь только тот репо, в котором запущен (его git-корень).
  Все соседние репо под `all_ai_orchestrators/` — READ-ONLY reference.» The fence is
  directory adjacency.
- `git-workflow.md:37-52` — the exception list enumerates repos **by name**
  (`spec-runner-tasks`, the root repo, `sdd-framework`, folders without `.git`).

Topology has already failed twice, and both failures are recorded rather than
hypothetical:

1. **It lost an active repository.** `kapelle` is a live product repo with its own
   remote, checked out at `~/labs/kapelle` — *outside* the workspace directory.
   `COWORK_CONTEXT.md:106` states it plainly: «Лежит вне этой папки… поэтому и выпадал
   из реестра». A rule keyed on "under `all_ai_orchestrators/`" has nothing to say about
   it in either direction: it neither protects it nor authorises work in it.

2. **The same fleet, pointed at a product, reads its own rule as a prohibition.** When
   agents are launched to build an application, that application's repository is neither
   "the repo the agent runs in" in the ecosystem sense, nor a sibling to be left alone —
   it is the *target of the work*. Read literally, the rule forbids the task the run
   exists to perform. This is the conflation this ADR is written to end.

```
today                                    the missing predicate
─────                                    ─────────────────────
"is it under all_ai_orchestrators/?"     "is it in this run's write_scope?"
   ├─ yes, and it's cwd  → write            ├─ yes → write
   ├─ yes, sibling       → read-only        └─ no  → read-only, request via inbox issue
   └─ no  (kapelle, …)   → undefined
```

The gap is not strictness. It is that **authority is a property of the run, while the
rules encode the filesystem.**

---

## Decision

### D1 — Two operating modes, declared per run

| | **product-delivery** | **ecosystem-development** |
|---|---|---|
| What is the product | an external application or a research result | the agent system itself and its subprojects |
| Where change is authorised | the target product/research repo(s) | the repo that owns the capability being changed |
| What an **issue** means | scope change, defect, follow-up, return to an earlier stage | a request to a neighbouring repo's owner; or a backlog item not yet ready to implement |
| What a **PR** means | an artifact or increment of a stage of the delivery plan | the implementation of an accepted change inside the current repo |
| Who merges | the agent (see D3) | a human (unchanged) |

The mode is **declared by the run**, never inferred from the working directory. An
undeclared run is `ecosystem-development`: that is the only mode in operation today, and
silent promotion into product-delivery authority must be impossible.

Note what this table does *not* do: it does not create two git mechanisms. There is one
GitHub mechanism — branch, PR, review, evidence, merge — and two policy profiles over
it. Anything that would have to be built twice is a sign the split is drawn wrong.

### D2 — `write_scope` replaces topological fencing

> An agent may modify only the repositories explicitly listed in the current workflow's
> `write_scope`. Every other repository is read-only; a request to change one is
> delivered as an `inbox` issue in the owning repo.

ADR-ECO-006 D5 already established that filing an issue in another repo is not a breach
of boundaries but the *sanctioned* form of "stop, do not edit, record a handoff". D2
generalises it: the channel is the same whether the other repo is an ecosystem sibling,
a repo outside the workspace directory, or a product repo owned by someone else.

**`repo-boundaries` becomes a derivation rather than an axiom.** In
`ecosystem-development` mode, `write_scope` = { the repo being developed } — which is
byte-identical in effect to today's rule. Nothing about current sessions changes.

**An undeclared `write_scope` resolves to { the git root of the run's cwd }** — today's
de-facto behaviour. This is chosen over failing closed so the decision can land without
a flag day; see OQ-3.

**Naming.** A repo in `workspace-manifest.toml` is named by its canonical manifest key
(the identity rule of ADR-ECO-005, restated in ADR-ECO-006 D7). A repo outside the
manifest — `kapelle`, any customer repo — is named by its remote `owner/name`. A
`write_scope` entry is **never a filesystem path**: a path is precisely the topological
coupling this ADR removes.

### D3 — Merge authority is a mode parameter; the base layer is evidence, not identity

The base layer holds in **both** modes and is not negotiable per profile:

- no direct commits to the default branch; every change arrives by PR;
- GitHub Copilot review is collected and each finding is resolved — fixed, or answered
  with a reason; never applied blindly;
- merge happens only through the receipted path with typed evidence, never a raw push;
- no force-push to shared branches;
- fail-closed when GitHub data is incomplete rather than treating unknown as green.

What varies by mode is the **subject** of the merge, not its conditions:

- `ecosystem-development` — a human merges. Unchanged from `git-workflow.md:26`.
- `product-delivery` — **the agent merges**, with a human checkpoint available as an
  enableable policy rather than the default.

**This records a target, not a switch that is now on.** ADR-ECO-004 D7 already decided
the shape of agent merging: it is a category shift, it requires a distinct `agent_merge`
evidence class, and it is admissible only when invariants I1–I4 hold. That work is still
in D7's *Deferred* list, and the open item is `steward/TODO.md:235` — *«Evidence
`agent_merge` с инвариантами I1–I4»*, `@blocked_by:prograph-vault#adr-eco-004-deferred`.
Until it lands, `product-delivery` runs on D7's stated default: **PR-authority, not
merge authority.**

**A tension this ADR must not paper over.** I1 grants merge authority only within
enumerated change-classes where green CI is *genuinely sufficient* — D7's examples are
dependency bumps, doc-only edits, regenerated files. The dominant change class of
product-delivery is feature code authored from a spec, which is exactly the class D7
argues CI does not settle. So agent merge in product-delivery **does not follow from
I1–I4 alone**; it needs an additional sufficiency argument. Candidate, recorded as OQ-2
rather than decided here: sufficiency shifts from *green CI* to *green CI plus
demonstrated conformance to an approved upper-level spec*.

### D4 — One decision vocabulary for every checkpoint

Every human or policy checkpoint — in either mode, at any stage — emits exactly one of:

| Decision | Meaning | Changes direction | Needs authority | Recorded as | Origin |
|---|---|---|---|---|---|
| `approve` | proceed as proposed | no | yes | gate decision | impresario |
| `hold` | stop, direction unchanged | no | yes | gate decision | impresario |
| `resume` | leave hold and continue at a named stage | no | yes | gate decision + `return_to` | impresario |
| `recycle` | return to a named earlier stage with required changes | **yes** | yes | gate decision + `return_to` | impresario |
| `kill` | terminate this initiative | **yes** | yes | gate decision | impresario |
| `amend` | change an already-approved scope or artifact | **yes** | yes | new version of the artifact | new |
| `supersede` | replace an approved artifact with a successor, keeping the original readable | **yes** | yes | successor + back-reference | new |
| `waiver` | proceed despite a known, named violation | no | yes, higher | audit record with reason and expiry | new |

**Five of the eight are impresario's existing outcomes, adopted under its own names.**
`impresario/docs/semantics.md:109` already defines `recycle` / `hold` / `kill` /
`resume` as *outcomes of decisions, not statuses*, with `recycle` and `resume` carrying
`return_to` — exactly the shape needed here. This vocabulary therefore **extends that
set rather than forking it**, and the naming follows: `kill`, not `reject`, because a
governance vocabulary that renames an existing outcome creates precisely the second,
parallel state ontology it exists to prevent. The three new entries name transitions
impresario has no reason to model, since they concern approved artifacts downstream of
its gates.

Why eight rather than "pause / continue": a single pause conflates *wait* with *go
back*, and a system that cannot tell them apart cannot count recycles — and the recycle
rate per stage is the one number that reveals whether an upstream stage is broken.
`waiver` is separated from `approve` for the same reason: a violation that is knowingly
accepted must remain countable.

### D5 — Enforcement is a ladder, and this ADR is layer 1

`repo-boundaries.md:24` is already honest about this and the honesty is preserved: rule
text lowers risk, it does not enforce. The levers, in increasing strength:

1. the run's working directory;
2. the declared `write_scope`, carried in the run record and readable after the fact;
3. a CI gate-check that fails a PR touching paths outside the declared scope;
4. `.claude/settings.local.json` deny rules for writes outside the scope.

`write_scope` enters ADR-ECO-004 D3's typed maturity ladder at `declared`. It must not
claim `ci-blocking` before the check in (3) exists — a rule asserting an enforcement
level it does not have is the specific defect that ladder was introduced to make
visible.

### D6 — Ownership

| Artifact | Semantic owner | Physical home |
|---|---|---|
| This decision; the D4 vocabulary | governance | `prograph-vault/authored/decisions/` |
| commit / PR / issue granularity table | governance | `prograph-vault/authored/rules/` (separate change) |
| Machine-readable policy profiles | **open — see OQ-1** | open |
| `write_scope` of a run | the orchestrator that launched the run | the run record |
| Merge evidence semantics (`human_merge` / `agent_merge`) | steward | steward contracts |
| GitHub write-path | github-checker | existing verbs, see *Non-goals* |
| Surfacing state and launching sanctioned actions | dispatcher | ADR-ECO-004 D1 |

---

## Non-goals

- **The commit / PR / issue granularity table.** Split off deliberately: an ADR is a
  dated decision with a rationale and should stay stable, whereas granularity guidance
  will be revised as experience accumulates. It becomes a rule in `authored/rules/`,
  changeable without re-deciding this ADR.
- **Re-implementing the GitHub path.** `github-checker` already ships `snapshot`,
  `pull`, `open-pr`, `propose-pr`, `pr-detail`, `merge` (nine gate predicates, re-read
  from live state at merge time), `post-merge-sync`, `issue-lookup`, `issue-create`.
  Anything built on this ADR sits *above* those verbs.
- **Another fleet scanner.** `devtools` already has `make morning`, `inbox.py` and
  `fleet_report.py`; `github-checker snapshot` already collects PRs, issues, Dependabot
  and Copilot status. What is missing is classification and a durable decision record,
  not another collector.
- **The product-delivery lifecycle stages** (discovery → business analysis → behaviour
  spec → architecture → decomposition → task specs → implementation → deploy →
  observation). Its own ADR, and it is largely a routing map over existing owners
  (`discovery`/`discovery-toolkit`, `impresario`, `spec-runner`, `maestro`,
  `github-checker`, `dispatcher`, `deployer`) rather than a new system.
- **No change** to ADR-ECO-005 plan semantics or ADR-ECO-006 inbox semantics.

## Open questions

- **OQ-1 — where machine-readable policy profiles live.** The two profiles must
  eventually exist as data, not prose. `steward` is the leading candidate — it already
  owns `gate-catalog` and `roles-catalog`, and consumers already receive pinned vendored
  copies. Not decided here because it determines a contract surface that deserves its
  own review.
- **OQ-2 — what makes agent merge safe for spec-authored feature code**, the class I1
  excludes (see D3). Must be answered before product-delivery merge authority is
  enabled, not after.
- **OQ-3 — whether an undeclared run should eventually fail closed** rather than
  defaulting to the cwd repo. Defaulting is chosen now to avoid a flag day; revisit once
  `write_scope` is actually carried by the orchestrators.

## Consequences

- `repo-boundaries.md` and `git-workflow.md` get amended to **derive** from D1/D2 rather
  than assert topology. Two separate PRs, not this one.
- `git-workflow.md`'s per-repo exception list survives intact: those exceptions are facts
  about *remotes* (no remote; backup mirror; external upstream), not about topology.
- **Surfaced, not fixed:** `impresario` is absent from the project registry in
  `COWORK_CONTEXT.md` although it owns the `Idea → RankedBacklog → ProductProposal →
  human gates → approved` path — half of the product-delivery contour. Verified by grep
  on 2026-08-15. Reconciling the registry is its own change.
- **Cost of this ADR alone: zero code and zero behaviour change.** It renames the
  predicate and fixes the vocabulary; every mechanism it mentions already exists or is
  already tracked as an open item elsewhere.

## Verification — planned, not executed

The status is *Proposed* precisely because nothing has been run. Three falsifiable
claims, in the order they should be tested:

1. **Derivation is faithful.** A `write_scope` declared for an ecosystem-development run
   must produce behaviour byte-identical to today's `repo-boundaries` — if it does not,
   D2 is a change of policy disguised as a refactor.
2. **Topology-independence is real.** A product-delivery run against `kapelle` — a repo
   outside the workspace directory — must be expressible in `write_scope`. Today's rule
   cannot express it at all, which is the failure that motivated this ADR.
3. **The vocabulary does not fork.** D4's five adopted decisions must round-trip through
   impresario's existing FSM without introducing a new *status* there, and the three new
   ones must be expressible without one. A required new status means the vocabulary was
   designed against the wrong model.
