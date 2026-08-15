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
modes; the minimal lifecycle protocol every checkpoint must satisfy — not a fleet-wide
decision enum, which stays with each gate's owner; who merges in each mode. **Not in scope:** the commit / PR / issue granularity table (a separate rule
in `authored/rules/`, split off deliberately — see *Non-goals*), the triage engine, the
`AgentJob` contract, Dependabot risk policy, and the product-delivery lifecycle stages.
Each of those is its own change.

**Related:** [[2026-07-18-adr-eco-004-governance-plane]] (D7 defines `agent_merge` and
its invariants I1–I4; its *Deferred* list is what gates D3 below),
[[2026-07-28-adr-eco-006-cross-repo-issue-inbox]] (D5 — the sanctioned cross-repo
request channel that D2 here generalises),
[[2026-07-27-adr-eco-005-plan-fields-two-plane-model]] (canonical repo identity),
[[repo-boundaries]], `authored/rules/git-workflow.md`,
`impresario/contracts/gate-decision/v1/schema.json` and `impresario/docs/semantics.md`
(the decision enum and record model D4 defers to), `steward/TODO.md:235` (the open
`agent_merge` item).

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

There is **one observed failure and one structural contradiction** — the distinction
matters, because only the first is evidence:

1. **Observed: topology lost an active repository.** `kapelle` is a live product repo
   with its own remote, checked out at `~/labs/kapelle` — *outside* the workspace
   directory. `COWORK_CONTEXT.md:106` states it plainly: «Лежит вне этой папки… поэтому
   и выпадал из реестра». A rule keyed on "under `all_ai_orchestrators/`" has nothing to
   say about it in either direction: it neither protects it nor authorises work in it.

2. **Structural: the same fleet, pointed at a product, reads its own rule as a
   prohibition.** When agents are launched to build an application, that application's
   repository is neither "the repo the agent runs in" in the ecosystem sense, nor a
   sibling to be left alone — it is the *target of the work*. Read literally, the rule
   forbids the task the run exists to perform. No run has yet failed this way, because
   product-delivery has not been operated under a declared mode; the contradiction is in
   the rules as written, not yet in a recorded incident.

```
today                                    the missing predicate
─────                                    ─────────────────────
"is it under all_ai_orchestrators/?"     "is it in this run's write_scope?"
   ├─ yes, and it's cwd  → write            ├─ yes → write
   ├─ yes, sibling       → read-only        └─ no  → read-only, request via the
   └─ no  (kapelle, …)   → undefined                 channel declared for it
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
| Who merges **today** | a human — agent merge is **not** enabled (D3) | a human |
| Who merges **as target** | the agent, within explicitly enabled change classes, once D3's gate opens | a human (unchanged) |

The mode is **declared by the run**, never inferred from the working directory. An
undeclared run is `ecosystem-development`: that is the only mode in operation today, and
silent promotion into product-delivery authority must be impossible.

Note what this table does *not* do: it does not create two git mechanisms. There is one
GitHub mechanism — branch, PR, review, evidence, merge — and two policy profiles over
it. Anything that would have to be built twice is a sign the split is drawn wrong.

### D2 — `write_scope` replaces topological fencing

> An agent may modify only the repositories explicitly listed in the current workflow's
> `write_scope`. Every other repository is read-only; a request to change one is
> delivered to its owner through the channel declared for that target.

ADR-ECO-006 D5 already established that filing an issue in another repo is not a breach
of boundaries but the *sanctioned* form of "stop, do not edit, record a handoff". What
D2 generalises is the **predicate** (read-only unless in scope), **not the transport**:

- **target is an ecosystem repo** → the ADR-ECO-006 `inbox` channel, unchanged: the
  `inbox` label, the `slug:`/`from:` body contract, acceptance derived against the
  target's `TODO.md`.
- **target is external** (a customer repo, or any repo outside the fleet) → a **handoff
  adapter declared by the workflow**. A GitHub issue is the preferred default where the
  target supports it, but nothing here assumes it: an external repo may have no `inbox`
  label, no distributed skill or `CLAUDE.md` rule, no `TODO.md` to derive acceptance
  from, and may not grant issue-creation rights at all.

Stating this as one channel would have quietly extended ADR-ECO-006's fleet-scoped
contract to repos where none of its machinery exists — and would have contradicted this
ADR's own non-goal of leaving inbox semantics untouched. Extending ADR-ECO-006 beyond
the fleet, if it is ever wanted, is its own decision.

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

### D4 — A minimal lifecycle protocol over three orthogonal axes; gate owners keep their own enums

**This ADR does not define a decision enum.** Checkpoint outcomes are already owned, and
the owner's enum is richer than a governance-level list would be:
`impresario/contracts/gate-decision/v1/schema.json:33` enumerates nine —
`approve, recycle, hold, kill, resume, select, defer, park, reject` — where `select` and
`defer` serve backlog ranking (`qg4_backlog`) and have no meaning at a delivery gate.
Declaring a single fleet-wide enum would either drop those or force every gate to carry
outcomes that are meaningless for it.

What this ADR fixes instead is that three different things were being conflated into one
list. They are orthogonal and have different carriers:

| Axis | What it expresses | Carrier | Owner |
|---|---|---|---|
| **decision** | the typed outcome of a checkpoint | that gate's own enum | the gate's owner |
| **artifact transition** | what happens to an already-approved artifact | `amend` (new version, same identity) · `supersede` (successor record + back-reference) | the artifact's contract |
| **exception evidence** | proceeding despite a known, named violation | a waiver record with reason, authority and expiry | governance |

The last two are **not** alternatives to `approve` / `hold` / `recycle`; they can
accompany a decision or occur without one. Both already have carriers in impresario:
`GateDecision.supersedes` is an append-only supersession relation between immutable
records (`docs/semantics.md:123` — «Исправление/перекрытие — только **новой** записью со
ссылкой `supersedes`… старая запись не правится»), and `human_waiver` already closes
blocking assumptions in a ConceptDraft (`:140`). Treating either as a ninth decision
value would have contradicted the record model they belong to.

**The minimal lifecycle protocol** — the only thing this ADR requires of a gate — is that
its enum can express all four of these classes, and that each outcome maps to exactly one:

| Class | Meaning | impresario's instances |
|---|---|---|
| `proceed` | continue on the current path | `approve`, `select` |
| `hold` | stop without changing direction; a paired outcome resumes | `hold` → `resume`, `park`, `defer` |
| `return` | go back to a named earlier stage with required changes | `recycle` (+ `return_to`, `required_changes[]`) |
| `terminate` | end this initiative | `kill`, `reject` |

A gate that cannot express `return` is the failure this protocol exists to catch: without
it, "wait" and "go back" collapse into one state, and the recycle rate per stage — the one
number revealing that an upstream stage is broken — becomes uncountable.

**Correction to an earlier draft of this ADR.** A prior revision listed eight values as a
single enum and justified preferring `kill` over `reject` on the claim that `reject`
would rename an existing outcome. That claim was false: the schema carries `kill` **and**
`reject` as distinct values. The record is corrected here rather than quietly rewritten,
because the earlier text rested on a fact that does not hold.

### D5 — Enforcement is a ladder, and this ADR is layer 1

`repo-boundaries.md:24` is already honest about this and the honesty is preserved: rule
text lowers risk, it does not enforce.

**The decisive constraint is that repo CI cannot enforce a cross-repo scope.** A PR in
one GitHub repository contains only that repository's changes; its CI has no way to
observe that the same run also wrote to a sibling. ADR-ECO-004's Batch-1 boundary gate is
correspondingly scoped — *«PR touches only its own repo»* (line 181), a path check
**inside one checkout**. Cross-repo `write_scope` is therefore enforced by the control
plane and by correlating the run's GitHub side effects, never by a repo's own CI:

| # | Lever | Enforces | Exists today |
|---|---|---|---|
| 1 | rule prose | nothing; it informs | yes |
| 2 | `write_scope` declared in the run record | auditability after the fact | no |
| 3 | runtime write/tool sandbox (e.g. `.claude/settings.local.json` deny) | writes on this machine | partially |
| 4 | credential / repository allowlist for the run's token | which repos are reachable at all | no |
| 5 | reconciler: PRs and commits attributable to the run ⊆ `write_scope` | the cross-repo predicate itself | no |
| 6 | per-repo CI: protected paths, evidence receipt | the within-repo half | yes (ADR-ECO-004 Batch 1) |

Layers 3–5 belong to the executor and control plane; layer 6 is the only one a repository
can enforce about itself. `write_scope` enters ADR-ECO-004 D3's typed maturity ladder at
`declared`, and must not claim `ci-blocking` — no CI check for it exists, and for the
cross-repo half none can. A rule asserting an enforcement level it does not have is the
specific defect that ladder was introduced to make visible.

### D6 — Ownership

| Artifact | Semantic owner | Physical home |
|---|---|---|
| This decision; the D4 lifecycle protocol | governance | `prograph-vault/authored/decisions/` |
| Checkpoint decision enums | **the owner of each gate** (impresario for its gates) | that repo's contracts |
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
  excludes (see D3). Sufficiency evidence is only one of four parts the answer must
  cover; I3 is explicit that an automated verifier buys provenance and revocability, not
  a second independent judgment, so an evidence rule alone cannot carry the argument. The
  answer must also fix **the admissible change classes**, **the blast radius** of a wrong
  merge in each, and **the revocation loop** that watches agent merges (I4). Must be
  answered before product-delivery merge authority is enabled, not after.
- **OQ-3 — whether an undeclared run should eventually fail closed** rather than
  defaulting to the cwd repo. Defaulting is chosen now to avoid a flag day; revisit once
  `write_scope` is actually carried by the orchestrators.
- **OQ-4 — how a `write_scope` entry resolves to a verified checkout.** D2 deliberately
  stores logical identity rather than a path, which leaves a resolver to be specified,
  and it must fail closed rather than guess. Undefined today: a repo with no remote;
  several checkouts or worktrees of the same repo on one machine; a remote renamed since
  the scope was declared; an `origin` that does not match the declared `owner/name`. Each
  of these must resolve to a refusal with a stated reason, never to a silent pick.

## Consequences

- `repo-boundaries.md` and `git-workflow.md` get amended to **derive** from D1/D2 rather
  than assert topology. Two separate PRs, not this one.
- `git-workflow.md`'s per-repo exception list survives intact: those exceptions are facts
  about *remotes* (no remote; backup mirror; external upstream), not about topology.
- **Surfaced, not fixed:** `impresario` is absent from the project registry in
  `COWORK_CONTEXT.md` although it owns the `Idea → RankedBacklog → ProductProposal →
  human gates → approved` path — half of the product-delivery contour. Verified by grep
  on 2026-08-15. Reconciling the registry is its own change.
- **Cost of this ADR alone: zero implementation and zero runtime behaviour change.**
  Every mechanism it mentions already exists or is already tracked as an open item
  elsewhere. **Governance behaviour does change**, and that is the point: once accepted,
  `repo-boundaries` and `git-workflow` are to be read through D1/D2 — the fence is the
  declared `write_scope`, and their topological wording is a legacy expression of it
  until the amending PRs land.

## Verification — planned, not executed

The status is *Proposed* precisely because nothing has been run. Three falsifiable
claims, in the order they should be tested:

1. **Derivation is faithful.** A `write_scope` declared for an ecosystem-development run
   must produce behaviour byte-identical to today's `repo-boundaries` — if it does not,
   D2 is a change of policy disguised as a refactor.
2. **Topology-independence is real.** A product-delivery run against `kapelle` — a repo
   outside the workspace directory — must be expressible in `write_scope`. Today's rule
   cannot express it at all, which is the failure that motivated this ADR.
3. **No second enum is created.** Every one of impresario's nine outcomes must map to
   exactly one of D4's four protocol classes, and impresario must need no new decision
   value, status, or record type to satisfy the protocol. If it does, the protocol was
   designed against the wrong model — and the same test applies to the next gate owner
   that adopts it.
