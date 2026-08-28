---
title: steward — activity journal
type: journal
source: kb-save
project: steward
updated: 2026-08-28
---

# steward — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-12 08:53 — change: WS-006 risk model + mandatory gates — design spec drafted (RD-004)

- Drafted the design-stage spec bundle for WS-006 (risk model as policy layer over
  profiles/gate-check + gates-in-DAG skeleton evaluated for Maestro project.yaml) and opened
  it as draft PR #5 (branch spec/ws-006-risk-model). Deliverable of contracts-roadmap RD-004;
  design only, M1 implementation blocked on design approval.
- Key decisions: profile=floor / risk=escalation-only (monotone max, no weights); 3 computable
  inputs (change_class path-rules fail-closed, blast_radius consumer-registry, trust_boundary);
  two-phase tier ex-ante(declared scope)/ex-post(diff) with scope-violation escalation;
  verdict pass/fail/waived/error with missing/error=fail on mandatory at every tier;
  verdict-record as evidence_ref (RD-003); SHA-bound verdicts/waivers; waiver-as-file via PR,
  forbidden on critical. Numbered WS-006 — WS-003..005 taken by spec/40-decomposition.md.
- Links: steward/workstreams/WS-006-risk-model/spec/{requirements,design,tasks}.md,
  steward/workstreams/WS-006-risk-model/risk-model.example.yaml,
  https://github.com/andrei-shtanakov/steward/pull/5

## 2026-07-12 09:00 — status: WS-006 design merged (PR #5 -> master 04accdd)

- Design-stage spec bundle merged by owner; RD-004 design deliverable done. M1
  (risk-classify implementation) stays blocked on OQ-1..4 decisions.
- Follow-ups executed: Maestro handoff note + RD-004 evidence_rules (vault PR).
- Links: authored/notes/2026-07-12-ws006-gates-maestro-handoff.md,
  authored/roadmaps/contracts-v1.yaml (RD-004)

## 2026-07-12 10:00 — result: WS-006 M1 shipped; RD-004 verified

- M1 core merged (PR #7, master d6cd1a3): profiles/risk-model.yaml (canonical),
  riskclassify/{model,classify,cli}.py, `steward risk-classify` CLI. Copilot
  found a real bug (reversed glob-intersection args for '**' scopes) — fixed
  with regression tests; load-time cross-ref validation + CLI type validation
  added. RD-004 flipped implemented -> verified on the dashboard (both
  evidence rules pass).
- TASK-607 waivers shipped as PR #8 (pending review/merge): waivers.py +
  `steward waivers-check`, SHA-bound, critical forbidden (OQ-3); waiver
  frontmatter carries `tier` (documented deviation). WS-006 M1 complete.
- Links: steward/src/steward/riskclassify/, steward/profiles/risk-model.yaml,
  https://github.com/andrei-shtanakov/steward/pull/8

## 2026-07-12 10:09 — status: WS-006 M1 complete (PR #8 merged, master dd8cbe6)

- Waivers merged after Copilot review round (2 valid findings fixed: accurate
  strict-mode parse message; full 40-hex SHA validation in waiver files and
  waivers-check --sha). Suite 118 passed on master.
- WS-006 closed end-to-end: TASK-601..607 done. RD-004 verified on the
  dashboard. steward side of the risk model is finished; remaining work is
  Maestro-side (handoff M-1..M-4).

## 2026-07-15 15:57 — change: C2 steward-side done — upstream_hashes + stale-cascade gate (PR #14)

- Frontmatter schema (REQ-002) extended with `upstream_hashes: {upstream node id -> git
  blob hash}`, stamped into a downstream artifact at approval; parsed into ArtifactMeta
  (steward/src/steward/meta.py). Stale-cascade gate REQ-206/DESIGN-207 implemented:
  gatecheck GC-STALE error on pin mismatch, GC-STALE-UNPINNED / GC-STALE-KEY warns
  (steward/src/steward/gatecheck/checks.py::check_stale_cascade). Suite 156 passed;
  dogfood gate-check clean. PR #14 open, awaiting review/merge.
- spec-runner half of C2 (owner_role + human approver in SpecMeta, SPEC_META_CONTRACT v2)
  handed off — steward re-vendors after upstream ships; _vendor copy stays at v1.
- Merged-branch cleanup on origin (feat/gov3-risk-model-atp-coverage,
  agent/add-governed-run-logs-20260714 deleted).
- Links: steward PR #14; authored/notes/2026-07-15-spec-runner-specmeta-v2-handoff.md;
  steward/NEXT-STEPS.md (C2/C3), steward/spec/20-design.md (REQ-002).

## 2026-07-15 16:39 — change: C5 compile-down emitters done — steward-compile (PR #15)

- New `steward-compile` CLI (steward/src/steward/compile/): `project-yaml` renders Maestro
  project.yaml and `delegation` renders the WS→spec-runner authoring manifest, both from a
  normalized `yaml steward-compile` fenced block inside the decomposition artifact
  (steward/spec/40-decomposition.md). Maestro deployment knobs pass through verbatim from
  steward/spec/maestro-base.yaml; priorities derive from DAG depth unless pinned.
- gate-check gained GC-COMPILE (checks.py::check_compile_block): dep-link integrity of the
  block upstream of compilation — closes the verified trap that Maestro `validate --no-fs`
  silently accepts a dangling depends_on (steward/emitter-contract-check.md).
- Root steward/project.yaml is now emitter-generated (values identical to the hand-compiled
  contract artifact) and pinned byte-equal by golden tests (steward/tests/contract/).
  Suite 190 passed; dogfood gate-check clean. PR #15 open, awaiting review/merge.
- Links: steward PR #15; steward/NEXT-STEPS.md (C5 ✅); steward/spec/20-design.md
  (compile-down interfaces).

## 2026-07-15 16:50 — status: C4/I1 verified already closed in Maestro; no handoff needed (PR #16)

- Verified read-only against Maestro (2026-07-15): C4 done there 2026-07-06 (PR #46 + #50 —
  decomposer delegates spec generation to `spec-runner plan --full`, no built-in tasks.md
  prompt copy) and I1 fixed 2026-07-06 (PR #47 — preflight `dangling-dep` error, runs in
  `validate --no-fs` too). The planned Maestro handoff was therefore stale; skipped.
- steward PR #16 un-stales the docs: NEXT-STEPS C4/I1 ✅, CLAUDE.md trap note now historical,
  emitter-contract-check.md addendum (finding closed on both sides). GC-COMPILE kept as
  defense-in-depth at the governance layer.
- Links: steward PR #16; Maestro PRs #46, #47, #50; steward/emitter-contract-check.md.

## 2026-08-09 — V1 live gated run: PASS, authoring seams measured (steward PR #58)

- V1 (steward TODO §4, `@id:v1-live-gated-run`) executed 2026-08-08/09 per the
  owner-approved design: real task = gate-break-glass-path runbook; profile `lite`
  both sides; spec-runner pinned at a fresh clean clone of tag v2.21.0 (`13e7667b`),
  steward @ `c2414f7`, claude CLI 2.1.226 / sonnet. Canonical evidence:
  steward/docs/evidence/2026-08-08-v1-live-run/ (manifest with pins, steps.md with
  verbatim commands + exits + per-step classification, emitted gate_verdicts.jsonl).
- Result: **PASS**. Negative slices: pre-commit gate-check → expected GC-GIT-BRANCH;
  pre-approval `run --strict` → correct refusal but exit 0 (spec-runner defect,
  recorded not worked around). Positive: 12/12 tasks (branch→tests→review→merge);
  the deliverable's verify_break_glass.sh passed against live steward (valid
  SHA-bound waiver accepted; stale-SHA and critical-tier waivers rejected
  fail-closed, messages distinguishable). Final gate: 0 err / 3 warn, correlation
  held (gate_id ⊆ catalog active, owner_roles ⊆ roles.yaml via profile side,
  identity ↔ bundle, source_commit == HEAD, dirty=false).
- Measured seams (deliberately not fixed pre-run): stage `tasks` vs lite node
  `task` (pre-registered hypothesis, confirmed — tasks.md verdicts carry
  node_id null / owner_roles []); gated approve writes no traces_to; pins no
  upstream_hashes. New steward TODO item `authoring-seam-ruling` (owner decision).
- Side discovery: SPEC_META_CONTRACT = 2 shipped in spec-runner v2.21.0 with
  first-class owner_role — steward §2 re-vendor trigger fired, items unblocked.
- Links: steward PR #58 (merged `4c41ef4`); steward/docs/evidence/2026-08-08-v1-live-run/;
  spec-runner inbox issue with run frictions (filed alongside this entry).

## 2026-08-27 21:10 — decision: приём inbox #126/#127, #124 с понижением (PR #128)

- Приняты в TODO.md три inbox-запроса: #126 → `review-dedup-diff-hash` (§10a, дедуп ревью по sha256-отпечатку входа; @trigger — эксперимент после закрепления терминального дефолта vault#106), #127 → `review-lens-test-tampering` (§10a, линза ослабления тестов в review-prompt.md, размер S), #124 → `review-kit-ceiling-vs-actions-outage` (§10, **принят с понижением** до док-абзаца: потолок timeout-minutes — не гарантия во время аварии Actions; выбор «понизить, не отказать» — урок измерен боевым днём dispatcher 2026-08-26, цена — абзац README).
- Слаги совпадают с телами issues — правка slug: не потребовалась; вывод принятия у make inbox работает (is_accepted матчит по raw-тексту айтема, включая continuation-строки — проверено по devtools/inbox.py).
- Терминальный цикл нового дефолта пройден целиком: local.sh чисто → драфт → review-pr.sh --dry-run → публикация approve от ai-prosto → ready. Мерж за владельцем.
- Links: steward TODO.md §10a/§10, steward PR #128, issues steward#126/#127/#124

## 2026-08-27 21:55 — change: реализация review-lens-test-tampering + ceiling-outage (PR #129)

- Реализованы два принятых пункта батчем (одна волна синка): линза ослабления тестов в §4 review-prompt.md (#127) и абзац «потолок ≠ гарантия в аварию Actions» к доводу timeout-minutes в codex-review.yml (#124). #126 (дедуп) не тронут — держит @trigger.
- Линза потребовала 4 итерации гейта, все находки валидны и о самосогласованности промпта: (1) противоречие §3 — определено, как файл/строка/вход/результат применяются к утрате покрытия; (2) чистое удаление невыразимо в схеме — конвенция «строка ближайшего контекста, line: 0 для удалённого файла», схема не менялась; (3) безусловная линза блокировала бы удаление тестов вместе с функциональностью — скоуп «охраняемое поведение остаётся в дереве»; (4) major по определению §4 не включал утрату покрытия — определение расширено.
- Зафиксирован недетерминизм ревьюера: dry-run на head d541e86 дал approve, боевой прогон на ТОМ ЖЕ head — request-changes (итерация 4 и была его находкой). Прямое свидетельство в пользу review-dedup-diff-hash (#126): дедуп по отпечатку унаследовал бы вердикт вместо второго платного прогона. Также один прогон review-pr.sh завис >10 мин без вердикта (норма 1–4) и был убит — в норму вернулся ретрай.
- Links: steward PR #129, .github/codex/review-prompt.md §4, .github/workflows/codex-review.yml (довод потолка), issues steward#127/#124/#126

## 2026-08-28 — change: эксперимент #126 запущен — кит-половина дедупа ревью влита (PR #132, #133)

- Триггер review-dedup-diff-hash сработал (владелец), дизайн утверждён с поправками: оффлайн-гарантия явная, framed-хеширование с версией протокола codex-terminal-review-fingerprint-v1, наследование только из строго распарсенного ревью, пустой дифф — исход без отпечатка, --fresh в review-pr.sh.
- PR #132 (влит): `local.sh --fingerprint-only` — 12 TDD-тестов красными до кода; собственный гейт нашёл два валидных minor жанра fail-honest (порог-каталог сквозь -r + пайплайн, глотающий cat; битый вывод хешера с кодом 0) — оба закрыты через красный тест. Итог: 1182 passed.
- PR #133 (влит): ожидание интеграции — @blocked_by:todo://devtools/review-pr-fp-inherit (devtools#72, контракт из 7 пунктов). Находка гейта: теги читаются ТОЛЬКО с физической строки чекбокса (devtools#57) — @blocked_by перенесён на неё; иначе невидимое ожидание.
- Побочно вскрыто прогоном check-plan-fields: 19 унаследованных DT-TAG-ON-CONTINUATION в §10a TODO.md (теги роадмапа 2026-08-23 невидимы Robin) + 1 PF-BLOCKER-STALE (TODO.md:178, dispatcher закрыл gate-verdicts-v1-prev-hash-revendor). Ждут решения владельца.
- Links: steward PR #132/#133, scripts/review/local.sh (--fingerprint-only), devtools#72, issues steward#126
