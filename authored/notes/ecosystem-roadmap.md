---
title: Ecosystem roadmap
type: note
status: living
owner: Andrei
updated: 2026-07-08
---

# AI Orchestrators ecosystem roadmap

**Date:** 2026-07-08 · **Horizon:** Q3 2026 + longer view
**Based on:** the ecosystem status snapshot (`status/2026-07-08-1228-status.md`, 14 repos + prograph
graph), the logging/observability audit (`status/2026-07-08-logging-audit.md`), and external factors
(GitHub Models retirement, MCP protocol evolution).

> **The previous roadmap** (`archive/2026-04-05-ecosystem-roadmap.md`, R-01..R-16 critical path) is
> archived — its critical path shipped (Maestro↔Arbiter MCP client, agent-ID normalization,
> spec-runner contract) and is confirmed live in the current status snapshot. This document replaces
> it as the live strategic surface.

> Confidence legend: ✅ confirmed by code/official source · ⚠️ from an external source, not
> independently verified this session · ❓ needs clarification.

## 0. GitHub Models: the fact is real, but our exposure ≈ zero

**External fact (✅ confirmed via GitHub's changelog):** GitHub Models is being fully retired on
**2026-07-30**, with brownouts on 07-16 and 07-23; the playground, model catalog, inference API, and
GitHub Models' own BYOK all go away.

**But checking the code shows ATP's exposure to this service is effectively zero (✅ verified):**

- Zero direct calls to the GitHub Models inference API (`models.github.ai`,
  `models.inference.ai.azure`, `inference/chat/completions`) found anywhere in the repos.
- Every `spec-runner` model preset is a **CLI agent**: `claude`, `codex`, `copilot`, `qwen`, `ollama`,
  `opencode`, `pi`, `llama-cli`. Model access goes through these CLIs, not an inference API.
- The `copilot` preset is the **GitHub Copilot CLI** (`command: copilot`,
  `gh auth`/`COPILOT_GITHUB_TOKEN`). **Copilot is not being retired** — the same changelog recommends
  it as a migration path. The earlier match on the word "copilot" was a false signal.
- `atp-platform`'s GitHub OAuth device flow is dashboard **auth**, not inference via Models.

**Conclusion (correcting an earlier version of this analysis):** this is NOT P0. The original
strategic point — "own a provider-abstraction layer so we don't depend on one hosted catalog" —
remains **sound architecture for later**, but there's **no 07-16 deadline urgency**, because we don't
actually use that catalog. What's left is a short *confirm* task (checklist in §6), not a migration.

- **Where to build the abstraction later:** `arbiter` already has a catalog layer (`arbiter-cli`
  catalog loader, ADR-ECO-003b; `route_task`) — the natural home for provider-independent routing.

## 1. Five anchor directions (refined)

### 1.1 ATP Platform — source of routing-grade data ✅
Treat it as a data provider for routing: cost, usage class, pass-rate/reliability, evaluator-model
provenance. The loop already exists: recent commits (`mean_run_pass_rate` in payload #234, reporter,
grading in `method`), and `arbiter` has a `routable-flip benchmark-evidence gate` (ADR-ECO-003a) that
consumes this data. The `report_benchmark-v1` contract has 5 owners (incl. ATP and arbiter), no drift.
**Focus:** stabilize the benchmark-contract payload and version it as strictly as the MCP protocol.

### 1.2 Maestro — recoverability + audit trail ✅
This is what separates an enterprise orchestrator from a toy. Already on the right trajectory:
`spawning sentinel` (#57), `runtime-decision instrumentation M3` (#55), portable `maestro init` (#56).
**Focus:** stranded-workstream recovery, merge ordering, a full runtime-decision log. **Depends on §3
(observability)** — an audit trail is only as reliable as the logs under it.

### 1.3 spec-runner — the formal planning/spec backend ✅
Maestro already treats it as a versioned backend: `SPEC_RUNNER_REQUIRED_VERSION` in
`maestro/spec_runner.py` + contract tests against `plan --full`. The mechanism exists.
**Risk (refining the earlier point):** version discipline is only enforced on Maestro's side. Other
consumers still pin `spec-runner >=0.1.x` while the real version is **2.9.0** (two majors off). Align
the pins and add a CI compatibility check (see `status/2026-07-08-1228-status.md` misalignment 1).

### 1.4 Arbiter — keeping pace with MCP's evolution ✅/⚠️
Arbiter as an MCP policy/gate engine is the right base for a governance proxy, approvals, and
agent/tool-call audit. This is the most forward-looking item — details in §4 (MCP evolution), since
arbiter is first to hit compatibility issues.

### 1.5 External risk → an owned model layer ✅ (de-urgentized)
See §0. The strategic conclusion of the original analysis holds — a provider-independent
catalog/routing layer in arbiter is useful. But after checking the code: there's no urgency, exposure
to the retiring GitHub Models catalog is ≈ zero (model access goes through CLI agents). This is
"someday" work, not a fire drill.

## 2. Gap in the earlier roadmap: where's proctor? ✅ (important)

`proctor` wasn't mentioned in the original analysis at all, yet it's now the most active new repo (250
commits, 87/30d). Per its README it "orchestrates LLM-powered agents that execute workflows (simple
prompts, DAG pipelines), calls tools, communicates through an internal event bus" — a **direct overlap**
with Maestro (DAG orchestration).

**A decision on role boundaries is needed:**
- Option A: proctor = a distributed execution substrate (NATS, Docker workers, registry) **under**
  Maestro; Maestro plans and decides, proctor executes.
- Option B: proctor = an independent event-driven agent runner for a different task class
  (proactive/scheduled/Telegram-triggered).

Until this is settled, there's a risk of duplicated DAG/workflow engines and competition for the
orchestrator role. The roadmap needs to state proctor's positioning explicitly — this is an
architectural decision, not a detail.

## 3. Gap in the earlier roadmap: observability as a foundation (enabler) ✅

Items 1.1 (routing-grade data), 1.2 (audit trail, runtime-decision logs), and 1.4 (tool-call audit) **all
ride on the obs contract v1** — and it's currently uneven (full detail in
`status/2026-07-08-logging-audit.md`):

- A standard exists and works end-to-end: `observability-contract/v1` (OTel-compatible JSON) +
  emitter `obs.py` (canon in spec-runner) / `obs.rs` (Rust) → `.jsonl` → read by `dispatcher`. ✅
- **But the foundation has cracks:** three copies of `obs.py` with different md5s — the ones vendored
  into Maestro/arbiter are ~50 lines behind canon; `proctor` (the most active service, already in the
  enum as `proctor-a`) logs via bare stdlib and doesn't write to the contract; `atp-platform` logs
  structurally but in its own format (`correlation_id/version/hostname`).

**Conclusion:** logging unification belongs in the roadmap as an **enabler under 1.1/1.2/1.4**, not as
separate hygiene. Concretely: (1) pull `obs.py` out of vendoring into an installable package; (2) move
proctor onto the contract (also turns on its dispatcher monitoring); (3) bring atp-platform to contract
fields; (4) CI check "copy == canon" + validate log samples against `log-schema.json`. `prograph`
already detects contract drift — hang this check off its indexing.

## 4. Longer view: MCP protocol evolution

> ✅ **Checked against the official MCP roadmap** (modelcontextprotocol.io/development/roadmap,
> updated 2026-03-05). Confirmed: the current spec revision is **2025-11-25** (so the cited date is a
> real revision). The line-by-line 2025-06-18 / 2025-11-25 changelog wasn't diffed in full, but the
> direction matches the official priorities below. The term **"MRTR" (❓)** doesn't appear in the
> official roadmap — leaving it as an open question (closest real mechanics: Tasks primitive
> SEP-1686, Result Type improvements, Triggers/Events).

### 4.1 Official MCP priorities (✅ per the 2026-03-05 roadmap)
Four priority areas, three directly relevant to ATP:

1. **Transport Evolution & Scalability** — stateless operation behind load balancers/proxies;
   scalable session handling (create/resume/migrate sessions transparently to the client); **MCP
   Server Cards** (server metadata via a `.well-known` URL for discovery without connecting).
   Important: **no new official transports this cycle** — the set is kept small for compatibility.
2. **Agent Communication** — the **Tasks primitive (SEP-1686)**, call-now/fetch-later; refined
   retry semantics and expiry policies.
3. **Governance Maturation** — Linux Foundation, Working Groups, contributor ladder (project
   governance, not our code).
4. **Enterprise Readiness** — **audit trails and observability** (end-to-end visibility feeding
   enterprise logging/compliance pipelines); enterprise-managed auth (moving off static client
   secrets → SSO, Cross-App Access); **gateway/proxy patterns** (authorization propagation, session
   semantics visible to a gateway); configuration portability. Roadmap caveat: "much of this will
   ship as **extensions**, not core changes."

**On the horizon:** Triggers/Event-Driven Updates (webhooks instead of polling —
our "subscriptions/listen"), Result Type Improvements (streamed/reference-based results — our
"resultType"), Security & Authorization (finer-grained scopes, DPoP SEP-1932, Workload Identity
Federation SEP-1933).

**Key takeaway:** MCP is maturing into an enterprise integration protocol (stateless, discoverable,
gateway-friendly, OTel-observable). The read that this is "a painful normalization, not a
catastrophe" **is confirmed by the official position**: transports are kept small for compatibility,
and enterprise features mostly land as extensions → fewer core breaking changes than one might fear.

### 4.1a How well this matches ATP's course (✅ good news)
MCP's official priorities line up almost word-for-word with this roadmap's directions:
- MCP "Enterprise: audit trails & observability, feed into existing logging pipelines" ↔ our §1.2
  (Maestro audit trail), §1.4 (arbiter tool-call audit), §3 (obs unification on the OTel contract).
  Our `observability-contract/v1` is already OTel-compatible — we're heading where MCP officially is.
- MCP "Gateway & proxy patterns" ↔ arbiter as a governance proxy (§4 below). Official validation of
  the direction.
- MCP "stateless + scalable session handling" ↔ our finding about stateful `atp-dashboard` MCP
  (see §4.2).
- MCP "Tasks primitive" ↔ Maestro/proctor's task-oriented orchestration.

So the bet on arbiter-as-governance-proxy + unified OTel observability isn't a guess — it matches
MCP's official direction.

### 4.2 Our actual exposure (✅ verified in code)
The ecosystem runs **several live MCP servers**, not one:
- `arbiter/arbiter-mcp` (Rust) — the policy engine;
- `spec-runner/src/spec_runner/mcp_server.py`;
- `prograph/prograph/mcp_server.py`;
- `atp-platform`: `atp/mock_tools/server.py`, `atp-dashboard`'s MCP tools (with `session_id`
  handling, handshake observability, PR #102), example servers.

**Finding #1 (compatibility):** `arbiter-mcp`'s `initialize` returns `"protocolVersion": "1.1.0"`
(`server.rs:418`). MCP uses **date-string** versions (`2025-06-18` etc.). This currently works only
because Maestro is a "custom" client with its own version check. Against a standards-compliant
client/gateway, this handshake is a failure risk — exactly the "version-aware" point the MCP
changelogs raise.

**Finding #2 (stateful):** `atp-dashboard`'s MCP carries state in `session_id` (first-tool-call per
session). Moving to a stateless model makes this a candidate for explicit handles instead of a
session.

### 4.3 Compatibility checklist ahead of the draft (per our MCP servers)
No need to panic (this is a draft, SDKs will give a transition period), but prepare a checklist per
server:

1. **protocolVersion:** bring `arbiter-mcp` to MCP's date-string format, with version negotiation
   support (keep "1.1.0" as arbiter's own internal contract, separate from the MCP field). —
   priority, ✅ found.
2. **Session/stateful:** review dependence on `Mcp-Session-Id`/`session_id` (atp-dashboard); decide
   what migrates to explicit handles.
3. **Auth:** plan a move to OAuth Resource Server + Resource Indicators (RFC 8707); arbiter/gate
   currently has no OAuth layer.
4. **Discovery / Server Cards:** readiness for MCP Server Cards (`.well-known` metadata) — our
   servers (arbiter-mcp, prograph, spec-runner) could publish capabilities without connecting.
   Official priority #1.
5. **JSON Schema:** confirm tool schemas are valid under 2020-12 (our contracts are already on
   `draft/2020-12` — ✅ a good start).
6. **Tasks / Triggers / Result types:** track adoption of the Tasks primitive (SEP-1686),
   event-driven updates, and streamed/reference results; also where the unresolved "MRTR" ❓ fits —
   clarify with the analysis's author.
7. **Versioning:** a strategy for supporting old and new protocol in parallel during the transition.

**Where this lives in the roadmap:** §4.x sits under §1.4 (Arbiter). Arbiter as a governance proxy
benefits directly from the new model (OAuth resource server, policy hooks, tool-call audit) — worth
tracking its roadmap in sync with MCP revisions rather than playing catch-up.

## 5. Priorities (summary)

| # | Action | Urgency | Rationale |
|---|---|---|---|
| P1 | Align `spec-runner` pins (0.1.x → 2.9.x) + CI | High | Direct risk to §1.3's "versioned contract" ✅ |
| P2 | Position proctor vs. Maestro | High | Otherwise: duplicated orchestrators ✅ |
| P3 | Unify observability (obs package, proctor→contract) | High | Enabler for §1.1/1.2/1.4 ✅ |
| P4 | `arbiter-mcp` protocolVersion → MCP date-string | Medium | Compatibility with external MCP clients ✅ |
| P5 | MCP compatibility checklist across all servers (§7) | Medium | Prep for protocol normalization ✅ |
| P6 | Stabilize + version the ATP benchmark payload | Medium | Feeds arbiter routing ✅ |
| P7 | Maestro: stranded recovery, merge ordering | Medium | Enterprise-grade orchestration ✅ |
| P8 | Confirm no GitHub Models exposure (§6); provider-abstraction — later | Low | Exposure ≈ zero, no urgency ✅ |

## 6. Checklist: GitHub Models (verify, don't migrate)

Since code-level exposure is ≈ zero (§0), this is a short "confirm and close" task, not a fire drill.
Can be done calmly, with no tie to 07-16.

- [ ] **Confirm no inference calls.** Re-grep every repo for: `models.github.ai`,
  `models.inference.ai.azure`, `inference/chat/completions`, `GITHUB_TOKEN` next to a model call.
  Expected — empty. (✅ empty as of 2026-07-08.)
- [ ] **Check env/secrets and CI.** No `GITHUB_TOKEN`/`AZURE_*` used as an inference key in GitHub
  Actions, `.env.example`, docker-compose, or deploy scripts.
- [ ] **Clarify the `copilot` preset.** Make sure users understand `--preset copilot` = GitHub
  **Copilot CLI** (staying), not GitHub Models (retiring). Add a note to the preset docs.
- [ ] **Check the arbiter catalog.** Confirm the catalog loader routes to **agents**, not to a
  hosted-Models endpoint.
- [ ] **Log the provider-abstraction decision** as a non-urgent backlog item: whether it's needed at
  all, and if so, target providers (Azure AI Foundry / direct APIs / multi-provider via arbiter).
- [ ] **(Optional) One smoke run** of each CLI preset in use, to catch any non-Models-related
  regressions before end of July.

## 7. Our MCP servers' readiness against MCP priorities (✅ per code)

| Server | Transport | Stateful? | protocolVersion | Auth | Main gap vs. MCP roadmap |
|---|---|---|---|---|---|
| **arbiter-mcp** (Rust) | stdio (JSON-RPC 2.0) | yes (`initialized` flag) | **`"1.1.0"`** — not date-string ❗ | none (process trust) | P4: bring version to MCP format; OAuth Resource Server readiness for the governance-proxy role |
| **spec-runner** `mcp_server.py` | stdio (FastMCP) | light (ExecutorState) | (FastMCP default) | none (inherits process trust) | Server Card/discovery; review write-tools (`run_task`,`stop`) under a gateway model |
| **prograph** `mcp_server.py` | stdio | no (reads a snapshot) | none | none | Server Card; otherwise fits well (read-only) |
| **atp-dashboard** MCP | (part of dashboard) | **yes — `session_id`** ❗ | dashboard-auth | none at the MCP level | Transport/session: candidate for explicit handles under a stateless model |
| **atp mock_tools** `server.py` | local test server | n/a | n/a | n/a | test-only, outside the production perimeter |

**Reading the table against MCP's official priorities (§4.1):**
- *Transport Evolution / stateless / Server Cards:* all our servers are currently stdio (1:1 process
  trust) — "stateless HTTP behind a gateway" isn't a pressure point today. But `arbiter-mcp` and
  `atp-dashboard` already carry state — first candidates for session refactoring if/when we move to
  an HTTP transport. Server Cards (`.well-known` metadata) are a cheap early win for
  arbiter/prograph/spec-runner.
- *Enterprise auth (OAuth Resource Server):* no auth at the MCP level anywhere yet (stdio inherits
  process trust). For arbiter-as-governance-proxy this is future work item #1.
- *Tool schemas / JSON Schema 2020-12:* our contracts are already on `draft/2020-12` — ✅ ready.
- *Priority action:* P4 (`arbiter-mcp` → date-string protocolVersion) is the one clear compatibility
  gap found in code.

## Open questions (need an owner's decision)

1. proctor: a substrate under Maestro, or an independent runner? (see §2)
2. Target model provider after GitHub Models: Azure AI Foundry, direct APIs, or multi-provider via
   the arbiter catalog? (§0)
3. "MRTR" in the MCP context — what does it actually refer to? (§4, ❓)
4. OAuth Resource Server for arbiter — an own IdP, or an external OIDC? (§4.3)

## Sources
- GitHub Models retirement: github.blog changelog, 2026-07-01 (✅ verified)
- MCP official roadmap: modelcontextprotocol.io/development/roadmap (✅ verified, updated
  2026-03-05; current spec 2025-11-25)
- MCP changelog 2025-06-18, 2025-11-25 (⚠️ revision date confirmed; line-by-line build list not
  diffed)
- Code: `arbiter/arbiter-mcp/src/server.rs`, `Maestro/maestro/spec_runner.py`, `atp-platform` (#234,
  dashboard MCP), `spec-runner` (presets, obs.py), `proctor/README.md`, `.prograph/graph.db`
