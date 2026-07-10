---
title: Robin — duty roster
type: note
status: living
owner: Andrei
updated: 2026-07-10
---

# Robin duty roster — AI-Orchestrators ecosystem

Robin's recurring work is declared here and changed by **PR under human review**, never by
config (ROBIN-SPEC §6.3). Each duty specifies trigger, inputs, output, destination, owner.
Machine-readable triggers only (cron with explicit TZ, or an explicit command/event).

> **TZ note:** crons below use `<TZ>` — set the ecosystem's working timezone (e.g.
> `Europe/Moscow`) before the scheduler reads this file.

> **Runtime source-of-truth:** Robin reads **prograph-vault** (persistent) and the ecosystem
> repos, all read-only. It MUST NOT read `_cowork_output/` at runtime (dev-scratch,
> ephemeral — the ecosystem's own rule: runtime never reads `_cowork_output`). Robin MUST
> NOT write the KB (§4); its own state lives in the runtime store, not here.

## Active

### 1. Employee/contributor onboarding — *first paid duty*
- **Trigger:** on-demand event — the maintainer registers a newcomer, or the newcomer sends
  `/onboard` in a DM. (Not cron; an explicit machine-readable invocation.)
- **Inputs:** prograph-vault (`CLAUDE.md`, `index.md`, `authored/rules/`,
  `authored/decisions/`, `authored/notes/`, `derived/contracts/`); the target repo's
  `CLAUDE.md` + `spec/`; the role checklist
  `authored/skills/onboarding/roles/<role>.yaml`.
- **Behavior:** guides the newcomer through the checklist step by step, answers each question
  **grounded in the KB with a citation**, marks steps done, and **escalates "not in the KB"
  instead of hallucinating** (§4). Progress state persists in the runtime SQLite store
  (`authored/skills/onboarding/progress-schema.sql`), never in the KB.
- **Output:** (a) the newcomer's onboarding progress; (b) a list of the newcomer's questions
  the KB could not answer → **KB-gap signal**, written as staged-learning candidates
  (read-back verified, §6.4).
- **Destination:** private DM with the newcomer; a KB-gap summary to the maintainer DM.
  PII is not written to the shared interaction log in the clear (§6.5).
- **Owner:** Andrei.
- **Implementation:** `authored/skills/onboarding/SKILL.md` (canonical; runtime consumes it
  as a thin pointer, §4/slot 22).
- **Why first:** closest to M0/M1 (grounded Q&A + a linear checklist), lowest risk, visible
  value — and every unanswered question is free KB-gap intel that feeds the later interview
  duties.

### 2. Ecosystem digest — *minimum roster (MUST, §6.3)*
- **Trigger:** `0 9 * * MON` (`<TZ>`) — weekly, Monday 09:00.
- **Inputs:** ecosystem-repo git since the previous digest; `authored/notes/status/*`;
  `derived/journal/*`; `derived/projects/*`.
- **Output:** what moved across the ecosystem since the last digest + open questions; collapse
  near-duplicates, report signal strength (which repos actually moved). Persisted to Robin's
  runtime store; "what did I miss this week?" is answerable from it.
- **Destination:** the team Telegram channel.
- **Owner:** Andrei.

### 3. Self-review — разбор провалов недели
- **Trigger:** `0 18 * * FRI` (`<TZ>`) — weekly, Friday 18:00.
- **Inputs:** stage-2 failure log `var/gaps.jsonl` (zero-retrieval, reformulation,
  `/gap`, 👎 — robin-runtime `gaps.py`) за неделю; `interactions.jsonl` для контекста;
  `QUESTIONS.md` (чтобы не дублировать уже заведённые находки).
- **Behavior:** кластеризовать провалы (класс вопроса × причина); для каждого кластера
  подготовить артефакт: KB-гэп → PR-кандидат в prograph-vault (staged-learning,
  read-back verified §6.4); инструментальный гэп → черновик спеки для spec-runner;
  неоднозначность формулировок → кандидаты в synonyms/rewrite-подсказки промпта
  (тоже PR). Кластеры без человека не становятся изменениями.
- **Output:** сводка «N провалов → M кластеров → K предложений» + ссылки на
  PR-кандидаты/спеки. Persisted в runtime store (`var/selfreview/`), не в KB.
- **Destination:** DM мейнтейнеру (`ROBIN_MAINTAINER_CHAT`); краткая сводка —
  в team-канал.
- **Инвариант:** Robin НЕ мержит и НЕ меняет себя сам — только предлагает
  (соответствует «acts only via PR» из ADR fleet-agent-role).
- **Owner:** Andrei.
- **Implementation:** robin-runtime `python -m robin.selfreview` (systemd timer
  `robin-selfreview.timer`); детекторы и лог — ступень 2 proposal
  `devtools/proposals/2026-07-10-robin-self-improvement.md`.
- **Closing the loop:** разобранные кейсы уходят eval-набором в atp-platform
  (ступень 4) и гейтят следующие изменения Robin.

## Planned (later phases — do not build before onboarding + M1 are proven)

### 4. Spec/ТЗ interview — *Phase 5*
- Generative interview that **generates questions from the actual repo `spec/` content** and
  scores answers **by comparison with a cited reference file**, never by model opinion. Output
  is a "knows / gap / diverges-from-spec" report with source citations — a **draft for a human**,
  not a final score (risk control, IMPLEMENTATION-PLAN §7.2). Reuses the onboarding
  grounded-Q&A + progress machinery.

### 5. Candidate interview — *Phase 6*
- Screening for role fit against requirements in the KB. **Destination follows sensitivity
  (§6.3):** private DM to the hiring maintainer, never a broadcast. Robin produces a
  structured fit summary **with sources, not a hire/no-hire verdict** — the decision stays
  human. Goes last: highest risk (people, privacy, legal), needs the §4 interview mechanics
  debugged first.

## Backlog (nice-to-have, not in the MVP path)

- **Integration-health / drift brief** — weekly flag of docs claiming an integration the code
  lacks (`authored/notes/integration-health.md` + `derived/contracts/*`).
- **AI-news digest** — adopt the existing `derived/digests/ai/` pipeline as a scheduled,
  logged, liveness-checked duty.

## Deferred (no evidence — do not build without it)

- **VoC / customer-voice** — no customer-signal source (internal tooling).
- **Meeting presence (M5)** — no meeting-recorder/transcription capture connected (§6.6).
- **Action-item tracker (Linear)** — considered, not adopted; low-cost add later.

<!-- Updated by /robin-init follow-up on 2026-07-07 (onboarding-first roster). Change by PR. -->
