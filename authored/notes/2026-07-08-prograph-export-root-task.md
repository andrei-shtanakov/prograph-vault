---
title: Task — prograph configurable export_root (P0a)
type: note
status: living
owner: Andrei
updated: 2026-07-08
---

# Task: prograph — configurable `export_root`

> Repo: `prograph/`. Run **inside** it. Decision context: [[2026-07-08-adr-prograph-vault-format-divergence]] (P0a).
> Result consumer: the promoter `authored/skills/promote-prograph.sh`.

## Goal

Let prograph write its Markdown export (`projects/`, `contracts/`, `index.md`) to an arbitrary **staging dir**, not only `.prograph/`. The DB and internal artifacts stay in `.prograph/`. This unblocks the external promoter that moves staging → `prograph-vault/derived/graph/` atomically with `rsync --delete`.

**Boundary:** `export_root` targets a **repo-local staging** (e.g. `.prograph/graph`), NOT the KB. prograph must not know about `prograph-vault`. KB-write ownership belongs to the promoter. No KB paths in code/defaults.

## Changes (3 files)

### 1. `prograph/prograph/paths.py`

`PrographPaths` is a frozen dataclass with one field `monorepo_root: Path` and path properties.

- Add `export_root: Path | None = None`; resolve relative to `monorepo_root` if not absolute.
- Resolve the **export** properties from `export_root` when set, else from `.prograph/`:
  - `projects_md_dir` → `<export_root>/projects` | `.prograph/projects`
  - `contracts_md_dir` → `<export_root>/contracts` | `.prograph/contracts`
  - `index_md_path` → `<export_root>/index.md` | `.prograph/index.md`
- **Do NOT touch** (always under `.prograph/`): `prograph_dir`, `config_path`, `db_path`, `lock_path`, `log_path`, `gitignore_path`, `mcp_patterns_dir`.
- `ensure_dirs()`: still create `prograph_dir` + `mcp_patterns_dir`; also create `projects_md_dir` + `contracts_md_dir` (which may now be under `export_root`).
- Invariant: with `export_root=None` all paths are **identical to today** (zero regression).

```python
@dataclass(frozen=True)
class PrographPaths:
    monorepo_root: Path
    export_root: Path | None = None

    @property
    def _export_base(self) -> Path:
        if self.export_root is None:
            return self.prograph_dir
        er = self.export_root
        return er if er.is_absolute() else (self.monorepo_root / er)

    @property
    def projects_md_dir(self) -> Path: return self._export_base / "projects"
    @property
    def contracts_md_dir(self) -> Path: return self._export_base / "contracts"
    @property
    def index_md_path(self) -> Path: return self._export_base / "index.md"
```

### 2. `prograph/prograph/config.py`

Add `read_export_root(config_path) -> str | None` next to `read_auto_export` (tolerant of parse errors): reads `[output] export_root`. Update the `.prograph/config.toml` template comment:

```toml
[output]
auto_export = false
# export_root = ".prograph/graph"   # staging for the promoter; relative to monorepo root
```

### 3. `prograph/prograph/cli.py`

- Thread `export_root` into every `PrographPaths(monorepo_root=root)` (`~109,156,213,282,317,418`).
- Priority: **CLI `--out-dir` > config `[output] export_root` > None**.
- Add `--out-dir PATH` to `index` (near `--export-md`, ~147) and `export-md` (~266), default `None`.
- Factor a small helper `_resolve_export_root(cli_out_dir, config_path) -> Path | None` to avoid duplication.

## Out of scope

- No references to `prograph-vault`/KB in code or defaults.
- Do not change card format/rendering (`export/render.py`) — paths only.
- Do not move `graph.db`, `mcp_patterns/`, locks, config out of `.prograph/`.
- JSON graph export, frontmatter provenance, `drift --exit-code`, `git init` — separate follow-up phases (ADR P1/P2).

## Acceptance criteria

1. **Zero default regression:** no `--out-dir`, no config → `prograph index --export-md` writes to `.prograph/{projects,contracts,index.md}`, `graph.db` in `.prograph/`. Existing tests green.
2. **CLI override:** `--out-dir /tmp/stage` → cards in `/tmp/stage/{projects,contracts}` + `/tmp/stage/index.md`; `graph.db` still in `.prograph/`.
3. **Config:** `[output] export_root=".prograph/graph"` → export under `.prograph/graph/...`; `graph.db` in `.prograph/`.
4. **Priority:** with both config and `--out-dir`, `--out-dir` wins.
5. **Rel/abs:** relative `export_root` resolves from root; absolute used as-is.
6. `export-md` (re-render without reindex) honors the same rules.

## Manual check

```sh
cd prograph
uv sync
uv run prograph index --export-md                            # default → .prograph/
uv run prograph index --export-md --out-dir .prograph/graph  # staging
ls .prograph/graph/projects | head
test -f .prograph/graph.db && echo "db intact (.prograph/)"
uv run pytest
```

## Status (2026-07-08)

Partly implemented locally in `prograph` (uncommitted): `cli.py/config.py/paths.py` + `tests/unit/test_paths.py`, `tests/unit/test_config.py`, `tests/integration/test_cli_export_root.py`. Commit + push before migrating machines.
