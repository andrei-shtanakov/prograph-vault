---
title: robin-runtime — activity journal
type: journal
source: kb-save
project: robin-runtime
updated: 2026-07-09
---

# robin-runtime — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-09 19:50 — result: Robin live in production — text+voice Q&A over Telegram and web

- Robin (AI chief of staff, ROBIN-SPEC M0→M2) shipped from the M0 tool-layer
  slice to a production bot in one day: grounded Q&A with `path:line` citations,
  "what changed today/this week/period" answers from read-only git history over
  the ecosystem mirrors (`repo@sha` citations), daily + weekly digest duty,
  §7 cost caps (daily budget, per-user quota, /cost), §6.7 HTML escaping with
  logged-not-silent send failures, liveness alerts.
- Surfaces: Telegram bot **@robin_atp_bot** (DM, group @mentions and replies to
  the bot's own messages, voice notes) and a token-gated web chat at
  **https://pr0sto.net** (text + browser-mic voice). Voice is full duplex:
  whisper-1 STT in, gpt-4o-mini-tts spoken replies out (models env-pinnable via
  ROBIN_STT_MODEL / ROBIN_TTS_MODEL).
- Slot 2 re-resolved by maintainer decision: direct `anthropic` SDK (Messages
  API, adaptive thinking, cached system prompt, usage-priced cost) instead of
  the headless claude CLI — no Node on the VPS. Recorded in
  ROBIN-SPEC.local.md (prograph-vault@520962e), implemented in
  robin-runtime@caca477.
- Deployed to the always-on VPS (slot 3): /srv/robin with 8 read-only mirrors
  synced every 10 min by systemd timer, digest timers (daily 09:00, weekly Mon
  09:00 Asia/Tbilisi), hourly liveness, nginx + Let's Encrypt TLS.
  Acceptance: M0 (cited answer CLI), M1-web (RU answer with sources over
  /api/ask), M2 ("what did I miss today?" answered from today's commits),
  full voice roundtrip verified. 68 offline tests green.
- CI proposed (branch `feat/ci-deploy`, PR pending): GitHub Actions — pytest +
  ruff on every push/PR, SSH auto-deploy to the VPS on master pushes.
- Field lessons worth upstreaming: systemd EnvironmentFile keeps inline
  `# comments` as part of values (env templates must keep comments on their own
  lines); curl without `--fail` writes API error JSON into `--output` files and
  exits 0 (masked a 403 as a "successful" TTS check); OpenAI `/v1/models` and
  the actual per-project model allowlist are both project-scoped — a 403
  `model_not_found` names the offending project id, which beats guessing.

## 2026-07-09 22:14 — change: retrieval fix — pure-Russian questions returned zero sources

- Production regression caught on day one via the interaction log (`n_sources=0`
  rows in var/interactions.jsonl): «что можешь сказать о сегодняшних изменениях
  в проектах?» and «есть что-то в KB?» both answered "SOURCES пуст".
- Two root causes in the retrieval layer: (1) the term tokenizer only matched
  Latin (`[A-Za-z0-9_.\-]+`) — all Cyrillic words were silently dropped, so
  pure-RU questions produced zero search terms; (2) period patterns matched
  «сегодня» only as a whole word, missing inflected forms («сегодняшних»), and
  short acronyms like `KB` fell under the 3-char minimum.
- Fix (robin-runtime@master, deployed via the new CI pipeline): Cyrillic
  tokenization + RU stopword list in `src/robin/kb.py`; short-acronym keep-set
  (kb/ci/api/adr/db/ui); inflected-form and vague-recency period patterns
  («сегодняшних», «вчерашние», «что нового», «недавно» → past week) in
  `src/robin/changes.py`, ordered after the specific windows so «за 3 дня»
  still wins. Regression tests added (75 offline tests green).
- Verified in production on the exact failing questions: both now return 8
  sources; the "today" question answers from today's commits with `repo@sha`
  citations.
- Known limit stated openly: retrieval is lexical — RU questions match RU text
  and Latin identifiers, but not EN translations of RU concepts; monitor
  `n_sources=0` rows and consider an embedding index if they accumulate.
- Links: robin-runtime/src/robin/kb.py, robin-runtime/src/robin/changes.py,
  robin-runtime/tests/test_kb.py, robin-runtime/tests/test_changes.py
