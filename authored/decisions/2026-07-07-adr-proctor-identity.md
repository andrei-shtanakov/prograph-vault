---
title: proctor identity — repo/dir `proctor` vs service-id `proctor-a`
type: adr
status: accepted
owner: Andrei
updated: 2026-07-07
---

# ADR: `proctor` (repo/dir) vs `proctor-a` (runtime service-id)

## Context

The project historically lived in a local directory named `proctor-a`, while its git
repository, Python package, and code are all `proctor`
(`github.com/andrei-shtanakov/proctor`, `src/proctor/…`). A fresh `git clone` produces a
`proctor/` directory, so keying anything on the local directory name `proctor-a` is not
portable across machines / re-clones.

Separately, `proctor-a` is used as a **runtime service / agent identity**: it appears in the
arbiter observability contract as an enum value
(`log-schema.json`: `["maestro","spec-runner","arbiter","atp","proctor-a"]`) and in the
dispatcher collector. So `proctor-a` is not merely a directory label — it is a service-id in
the logs/observability plane. Read `proctor-a` as **"proctor-agent"**.

## Decision

Treat these as **two deliberate namespaces**:

- **Repo / directory / package / KB project identity → `proctor`.** The local directory is
  renamed `proctor-a → proctor` (matches the repo and what a clone yields). KB identity is
  derived from the **git-remote repo name** (`kb_project` in `authored/skills/kb-utils/kb-env.sh`),
  so journals/facts stay stable across clones and directory renames — for every repo, not just
  this one.
- **Runtime observability service / agent-id → `proctor-a`** ("proctor-agent"), unchanged. The
  arbiter log-schema enum keeps `proctor-a`; the dispatcher collector keeps emitting
  `service="proctor-a"` while its discovery-facing `name` is `proctor` (discovery is by
  on-disk directory). This mirrors the agent-id convention (agent identity is its own axis,
  independent of the repo name).

## Consequences

- `dispatcher/…/collectors/proctor.py`: `name = "proctor"` (discovery), `service = "proctor-a"`
  (observability) — with a comment pointing here.
- arbiter `log-schema.json` enum is left as `proctor-a` (no contract change; historical logs
  keyed `proctor-a` stay valid).
- Registry (`COWORK_CONTEXT`), human docs, Maestro `repo_path`/`workspace_base`, and KB living
  notes use `proctor` (the project/repo). Dated historical KB archives and `_cowork_output/`
  scratch keep `proctor-a` as the record of the time.
- Operational: renaming the directory invalidated `proctor/.venv` console-script shebangs
  (hardcoded to `…/proctor-a/.venv/…`); the venv must be recreated (`uv sync`). Stale
  `/tmp/maestro-ws/proctor-a` workspaces should be removed.
- prograph output keyed on the old dir (`derived/projects/proctor-a.md`, `.prograph/`) is
  regenerable — re-run prograph to re-key on `proctor`.

## Alternatives considered

- **Align everything to `proctor`** (also rename the service-id in the arbiter enum): rejected —
  it churns the observability contract and desyncs already-emitted `proctor-a` logs, for no real
  benefit. Agent/service identity is legitimately a separate namespace from the repo name.
- **Keep the directory `proctor-a`**: rejected — it is not clone-portable and diverges from the
  repo/package name; the fragility is better removed at the source.
