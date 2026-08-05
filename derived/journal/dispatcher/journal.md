---
title: dispatcher — activity journal
type: journal
source: kb-save
project: dispatcher
updated: 2026-08-02
---

# dispatcher — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-08-02 19:07 — result: WS-005 governance-бандл закрыт насквозь (WS-B + WS-C за один день)

- Capability «достоверная read-only панель governance-бандла» доведена до конца:
  WS-A (steward PR #33, контракт gate-verdicts/v1 + emitter) → WS-B (dispatcher
  PR #107, inbox #106) → WS-C (dispatcher PR #109, inbox #108). Оба inbox-issue
  прошли полный цикл ADR-ECO-006 (принятие пунктом TODO.md → PR → ревью → мерж
  пользователем → закрытие issue со ссылкой на PR) и закрыты completed.
- WS-B: вендор канона steward @ 4836345 в contracts/steward-gate-verdicts/v1
  (одновходовый скрипт scripts/revendor_steward_gate_verdicts.sh + runbook
  docs/revendor-steward-gate-verdicts.md); две раздельные гарантии по правилу
  PR #99 — offline copy-integrity (tests/test_gate_verdicts_vendor.py, PR-гейт,
  не скипается) и scheduled drift-джоб (upstream-drift.yml, репортёр получил
  --canon-probe: канон steward без manifest.json, роль пробы — SCHEMA.json).
  Collector dispatcher/core/governance.py: классификация бандла в 6 состояний
  (no-data → unreadable → stale → unresolvable → blocked → pass, приоритет
  первого совпадения), fail-closed (NFR-02): нет файла → no-data через саму
  попытку чтения (без TOCTOU), любая ошибка чтения/парсинга и неизвестные
  git-факты — никогда не pass. ARCH-C1 (не импортирует steward) закреплён
  структурным тестом; ARCH-C3 — по построению (только классификация,
  единственный subprocess — локальный git).
- WS-C: GET /api/projects/{name}/governance через read_api-фасад (DESIGN-701);
  ARCH-C4 — панель потребляет только collect_governance; BEH-09/ARCH-C2 —
  route-enumeration тест (governance-поверхность только GET/HEAD). Веб-панель
  renderGovernance(): «✅» может появиться только у pass (M-01), блокер бандла
  читается с одного экрана (M-02), provenance из header (FR-05); 7 кейсов в
  Node-harness tests/web/governance_harness.js (вкл. XSS-экранирование).
  Сквозной smoke: scripts/install_pinned_steward.sh ставит настоящий gate-check
  на пине из вендоренного манифеста (второй копии пина нет), smoke детерминирован
  на пине (blocked: GC-TRACE-EMPTY + GC-STALE-UNPINNED); в CI рядом с пиненным
  github-checker, падает-не-скипается (дисциплина PR #98).
- Ревью: PR #107 — валидное замечание Copilot (вводящая в заблуждение причина
  «unsupported schema_version None») исправлено с регрессионным тестом, невалидное
  (мутабельные дефолты pydantic) отклонено с обоснованием; PR #109 — без замечаний.
  Полный сьют после мержа: 772 passed, 0 skipped.
- Links: dispatcher PR #107, #109; issues #106, #108; steward PR #33 @ 4836345;
  spec: steward/workstreams/WS-005-gate-verdicts/spec/; TODO.md
  @id:ws005-governance-collector, @id:ws005-governance-panel.
