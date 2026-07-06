---
title: "ADR-ECO-003a: Model lifecycle — discovery → benchmark-gated adoption"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-02
---

# ADR-ECO-003a: Model lifecycle — discovery → benchmark-gated adoption

**Status:** Proposed (2026-07-02, Andrei) · **Date:** 2026-07-02
**Deciders:** Andrei (owner Maestro / arbiter / ATP)
**Scope:** ecosystem-wide (ATP + Maestro + arbiter + devtools)
**Type:** Amendment to `decisions/2026-07-01-adr-eco-003-agent-catalog.md` (ADR-ECO-003)
**Related:** ADR-ECO-002 (`2026-06-20-adr-harness-model-management.md`, D3),
`contracts/add-new-agent-runbook.md`,
`contracts/2026-06-19-agent-id-convention-atp-confirm.md`
**Amended by:** ADR-ECO-003b (distribution), 003c (breadth + cost classes),
**003d (cloud-`$` pricing mechanics; P2 token-fix — pre-req)**

> This amendment refines **Flow 1** ("the vendor updated a model / a new player appeared")
> from ADR-ECO-003 with a concrete lifecycle and answers two owner questions
> (2026-07-02): (1) can we auto-update `agent_id` by version, like pinning a dependency;
> (2) how to introduce a new model so it starts not from scratch, but is compared against
> its predecessor. It also records the blocking pre-req — a token-accounting bug in the
> claude_code shim.

---

## TL;DR

1. **`agent_id` is an identity, not a dependency version.** `claude-sonnet-4-6` is not `python>=3.12`; it is a hash in a lockfile: the join key between ATP benchmarks and arbiter routing. An auto-bump `sonnet-4-6 → sonnet-5` zeros out the `benchmark_runs` under the old key → "silent None → re-rank no-op" (exactly the class from R-07). **Automatic `agent_id` bump is rejected.**
2. **We separate two lifecycles: discovery (automatic) and adoption (gated).** We automate discovery of new models as a notifier that opens a PR **only against Plane 1** of the catalog. Promotion into routing (Plane 2) is manual + benchmark-gated.
3. **A new model starts not "from scratch" but anchored — but we anchor the test SUITE, not the score.** `sonnet-5` is run on the same golden `suite_id` as `sonnet-4-6`. Two fresh `rank_score` values are then comparable → a fair A/B. Inheriting the predecessor's `rank_score` as a prior is **forbidden** (that is once again an assumption of similarity).
4. **Two artifacts in two places:** identity (`agents-catalog.toml`) lives in git and changes via PR; measured performance (`rank_score`) lives in arbiter's runtime store (`benchmark_runs`) and is not committed to git. Merging a routable-PR is **gated on the existence of a benchmark**.
5. **Discovery owner is devtools (PM-tooling), NOT arbiter and NOT Maestro.** Discovery feeds the SSOT that all three repos vendor; it must not be baked into a runtime consumer. ATP owns the benchmark gate, arbiter owns routable-promotion.
6. **Pre-req (P2, blocks re-sweep):** `atp-platform/method/spawners/claude_code_shim.py:57-58` computes `total_tokens` without the cache classes. Fix before the re-sweep, so the re-sweep inherits correct numbers. **✅ Closed 2026-07-02** (atp-platform #213; re-sweep confirmed 1336 → ~575k).

---

## Context

### Trigger (2026-07-02)

The owner noticed that the Claude Code interactive picker now shows **Sonnet 5**
(probably `claude-sonnet-5`), whereas the catalog and the sweep are pinned to
`claude-sonnet-4-6`. This raised the question of an automatic "versioned" model update
and of a mechanism for regularly checking for current models.

### What is already true (read off the code 2026-07-02)

- **The label and the model actually launched on the harness path are guaranteed to match.**
  `agent_id = f"{harness}@{model}"` and `CLAUDE_MODEL` are projected from the same catalog
  field `model` (`atp-platform/method/run_pipe_check.py:122-130`); the shim pins the model
  explicitly with the flag `claude --model $MODEL` (`claude_code_shim.py:24,36`). Changing
  the Claude Code interactive default **does not affect** the re-sweep as long as the catalog
  holds `claude-sonnet-4-6`.
- **"Sonnet 5 in the menu" ≠ "sonnet-4-6 removed."** This is a UX default of the picker; via
  `--model` / the API the specific version is usually still available. We must not retire
  `4-6` just because it disappeared from the menu — check availability first.
- **The SSOT catalog is actually consistent across repos:** `atp-platform/method/agents-catalog.toml`
  and `arbiter/config/agents-catalog.toml` are currently byte-for-byte identical.

### What hurts

- **A divergence can arise only outside the harness:** a manual run of the shim with a stray
  `CLAUDE_MODEL` in the environment would split the label (set by the catalog/suite) from the
  model. Inside the harness there is none of this — but it is a loophole for manual runs.
- **A hole in the SSOT:** `atp-platform/atp/core/settings.py:250` hardcodes
  `claude-sonnet-4-20250514` (the evaluator's model) — **a different model, a different naming
  convention (dated API id vs short alias), and outside the catalog.** The "single point" is
  incomplete.
- **Hardcoded strings in tests:** `tests/unit/method_spawners/test_run_pipe_check.py:28` and
  Maestro's tests fix model strings as literals → a `retired` in the catalog would break CI in
  the wrong place.
- **A blocking token-accounting bug** (see the "Pre-req" section).

---

## Decision

### D1. `agent_id` does not auto-bump. The single point of change is Plane 1 of the catalog.

A model as **identity** (the routing/bench join key) changes only by declaring a new
`[models."…"]` record in the SSOT catalog. The local configs of the three repos remain
`# GENERATED`. Manually editing `arbiter/config/agents.toml`, `Maestro/.../spawners/*.py:24`,
`atp-platform/method/run_pipe_check.py` is an anti-pattern (the model string lives in ≥6 places).

We distinguish by the nature of the use:

| Use | Example (`file:line`) | Nature | Auto-bump? |
|---|---|---|---|
| `agent_id` for routing/benches | `arbiter/config/agents.toml:5`, `arbiter/models/agent_policy_tree.json:5` | **Identity** (ATP↔arbiter join) | ❌ Never |
| default evaluator/LLM-judge model | `atp-platform/atp/core/settings.py:250` | Preference ("the current sane, cheap one") | ✅ Drift OK (not a join key) |
| spawner `DEFAULT_CLAUDE_MODEL` | `Maestro/maestro/spawners/claude_code.py:21`; shim default `envelopes.py:16` (`claude-opus-4-8`) | Fallback if none passed explicitly | ⚠️ Only via codegen from the catalog |

### D2. Two lifecycles: discovery (auto) vs adoption (gated)

```
[discovery: auto, weekly]             [adoption: manual + benchmark-gated]
provider model list / claude --model
        │
        ▼
  diff against catalog
        │  new model?
        ▼
  PR only against Plane 1 ──► review ──► merge (model "active", NOT routable)
  ([models."claude-sonnet-5"],                      │
   alias normalization)                             ▼
                                        pipe-check on golden-suite
                                        (same suite_id as 4-6)
                                                    │
                                                    ▼
                                        rank_score into benchmark_runs
                                                    │
                                                    ▼
                                        A/B view: 4-6 vs 5 on suite T
                                                    │  human gate
                                                    ▼
                                        separate PR: flip into routable (Plane 2)
```

Why C, and not auto-bump: the ecosystem's value is in **empirical** routing (`rank_score`
from real runs). Auto-bump substitutes an assumption for what was measured, which contradicts R-07.

### D3. We anchor the test SUITE, not the score

- ✅ The new model is run on the **pinned golden `suite_id`** on which its predecessor was
  measured → two comparable `rank_score` values → a fair A/B and a meaningful delta.
- ❌ Inheriting the predecessor's `rank_score`/prior is **forbidden** — that is an assumption
  of similarity (auto-bump through the back door again).
- "Comparison" is not a new store but a **view/query over `benchmark_runs`**, where both
  `agent_id` values are present on the same `suite_id`. We fix not a table but the **guarantee
  that both models passed the same suite**. Related to golden-runs (`CLAUDE.md` §6.1).

### D4. git/PR vs runtime — what lives where

| Artifact | Where | How it changes |
|---|---|---|
| Identity (`[models."…"]`, `status`, `aliases`, `agent_id` declaration) | git → `agents-catalog.toml` (SSOT) | PR from the discovery bot, manual approval |
| Measured performance (`rank_score`, delta vs predecessor) | arbiter runtime store (`benchmark_runs`) | written by pipe-check; **not committed to git** |

**Gate:** the "make routable" PR (Plane 2) does not merge until pipe-check has emitted a
`rank_score` for the new `agent_id` on the golden-suite. This combines the human-gate and the
data-gate.

### D5. Ownership by project (answer to "who is responsible for discovery")

| Responsibility | Owner | Rationale |
|---|---|---|
| **Discovery** (reconciling providers ↔ catalog, auto-PR against Plane 1) | **devtools/** (`_cowork_output/devtools/`, PM-tooling) | Discovery feeds the SSOT that **all three repos vendor**. It must not be baked into a runtime consumer (arbiter) — that would tie routing to polling external providers. It lives next to `gen_agents_toml.py`. |
| **Model lifecycle owner** (`status` active/deprecated/retired, PR approval) | **PM / Andrei** | A cross-cutting fact (already so in ADR-ECO-003). |
| **Benchmark gate** (pipe-check, golden-suite, emission of `rank_score`) | **atp-platform** | ATP is the authority on measurement; the canonical copy of the catalog and `run_pipe_check.py` live here too. |
| **Routable-promotion** (Plane 2 flip, re-rank weight, A/B on a tie) | **arbiter** | Policy and routing are arbiter's zone; promotion = a deliberate gate. |
| **Consumer defaults** (spawner, evaluator model) | **Maestro / ATP** | Via codegen from the catalog; the evaluator model — to be derived under the catalog (see actions). |

> Note on SSOT placement — **RESOLVED 2026-07-03 (owner ruling): canon =
> `atp-platform/method/agents-catalog.toml`.** The decisive argument is the distribution
> boundary: `_cowork_output` is a dev-only communication workspace; users and teams that
> install the projects **do not have** it; putting the canon there would make a dev folder a
> prod dependency. (An intermediate resolution the same day in favor of contracts/ — was
> overturned by the owner on exactly this ground.) Roles: the ATP repo = canon
> (distributable, PR/review/CI); `arbiter/config/` = a vendored copy;
> `_cowork_output/contracts/` = a dev mirror for cross-team communication, kept in
> byte-sync by conformance. `devtools/discover_models.py` and
> `check-agent-id-conformance.py` point at the canon in atp-platform.

---

## Pre-req (P2, blocks re-sweep): token accounting in the claude_code shim

> **Status 2026-07-03: ✅ closed** — atp-platform #213 (the shim sums all 4 classes;
> cache fields were added to the protocol model `Metrics` as well, otherwise `extra="ignore"`
> would drop them at the adapter boundary). The 2026-07-02 re-sweep confirmed it on a live run.
> For the cost axis (003d) it matters that: the classes reach the **shim metrics** but NOT
> `benchmark_runs` — the `report_benchmark-v1` contract carries only `total_tokens`;
> per-class usage in the rows requires `report_benchmark-v2` (see 003d, "Contingency").

`atp-platform/method/spawners/claude_code_shim.py:57-58` sums only
`input_tokens + output_tokens`. But `claude -p --output-format json` actively uses
prompt caching and returns two more classes that the shim ignores:
`cache_creation_input_tokens`, `cache_read_input_tokens`. In Claude Code the bulk of the
input is `cache_read` (system prompt + tool-defs + context), while `input_tokens` is only
the uncached delta. Hence `total_tokens=1336` alongside a correct `cost_usd`
(`:77` takes `total_cost_usd`, where the price is computed across all classes).

**Confirmation by contrast:** the anthropic_api shim counts the same way (in+out) and produced
a plausible ~9204 — because the raw API has no prompt caching (the cache classes are zero).
This means the bug is specific to the claude_code path.

**Fix (minimal):**

```python
total = sum(
    v for v in (
        usage.get("input_tokens"),
        usage.get("cache_creation_input_tokens"),
        usage.get("cache_read_input_tokens"),
        usage.get("output_tokens"),
    ) if v is not None
) or None
```

Optionally — expose the cache tokens as separate fields in `metrics` for transparency.
**Order:** fix → re-sweep the 2 routable agents (`claude_code@claude-sonnet-4-6`,
`codex_cli@gpt-5.5`) → ingest — so that the new `benchmark_runs` rows carry correct tokens.

---

## Consequences

**Upsides:** we do not miss model releases; identity is stable → the benchmark history stays
intact; a human in the loop where money/routing is involved; a new model is immediately
comparable with its predecessor.
**Downsides / cost:** we need a discovery script + alias normalization + a pinned golden-suite;
two PRs instead of one (declare ≠ enable). Justified: the cost of an auto-bump error is
non-deterministic routing on invalid data.

**Risks:** (1) the golden-suite drifts → the A/B is invalid (mitigation: pin the `suite_id`);
(2) the discovery bot is noisy on marketing re-labels (mitigation: a PR proposal, not an
auto-merge); (3) the `settings.py` evaluator model stays outside the catalog (see actions).

---

## Recommended actions

**devtools/** (`_cowork_output/devtools/`)
- Discovery notifier: a scheduled task (weekly) → reconcile the catalog against provider models
  and `claude --model` → auto-PR **only against Plane 1**; alias normalization
  `claude-sonnet-5` → catalog convention (the `aliases` field).
- Fix the canonical SSOT path (atp `method/` vs `contracts/`) before implementing the bot.

**atp-platform**
- [x] Pre-req P2: fix the cache tokens in `method/spawners/claude_code_shim.py:57-58`; then
  re-sweep. ✅ 2026-07-02 (#213 + re-sweep).
- [x] Pinned golden `suite_id` for cross-model comparison. ✅ 2026-07-02
  (#215: `SUITE.lock.toml` per case-dir, sha256 pin + drift refusal + `--write-suite-lock`).
- ~~Derive the evaluator model `atp/core/settings.py:250` (`claude-sonnet-4-20250514`) under
  the catalog as a "floating evaluator model" class, or explicitly mark it "not a join key".~~
  **Superseded by 003b (marked 2026-07-03):** the direction was reversed — the evaluator model
  already lives in the user-config contour (env/`.env`, `settings.py` pydantic `ATP_` settings),
  and 003b brings **the agent catalog to the same resolution mechanism** ("one loader",
  003b D2/actions), rather than putting the evaluator model into the git catalog. This item
  need not be executed literally; only its second half remains — the evaluator model is
  explicitly NOT a join key (the D1 table already records this).
- Replace the hardcoded model strings in `tests/unit/method_spawners/test_run_pipe_check.py:28`
  with a fixture tied to the catalog.

**arbiter**
- Bring the dead keys (`claude_code@claude-opus-4-8`, `codex_cli@gpt-5-codex`) to
  `status="retired"` in `config/agents-catalog.toml` (currently only crossed out in a comment,
  lines 243-244); ensure conformance-CI fails on a live reference.
- Gate merge: the routable-PR (Plane 2) is blocked until a `rank_score` exists on the golden-suite.
- An A/B view over `benchmark_runs` "model A vs B on suite T" for the flip decision.

**Maestro**
- `DEFAULT_CLAUDE_MODEL` (`spawners/claude_code.py:21`) — only via codegen from the catalog.

**General**
- Ratify this amendment; on acceptance — update the status of ADR-ECO-003 with a reference to 003a.
