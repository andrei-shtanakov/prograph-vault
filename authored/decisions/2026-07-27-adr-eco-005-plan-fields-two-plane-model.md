---
title: "ADR-ECO-005: Plan-fields — two plan planes, one graph, evidence flows governance→operational"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-27
---

# ADR-ECO-005: Plan-fields two-plane model

**Status:** Proposed (2026-07-27, Andrei) · **Date:** 2026-07-27
**Deciders:** Andrei (sole owner of the ecosystem today)
**Scope:** how per-repo operational plans (`TODO.md`) and the governance roadmap
(`authored/roadmaps/*.yaml`) relate — identity, evidence direction, the derived graph
over both, and the drift sensor. **Not** a new plan *format* for owners; it decides the
contract, ownership, and enforcement plane around the operational tag format already in
use (inline `@owner` / `@blocked_by` / `@trigger` tags in the checkbox tail, parsed by
robin-runtime #27).
**Related:** [[2026-07-18-adr-eco-004-governance-plane]] (this is the plan-layer
instance of that plane), [[repo-boundaries]], `authored/rules/git-workflow.md`,
the umbrella `workspace-manifest.toml`, `dispatcher/dispatcher/core/roadmap.py`
(evidence engine), `atp-platform/scripts/ci/check_plan_citations.py` and
`devtools/check-plan-fields.py` (current parsers to be unified).

---

## Root cause (thesis first)

The plan machinery does **not** lack a format. It has *four* parsers over plan data —
`atp-platform/scripts/ci/check_plan_citations.py` (481 loc),
`devtools/check-plan-fields.py` (383), `robin-runtime/src/robin/plan_state.py` (338),
and `dispatcher/dispatcher/core/roadmap.py` (616). The first three read `TODO.md`
checkboxes; the fourth deliberately does **not** — its docstring is explicit
(*"Status is never a manual checkbox: it is derived"*), it loads typed YAML from
vault roots with a closed evidence-rule vocabulary
(`project_detected | file_exists | sqlite_has_row | contract_in_sync | work_item_chain`).

So the visible symptom (a continuation-line divergence where the ATP checker showed
46/46 while the fleet saw 7/46, fixed in atp-platform PR #275) is one instance of a
deeper fact: **there are two plan planes with different status semantics, and no single
graph that keeps them distinct while relating them.** Collapsing them into one
"true status" would destroy information; leaving them as four hand-rolled parsers keeps
reproducing the drift.

```
operational plane            governance plane
repo/TODO.md                 authored/roadmaps/*.yaml
owner-declared open/closed   engine-computed planned/implemented/verified/blocked
      \                            /
       \                          /
        canonical plan graph  (pure derived projection, provenance preserved)
                    |
          dispatcher control plane (history, divergence, remediation → github-checker PR)
```

The fix is not "one plan format." It is **one contract + one operational parser + one
derived graph over two typed sources**, with evidence flowing only governance→operational
and status never manually ticked into the governance plane.

---

## Decision

### D1 — Two plan ontologies, never collapsed to one status

- **Operational item** — source `repo/TODO.md`; status *declared* by the owner
  (`open`/`closed`/`unknown`); a checkbox is an owner **assertion**, not an independently
  proven fact; granularity = near-term work.
- **Roadmap item** — source `authored/roadmaps/*.yaml`; status *computed* by the
  Dispatcher engine from typed evidence (`planned/implemented/verified/blocked/unknown`);
  manual ticks are forbidden by construction; granularity = capability / milestone / contract.
  Note `drift` is a further *derived roadmap projection* (contract-sync, `build_drift` /
  `_apply_drift` in `roadmap.py`), computed **after** evidence and dependency processing — not
  a value of the status enum but a separate lens the graph must be able to carry.

`TODO [x] ≠ roadmap verified`. A closed implementation task is at most *one evidence input*
to a roadmap capability. The canonical graph stores both node kinds with provenance and
does **not** compute a shared "true status."

### D2 — Evidence direction is governance → operational (the bridge is a rule, not a tag)

The authoritative link that makes an operational item count toward a capability lives
**governance-side**, as a new entry in the closed `evidence_rules` vocabulary — mirroring
how `file_exists`/`work_item_chain` already point *down* at operational artifacts. It is
**not** a `@implements` tag inside `TODO.md`: an owner-declared upward edge would let a repo
self-promote a capability, exactly the trust inversion the governance plane exists to avoid.

`@implements`/`@verifies` as TODO tags are, at most, non-authoritative human hints —
**deferred, not part of v1**, and never inputs to status computation.

### D3 — `plan_item_declared_closed` evidence rule; attestation is loud and visible in the projection

Add one rule kind to the governance closed set:

```yaml
evidence_rules:
  - rule: plan_item_declared_closed   # attestation-grade, deliberately named
    kind: implementation
    ref: todo://atp-platform/benchmark-2
```

- The status engine is **unchanged** (`if all(implementation_rules): implemented`), so this
  rule *can* promote a roadmap item to `implemented` — the ADR records that a governance
  author consciously accepts owner attestation as sufficient *implementation* evidence
  (the same known weakness as `file_exists`: presence ≠ quality).
- Attestation is a **property of the rule in the registry, not of its name.** The evidence
  vocabulary carries a grade:

  ```yaml
  plan_item_declared_closed:
    evidence_grade: attestation      # vs. machine
  ```

- To keep promotion honest **without** extending the status enum, the derived projection MUST
  carry an additive flag, defined over registry metadata (never a hard-coded name list, so a
  second attestation rule needs no projection-code change):

  ```
  implementation_is_attested_only =
        computed_status in {implemented, verified}
    AND implementation evidence is non-empty
    AND every implementation rule has evidence_grade = attestation
  ```

  A mixed machine+attestation set → `false`. `verified` layered over an attested
  implementation → stays `true`, so the UI never loses that provenance. Such items render as
  **`implemented (attested)`** / **`verified (attested impl)`**, distinct from machine-checked.
  This is the "declared done / unverified" cell of D10 — Variant-B honesty in the projection,
  Variant-A simplicity in the engine.
- The rule is still named `plan_item_declared_closed`, never `plan_item_closed`, so its
  attestation nature is legible at the call site too.

**Hard UI/API invariant.** A consumer MUST NOT render or report `implemented (attested)` as a
plain machine-backed `implemented`, even though the base `computed_status` is identical. The
`implementation_is_attested_only` flag travels with the item across every surface (dispatcher
UI, `/api/roadmap`, KB snapshot, Robin). Rationale: `plan_item_declared_closed` **is** a
verified fact — the owner publicly closed the item — sufficient to promote to `implemented`,
but **not** a claim the result is machine-verified; erasing the flag downstream re-collapses
exactly the distinction D1 draws. Adding machine evidence later is purely additive — the
projection then stops being attested-only on its own, with no enum or engine change.

### D4 — Namespaced identity; minimal operational contract v1

Identity is uniform in *form*, namespaced by *kind*:

```
todo://<repo>/<item-id>
roadmap://<roadmap>/<item-id>
```

Operational `@id` invariants: unique within a repo; stable across title renames; never
reused. **v1 load-bearing operational fields only:** `@id`, `@owner`, `@blocked_by`,
`@trigger`, freshness metadata (`@source-ref`/`@observed-at`/`@recheck-by`), and
scanner-computed provenance. **No** `implements/verifies/tracks/supersedes` — the governance
plane already owns cross-item dependencies (`depends_on`) and evidence, so the operational
edge set is only `@blocked_by` (operational↔operational, intra-plane).

Back-compat and safe migration: `@id` is the **only** source of a `todo://<repo>/<id>` URI — a
canonical URI is **never synthesized from title text or a legacy slug** (a substring slug is
not a stable identifier; synthesizing one manufactures false identity). The legacy
`@blocked_by:<repo>#<slug>` form stays valid transitionally and resolves as: locate the
concrete target item; if it carries an `@id`, emit a canonical edge; if it has no `@id` or the
match is ambiguous, keep the raw `legacy_blocker_ref` and emit a warning — do not invent a URI.
`@id` MUST sit on the **first line** of the checkbox item (the line Robin and the fleet parser
read); it is a new tail tag → excluded from robin's identity key (robin-runtime #27), so adding
it does not churn snapshots.

### D5 — Tombstones: a closed item with inbound edges is not deleted

An `@id` referenced by a governance rule or a cross-repo `@blocked_by` must survive closure.
Form:

```markdown
- [x] Completed item @id:benchmark-2
```

The checkbox `[x]` already **is** the declared status, so there is **no `@status` tag** — it
stays out of v1 (D4); a `[ ] … @status:done` pair would be a second, contradictory status
source. `@id` is never reused; a vanished referenced `@id` is a first-scan warning, an error once
confirmed on a second independent snapshot (D7). Git-history lookup is used **only** to
diagnose "this ID was deleted," never as a normal runtime resolver — otherwise the tombstone
rule becomes optional. This lifts dispatcher's existing "do not delete a closed line" note to
an ecosystem invariant.

### D6 — Canonical plan graph is a pure derived projection, never a store

The graph is a pure function of its recorded inputs. It MAY be persisted for history, but
every snapshot is immutable, never edited, never assigned an independent status; a new scan
writes a new snapshot rather than fixing a previous one. It is **fully reproducible only for
git-sourced evidence**; evidence that reads mutable runtime state (`sqlite_has_row`,
`work_item_chain`, runtime snapshots) is **traceable, not reproducible** unless the snapshot
also captures those inputs. Snapshot identity therefore records more than git SHAs:

```json
{
  "manifest_ref": "...",
  "sources": { "atp-platform": "sha", "dispatcher": "sha", "prograph-vault": "sha" },
  "collector_version": "...", "parser_version": "...",
  "runtime_state": { "<db-or-snapshot-id>": "hash-or-immutable-id" },
  "effective_config": "...",
  "generated_at": "...",
  "nodes": [], "edges": [], "diagnostics": []
}
```

Until the runtime-state inputs are actually captured, the ADR's word is **traceable**, not
reproducible.

### D7 — Snapshot consistency: freeze refs, escalate on the second snapshot

Because reading live HEADs sequentially yields a multi-commit cut, cross-repo checks are
not blanket-warnings (that would mean a stale blocker never blocks). Instead:

1. At scan start, resolve and **pin** every input's SHA; check out and read only the pinned
   refs/worktrees — never live HEAD mid-scan.
2. First cross-repo/cross-plane divergence → warning.
3. Same divergence on the next **independent** snapshot → error (or issue overdue).
4. Divergence gone on a later scan → auto-resolve.

An **independent snapshot** = a new `scan_id` at a new observation time, re-detecting the same
divergence after **≥1 completed fleet-scan** in between; a plain rerun over identical inputs is
**not** independent. Escalation to error (step 3) therefore requires the `first_seen`
persistence introduced in Phase 0b (D8) — before that the sensor is **warnings-only** (see
Sequencing). A single race does not break CI; durable drift becomes blocking. Intra-repo
diagnostics may be hard errors immediately.

### D8 — Diagnostic lifecycle via GitHub issues in the umbrella repo

Phase-0b persistence is **GitHub issue state** (not a dispatcher DB — so the lifecycle does
not depend on the control-plane phase). Fingerprint =
`diagnostic_code + subject_uri + related_uri + rule_id` (`rule_id` included so two rules of
the same type between the same nodes do not collapse into one issue). Reconciler: first sight →
open issue; recurrence → update `last_seen`; disappearance → auto-close resolved; reappearance
→ reopen, no duplicate. Suppression lives in issue labels/body (or a source annotation) and
REQUIRES a ref + expiry; expired suppression → error. Issues live in
**ai-orchestrators-workspace** (the fleet snapshot's owner), not in any single producer repo.

**Mutation authority (reconciles with D9).** Issues are *sensor state*, not a change to any
owner repo, so the reconciler is its **own** narrowly-scoped authorized mutator of the umbrella
workflow — it touches **only** issues carrying its label and a hidden ownership marker, nothing
else. It is **not** routed through github-checker, whose PR-only mandate covers *repo content*.
This keeps github-checker's invariant intact instead of widening it.

### D9 — Ownership split; vocabulary changes are governance-gated

| Artifact | Semantic owner | Physical home |
|---|---|---|
| Ontologies, identity, evidence vocabulary | steward / governance | `prograph-vault/authored/` |
| Operational parser / CLI (`plan-fields`) | plan-fields package owner | first `dispatcher/packages/plan-fields` |
| Roadmap evidence execution | Dispatcher | `dispatcher/core/roadmap.py` |
| TODO content | owner repo | `<repo>/TODO.md` |
| Fleet composition | workspace owner | `ai-orchestrators-workspace` |
| Repo-content mutations | github-checker | PR-only |
| Diagnostic-issue lifecycle | umbrella fleet workflow (own authorized mutator, label-scoped) | GitHub issues in umbrella repo |

`plan-fields` is an offline package: own version/changelog/fixtures, an offline CLI, **no
dispatcher import**, release cadence independent of the web app. First consumer is
`roadmap.py` (dogfoods the boundary). A **new evidence-rule kind goes through a governance
ADR/handoff first**; Dispatcher does not extend the vocabulary unilaterally. Extraction to a
standalone repo becomes mechanical once ≥3 external CI consumers pin it (a threshold already
effectively met: ATP, devtools, robin) — deferred cost, not speculative.

### D10 — The divergence view is the payoff

Dispatcher renders declared-vs-computed pairs; collapsing to one status would erase them:

| Operational claim | Governance evidence | Result |
|---|---|---|
| TODO `[x]` | no evidence | declared done / unverified |
| TODO `[ ]` | capability verified | stale operational plan |
| blocker closed | dependent item open | stale blocker |
| roadmap `planned` | active TODO items exist | implementation active |
| roadmap `implemented` | no verification evidence | awaiting verification |

### D11 — Machine-readable companion contract, vendored to consumers

This ADR fixes semantics; the *physical* canon of the plan-fields schema and the evidence
vocabulary (rule kinds + `evidence_grade`) is a **companion artifact** in
`prograph-vault/authored/` (e.g. `authored/contracts/plan-fields/v1/` — `schema.json` +
`fixtures/`), PR-gated like all authored canon, in the ADR-ECO-004 authored-vs-derived pattern.
Delivery chain:

```
vault-authored contract  →  generated/reviewed versioned package schema + fixtures
                         →  pinned dependency / vendored copy  →  offline consumers
```

**No parser or runtime reads a neighbor `prograph-vault/` or `_cowork_output/` at run time.**
Consumers vendor a pinned copy inward (the repo-boundaries vendoring rule). This is
load-bearing for pre-commit in autonomous clones, which have neither directory on disk.

---

## Sequencing

1. **Phase 0a — nightly fleet sensor.** A new umbrella workflow (not a wrapper of today's
   script): read the workspace manifest → **freeze every input's SHA before analysis** →
   check out each repo at its frozen SHA → run the checker over the frozen roots → emit an
   artifact (JSON via a new `--format json` if ready, else raw stdout in the first cut).
   **Warnings-only** — no escalation yet (no persistence). NB: today's
   `devtools/check-plan-fields.py` discovers siblings via `iterdir()` + `origin` parsing and
   has neither manifest-pinning, SHA-freezing, nor JSON, so 0a is genuinely new functionality,
   not a wrapper. The workflow canonically belongs to `ai-orchestrators-workspace` (owns fleet
   composition); living in devtools short-term does not make devtools the contract owner.
2. **Phase 0b — diagnostic fingerprints + GitHub-issue lifecycle** (D8): adds `first_seen`
   persistence; only now does D7 second-snapshot escalation turn on.
3. **This ADR** landed in vault (D1–D11): two ontologies, namespaced IDs, tombstones, evidence
   direction, `plan_item_declared_closed`, snapshot consistency, companion contract.
4. Add `@id` to the operational contract (D4).
5. Extract the offline `plan-fields` package (D9 / D11).
6. Implement the governance rule in Dispatcher (D3), governance-gated.
7. Wire `roadmap.py` as the first consumer.
8. Migrate ATP, devtools, and Robin onto the package.
9. After stabilization, decide standalone-repo extraction.

Sensor first; then the two ontologies and the shared graph; then the single parser.
Dispatcher aggregates observations without erasing declared-vs-proven.

---

## Consequences & non-goals

- **Non-goal:** a single central `TODO.md`. Ownership stays per-repo; the graph is derived.
- **Non-goal:** one "true status" across planes.
- **Non-goal:** owner-declared upward evidence edges; owners cannot self-promote roadmap status.
- **Cost:** `plan-fields` needs its own CI/versioning; devtools needs CI it lacks today
  (only `CODEOWNERS` under `.github/`); a new evidence-rule kind is a governance change.
- **Open questions** (re-snapshotted 2026-07-27 against the live fleet — **coverage is no
  longer one of them**: all 11 core repos now carry a `TODO.md`, incl. deployer 27 / steward
  29 / dispatcher 11 / discovery 11 / robin 7 open items). Remaining owner calls: `@owner`
  handle grammar (one human + a set of agents — already partly ratified in ATP's canonical
  form); who owns the ATP/Maestro bulk `@id`+owner markup (the real labor); and, for low-work
  KB-like repos, thin `TODO.md` vs a `@source-ref`+TTL index.
