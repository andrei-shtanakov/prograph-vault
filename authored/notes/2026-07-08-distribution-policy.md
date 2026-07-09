---
title: Distribution policy — what ships as PyPI / binary / container vs source-only
type: note
status: living
owner: Andrei
updated: 2026-07-08
---

# Distribution policy — PyPI / binary / container vs source

## Principle

**Distribution format follows the consumer and the boundary it crosses, not the producer's convenience.** And it is constrained by an existing decision: cross-repo contracts are **vendored as pinned copies** (arbiter-client in Maestro, `obs.py`, SpecMeta in steward, agents-catalog in arbiter — see root `CLAUDE.md`). Vendoring gives hermetic pins and no runtime coupling.

So publishing (PyPI/binary) is justified only when one of four conditions holds:

1. **External consumer** (not you, not your repos).
2. **Heavy toolchain** — packaging removes a build burden.
3. **It is an app people install and run** (end-user CLI / service).
4. **It is a service/daemon** → its "binary" is a container image.

For internal contract sharing the default stays **vendoring**, not PyPI.

## Recommendation by component

| Component | Consumer / boundary | Format | Why | When |
|---|---|---|---|---|
| **atp-platform SDK** | benchmark participants + Maestro | **PyPI** (already) | classic external-consumer case | keep |
| **spec-runner** | Maestro (subprocess) + external | **PyPI + console-script** (already) | stable contract, invoked as CLI | keep |
| **prograph** | you on any machine + agents (MCP) | **PyPI wheel (maturin manylinux)** | removes rustup on a new machine — the exact migration pain; `uvx prograph` | **high priority** |
| **Maestro** | human operator (top-level CLI) | **pipx / `uv tool install`** (console-script) | it is an entry point you install, not import | once CLI stabilizes |
| **arbiter** | Maestro spawns it as an MCP server | **standalone binary → GitHub Releases** | CI already builds linux-x64/macos-arm64; protocol version-negotiated | almost there — formalize releases |
| **proctor** | deployed as a distributed runtime | **OCI image(s)** | it is a service with Docker workers; its "binary" is a container | when Phase 3 stabilizes |
| **robin-runtime** | always-on service on a VPS | **container / systemd** (not a PyPI lib) | deployed, not imported; currently M0 | **too early** |
| dispatcher | local dev, reads sibling artifacts | **source** (pipx for the TUI at most) | workspace-coupled, narrow niche | source |
| steward / deployer | early governance / research-bench | **source** | moving fast; steward → pipx CLI later | source for now |
| robin-toolkit / sdd-framework / open-prose | methodology / spec / skills | **git bundle / plugin** | content, not a package; already shipped as skills | as-is |

## Top moves and traps

**Highest ROI — `prograph` as a PyPI wheel.** maturin builds manylinux wheels with the Rust extension pre-compiled, so `uvx prograph index` needs no Rust toolchain. Directly removes a chunk of the [[2026-07-08-migration-runbook]] pain (no rustup 1.85 on the new machine). It is also an MCP server for agents.

**arbiter — finish binary releases.** CI already builds binaries and it has protocol version-negotiation; only formal tagged GitHub Releases are missing. Its natural format: spawned as a process, not imported.

**Trap 1 — do not publish internal contracts.** Publishing arbiter-client / obs / SpecMeta as PyPI libs contradicts the vendoring decision. Keep them vendored. (Whether to replace vendored arbiter-client with a thin published client is a separate ADR change — do NOT do it lightly; vendoring gives a hermetic pin and arbiter is already a binary.)

**Trap 2 — timing.** Publishing costs semver discipline, release automation, changelog (ATP already built CHANGELOG enforcement). Publish the **stable** (atp SDK, spec-runner, prograph, Maestro); keep the **moving** in source (steward, robin-runtime, proctor Phase 3, deployer). Early publication of a moving project = constant breaking releases.

**Trap 3 — service ≠ library.** proctor and robin-runtime tempt a PyPI publish, but they are not imported — they are deployed. Their artifact is a container; a pip-lib makes no sense.

## Priority summary

1. **prograph → PyPI wheel** (now, high ROI).
2. **arbiter → formalize binary releases** (almost done).
3. **Maestro → pipx app** (once CLI freezes).
4. All internal-contract code → **stays vendored**.
5. Services (proctor / robin-runtime) → **containers, later**.
