---
title: R-07 / benchmark #2 — crossover attempted, null result (confirms decision C)
type: note
status: archived
owner: Andrei
updated: 2026-07-02
archived: 2026-07-06
reason: historical status snapshot (bulk-archived on graduation from _cowork_output)
---

# R-07 / benchmark #2 — crossover attempted, null result (confirms decision C)

> Date: 2026-07-02 · From: ATP (measurement side)
> Continues: `2026-07-02-r07-rerank-tiebreaker-scope.md` (owner decision C),
> `2026-06-21-r07-benchmark2-request-to-atp.md` (crossover request).
> Context: the doc `…-rerank-tiebreaker-scope.md` downgraded benchmark #2 from "enabling
> gate" to "demonstrate value through a crossover". This doc is that very
> demonstration, executed and measured.

## What was done

A crossover slice was designed and run on **two real verticals** for the two
routable agents (`claude_code@claude-sonnet-4-6`, `codex_cli@gpt-5.5`), n=3,
deterministic graders, both verticals under the golden-suite lock (ADR-ECO-003a D3):

- **V1 code-review** (15 cases, planted-defect, findings_match) — already measured.
- **V2 req-extraction** (expanded 5→14, ATP PR #216: fabricated deadline/actor/
  condition, json_path) — hypothesis: the same aggressiveness that gives codex a win on
  V1 sinks it on a task that rewards **restraint** (not fabricating an
  absent field); claude should lead.

## Result — no crossover, cause = CEILING (not codex dominance)

| | V1 code-review | V2 req-extraction (inline) |
|---|---|---|
| claude rank_score | 0.705 | **0.879** |
| codex rank_score | 0.781 | **0.879** |
| Δ (codex − claude) | **+0.076** | **0.000** |

- The sign does not invert → **no crossover**.
- But on the **13 inline cases both agents are perfect (13/13)** — a ceiling. The hypothesis
  "restraint-agent vs recall-agent" is **falsified** for this pair: codex is just
  as flawless at not fabricating. "Restraint" does not separate the two frontier agents.
- The only failure for both is 1 **corpus** case (`corpus-clean`,
  citation_grounding, axis=clean). Both frontier agents fail at the easiest
  level → this is a **harness artifact**: `run_pipe_check` does not pass the corpus's
  `assets/` to CLI-adapter agents (the harness was built for inline cases). It drags
  breakpoint→clean down for both. A separate bug, not a signal; inline-only = both 100%.
- V2 was **not ingested** into arbiter's `benchmark_runs` (a ceiling tie polluted by
  a broken corpus case — useless to routing).

## Conclusion

- **Benchmark #2 demo goal closed as null.** On this pair of frontier agents
  code-review discriminates (codex>claude, but re-rank is DT-inert — see previous doc),
  req-extraction-restraint does not discriminate (ceiling). Neither a crossover nor
  a `|Δ|≥0.15`-that-moves-routing.
- **Decision C confirmed empirically, not only architecturally.** The two frontier agents
  are close; contextual routing between them yields no demonstrable value on the
  measured slices. Re-rank stays an honest tiebreaker.
- The artifacts were not wasted: the expanded 14-case req-extraction vertical is a
  valid calibration vertical (both agents pass it = floor); golden-locked.

## Open loose ends (not blockers)

1. **corpus-wiring in run_pipe_check** — the harness does not mount the corpus `assets/` for
   CLI-adapter agents. Either fix the wiring or mark corpus cases as
   not-runnable by this harness. Separate hygiene.
2. Lever A (blend `α·DT + β·rank_score`) remains available if we later decide that
   the empirics should steer more strongly (per the previous doc). Not now.
3. The crossover as such is not disproven at all — it is disproven for *this pair* on the
   *restraint axis*. A more divergent pair of agents or a different axis might yield a
   signal, but that is fishing without a hypothesis — deliberately not pursued.
