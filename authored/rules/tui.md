---
title: TUI rules (cross-cutting)
type: rule
status: accepted
owner: Andrei
updated: 2026-07-05
---

# TUI rules (cross-cutting)

> Applies to interactive terminal interfaces (dispatcher TUI, spec-runner watch/costs).
> Stack: **textual** (interactive) + **rich** (formatted output).

## Tool choice

- **Interactive TUI app** (panels, navigation, live updates) → **textual**.
- **One-off formatted output** (tables, statuses, progress in a CLI) → **rich**.
- Don't pull in textual for a simple table; don't build interactivity on bare rich.

## Architecture

- **Separate data and rendering.** The TUI is a thin layer over the **read-model** (like dispatcher:
  it reads on-disk artifacts, contains no business logic). Logic lives in the core/service, the TUI
  only displays.
- Keep screen state in the widget's model, not in globals.
- Updates — on event/polling of the read-model, without blocking the UI loop (anyio/async).

## Terminal and compatibility

- **Detect TTY:** `sys.stdout.isatty()`; on non-TTY / `--no-interactive` — degrade to
  plain output (spec-runner does exactly this in the gated flow).
- **Color:** respect `NO_COLOR`; account for CI forcing `FORCE_COLOR=1` (Rich ignores `NO_COLOR`
  for bold/dim — a known Maestro CI gotcha). In TUI tests set `TERM=dumb`.
- Do not tie output parsing to ANSI — for machine-readable output provide `--format json`.

## Tests

- Unit-test TUI logic (read-model → view-state) **without** a real terminal.
- Textual snapshot tests — where available; otherwise test the model, not the pixels.

## Enforcement

The TTY/color rule is a frequent regression; cover it with a test on the non-TTY path.
