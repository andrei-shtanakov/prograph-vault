---
title: Polyrepo workflow setup
type: note
status: living
owner: Andrei
updated: 2026-05-25
---

# Organizing work with the AI Orchestrators polyrepo ecosystem

> Date: 2026-05-25
> Role: TPM / systems architect
> Mode: read-only, tooling artifacts in `_cowork_output/devtools/`
> Chosen goal: **don't touch the structure, improve the daily workflow**

> **Update 2026-07-07 (staleness flag, /robin-init onboarding dry-run):** the repo roster
> below is a **2026-05 snapshot** and is stale. The current ecosystem the team names is
> **atp-platform, Maestro, arbiter, spec-runner, deployer, dispatcher, steward** — `deployer`,
> `dispatcher`, `steward` did not exist yet here; `proctor`, `open-prose`,
> `atp-platform-testing-en` are no longer part of the named set. The polyrepo *mechanics*
> (not submodules, iterate an explicit list, `--ff-only`, heterogeneous branches) still hold;
> only the list is dated. Do not treat §1's table as the current roster. `last_reviewed` due.

---

## TL;DR

1. **This is not a monorepo, but 7 independent repos** in one folder (no `.gitmodules` — not submodules). The root `.git` tracks only cowork artifacts and `.gitignore` (`.aider*`). Therefore any cross-repo tool must iterate over an **explicit list** of repos, not the git root.
2. **The main source of friction is not "they sit side by side," but contract vendoring**: `obs.py` is copied to 3 places, the arbiter MCP client is vendored into Maestro, schemas are maintained by hand. `COWORK_CONTEXT.md:204,279` itself records the doc drift.
3. **An ergonomics layer is ready without migration** (4 files in `_cowork_output/devtools/`): a VS Code multi-root workspace, `repos.sh` (status/fetch/pull/dirty/branches/bootstrap/exec), a `Makefile` wrapper, `check-contract-drift.sh`. All checked: syntax ok, dry-run against the real repos passes.
4. **The scripts account for your reality**: branches are heterogeneous (`master`/`main`/feature), 5 of 7 repos are currently dirty, `atp-platform-testing-en` has no upstream — you can't hardcode `pull` to `origin main`, so it works `--ff-only` on the current branch and skips dirty/detached ones.
5. **Two signals for the radar**: (a) a new project **`prograph`** appeared in the folder, absent from the registry; (b) the drift-checker confirmed that the `report_benchmark` schema is in sync, and the `obs.py` divergence is **cosmetic** (header + reformat by the linter), not logic drift.

---

## 1. Current state (facts)

| Repository | Current branch | Dirty | Upstream | Remote |
|---|---|---|---|---|
| Maestro | `docs/r-06b-m4-followup` | 2 files | yes | `andrei-shtanakov/Maestro.git` |
| arbiter | `docs/r-06b-m4-update` | 2 files | yes | `andrei-shtanakov/arbiter.git` |
| atp-platform | `chore/sync-phase6-status` | 1 file | yes | `andrei-shtanakov/atp-platform.git` |
| spec-runner | `master` | clean | yes | `andrei-shtanakov/spec-runner.git` |
| proctor | `master` | 4 files | yes | `andrei-shtanakov/proctor.git` |
| open-prose | `main` | 3 files | yes | `andrei-shtanakov/open-prose.git` |
| atp-platform-testing-en | `ru_version` | clean | **no** | `andrei-shtanakov/atp-platform-testing.git` |

Observations that dictated the tooling design:

- **Not submodules.** The root's `git -C . config` contains no `.gitmodules`. So "one `git pull`" from the root of the repo nesting won't pull anything — you need an external loop over the list.
- **Branches are inconsistent.** Three repos on feature branches, two on `master`, one on `main`, one on `ru_version`. The `pull` script doesn't do `git pull origin main`, it pulls the current upstream `--ff-only`.
- **Dirty right now (5/7).** A morning review of "what's dirty / on which branch" is real value, not decoration.
- **Folder name ≠ remote name** in two cases: `proctor → proctor.git`, `atp-platform-testing-en → atp-platform-testing.git` (and it sits on branch `ru_version` without an upstream). Not a bug for the tooling, but worth keeping in mind.

---

## 2. Why the ergonomics layer and not a merge (briefly, for the record)

You chose "don't touch the structure." That is a justified decision — I'm recording the comparison so it's on paper:

| Option | What it solves | Cost | Verdict for your ecosystem |
|---|---|---|---|
| **A. Polyrepo + ergonomics layer** (chosen) | the daily routine (status/pull/bootstrap across all at once) | ~0, no migration | ✅ Fast ROI. Does **not** remove the vendoring pain |
| B. Full monorepo (merge all 9) | atomic cross-repo commits | high: merging histories, merging 7 CIs, breaks the independent release of `atp-platform-sdk` | ❌ Overkill: open-prose/proctor/agents-for-game are weakly coupled, dragging them into a monorepo is harmful |
| C. Polyrepo + 1 repo of shared contracts | a single source of truth for obs/MCP/executor-state schemas instead of vendoring | medium: a new contract release cycle | 🟡 This is the right **next** step if the drift keeps hurting. ATP already proved the pattern via `atp-platform-sdk` on PyPI |

The key argument: the ATP boundary is already done "right" — it is consumed as a versioned package `atp-platform-sdk>=2.0.0` (`COWORK_CONTEXT.md:203,234`), and there is no vendoring pain there. The pain remains where files are copied: `obs.py` and `arbiter_client.py`. So option A closes the routine now, and we keep option C as a deliberate next step — without it the monorepo is redundant.

---

## 3. Ergonomics layer — the kit

All files are in `_cowork_output/devtools/`. Deploy: copy into the **root** of `all_ai_orchestrators/`, grant permissions, and use.

```bash
cp _cowork_output/devtools/{repos.sh,check-contract-drift.sh,Makefile,all-orchestrators.code-workspace} .
chmod +x repos.sh check-contract-drift.sh
```

| File | Purpose | Commands |
|---|---|---|
| `all-orchestrators.code-workspace` | VS Code multi-root: all 7 repos + root + `prograph` in one Source Control panel; rust-analyzer on `arbiter/Cargo.toml`, ruff/uv per-folder | `File → Open Workspace from File…` |
| `repos.sh` | the engine of cross-repo operations over the explicit list | `status` `fetch` `pull` `dirty` `branches` `bootstrap` `exec '<cmd>'` |
| `Makefile` | friendly aliases | `make status/fetch/pull/dirty/branches/bootstrap/drift/morning` |
| `check-contract-drift.sh` | read-only check of the desync of vendored contracts | `make drift` |

Typical scenarios:

- **Morning:** `make morning` → fetch all + a summary table (branch / ↑↓ / dirt).
- **Before a coupled commit:** `make drift` → whether the schemas/obs have diverged before it goes into a PR.
- **Bring up the environment from scratch:** `make bootstrap` → `uv sync` across the 5 python repos + `cargo build` for arbiter (determined by the presence of `pyproject.toml`/`Cargo.toml`).
- **Any bulk operation:** `./repos.sh exec 'git log --oneline -3'`.

Design decisions important for safety:

- `pull` pulls **only** the current upstream `--ff-only`; dirty, detached and no-upstream repos are skipped with a warning (on your `atp-platform-testing-en` this triggered in the dry-run).
- The scripts write nothing into the project folders — read-only mode is preserved.

---

## 4. Signal found: state of the vendored contracts

`check-contract-drift.sh` (dry-run against the real repos):

| Contract | Reference | Copy | Result |
|---|---|---|---|
| `report_benchmark-v1.schema.json` | `arbiter/arbiter-mcp/tests/contract/` | `Maestro/_cowork_output/benchmark-contract/` | ✅ identical (byte-for-byte) |
| `obs.py` | `spec-runner/src/spec_runner/obs.py` | `Maestro/maestro/_vendor/obs.py` | ⚠ −/+21 lines |
| `obs.py` | `spec-runner/src/spec_runner/obs.py` | `arbiter/orchestrator/_vendor/obs.py` | ⚠ −/+20 lines |

The `obs.py` divergence is **not logic drift**: it is a 2-line provenance header (`# Vendored from spec-runner@fa6b106…`) plus reformatting (the consumer ran the copy through its own ruff — dict-comprehension wrapped across lines). The behavior is identical.

Conclusion for the tooling: a naive byte-for-byte check of `.py` gives false positives. If you want a reliable gate on `obs.py` — normalize before comparing (strip the header + compare the AST, e.g. `python -c "import ast"` normalization or `ruff format -` on both sides to stdout). For JSON schemas byte-for-byte is correct and already green.

---

## 5. New project `prograph` (not in the registry)

A `prograph/` directory appeared in the root (modified 2026-05-25). It is **not a separate repo** — it has no `.git` of its own, it is tracked by the root git. Inside: `CLAUDE.md` (~7.4 KB), `.vscode/`, `docs/`, and a subdirectory `Sourcetrail/` (a code visualization tool). It is not in `COWORK_CONTEXT.md`.

I suggest adding an entry to the registry (section "Auxiliary projects"). Since the mode is read-only, I don't edit the file myself — here is a ready-made row:

```markdown
| **prograph** | ? (see CLAUDE.md) | — | Code-graph visualization/analysis (Sourcetrail), tracked by the root git | 🆕 New 2026-05-25, needs categorization |
```

---

## Recommended actions

1. **[root]** Copy the 4 files from `_cowork_output/devtools/` into the root and `chmod +x` (see §3). Open `all-orchestrators.code-workspace` — you get a single Source Control panel across all repos.
2. **[root / process]** Build the habit of `make morning` and `make drift` before coupled PRs. `drift` catches exactly the problem already noted in `COWORK_CONTEXT.md:204` ("the arbiter docs are not updated for the 6th tool").
3. **[COWORK_CONTEXT.md]** Add `prograph` to the registry (ready-made row in §5) and define its role/language — right now it's a "blind spot" of the ecosystem.
4. **[Maestro / arbiter / spec-runner]** Decide the fate of the `obs.py` vendoring: either accept that the copies are reformatted (then the drift-gate on `obs.py` must normalize the input), or move toward option C — extract `obs.py` + the MCP schemas into a single versioned package modeled on `atp-platform-sdk`. This removes the recurring tax of manual syncing.
5. **[atp-platform-testing-en]** Check the configuration: the `-en` folder sits on branch `ru_version` without an upstream, remote — `atp-platform-testing.git`. Possible ru/en confusion — a separate minor investigation.

---

*Tooling artifacts:* `_cowork_output/devtools/` — `all-orchestrators.code-workspace`, `repos.sh`, `Makefile`, `check-contract-drift.sh`.
