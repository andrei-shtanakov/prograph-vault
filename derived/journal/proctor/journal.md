---
title: proctor — activity journal
type: journal
source: kb-save
project: proctor
updated: 2026-07-16
---

# proctor — activity journal

> Append-only log of significant project actions (written by the kb-save skill).
> Not authoritative and not regenerable. Curation/archival by kb-curator.

## 2026-07-06 15:02 — result: Phase 2 closed, Phase 3 part 1 shipped (distribution loop)

- Phase 2 completed 2026-07-05: TaskRouter admission layer (4 safety invariants,
  TTL pending queue, atomic slot reservation) merged as PR #28; final-review
  follow-ups closed in PR #29.
- Phase 3 part 1 completed 2026-07-06: worker registry + remote dispatch merged
  as PR #30. worker.* protocol on the EventBus, WorkerRegistry with
  first-alive-owns incarnation fencing and loss-callback delivery, WorkerNode
  (subscription barrier, safe shutdown), real capability scoring, dispatch
  fencing on (task_id, dispatch_id, instance_id), worker-loss policy with
  opt-in retry. At-most-once per dispatch; JetStream deferred with a stable
  wire-contract seam. Multi-node loop live-verified against a real NATS
  container.
- Design spec went through 3 structured human review rounds (fencing policy,
  self-healing discovery, dispatch rollback, offline asymmetry); two significant
  bugs caught by per-task/final reviews mid-flight (slot leak on save-fail
  rollback; worker_busy defeating retry policy) — both fixed with regression
  tests before merge.
- Links: proctor/docs/superpowers/specs/2026-07-06-worker-registry-dispatch-design.md,
  proctor/docs/superpowers/specs/2026-07-05-task-router-design.md,
  PRs #28 #29 #30 (andrei-shtanakov/proctor)

## 2026-07-07 13:30 — result: Phase 3 part 2 shipped — docker worker (PR #32)

- Core-managed container worker fleet merged as PR #32. infra/docker.py
  (ContainerRuntime, runtime-agnostic docker|podman CLI wrapper) +
  workers/docker.py (DockerWorkerManager: poll-loop restart on container
  exit, exponential backoff + full jitter, stability-window reset,
  crash-loop ceiling → docker_worker.failed with log tail). Fresh
  worker_id per launch dodges the registry first-alive-owns fencing on
  restart; secret env-file written atomically 0600 in a private mkdtemp
  0700 dir. Dockerfile + base worker.yaml (drain_timeout 20 < stop_timeout
  30 so SIGTERM drains before SIGKILL). 704 tests pass; docker-marker
  integration test is collect+skip (no image to build here).
- Two review catches fixed mid-flight with regression tests: automated
  commit-time security review found a credential env-file TOCTOU/symlink
  (MEDIUM); the final human review found an env-override validation bypass
  that would collapse all replicas onto one worker_id if PROCTOR_WORKER_ID
  were unset. Copilot PR review added: fractional stop_timeout flooring to
  0 (immediate SIGKILL) and non-independent stop/remove leaking containers.
- Links: proctor/docs/superpowers/specs/2026-07-07-docker-worker-design.md,
  proctor Dockerfile, PR #32 (andrei-shtanakov/proctor)

## 2026-07-07 16:18 — result: Phase 3 part 3 shipped — remote docker workers (PR #33)

- Remote container workers via DOCKER_HOST=ssh:// merged as PR #33. A docker
  fleet with ssh_host runs its containers on a remote host over an SSH-tunneled
  socket, reusing the entire part-2 docker-worker lifecycle. The full bare-host
  SSHBackend (asyncssh/nohup/pidfile + WorkerFleetManager base extraction) was
  deferred (rule of three) — a reviewer's docker-over-ssh call removed ~half the
  planned work and the whole bare-SSH bug class (PID-reuse, orphan-after-reconnect,
  secret-on-remote-disk).
- Load-bearing correctness from the review rounds: ContainerRuntime got per-fleet
  env + a per-op timeout that explicitly kills+reaps the subprocess (a hung ssh
  hangs rather than crashes and would stall the whole poll loop / leak zombies);
  stop() runs under stop_timeout+op_margin (not op_timeout) so drain is never cut
  mid-grace; the manager got a bounded observable unreachable-ceiling with recovery
  reset and failure-tolerant launch. NATS-reachability validator (exact host via
  urlsplit, rejects loopback/host.docker.internal/172.17.0.1 for remote fleets).
- Final review strengthened a weak kill+reap regression guard; Copilot review
  caught two validator gaps (any-scheme rejection, schemeless host:port bypass).
  732 tests pass. Integration behind the docker marker (collect+skip, no image here).
- Links: proctor/docs/superpowers/specs/2026-07-07-remote-docker-worker-design.md,
  proctor/docs/remote-workers.md, PR #33 (andrei-shtanakov/proctor)

## 2026-07-16 11:13 — decision: pass на оффер open-prose (receipts/IR); первый потребитель — atp-platform

- open-prose опубликовал машинные контракты (`openprose.receipt.v1`,
  `openprose.compile-ir.v1`) как evaluation-входы для соседей
  (нота `authored/notes/2026-07-16-openprose-contracts-offer.md`).
- proctor — pass: не исполняет `.prose`-программы, eval-контура в roadmap нет,
  скоуп минимален (dogfooding Maestro, следующая фаза — mcp/). Вендорить
  контракт без потребляющего кода — speculative.
- Receipt-паттерн (append-only hash-chain + fingerprints + атрибуция usage)
  зафиксирован как дизайн-референс для возможной будущей верифицируемости
  episodes.db — читать как образец, не вендорить.
- Первым потребителем назначен atp-platform (задача заводится в его репо);
  arbiter отложен. Нюанс по гейтам: оффер сам по себе не открывает Rust-гейт
  4.6 / Phase 6 open-prose — критерий «потребитель появился» требует факта
  (вендоренный контракт + reader на master потребителя).
- Links: authored/notes/2026-07-16-openprose-contracts-response.md,
  authored/notes/2026-07-16-openprose-contracts-offer.md,
  open-prose/docs/plans/2026-07-16-development-plan.md (задача 4.6, Phase 6)
