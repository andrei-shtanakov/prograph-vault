# MCP Python SDK v2 Migration Plan (ecosystem-wide)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate every subproject that uses the `mcp` Python SDK from 1.x to 2.x, and close the unbounded-dependency hazard everywhere else, so a fresh `uv sync` in any repo resolves cleanly and every MCP server/client runs on the current SDK line.

**Architecture:** Five independent per-repo phases behind one urgent hotfix. spec-runner (FastMCP decorator API → `MCPServer`, near-mechanical), prograph (low-level `Server` → v2 constructor-based handlers + client tests → v2 `Client`), proctor (drop unused dep), Maestro and atp-platform (ceiling pins only — their MCP surface is the standalone `fastmcp` package, which itself pins `mcp<2.0` even at latest 3.4.5, so real migration is blocked upstream). arbiter is out of scope: its MCP server is hand-rolled Rust JSON-RPC with no SDK dependency, and its only in-ecosystem client (Maestro's vendored `arbiter_client.py`) is likewise hand-rolled JSON-RPC over subprocess stdio.

**Tech Stack:** Python 3.11+, uv, `mcp` 2.x (`pip install mcp` now installs 2.x; v1.x branch is security-fixes only), pytest + anyio, pyrefly/mypy, ruff.

## Verified facts this plan rests on (checked 2026-08-04)

- `mcp==2.0.0` (released 2026-07-28) removed `mcp.server.fastmcp`; verified live: `import mcp.server.fastmcp` → `ModuleNotFoundError`. `requires_python >= 3.10`.
- Official migration guide: <https://py.sdk.modelcontextprotocol.io/migration/> ; tour: <https://py.sdk.modelcontextprotocol.io/whats-new/>.
- Key v2 changes used below:
  - `FastMCP` → `MCPServer`, import `from mcp.server import MCPServer`; decorator API (`@mcp.tool()` etc.) unchanged; submodules `mcp.server.fastmcp.*` → `mcp.server.mcpserver.*`.
  - Low-level `Server`: decorator registration (`@server.list_tools()` / `@server.call_tool()`) **removed**; handlers are now constructor kwargs (`on_list_tools=`, `on_call_tool=`) with `(ctx, params)` signatures returning explicit `ListToolsResult` / `CallToolResult`. `stdio_server()`, `server.run(read, write, init_options)`, `create_initialization_options()` unchanged.
  - Types: camelCase → snake_case (`Tool(inputSchema=…)` → `Tool(input_schema=…)`).
  - Client: one `Client` object replaces `ClientSession` + `initialize()`; `StdioServerParameters` + `stdio_client` remain as the transport factory: `async with Client(stdio_client(params)) as client:`.
- Dependency inventory across the polyrepo (found by grepping **all** `pyproject.toml` at any depth plus all Python imports — an earlier two-level scan missed `atp-platform/packages/*`):
  - `spec-runner/pyproject.toml:29` — `"mcp>=1.26.0"` (unbounded → **broken today** on fresh install). Uses FastMCP decorators in `src/spec_runner/mcp_server.py`; `src/spec_runner/__init__.py:34` imports it eagerly, so **any** `import spec_runner` crashes under mcp 2.0 (this is what broke `spec-runner-init`).
  - `prograph/pyproject.toml:16` — `"mcp>=1.28.1,<2"` (safe today; ceiling was deliberate). Uses low-level `Server` in `prograph/mcp_server.py`; 3 integration test files use v1 client API. Security floor 1.28.1 = patched for CVE-2026-59950 / -52869 / -52870.
  - `Maestro/pyproject.toml:27` — `"mcp>=1.28.1"` (security floor for the SDK transitively pulled by `fastmcp>=2.14.5`; lock has fastmcp 3.2.0 + mcp 1.28.1). fastmcp 3.2.0 requires `mcp<2.0,>=1.24.0`; fastmcp/fastmcp-slim 3.4.5 (latest) still `mcp<2.0`.
  - `proctor/pyproject.toml:13` — `"mcp>=1.28.1"` with **zero** `mcp` imports anywhere in the repo (the only hit is the literal event-type string `"mcp.call"`). Unused dependency.
  - `atp-platform/packages/atp-dashboard/pyproject.toml:19` — `"fastmcp>=3.0"`, **no direct `mcp` specifier and no CVE floor** (unlike Maestro). Real MCP server: `atp/dashboard/mcp/` uses `fastmcp.FastMCP`, `fastmcp.Context`, `fastmcp.server.dependencies.get_http_request`. Same upstream block as Maestro (fastmcp pins `mcp<2.0`). Additionally `scripts/repro_mcp_concurrent_tools_list.py` and `participant-kit-el-farol-en/bot_el_farol_random.py` import the v1 SDK client (`ClientSession`, `sse_client`) directly, relying on the transitive `mcp` — they migrate together with the future fastmcp→v2 move.
  - `atp-platform/packages/atp-adapters` (MCPAdapter) — speaks MCP over a **hand-rolled** transport (`atp/adapters/mcp/transport.py`: asyncio + httpx + raw JSON-RPC; package deps are only `atp-core` + `httpx`). No SDK import; SDK v2 does not touch it.
- prograph's MCP **detector** (tree-sitter queries `prograph-core/src/ts_queries/python_mcp.scm`) matches idioms generically (`@<expr>.tool(...)`, `add_tool("…")`, `call_tool("…")`), not the `FastMCP` symbol — v2-style code (`MCPServer`, v2 `Client`) is detected without any detector change. Fixture files importing `mcp.server.fastmcp` are parser *inputs*, never executed; they keep working as-is.

## Global Constraints

- uv only, never pip; run tools via `uv run`.
- Polyrepo boundaries: each phase touches exactly one repo; work inside that repo's directory; PR-only, no direct commits to `master`; merge is done by the human; after `gh pr create`, process GitHub Copilot review comments before calling the PR done.
- Ruff line length is **100** in spec-runner and prograph (their pyproject wins over the global 88).
- Type checks: `uv run mypy src` (spec-runner), `uv run pyrefly check 'prograph/**/*.py' 'tests/unit/**/*.py' 'tests/integration/**/*.py'` (prograph — always with explicit globs).
- prograph has **no CI running tests** — the local check block in its CLAUDE.md is the gate; run it fully before pushing.
- spec-runner interop contract (`.executor-state.db` schema, `--json-result`) must not change; none of these tasks touch it.
- New behaviour requires tests; bug fixes require regression tests. Async tests use anyio, not asyncio.

## Phase ordering

- **Phase 0 (spec-runner hotfix) ships first and alone** — it unblocks every fresh install today and must not wait for the migration.
- Phases 1–5 are independent (different repos) and can run in parallel or any order. Suggested order by value: 1 (spec-runner v2), 2 (prograph v2), 3 (proctor cleanup), 4 (Maestro guard), 5 (atp-platform guard).

---

## Phase 0 — spec-runner 2.11.1 hotfix: pin `mcp<2` (repo: `spec-runner/`)

### Task 0.1: Ceiling pin + patch release

**Files:**
- Modify: `spec-runner/pyproject.toml:29` (dependency) and the `version = "2.11.0"` field
- Test: existing suite only (no new tests — packaging-only change)

**Interfaces:**
- Produces: spec-runner 2.11.1 on PyPI-equivalent channel; fresh `uv sync` resolves mcp 1.x again.

- [ ] **Step 1: Branch**

```bash
cd spec-runner && git switch master && git pull --ff-only
git switch -c fix/mcp-v2-ceiling-pin
```

- [ ] **Step 2: Pin the dependency**

In `pyproject.toml` change:

```toml
    "mcp>=1.26.0",
```

to:

```toml
    # v2 (2026-07-28) removed mcp.server.fastmcp; ceiling until the v2
    # migration lands (see prograph-vault note 2026-08-04-mcp-v2-migration-plan).
    "mcp>=1.26.0,<2",
```

- [ ] **Step 3: Bump version to 2.11.1**

In `pyproject.toml` set `version = "2.11.1"`. Grep for hardcoded version strings in tests (`grep -rn "2\.11\.0" tests/`) and update any that assert the version.

- [ ] **Step 4: Re-lock and verify resolution**

```bash
uv sync
uv run python -c "import mcp, spec_runner; print(mcp.__file__)"
```

Expected: resolves an `mcp` 1.x; import succeeds.

- [ ] **Step 5: Run the suite + linters**

```bash
uv run pytest tests/ -v -m "not slow"
uv run ruff format . && uv run ruff check .
uv run mypy src && pyrefly check
```

- [ ] **Step 6: Commit, push, open PR; process Copilot review**

```bash
git add pyproject.toml uv.lock
git commit -m "fix: pin mcp<2 (v2 removed mcp.server.fastmcp); release 2.11.1"
git push -u origin fix/mcp-v2-ceiling-pin && gh pr create --fill
```

---

## Phase 1 — spec-runner → mcp v2 (release 2.12.0) (repo: `spec-runner/`)

Do this **after Phase 0 is merged** (rebase on it).

### Task 1.1: Lazy MCP import in `__init__.py` (regression for the spec-runner-init breakage)

Independent of the SDK version: a broken/missing `mcp` must not make `import spec_runner` (and thus `spec-runner-init`) crash — only the MCP feature itself may fail.

**Files:**
- Modify: `spec-runner/src/spec_runner/__init__.py:34` (remove eager import; add module `__getattr__`)
- Test: `spec-runner/tests/test_lazy_mcp_import.py` (create)

**Interfaces:**
- Produces: `spec_runner.mcp_run_server` still resolves (lazily); `__all__` unchanged.

- [ ] **Step 1: Write the failing tests**

```python
"""Importing spec_runner must not import the mcp SDK (regression: mcp 2.0
made `import spec_runner` crash, taking spec-runner-init down with it)."""

import subprocess
import sys


def test_import_spec_runner_does_not_import_mcp() -> None:
    code = (
        "import sys; import spec_runner; "
        "sys.exit(0 if 'mcp' not in sys.modules else 1)"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True)
    assert proc.returncode == 0, proc.stderr.decode()


def test_mcp_run_server_attribute_still_resolves() -> None:
    import spec_runner

    assert callable(spec_runner.mcp_run_server)
```

- [ ] **Step 2: Run to verify the first test fails**

Run: `uv run pytest tests/test_lazy_mcp_import.py -v`
Expected: `test_import_spec_runner_does_not_import_mcp` FAILS (mcp is in sys.modules via the eager import); the second PASSES.

- [ ] **Step 3: Make the import lazy**

In `src/spec_runner/__init__.py` delete line 34 (`from .mcp_server import run_server as mcp_run_server`) and add before `__all__`:

```python
def __getattr__(name: str) -> object:
    """Lazy access to the MCP entry point so importing spec_runner never
    requires (or breaks on) the mcp SDK."""
    if name == "mcp_run_server":
        from .mcp_server import run_server

        return run_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

Keep `"mcp_run_server"` in `__all__`.

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_lazy_mcp_import.py tests/test_mcp.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/spec_runner/__init__.py tests/test_lazy_mcp_import.py
git commit -m "fix: lazy mcp import so 'import spec_runner' survives a broken mcp SDK"
```

### Task 1.2: Migrate `mcp_server.py` to `MCPServer` and require mcp>=2

**Files:**
- Modify: `spec-runner/src/spec_runner/mcp_server.py:12,18` (import + constructor)
- Modify: `spec-runner/pyproject.toml` (dependency + version 2.12.0)
- Test: `spec-runner/tests/test_mcp_v2_wire.py` (create — in-memory wire smoke)

**Interfaces:**
- Consumes: v2 `MCPServer` (`from mcp.server import MCPServer`), v2 `Client` (in-memory connection to a server object).
- Produces: `mcp_app: MCPServer` module global; `run_server()` unchanged signature.

- [ ] **Step 1: Write the failing wire test**

The v2 `Client` connects straight to a server object in memory — this finally lets spec-runner test the actual MCP surface, not just the handlers. (Exact `Client` construction is per the v2 docs "Testing utilities" section — <https://py.sdk.modelcontextprotocol.io/migration/> — the client accepts the server object.)

```python
"""Wire-level smoke: the MCP server serves its tools under SDK v2."""

import pytest
from mcp import Client

pytestmark = pytest.mark.anyio


async def test_mcp_server_lists_all_tools_in_memory() -> None:
    from spec_runner.mcp_server import mcp_app

    async with Client(mcp_app) as client:
        result = await client.list_tools()
        names = {t.name for t in result.tools}
    assert {
        "spec_runner_status",
        "spec_runner_tasks",
        "spec_runner_costs",
        "spec_runner_logs",
        "spec_runner_run_task",
        "spec_runner_stop",
        "spec_runner_next_tasks",
        "spec_runner_task_detail",
    } <= names
```

If the suite lacks an anyio backend fixture, add to `tests/conftest.py`:

```python
@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
```

- [ ] **Step 2: Run to verify it fails**

Run: `uv run pytest tests/test_mcp_v2_wire.py -v`
Expected: FAIL — `mcp` is still 1.x (`ImportError: cannot import name 'Client'`).

- [ ] **Step 3: Bump the dependency and re-lock**

In `pyproject.toml`:

```toml
    "mcp>=2.0.0,<3",
```

(drop the Phase-0 comment), set `version = "2.12.0"`, then `uv sync`.

- [ ] **Step 4: Migrate the imports**

In `src/spec_runner/mcp_server.py`:

```python
from mcp.server import MCPServer
```

replacing `from mcp.server.fastmcp import FastMCP`, and:

```python
mcp_app = MCPServer("spec-runner")
```

All `@mcp_app.tool()` decorators and `mcp_app.run(transport="stdio")` are unchanged in v2.

- [ ] **Step 5: Run the full suite**

Run: `uv run pytest tests/ -v -m "not slow"`
Expected: PASS, including the new wire test and `test_mcp.py` (handlers are SDK-independent).

- [ ] **Step 6: Update docs that name FastMCP**

`CLAUDE.md` (module table row for `mcp_server.py`, "Key Dependencies") and `README.md` if it mentions FastMCP: say "MCP server (`MCPServer`, stdio)".

- [ ] **Step 7: Lint, typecheck, commit, PR**

```bash
uv run ruff format . && uv run ruff check . && uv run mypy src && pyrefly check
git add -A && git commit -m "feat: migrate MCP server to SDK v2 (FastMCP -> MCPServer); require mcp>=2,<3"
git push -u origin feat/mcp-v2-migration && gh pr create --fill
```

Process Copilot review. Human merges.

---

## Phase 2 — prograph → mcp v2 (repo: `prograph/`)

One branch/PR: server rewrite + client-test migration + pin flip must land together (they break individually).

### Task 2.1: Rewrite `mcp_server.py` handlers to v2 constructor style

**Files:**
- Modify: `prograph/prograph/mcp_server.py` (imports, `build_server`, `_tool_definitions`)
- Test: existing `tests/integration/test_cli_mcp.py` (migrated in Task 2.2) is the acceptance gate

**Interfaces:**
- Produces: `build_server(monorepo_root: Path) -> Server` (same name/signature); `serve()` / `main()` unchanged. `_dispatch` and `_tool_definitions` keep their signatures.

- [ ] **Step 1: Flip the pin and re-lock**

In `prograph/pyproject.toml:16`:

```toml
    "mcp>=2.0.0,<3",
```

Then `uv sync`. (The 1.28.1 CVE floor is subsumed: all 2.x releases postdate the patched 1.28.1.)

- [ ] **Step 2: Migrate imports and handler registration**

Replace the header imports:

```python
from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListToolsResult,
    PaginatedRequestParams,
    TextContent,
    Tool,
)
```

and rewrite `build_server` (decorators are gone in v2; handlers move to constructor kwargs, return explicit result types):

```python
def build_server(monorepo_root: Path) -> Server:
    """Construct an MCP server bound to the given monorepo's .prograph/graph.db."""
    paths = PrographPaths(monorepo_root=monorepo_root)
    db_path = str(paths.db_path)

    async def _list_tools(
        ctx: ServerRequestContext, params: PaginatedRequestParams | None
    ) -> ListToolsResult:
        return ListToolsResult(tools=_tool_definitions())

    async def _call(
        ctx: ServerRequestContext, params: CallToolRequestParams
    ) -> CallToolResult:
        args = params.arguments or {}
        try:
            result = await _dispatch(params.name, args, db_path)
        except Exception as exc:
            err = {"error": str(exc), "tool": params.name}
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(err))],
                is_error=False,
            )
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))],
            is_error=False,
        )

    return Server("prograph", on_list_tools=_list_tools, on_call_tool=_call)
```

`is_error=False` on the error branch is deliberate: it preserves v1 wire behaviour, where `_call` caught exceptions and returned them as an ordinary JSON payload (`test_mcp_unknown_tool_returns_error` pins this).

- [ ] **Step 3: snake_case the tool schemas**

In `_tool_definitions()` replace every `inputSchema=` with `input_schema=` (10 occurrences). The JSON schema dicts themselves are unchanged.

- [ ] **Step 4: Confirm `serve()` needs no change**

`stdio_server()`, `server.run(read_stream, write_stream, server.create_initialization_options())` kept their v1 call shapes in v2. No edit expected — just re-read the function.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml uv.lock prograph/mcp_server.py
git commit -m "feat: migrate MCP server to SDK v2 constructor-based handlers"
```

(Integration tests are red until Task 2.2 — same branch, land together.)

### Task 2.2: Migrate the three integration test files to the v2 `Client`

**Files:**
- Modify: `prograph/tests/integration/test_cli_mcp.py`, `test_mcp_find_drifts.py`, `test_mcp_find_symbol_references.py`

**Interfaces:**
- Consumes: `from mcp import Client, StdioServerParameters`, `from mcp.client.stdio import stdio_client`.

- [ ] **Step 1: Rewrite the connection boilerplate**

In each file, imports become:

```python
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
```

and every test body changes from the v1 triple layering:

```python
async with stdio_client(_server_params(fixture)) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("monorepo_overview", arguments={})
```

to the v2 single object (no `initialize()` — the `Client` handles it):

```python
async with Client(stdio_client(_server_params(fixture))) as client:
    result = await client.call_tool("monorepo_overview", arguments={})
```

`list_tools()` / `call_tool(name, arguments=…)` call shapes and `result.content` / `result.tools` stay the same; the `_text()` helper and every assertion are untouched.

- [ ] **Step 2: Run the integration tests**

Run: `uv run pytest tests/integration/test_cli_mcp.py tests/integration/test_mcp_find_drifts.py tests/integration/test_mcp_find_symbol_references.py -v`
Expected: PASS (11 + drift + symbol-ref tests).

- [ ] **Step 3: Run the full local gate (this repo has no test CI)**

```bash
cargo test --all-targets
uv run pytest -v
cargo fmt --all -- --check && cargo clippy --all-targets -- -D warnings
uv run ruff check . && uv run ruff format --check .
uv run pyrefly check 'prograph/**/*.py' 'tests/unit/**/*.py' 'tests/integration/**/*.py'
```

Expected: all green. (Rust is untouched; `cargo test` guards against accidental drift.)

- [ ] **Step 4: Commit**

```bash
git add tests/integration/
git commit -m "test: migrate MCP integration tests to SDK v2 Client"
```

### Task 2.3: Update the pin rationale in prograph's CLAUDE.md; PR

**Files:**
- Modify: `prograph/CLAUDE.md` ("Tooling pins worth knowing" — the `mcp` bullet)

- [ ] **Step 1: Rewrite the `mcp` pin note**

Replace the `**`mcp` is `>=1.28.1,<2`.**` bullet with:

```markdown
- **`mcp` is `>=2.0.0,<3`.** Migrated to SDK v2 (2026-08): lowlevel `Server` uses
  constructor-based handlers (`on_list_tools=`/`on_call_tool=`), tests use the v2
  `Client`. The `<3` ceiling exists because Dependabot only ever raises the *lower*
  bound, so an unbounded specifier would silently resolve the next breaking major.
  The old 1.28.1 CVE floor (CVE-2026-59950 / -52869 / -52870) is subsumed — every
  2.x postdates the patch.
```

- [ ] **Step 2: No detector change — verify and note**

Detector queries (`prograph-core/src/ts_queries/python_mcp.scm`) match `@<expr>.tool(...)` / `call_tool("…")` idioms, not the `FastMCP` symbol, so v2-style scanned code is already detected. Sanity check: `uv run pytest -k "mcp" -v` green (fixtures with v1-style imports are parser inputs and still parse).

- [ ] **Step 3: Commit, push, PR; process Copilot review**

```bash
git add CLAUDE.md
git commit -m "docs: mcp v2 pin rationale"
git push -u origin feat/mcp-v2-migration && gh pr create --fill
```

Note: `master` requires the governance gate + code-owner review; `BLOCKED` with green checks = waiting on human review, not CI.

---

## Phase 3 — proctor: drop the unused `mcp` dependency (repo: `proctor/`)

### Task 3.1: Remove the dependency

**Files:**
- Modify: `proctor/pyproject.toml:13`

- [ ] **Step 1: Re-verify it is unused**

```bash
grep -rn --include="*.py" "from mcp\|import mcp" src tests
```

Expected: no output (verified 2026-08-04; the only "mcp" hits are the literal event-type string `"mcp.call"` in models/tests, which needs no SDK).

- [ ] **Step 2: Delete the line, re-lock, run the suite**

Remove `"mcp>=1.28.1",` from `dependencies`, then:

```bash
uv sync
uv run pytest -v
```

Expected: PASS. If anything imports mcp after all, revert and pin `"mcp>=1.28.1,<2"` instead — but Step 1 says nothing will.

- [ ] **Step 3: Commit, push, PR; process Copilot review**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: drop unused mcp dependency (no imports; v2 made the unbounded pin hazardous)"
git push -u origin chore/drop-unused-mcp && gh pr create --fill
```

If MCP support lands in proctor later, it starts directly on `mcp>=2,<3`.

---

## Phase 4 — Maestro: ceiling guard; real migration deferred upstream (repo: `Maestro/`, canonical name `maestro`)

Maestro's MCP surface is the standalone **`fastmcp`** package (`from fastmcp import FastMCP`), not `mcp.server.fastmcp`. fastmcp — including latest 3.4.5 / fastmcp-slim — pins `mcp<2.0`, so Maestro *cannot* move to SDK v2 until fastmcp does, and is *not broken* today (fastmcp's ceiling protects resolution). Maestro's own `mcp>=1.28.1` is only a CVE floor on the transitive SDK.

### Task 4.1: Make the floor a floor-plus-ceiling and record the trigger

**Files:**
- Modify: `Maestro/pyproject.toml:27` and the comment block above it
- Modify: `Maestro/TODO.md` (add a trigger item)

- [ ] **Step 1: Pin the ceiling to match fastmcp's own constraint**

```toml
    "mcp>=1.28.1,<2",
```

Extend the existing security-floor comment with one line:

```toml
    # <2 mirrors fastmcp's own ceiling (fastmcp<=3.4.5 requires mcp<2.0);
    # lift both together when fastmcp ships SDK-v2 support.
```

Rationale: if fastmcp later allows mcp 2.x, an unbounded floor here would let the resolver silently jump majors under Maestro's own imports' feet; with the ceiling, that day produces a loud resolution conflict instead — the correct signal to run the (then-scoped) migration.

- [ ] **Step 2: Record the deferred migration trigger in TODO.md**

Add under the appropriate section:

```markdown
- [ ] mcp SDK v2: blocked on upstream — fastmcp (≤3.4.5) pins mcp<2.0.
      @trigger: fastmcp release notes announce mcp>=2 support.
      Then: lift both pins together, re-run test_mcp_server.py, and check the
      fastmcp 3→v2-based changelog for Client/transport API changes.
      Context: prograph-vault/authored/notes/2026-08-04-mcp-v2-migration-plan.md
```

- [ ] **Step 3: Re-lock, test, PR; process Copilot review**

```bash
uv sync
uv run pytest tests/test_mcp_server.py -v && uv run pytest -v -m "not slow"
git add pyproject.toml uv.lock TODO.md
git commit -m "chore: cap mcp<2 (mirror fastmcp's ceiling); record SDK-v2 trigger"
git push -u origin chore/mcp-v2-ceiling && gh pr create --fill
```

---

## Phase 5 — atp-platform: ceiling guard + CVE floor for atp-dashboard (repo: `atp-platform/`)

Mirror of Phase 4: atp-dashboard's MCP server is built on standalone `fastmcp`, which pins `mcp<2.0`, so it is not broken today and cannot migrate until fastmcp does. Unlike Maestro, atp-dashboard has **no direct `mcp` specifier at all** — meaning no CVE-2026-59950/-52869/-52870 floor either. One pin fixes both.

### Task 5.1: Add the mcp floor+ceiling to atp-dashboard and record the trigger

**Files:**
- Modify: `atp-platform/packages/atp-dashboard/pyproject.toml` (dependencies)
- Modify: `atp-platform/TODO.md` (add a trigger item)

- [ ] **Step 1: Add the direct specifier next to fastmcp**

In `packages/atp-dashboard/pyproject.toml` dependencies, after `"fastmcp>=3.0",` add:

```toml
    # Direct floor+ceiling for the transitive `mcp` SDK: >=1.28.1 is the
    # patched version for CVE-2026-59950 / -52869 / -52870; <2 mirrors
    # fastmcp's own ceiling (fastmcp<=3.4.5 requires mcp<2.0). Lift both
    # together when fastmcp ships SDK-v2 support.
    "mcp>=1.28.1,<2",
```

- [ ] **Step 2: Record the deferred migration trigger in TODO.md**

```markdown
- [ ] mcp SDK v2 (atp-dashboard): blocked on upstream — fastmcp (≤3.4.5) pins mcp<2.0.
      @trigger: fastmcp release notes announce mcp>=2 support.
      Then: lift the pins, migrate scripts/repro_mcp_concurrent_tools_list.py and
      participant-kit-el-farol-en/bot_el_farol_random.py off the v1 client API
      (ClientSession/sse_client → v2 Client), re-run tests/unit/dashboard/mcp/.
      Context: prograph-vault/authored/notes/2026-08-04-mcp-v2-migration-plan.md
```

- [ ] **Step 3: Re-lock, run the dashboard MCP tests, PR; process Copilot review**

```bash
uv sync
uv run pytest tests/unit/dashboard/mcp/ -v
git add packages/atp-dashboard/pyproject.toml uv.lock TODO.md
git commit -m "chore(atp-dashboard): floor+cap transitive mcp (CVE floor; mirror fastmcp's <2 ceiling)"
git push -u origin chore/mcp-v2-ceiling && gh pr create --fill
```

(atp-adapters' MCPAdapter needs nothing: its transport is hand-rolled asyncio/httpx JSON-RPC with no SDK dependency.)

---

## Out of scope (deliberately)

- **arbiter** — will not break, three ways: (1) its MCP server is hand-rolled Rust (JSON-RPC 2.0 over stdio in `arbiter-mcp`; no `rmcp`, no Python SDK); (2) its only in-ecosystem client — Maestro's vendored `coordination/arbiter_client.py` — is likewise hand-rolled JSON-RPC over subprocess stdio ("Do NOT modify: subprocess lifecycle, reconnect logic, stdio line framing"), so no SDK release can reach it; (3) arbiter has no Python `mcp` imports or specifier anywhere. SDK migration doesn't apply. Separate future track if desired: conformance with the 2026-07-28 *protocol* revision, which drops the initialize handshake — v2-era clients still speak earlier revisions, so nothing is broken today.
- **dispatcher, steward, deployer, libretto, research-bench** — no `mcp` dependency and no mcp/fastmcp imports (inventory above; atp-platform was initially mislisted here — corrected, see Phase 5).
- prograph fixture modernization (adding a v2-idiom `MCPServer` fixture project to the detector corpus) — nice-to-have, not required: detection is idiom-based and already covers v2 style. Open as a prograph inbox issue only if detector coverage for v2-specific idioms is ever questioned.

## Execution amendments (2026-08-04, post-implementation)

The plan above is kept as written; execution deviated in these ways (the code, not the plan text, is authoritative):

- **Phase 2 / Task 2.1–2.2 — pre-dispatch validation restored.** Implementation discovered that v2's lowlevel `Server` also dropped v1's SDK-side pre-dispatch inputSchema validation, which three prograph integration tests pin as wire contract (plain-text message, `is_error=True`). The Task 2.1 `build_server` block above is therefore incomplete: the landed version additionally builds a per-tool validator map (explicit `jsonschema.Draft202012Validator`) and validates `params.arguments` before `_dispatch`, returning plain-text `is_error=True` on failure; `jsonschema>=4.26.0` became a **runtime** dependency. Unknown-tool and dispatch-exception branches keep the JSON `{"error": ...}` / `is_error=False` behaviour. v1's own validation was jsonschema-based (both mcp 1.28.1 and 2.0.0 depend on jsonschema), so this reproduces the old wire messages exactly.
- **Task 2.2 — "every assertion untouched" was inexact:** three assertions were renamed `isError` → `is_error` (v2 spelling), and the final review added explicit `is_error is False` pins (the plan's claim that `test_mcp_unknown_tool_returns_error` pinned `is_error=False` was false — it only checked the JSON payload; now an assert pins it).
- **Task 2.3 — the CLAUDE.md bullet** as landed carries an extra sentence documenting the app-side validation restoration.
- **Tasks 0.1 / 1.2 (spec-runner) — plan defect: no CHANGELOG steps.** The repo treats version bumps as release commits; CHANGELOG sections for 2.11.1 and 2.12.0 were added in the final-review fix wave. Merge sequencing (#75 then tag/publish v2.11.1 before merging #76, vs folding) is an explicit human decision recorded in the SDD ledger.
- **Task 1.1 — TYPE_CHECKING guard added** alongside `__getattr__` (pyrefly `bad-dunder-all` otherwise).
- **Phase-1 PR (#76) opened stacked** with base `fix/mcp-v2-ceiling-pin`, not master, to keep the diff Phase-1-only; retarget after #75 merges.

## Self-review notes

- Every repo with an `mcp` specifier line has exactly one phase; repos without one are listed in "Out of scope" with the reason.
- The one uncertain API detail is the exact in-memory `Client(server)` construction in Task 1.2 Step 1 — the v2 docs' "Testing utilities" section is the authority if the constructor call needs adjustment; the rest of the task does not depend on it (the stdio path is exercised by prograph's tests).
- Wire-behaviour preservation in prograph (errors as JSON payload with `is_error=False`) is pinned by an existing test and called out explicitly so a reviewer doesn't "fix" it into `is_error=True`.
