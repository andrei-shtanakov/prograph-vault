-- Onboarding progress — state contract for the runtime (robin-runtime/), NOT the KB.
-- The KB owns the checklist CONTENT (roles/<role>.yaml); the runtime owns per-user PROGRESS
-- (ROBIN-SPEC §5 placement rule). This file is the canonical schema the runtime implements.
-- Flat files suffice until M3; onboarding introduces session state, hence SQLite (plan slot 4).

PRAGMA foreign_keys = ON;

-- One row per (newcomer, role) onboarding run.
CREATE TABLE IF NOT EXISTS onboarding_session (
    session_id       TEXT PRIMARY KEY,          -- uuid
    user_id          TEXT NOT NULL,             -- chat identity (registry, §6.5) — not raw PII
    role             TEXT NOT NULL,             -- matches roles/<role>.yaml
    role_version     INTEGER NOT NULL,          -- yaml `version` at start; detect checklist drift
    status           TEXT NOT NULL DEFAULT 'active'
                       CHECK (status IN ('active','paused','complete','abandoned')),
    current_step_id  TEXT,                       -- step id from the role yaml
    started_at       TEXT NOT NULL,              -- ISO-8601 UTC
    last_activity_at TEXT NOT NULL,              -- drives the DM idle-window reseed (§6.1)
    completed_at     TEXT
);

-- Per-step progress. One row per (session, step) the newcomer has reached.
CREATE TABLE IF NOT EXISTS onboarding_progress (
    session_id    TEXT NOT NULL REFERENCES onboarding_session(session_id) ON DELETE CASCADE,
    step_id       TEXT NOT NULL,                 -- step id from the role yaml
    status        TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','in_progress','done','skipped')),
    check_passed  INTEGER NOT NULL DEFAULT 0,    -- 1 when the step's `check` question was answered
    completed_at  TEXT,
    notes         TEXT,
    PRIMARY KEY (session_id, step_id)
);

-- Every question the newcomer asked. was_in_kb = 0 => KB-gap candidate (staged learning, §6.4).
CREATE TABLE IF NOT EXISTS onboarding_question (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT NOT NULL REFERENCES onboarding_session(session_id) ON DELETE CASCADE,
    step_id       TEXT,                          -- nullable: free-floating questions allowed
    question      TEXT NOT NULL,
    answered      INTEGER NOT NULL DEFAULT 0,
    source_cited  TEXT,                          -- KB path / ADR id / contract; NULL if none
    was_in_kb     INTEGER NOT NULL DEFAULT 0,    -- 0 => escalated "not in the KB" => gap signal
    staged_ref    TEXT,                          -- learnings/staged/<file> once written (read-back verified)
    created_at    TEXT NOT NULL
);

-- The KB-gap report the onboarding duty DMs to the maintainer on completion.
CREATE INDEX IF NOT EXISTS idx_onboarding_gap
    ON onboarding_question (session_id) WHERE was_in_kb = 0;
