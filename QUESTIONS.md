# QUESTIONS.md — Robin implementation log

Every clarifying question the implementer must ask is a **spec bug for upstreaming**. Do
NOT patch `ROBIN-SPEC.local.md` to answer these — log them here; the maintainer routes
them to the upstream spec (ROBIN-SPEC.md @ git b5ad49e).

## Findings from /robin-init (2026-07-07) — resolve before or during M0

1. **Config placement vs the KB constitution.** prograph-vault has a hard `authored/` vs
   `derived/` boundary (`CLAUDE.md` §3) and reserves the root for `index.md` + `CLAUDE.md`.
   Robin's files (`soul.md`, `robin/duties.md`, `ROBIN-SPEC.local.md`, `KICKOFF.md`,
   `QUESTIONS.md`) were placed at the KB root per the /robin-init convention. **Ratify with
   an ADR:** do these belong at root, under `authored/robin/`, or in a sibling repo?
   *Upstream candidate:* the spec assumes a plain Team OS repo, not one with its own
   authored/derived governance.

2. **No glossary file.** §4 says "Robin MUST check the repo's glossary," but prograph-vault
   has none — vocabulary lives across `product` docs, `authored/decisions/`, and the SSOT
   boundary table. Resolved for now: consult those and answer "not in the KB" when silent.
   *Upstream candidate:* clarify "glossary **or equivalent vocabulary source**."

3. **Timezone for cron triggers.** `robin/duties.md` uses `<TZ>`; §6.3 requires an explicit
   timezone. Set the ecosystem's working timezone (e.g. `Europe/Moscow`) before the
   scheduler reads the roster. **Resolved 2026-07-10: `Asia/Tbilisi`** (maintainer decision) —
   duties.md updated, `ROBIN_TZ=Asia/Tbilisi` in robin.env, explicit zone in systemd
   `OnCalendar` (robin-runtime PR).

4. **Digest persistence target.** Robin MUST NOT write the KB (§4), yet the KB already has a
   tool-owned `derived/digests/` pipeline. Resolved: Robin's digests persist to Robin's own
   learnings store; a human/tool may copy notable ones into the KB. Confirm this is the
   intended split.

5. **AI-news digest takeover.** Identify what currently generates `derived/digests/ai/`
   (Russian "AI Дайджест") and retire it once the Robin duty runs, so there is one
   scheduler of record. Confirm the intended destination (team channel vs current target).

6. **Chat identity registry + passive-capture scope (slots 7, 8).** The team Telegram
   channel/`chat_id` and the passively-logged channel(s) are TBD — set via `/telegram:access`
   at deploy, and disclose logged channels to the team (§6.5).

7. **Duty output language.** The "answer in the asker's language" rule (§4) covers Q&A. Duty
   *output* language is unspecified: KB is English, the existing AI-news digest is Russian,
   the owner writes Russian. Decide per duty (proposed: ecosystem/integration digests EN,
   AI-news digest RU to match the existing pipeline).

## Findings from the M0 tool-layer dry-run (2026-07-07)

8. **Retrieval ranks Robin's own scaffolding above the authoritative source.** A naive literal
   KB search for `agents-catalog.toml` returns `KICKOFF.md` and `ROBIN-SPEC.local.md` (Robin's
   own generated files, which quote the answer) *above* the authoritative
   `authored/decisions/2026-07-01-adr-eco-003-agent-catalog.md`. The M1 grounding/answer layer
   MUST prefer authoritative sources (`authored/decisions/`, `authored/rules/`, producing-repo
   `spec/`) and SHOULD exclude Robin's own scaffolding (`KICKOFF.md`, `ROBIN-SPEC.local.md`,
   `soul.md`, `robin/`) from grounding — otherwise Robin cites itself.

9. **agents-catalog ADR has the same authority-in-`_cowork_output` tension as ADR #2.** The
   amendment (2026-07-03) names `atp-platform/method/agents-catalog.toml` as canonical, but the
   ADR body (lines ~90–93) still calls `_cowork_output/contracts/agents-catalog.toml` the
   "contract home" with repos vendoring pinned copies. Reconcile alongside
   `2026-07-07-adr-contract-authority-not-in-cowork.md` — the onboarding `answer_note` follows
   the amendment (the latest word), but the ADR should be made internally consistent.

## Incident log (production failures → spec/tooling bugs)

### 2026-07-09 — «какие сегодняшние изменения в проекте?»

- **Ответ Robin:** «изменений нет» (неверно: изменения были).
- **Причина 1 (tooling gap):** темпоральный запрос обслужен единственным
  инструментом — поиском по KB. Ответ на «что изменилось сегодня» не лежит
  в документах — он вычисляется из git-метаданных (log/status/mtime).
- **Причина 2 (spec bug, negative evidence):** ноль результатов поиска
  интерпретирован как «изменений нет». Нарушение правила «escalate "not in
  the KB" instead of hallucinating». Hardening «negative-evidence» из
  ROBIN-SPEC Appendix предвидел этот failure mode — не реализован.
- **Фикс:** инструмент recent_changes (обкатан: `devtools/recent_changes.py`,
  `make today`; предложение — devtools/proposals/2026-07-10-robin-self-improvement.md)
  + правило negative-evidence в промпт.
- **Eval-кейс:** «сегодняшние изменения» → ожидаемый класс ответа: temporal,
  источник git, либо честная эскалация.

## Implementer questions (append below)

<!-- Each clarifying question you must ask goes here, dated. Do not edit ROBIN-SPEC.local.md
     to answer it. -->
