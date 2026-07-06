---
title: "ADR-ECO-003b: Model catalog — distribution & configuration resolution"
type: adr
status: proposed
owner: Andrei
updated: 2026-07-02
---

# ADR-ECO-003b: Model catalog — distribution and configuration resolution

**Status:** Proposed (2026-07-02, Andrei) · **Date:** 2026-07-02
**Deciders:** Andrei (owner Maestro / arbiter / ATP)
**Scope:** ecosystem-wide — the distribution boundary (installed Maestro / ATP / arbiter)
**Type:** Amendment to `decisions/2026-07-02-adr-eco-003a-model-discovery-adoption.md`
and ADR-ECO-003 (`2026-07-01-adr-eco-003-agent-catalog.md`)
**Related:** ADR-ECO-003a (discovery→adoption), ADR-ECO-003 (SSOT catalog, 3 planes)

> ADR-003/003a describe the model catalog as a **vendored file in git** with
> conformance-CI across repos. This is a dev-time contour. It **does not reach** the
> user who ran `pip install atp-platform` (or built arbiter from a crate). This
> amendment closes the distribution boundary: how an installed user configures and
> updates models **without git and without re-releasing the package**.

---

## TL;DR

1. **Models are NOT shipped in the package.** The ATP wheel packs only `atp/`
   (`pyproject.toml:119-120`), and `method/agents-catalog.toml` lies outside the package →
   the pip user has no model catalog at all. This is not a delivery bug —
   it is the correct boundary: models are volatile and per-user, they must not be baked into a distribution.
2. **The model catalog = user configuration**, not source and not package-data. A user's model
   update goes through user-config; the package release does not participate in it.
3. **The package ships only:** the loader + the validation schema + an inert template
   (for `models init`). No active `claude-sonnet-*` inside the wheel.
4. **Resolution (with no baked default):** `$ATP_CATALOG` → XDG user-config → env-override
   of individual fields. No config → **a loud, clear error**, not a silent hidden default.
5. **Two different catalogs, one schema:** the dev/ops SSOT (git, drives the benchmark→routing
   contour of the ecosystem) ≠ the user-runtime catalog (on the user's machine). Conflating them is
   the source of the thesis "git is unsuitable for updating models".
6. **Cross-tool:** since there are no baked defaults — there is nothing to drift. One
   user-config, three readers (Maestro / ATP / arbiter, including Rust). Optionally
   `$ATP_CATALOG` → a shared file for the team/organization.
7. **`atp/catalog/` is a catalog of TESTS** (`builtin/` + `sync.py`), not of models. It must not
   be the home for models; the name must not confuse.

---

## Context

### What the check exposed (2026-07-02)

| Fact | Source | Consequence |
|---|---|---|
| The wheel packs only `atp/` | `atp-platform/pyproject.toml:119-120` (`packages = ["atp"]`) | `method/agents-catalog.toml` does not make it into the wheel |
| The model catalog lives in `method/` | `atp-platform/method/agents-catalog.toml` | dev-tooling, outside the package |
| `atp/catalog/` = tests | `atp/catalog/sync.py:10` (`BUILTIN_DIR`), `parse_catalog_yaml`, CLI `atp catalog` | NOT models; do not confuse |
| the evaluator model is already from env/.env | `atp/core/settings.py:326` (`env_prefix="ATP_"`, `env_file=".env"`), `:362-364` | A precedent of user-config for a model **already exists** — we extend it to the harness catalog |

Bottom line: an installed user configures the **evaluator model** through env/`.env` (already
works), but the **harness/agent catalog** has nowhere for them to set it — it exists only in the
dev `method/`. The distribution hole is precisely in the agent catalog.

### Why git is not the update channel

Git is the dev-SSOT and the release channel for *code* (loader/schema). A user's model update
is an edit of *configuration data* on a specific machine, with a frequent and individual
cadence. Mixing them = requiring a git-clone/re-release just to change a model string. Rejected.

---

## Decision

### D1. The package contains no active model data

Shipped:
- the catalog **loader** (resolution + layer merge);
- the **validation schema** (Plane 1/2/3 from ADR-003, reused);
- an **inert template example** — only as a resource for `models init`, **never**
  loaded as live data.

NOT shipped: an active `agents-catalog.toml`, any default `claude-sonnet-*`.
Boundary: "the package knows the format" ≠ "the package imposes the models".

### D2. Configuration resolution (priority top to bottom)

1. `$ATP_CATALOG` (an explicit path to a file; for teams — a shared file on a share/URL cache).
2. XDG user-config: `$XDG_CONFIG_HOME/<eco>/agents-catalog.toml` → `~/.config/<eco>/agents-catalog.toml`.
3. Env-override of individual fields (`CLAUDE_MODEL`, `ATP_LLM__DEFAULT_LLM_MODEL` — ATP's
   pydantic already handles this).
4. **No layer at all → fail-loud:** `model catalog not configured: 'atp models init'
   or set $ATP_CATALOG`. No hidden default.

Trade-off (deliberately accepted): no baked default → worse first-run UX (it does not work
out of the box until configured), but better correctness — we do not impose an
unavailable/stale model, there is no false endorsement. Mitigation: `models init` + clear
errors + docs.

### D3. Management CLI (discovery for the user)

`<tool> models init | list | discover | update`:
- `init` — generates a starter user-config from a template into the XDG path.
- `discover` — reconciles provider lists against the user catalog, **proposes** additions to
  the **user** file (the logic of the prototype `devtools/discover_models.py` moves here).
- The package is never touched in the process.

### D4. Two catalogs — different entities, a shared schema

| | Dev/ops SSOT | User-runtime |
|---|---|---|
| Where | git-SSOT `atp-platform/method/agents-catalog.toml` (arbiter vendors `config/`; `_cowork_output/contracts/` — a dev mirror, NOT the source; owner ruling 2026-07-03, see the 003a note) | user-config (XDG/`$ATP_CATALOG`) |
| Why | the ecosystem's benchmark→routing contour (`benchmark_runs`, arbiter) | which models *my* instance uses |
| Shipped | no (dev-tooling) | no (the user writes it) |
| Discovery | `devtools/discover_models.py` (workspace/PM, ADR-003a D5) | the shipped `models` CLI |
| Benchmark-gated adoption | yes (rank_score, arbiter gate) | no — an ordinary user does not need it |

The format/schema are shared → the tooling is reused. The fate and the owner are different.

### D5. Cross-tool and arbiter (Rust)

No baked defaults → no source of drift: **the only catalog = the user's, one file,
three readers.** Maestro / ATP / arbiter try the same user-config path at startup. arbiter in
Rust reads the same language-neutral TOML, also with no bundled default, also fail-loud on
absence. Optionally `$ATP_CATALOG` → a file shared by all.

---

## Consequences

**Upsides:** updating a model without git and without a re-release; per-user configuration
(one's own providers/keys/local ollama models); zero baked drift; correctness (nothing
unavailable is imposed); the dev-SSOT and the user contour are decoupled.

**Downsides / cost:** first-run requires `models init`; the loader+schema+CLI must be
implemented in three distributions (Rust — a separate read implementation); documentation for
the XDG path.

**Risks:** (1) the three loader implementations diverge in behavior → mitigation: a shared
conformance test on catalog fixtures; (2) the user sets a model unavailable for their key →
an error at runtime, not at startup → mitigation: `models discover`/`list` shows availability;
(3) the evaluator model (`settings.py:362`) and the agent catalog are two different
configuration points for ATP → collapse them to one loader (see actions).

---

## Recommended actions

**atp-platform**
- Move the agent catalog out of `method/` into the user-config contour: the loader
  (resolution D2) in the `atp/` package, the schema + template resource,
  `atp models init/list/discover/update`.
- Do NOT add an active `agents-catalog.toml` to the wheel (confirm `pyproject.toml:119-120`).
- Collapse the evaluator model (`atp/core/settings.py:362-364`) and the agent catalog to one
  resolution mechanism, so there are not two edit points.
- Rename/document `atp/catalog/` as a test-catalog, so it is not confused with the models.

**Maestro**
- Read the same user-config path for `DEFAULT_<H>_MODEL` (`spawners/*.py:21`) instead of the
  hardcode; fail-loud on absence.

**arbiter (Rust)**
- A loader for the same TOML from user-config (`$ATP_CATALOG`/XDG); no bundled default.

**devtools/**
- Keep `discover_models.py` as the **dev-SSOT** discovery (workspace/PM, ADR-003a D5).
  The user-facing `models discover` — a separate shipped implementation of the same logic.
- Fix a shared conformance test on catalog fixtures for the three loaders.

**General**
- Ratify 003b; on acceptance — update the status of ADR-003/003a with a reference.
- Agree on the canonical XDG path and the `<eco>` name (e.g. `atp/` vs a shared namespace).
