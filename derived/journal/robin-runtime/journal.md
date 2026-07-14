---
title: robin-runtime — activity journal
type: journal
source: kb-save
project: robin-runtime
updated: 2026-07-13
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

## 2026-07-13 17:55 — change: M3 ambient context implemented (PR #10, awaiting merge)

- ROBIN-SPEC M3 (§6.2): group @mentions are now answered with ambient context —
  the asker's identity, the last N=10 channel messages, and the newest persisted
  digests enter the prompt as explicitly-untrusted blocks, with the §6.2
  conciseness rule (2–5 sentences).
- Slot 8 passive capture is opt-in per chat via new env `ROBIN_CAPTURE_CHATS`
  (ids or @names; empty = off — §6.5 disclosure enforced by configuration, and
  /help discloses the behavior). Captured messages go to Robin's own store
  (`var/channel/<chat>.jsonl`), bounded to a 200-line rolling window, flattened
  to one line each so a multi-line message cannot fake other prompt blocks.
  Unaddressed chatter never triggers a reply or an LLM call.
- New env `ROBIN_AMBIENT_N` (slot 13, default 10); `digest.latest()` exposes
  recent digests for the ambient block. All five Copilot review findings were
  valid and fixed (rolling bound, newline flattening, n<=0 guard, utf-8 reads,
  digests marked untrusted). 119 offline tests green.
- Deployment note: M3 acceptance on the VPS requires `ROBIN_CAPTURE_CHATS` set
  to the team group chat and BotFather privacy mode OFF (done for M1).
- Links: robin-runtime/src/robin/adapters/telegram.py, robin-runtime/src/robin/memory.py,
  robin-runtime/src/robin/agent.py, robin-runtime/src/robin/digest.py,
  robin-runtime/deploy/env.example

## 2026-07-13 19:30 — result: M3 accepted in production

- PR #10 merged and auto-deployed; `ROBIN_CAPTURE_CHATS=-5301459591` (team group)
  set on the VPS, bot restarted. Live acceptance: a vague group mention
  («что думаешь по этому поводу?» after a two-message presentation draft) was
  answered about the draft's theses with KB citations — ambient context works
  end-to-end ($0.049, 12 sources, 23s latency). ROBIN-SPEC M0–M3 are now done;
  remaining: M4 learning loop, M5 (optional, deferred).

## 2026-07-13 20:15 — change: M4 learning loop implemented (PR #11, awaiting merge)

- ROBIN-SPEC §5/§6.4: explicit negative feedback (👎 / /gap) now produces a
  staged learning file under var/learnings/staged/ — one insight per file,
  dated, read-back verified. Robin's write surface stays staged/-only.
- Promotion is a human, out-of-band CLI action (§6.5: chat cannot promote):
  `python -m robin.learnings list|show|promote <name> --route memory|skill|kb
  |reject`. memory → promoted/ (distilled into the system prompt as
  PROMOTED TEAM LEARNINGS, loaded into every session per §5 MUST); skill/kb →
  routed/ (audit trail; human applies via PR — Robin never writes the KB);
  reject → rejected/ (nothing deleted). Every action logged to
  var/learnings/audit.jsonl.
- Copilot review: 3 of 4 findings fixed (rule distillation without metadata
  leakage, --route value guard, message_id carried into staged files), 1
  declined with rationale (collision-suffix numbering). 130 offline tests.
- Acceptance (human, after merge+deploy): 👎 → maintainer DM → promote on the
  VPS → the same question answers differently.
