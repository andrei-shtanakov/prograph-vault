---
title: Migration runbook — move the ecosystem to a new machine via GitHub
type: note
status: living
owner: Andrei
updated: 2026-07-08
---

# Migration runbook — new machine via GitHub

> Parent dir: `all_ai_orchestrators/` (polyrepo, NOT submodules).

## TL;DR

1. Everything durable is a **separate git repo** (projects + the KB `prograph-vault`). Move them via GitHub; the **root repo and `_cowork_output/` do NOT travel** (dev-scratch — clones don't have them by project rule).
2. **Uncommitted work does not travel.** Commit in every repo before push. Three repos have no remote yet — create them first (`prograph-vault`, `robin-runtime`, `spec-runner-tasks`).
3. On the new machine: `git clone` all into one parent (default names) → `uv sync` in `prograph/` and `robin-runtime/` → `prograph init && index` (graph is regenerated) → `install-skills.sh`.
4. **Obsidian is NOT required** — the kb-* skills and Robin are filesystem-only.
5. Regenerable data (`.prograph/graph.db`) and Robin's runtime store (`robin-runtime/var/`) do not travel by design — rebuild them in place.

## What travels, what does not

| Category | What | Travels? |
|---|---|---|
| Durable | all project git repos + KB `prograph-vault` | ✅ via GitHub |
| Regenerable | `.prograph/graph.db`, `derived/graph` snapshot | ⚙️ rebuild with `prograph index` |
| Runtime store | `robin-runtime/var/` (Robin log/SQLite) | ❌ gitignored, stays on old machine |
| Dev-scratch | `_cowork_output/`, root repo, `.prograph/` | ❌ does not travel by project rule |
| Machine-local | `.claude/settings.local.json`, `.DS_Store` | ❌ and not needed |

> If something useful lives in `_cowork_output/` (ADRs, plans, tooling), **graduate** it first: ADRs → `authored/decisions/` (via `kb-curator`), scripts → `authored/skills/`. The `promote-prograph.sh` promoter already lives in `authored/skills/`.

## Stage A — on the OLD machine (prepare + push)

**A1. Commit everything uncommitted.** Walk each repo (`_cowork_output/devtools/repos.sh dirty` helps). Anything not in git disappears on clone. Watch especially: `prograph/` (uncommitted `export_root` work in `cli.py/config.py/paths.py` + tests); `prograph-vault/` (fresh `derived/digests/{ai,it}/*.md` are often untracked).

**A2. Create remotes for the repos without one** (local git, no remote):

```bash
cd prograph-vault    && gh repo create andrei-shtanakov/prograph-vault    --private --source=. --remote=origin --push && cd ..
cd robin-runtime     && gh repo create andrei-shtanakov/robin-runtime     --private --source=. --remote=origin --push && cd ..
cd spec-runner-tasks && gh repo create andrei-shtanakov/spec-runner-tasks --private --source=. --remote=origin --push && cd ..
# manual alternative: create empty repos in UI, then per repo:
#   git remote add origin git@github.com:andrei-shtanakov/<repo>.git
#   git push -u origin <branch>   # robin-runtime branch is master
```

**A3. Push the rest** (remote already set): commit → `git -C <repo> push` (or `push -u origin <branch>` for `atp-platform-testing-en`, which has no upstream). Repos with a remote: `Maestro arbiter atp-platform deployer dispatcher libretto proctor prograph robin-toolkit spec-runner spec-runner-vscode steward atp-platform-testing-en`. Note: `sdd-framework` is on **git.epam.com** under another owner — clone-only, do not push.

**A4. (Optional) Prototypes without git** — `appgraph agents-for-game atp-platform-testing(ru) spec-runner-test spec-runner-test-vscode` are scratch/prototypes, not needed for a working KB+Robin+prograph. `git init` + remote only if you want to keep one.

### What-to-push summary

| Action | Repos |
|---|---|
| commit + push (remote exists) | Maestro, arbiter, atp-platform, deployer, dispatcher, libretto, proctor, **prograph**, robin-toolkit, spec-runner, spec-runner-vscode, steward |
| push -u (remote exists, no upstream) | atp-platform-testing-en |
| create remote + push -u | **prograph-vault**, **robin-runtime**, spec-runner-tasks |
| clone-only (external) | sdd-framework (EPAM) |
| decide / skip | appgraph, agents-for-game, atp-platform-testing (ru), spec-runner-test, spec-runner-test-vscode |

## Stage B — on the NEW machine (bootstrap)

**B0. Install tools:** git, uv, rustup (Rust; channel 1.85 comes from `prograph/rust-toolchain.toml`), ripgrep (`rg`), rsync, a C compiler/linker (`build-essential` / Xcode CLT). Optional: gh CLI, Obsidian (human-only KB browsing).

**B1. Clone everything into ONE parent, default names:**

```bash
mkdir -p ~/labs/all_ai_orchestrators && cd ~/labs/all_ai_orchestrators
git clone git@github.com:andrei-shtanakov/prograph-vault.git   # KB — required
git clone git@github.com:andrei-shtanakov/prograph.git          # graph tool
git clone git@github.com:andrei-shtanakov/robin-runtime.git     # Robin runtime
git clone git@github.com:andrei-shtanakov/maestro.git
git clone git@github.com:andrei-shtanakov/arbiter.git
git clone git@github.com:andrei-shtanakov/atp-platform.git
git clone git@github.com:andrei-shtanakov/spec-runner.git
git clone git@github.com:andrei-shtanakov/proctor.git
git clone git@github.com:andrei-shtanakov/dispatcher.git
git clone git@github.com:andrei-shtanakov/deployer.git
git clone git@github.com:andrei-shtanakov/steward.git
git clone git@github.com:andrei-shtanakov/spec-runner-vscode.git
git clone git@github.com:andrei-shtanakov/robin-toolkit.git
git clone git@github.com:andrei-shtanakov/libretto.git
git clone git@github.com:andrei-shtanakov/atp-platform-testing.git  # (-en repo)
git clone git@git.epam.com:Dmytro_Honcharuk/sdd-framework.git
```

> **Default names matter:** project identity resolves by git-remote name (portable), but relative paths expect the vault at `<parent>/prograph-vault` (read by `robin-runtime` → `../prograph-vault` and `install-skills.sh` → `WORKSPACE = parent of KB`). `git clone …/prograph-vault.git` yields folder `prograph-vault` — exactly what's needed.

**B2. Build the tool and the runtime:**

```bash
cd prograph      && uv sync && uv run prograph --version && cd ..   # builds the Rust extension (maturin)
cd robin-runtime && uv sync && cd ..
```

**B3. Regenerate the graph (from the workspace root).** `.prograph/graph.db` does not travel:

```bash
uv run --project prograph prograph init            # creates .prograph/config.toml
uv run --project prograph prograph index --export-md
prograph-vault/authored/skills/promote-prograph.sh # promote snapshot → derived/graph
```

**B4. Install the kb-* skills into siblings:**

```bash
cd prograph-vault/authored/skills && ./install-skills.sh --from-config && cd -
```

**B5. Build ecosystem repos as needed** — `uv sync` (Python) / `cargo build` (arbiter) per project. `repos.sh bootstrap` helps but lives in dev-scratch (won't be on the new machine) — copy it or build repo-by-repo.

**B6. Verify (no Obsidian).** Ask the KB the M0 acceptance question via a coding agent: *"Which repo owns the agents-catalog SSOT?"* → expected `atp-platform/method/agents-catalog.toml`, cited from the vault. If it answers with a citation, the KB works.

## Lost-if-skipped checklist

- [ ] Uncommitted edits in every repo (esp. `prograph` export_root, fresh KB digests).
- [ ] No-remote repos created & pushed (`prograph-vault`, `robin-runtime`, `spec-runner-tasks`).
- [ ] Needed `_cowork_output/` content graduated into the KB (else it does not travel).
- [ ] `.prograph/graph.db` rebuilt on the new machine (`prograph index`).
- [ ] Robin runtime store (`robin-runtime/var/`) moved manually if needed (gitignored).
- [ ] Sibling repos have `origin` (needed by `kb_project` remote-name resolution).

## Why this works

- Vault `.gitignore` = only `.DS_Store` → all knowledge (authored + derived snapshot + journal + skills + `.obsidian/`) travels.
- No absolute paths in tracked files; `kb-env.sh` finds the KB dynamically (env → ancestor with `prograph-vault/authored` → the vault itself).
- Project identity = git-remote name (stable across machines and renames), see [[2026-07-07-adr-proctor-identity]].
