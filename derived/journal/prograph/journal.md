---
title: prograph — activity journal
type: journal
source: kb-save
project: prograph
updated: 2026-08-16
---

# prograph — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-08-16 16:50 — change: export-md case-only rename fix (inbox #30 accepted, PR #32)

- Accepted inbox issue #30 (slug export-md-case-rename-loss, from devtools) into TODO.md.
- Root cause: on case-insensitive FS the exporter wrote projects/maestro.md into the
  on-disk Maestro.md entry, then the case-sensitive stale cleanup unlinked the fresh page
  (exit 0, counters intact). Fix: unlink-before-write for exact-case entries +
  (st_dev, st_ino) identity check in _cleanup_stale_project_mds; regression test
  test_export_md_survives_case_only_project_rename.
- Links: prograph/export/__init__.py, tests/integration/test_cli_export_md.py, TODO.md;
  PR https://github.com/andrei-shtanakov/prograph/pull/32 (merged 2026-08-16, closed #30).
