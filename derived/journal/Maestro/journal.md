---
title: Maestro — activity journal
type: journal
source: kb-save
project: Maestro
updated: 2026-07-12
---

# Maestro — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 11:44 — change: WS-006 handoff M-1..M-4 implemented (PRs #72, #73)

- M-4 (PR #72, CI green, review addressed): EvidenceRef kind=gate-verdict —
  pipeline_id+gate_id+sha, pre-adoption additive; null-hole in ALL kinds'
  allOf branches closed (Copilot finding); inline WorkCorrelation copy synced.
- M-1..M-3 (PR #73, pending review): opt-in gates: config; ex-ante/ex-post
  guards shelling to steward risk-classify; fail-closed; NEEDS_REVIEW routing
  with SHA-bound operator-approval marker; verdict-records JSONL in
  logs/<ULID>/; advisory channel for host-enforced gates; READY->NEEDS_REVIEW
  edge added to workstream state machine; preflight gates-* checks.
- Links: maestro/gates.py, contracts/observability/evidence-ref.schema.json,
  https://github.com/andrei-shtanakov/Maestro/pull/72,
  https://github.com/andrei-shtanakov/Maestro/pull/73

## 2026-07-12 12:33 — result: gates live e2e passed (real steward x real GateKeeper)

- Both handoff PRs merged (#72, #73 -> master eedd7bf). Live e2e on real
  components: allow (docs scope) -> block (contracts scope, ecosystem-contract
  /critical via consumer registry) -> operator re-queue approval -> SHA
  invalidation on new commit -> ex-post scope_violation block. 25 verdict
  records in gate_verdicts.jsonl, every one round-trips into EvidenceRef
  kind=gate-verdict (schema-validated). maestro validate catches
  gates-steward-missing live.
- Observed: ex-ante docs/** classifies medium (unknown), not low — per-repo
  Maestro section of risk-model.yaml lacks a docs rule and name-based generic
  rules are excluded from ex-ante by design. Candidate data tweak in steward.

## 2026-07-12 20:04 — result: first governed orchestrate run — gates blocked correctly, 5 findings

- Live run (steward risk-model task, scope profiles/** = high): ex-ante block ->
  operator approval -> spawn -> ex-post scope_violation block. Gates caught an
  EMPTY implementation (spec-runner rc=0 on "No tasks found"). Task shipped as
  steward #10 instead. Findings H-1..H-5 in
  authored/notes/2026-07-12-governed-run-findings.md (spec-runner exit-0 bug,
  plan<->run task-format drift, approval-marker overwrite, orchestrator
  spec-commits vs scope gate, missing requeue CLI).

## 2026-07-12 23:05 — result: governed run #2 — first agent-authored change through the gates (steward PR #11)

- Arc: plan fail (H-2 honest exit) -> H-2b fix -> workstream-approve (H-5
  debut) -> agent implemented docs/risk-classify.md BUT touched
  .gitignore+tests outside docs/** -> ex-post scope_violation block (real
  agent violation caught live) -> operator curation (out-of-scope stripped;
  root cause H-7: orchestrator spec/ collides with steward's dogfood spec/)
  -> final ex-post: tier low, no flags (the docs rule from run #1 classifies
  it) -> branch pushed + PR operator-side (process was stopped mid-resume).
- New findings: H-6 (resume-after-ex-post-approval respawns from DECOMPOSING,
  regen mints a new sha and invalidates the approval — needs pipeline-position
  preservation or idempotent spec regen), H-7 (spec/ dir collision).
- Links: https://github.com/andrei-shtanakov/steward/pull/11

## 2026-08-06 10:22 — change: волна 2 inbox (#137 принят) + notify PR_CREATED shipped

- Принят inbox #137 `expost-approver-cmd` (PR #138, merge c2d1cf7), design-first; зафиксирована scope-граница: approver_cmd работает ДО создания PR, spec-runner#102 — соседний механизм на более поздней lifecycle-границе.
- Утверждён порядок трека «нотификации и post-PR» (6 шагов, TODO.md секция «Нотификации и post-PR»): notify PR_CREATED → webhook → spec-runner#102 → #137 decision hook → post_pr_command → service install design.
- Шаг 1 реализован (PR #139, merge 085c13a): WORKSTREAM_PR_CREATED notification, URL как структурированный payload перехода, декларативный гейт notification_requires_url (пустой URL = отсутствие, Copilot catch).
- Links: maestro/transitions.py, maestro/notifications/base.py, TODO.md

## 2026-08-06 12:38 — change: webhook-канал нотификаций shipped (PR #141)

- Шаг 2 notify-трека: generic webhook (конверт maestro.notification/v1, event_id ULID стабилен через retry + Idempotency-Key, per-event allowlist — message не форвардится). Managed bounded queue + worker, drain с дедлайном в shutdown обоих CLI-путей; retry 408/429/5xx/transport в wall-clock бюджете, redirects off.
- Security-находка: httpx логирует полный URL на INFO — закрыто per-instance logging-фильтром на httpx/httpcore; URL/тела ответов в логи не попадают.
- Семантика зафиксирована: at-least-once (живой процесс + graceful shutdown), best-effort через hard crash; durable outbox — follow-up за тем же швом. telegram-поля deprecated; httpx — прямая зависимость. Merge ee4127e.
- Links: maestro/notifications/webhook.py, README.md (секция Notifications), CHANGELOG.md

## 2026-08-06 14:28 — decision: дизайн approver_cmd (#137) одобрен и смержен (PR #143)

- Спека прошла 4 ревизии владельца. Форма: хук = автоматизированный оператор поверх существующего approve-API (gate_approvals — единственная власть), не новый гейт.
- Ключевые решения ревизий: observations ≠ evaluation attempts (kill-switch обратим); persist-at-block gate_block_contexts для restart-триггера; post-verdict cost authority check + stale-SHA recheck + CAS; bounded stdout/stderr; механический allowlist убран из v1; maestro.gate-verdict-record/v1 явно отделён от steward contracts/gate-verdicts/v1.
- Реализация — отдельным PR (миграция 20: actor/approval_run_id + две новые таблицы). Merge b41703b.
- Links: docs/superpowers/specs/2026-08-06-expost-approver-cmd-design.md, maestro/gates.py, maestro/gate_approvals.py

## 2026-08-06 15:49 — result: approver_cmd (#137) реализован и смержен — волна 2 inbox закрыта

- PR #145 (merge 280c74e): maestro/approver.py (контракт v1 + bounded-раннер), миграция 20 (gate_approver_runs, gate_block_contexts, actor в gate_approvals), обвязка оркестратора по спеке rev.4 — guards-как-observations, sentinel до create_task, PASS через cost-check → rechecks → CAS, drain на shutdown. 66 новых тестов.
- Полный цикл #137: принятие #138 → дизайн #143 (4 ревизии владельца) → имплементация #145; issue закрыта.
- Волна 2 целиком: notify PR_CREATED (#139), webhook-канал (#141), approver_cmd (#143+#145). Открытые хвосты трека: post_pr_command (ждёт spec-runner#102), дизайн service install (после стабилизации автономных операций).
- Links: maestro/approver.py, docs/superpowers/specs/2026-08-06-expost-approver-cmd-design.md, docs/superpowers/plans/2026-08-06-approver-cmd.md

## 2026-08-06 17:58 — decision: дизайн `maestro review-pr` одобрен (PR #147), реализация ждёт spec-runner#116

- spec-runner#102 закрыт апстримом (M1–M3, v2.18–2.20) — разблокировал шаг 5 нашего notify/post-PR трека.
- Форма изменилась после разведки: не хук на границе PR_CREATED, а отдельная команда `maestro review-pr` — потому что resumable-state spec-runner лежит в state_file ВНУТРИ checkout. Отсюда: durable state вне worktree, retention незавершённой работы, Maestro-owned push-recovery (spec-runner требует строгого local_head == remote head_sha), per-PR flock, immutable-after-finalization аудит (миграция 21).
- v1 честно объявлен advisory/post-delivery cleanup: review-фиксы двигают PR head, а не уже влитую локальную base — не гарантия корректности DAG.
- Заведена парная issue spec-runner#116 (`--json` purity) — блокер реализации; версия будет запинена preflight-гейтом. Merge 458039c, 3 ревизии владельца.
- Links: docs/superpowers/specs/2026-08-06-post-pr-review-command-design.md, TODO.md (@blocked_by)

## 2026-08-06 19:22 — result: `maestro review-pr` отгружен (PR #149) — notify/post-PR трек закрыт 5/6

- spec-runner#116 закрыт апстримом (v2.21.0, payload получил exit_code) → блокер снят, реализация выполнена в тот же день.
- Команда `maestro review-pr <config> <ws>|--all|--gc`: миграция 21 (post_pr_review_runs, immutable-after-finalization + CAS), durable state вне checkout, push-recovery (ls-remote проверка + обычный fast-forward push — force убран совсем после ревью), per-PR flock (exit 3 без строки прогона), retention по exit-коду, --gc только после подтверждённого closed/merged, version-gate >= 2.21.0, 3 notification-события. 74 теста.
- Copilot нашёл два настоящих дефекта: KeyError мимо fail-closed контура в fetch_pr_meta и detached-HEAD воркспейс там, где fix-путь spec-runner требует ветку.
- Трек «нотификации и post-PR» закрыт на 5 из 6 шагов; остался дизайн service install (P3). Merge fea2992.
- Links: maestro/review_pr.py, maestro/review_workspace.py, maestro/review_runner.py, docs/superpowers/specs/2026-08-06-post-pr-review-command-design.md

## 2026-08-07 07:37 — result: `maestro service` отгружен (PR #154) — трек notify/post-PR закрыт 6/6

- Шаг 6: планировщик запускает обёртку `maestro service run`, а не `orchestrate` — решение resume/fresh/no-op принимает Maestro по состоянию БД. Две независимые стадии (--stage orchestrate|review) со своими локами, леджером и логами.
- Двухуровневая иерархия flock по решению владельца: legacy — global exclusive, scoped — global shared + exclusive <stage>.lock; взаимное исключение в обе стороны. Разведка вскрыла, что существующий pid-lock был глобальным (один Maestro на машину).
- Миграция 22 (service_ticks: stage + раздельные decision/outcome, sentinel+CAS), консервативный sweep worktree, install-preflight с отказом при нерезолвимых бинарниках/креденшлах, дедуп нотификаций review-pr. ~93 теста. Merge 5df61bc.
- Трек целиком: #139 notify PR_CREATED → #141 webhook → spec-runner#102 → #145 approver_cmd → #149 review-pr → #154 service.
- Links: maestro/service/, docs/superpowers/specs/2026-08-06-service-install-design.md

## 2026-08-08 14:55 — decision: принят inbox #160 gate-catalog-for-ws006 (steward gate-id catalog)

- Принят кросс-репный запрос steward (maestro#160, от steward#gate-id-catalog): привести
  писатель `gate_verdicts.jsonl` к каноническим gate_id из `steward/profiles/gate-catalog.yaml`
  (v1) и завендорить пиненую копию каталога. Пункт заведён в TODO.md
  (@id:gate-catalog-for-ws006), PR maestro#161.
- В issue отправлены уточнения состояния потребителя: триггер «старт WS-006 M-1» уже сработал
  (писатель живёт с gates v1.0–1.3 как `maestro.gate-verdict-record/v1`, maestro/gates.py);
  steward-схема contracts/gate-verdicts/v1 в maestro НЕ вендорена; словари obligation расходятся
  по осям — maestro `mandatory|advisory` (enforcement) vs каталог `quality|approval` (интент).
- Открытый вопрос к steward: маппинг словарей (предложено: два поля, а не замена) и судьба
  producer-специфичных id (`steward.risk_classify_*`, `human.owner_approval`,
  `maestro.validate_strict`) вне GC-*. Реализация блокирована на ответ.
- Links: maestro/TODO.md (@id:gate-catalog-for-ws006), maestro#160, maestro PR #161,
  maestro/gates.py:81, steward/profiles/gate-catalog.yaml, ADR-ECO-006
