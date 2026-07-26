---
title: libretto — activity journal
type: journal
source: kb-save
project: libretto
updated: 2026-07-16
---

# libretto — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.
>
> Note: the repo was renamed `open-prose` → `libretto` on 2026-07-16 (canonical name =
> clone directory name). Entries below predating the rename keep the historical name.

## 2026-07-16 15:38 — result: контракты open-prose получили первого внешнего потребителя (atp-platform)

- atp-platform вендорил пинованные копии `contracts/receipt.md` + `contracts/ir.md`
  (с corpus/битыми фикстурами), реализовал stdlib-верификатор ledger'ов
  (`atp/evaluators/openprose_receipts/`), четвёртый детерминированный checker
  `receipt_chain`, schema-валидацию в Grader и dispatch-owned `_case_dir` инъекцию;
  фича в main atp-platform. Это замыкает handoff Phase 5 (задача 5.4).
- Следствие для open-prose: `openprose.receipt.v1` / `openprose.compile-ir.v1`
  теперь load-bearing — append-frozen дисциплина версионирования (bump `v`,
  никаких переименований/переинтерпретаций) обязательна на практике, не на бумаге.
- Гейты НЕ триггерятся: Rust-гейт (потребление не latency-sensitive, язык Python —
  `docs/decisions/2026-07-16-rust-decision-gate.md`) и Phase 6 (потребляются
  bounded-run артефакты, не standing jobs —
  `docs/decisions/2026-07-16-phase6-responsibility-v2.md`) остаются в силе.
- Links: prograph-vault/authored/notes/2026-07-16-openprose-contracts-offer.md
  (status: accepted), open-prose/contracts/{receipt.md,ir.md}
