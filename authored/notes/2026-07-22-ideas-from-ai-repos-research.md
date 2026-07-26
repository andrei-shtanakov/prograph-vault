> Источник: ~/labs/ai-repos-research/IDEAS-FOR-ALL-AI-ORCHESTRATORS.md (копия, 2026-07-22)

# Идеи из ai-repos-research для развития all_ai_orchestrators

> Дата: 2026-07-22 | Изучено: 15 репозиториев | Целевая экосистема: `../all_ai_orchestrators/` (Maestro, arbiter, atp-platform, spec-runner, steward, libretto, proctor, dispatcher, robin-runtime, deployer, prograph, appgraph и др.)

## Ключевые пробелы экосистемы (из обзора TODO/roadmap подпроектов)

- **libretto**: concurrency-лимиты для `parallel`, pause/cancel, deterministic replay, structured errors, `timeout:`/`watch:`, наблюдаемость; известный 2–6× token premium.
- **arbiter ↔ atp-platform**: незамкнутая петля eval→routing (backfill бенчмарков, re-sweep под нормализованный pricing-контракт).
- **proctor**: динамический MCP-слой инструментов; эскалации.
- **Maestro / spec-runner**: формализация кросс-проектных контрактов; стоимость 5-ролевого ревью.
- **robin-runtime**: память/поиск по знаниям, voice отложен.
- **deployer**: MVP, нужен arbiter-gated deploy agent.
- **discovery**: runtime не построен (есть только toolkit).

## Сводная таблица идей

### Высокий приоритет

| # | Идея | Источник (репо → код) | Куда внедрять | Что даёт / как применить |
|---|------|----------------------|---------------|--------------------------|
| 1 | **Сериализуемый RunState** со schema-version, interruptions и approvals | openai-agents-python → `src/agents/run_state.py`, `.agents/references/runstate-schema.md` | **libretto**, Maestro | Закрывает сразу три пункта роадмапа libretto: pause/cancel-протокол, deterministic replay, возобновление с human-approval. Версионированная схема состояния — готовый образец для receipts/run ledgers. |
| 2 | **Трёхзонная компрессия контекста** (frozen prefix / compressible middle / active zone; порог 60% → async-компрессия, 80% → синхронная) | open-code-review → `internal/llmloop/compression.go` | **libretto**, spec-runner | Прямой ответ на 2–6× token premium libretto: компрессия середины сессии без потери префикса спеки. В spec-runner — для длинных retry-циклов. |
| 3 | **Семафорный dispatch подзадач** с изолированным контекстом на файл/бандл (default 8, `BatchStrategy`: none/by-language/by-directory) | open-code-review → `internal/agent/agent.go`, `internal/scan/batch.go` | **libretto** (`parallel`), Maestro | Готовый паттерн для concurrency-лимитов `parallel: all/first/any` (роадмап P3) и для бандлинга связанных файлов в один контекст ревью. |
| 4 | **Методология eval'ов харнесса**: фиксированный worker, одна интервенция за раз, condition-blind grading, таксономия невалидных результатов, метрики available/retrieved/invoked/relevant раздельно | harness-engineering → `evals/README.md`, `playbooks/improve-harness.md` | **atp-platform**, arbiter | Поднимает строгость re-sweep бенчмарков: изолировать эффект интервенции от шума модели. Gap-таксономия (Context/Capability/Authority/Proof/…) — готовая схема классификации провалов агентов для отчётов ATP. |
| 5 | **Attributed learning / evolution агентов**: фидбек резолвится только на роли-владельцы work items, повторяющиеся уроки (порог ≥2) промоутятся в общие playbooks | OpenOPC → `opc/layer5_memory/employee_evolution.py`, `skill_library.py` | **arbiter** (+ atp-platform) | Модель замыкания петли eval→routing: исходы задач атрибутируются конкретным агент-парам, накопленный опыт влияет на выбор агента. Дополняет shadow routing arbiter'а. |
| 6 | **Дешёвый adversarial-verifier**: judge на Haiku читает диф «считая его сломанным», 11 паттернов «fake done», строгий JSON-вердикт; + трёхуровневый model-routing (planner/executor/judge через env) | loopkit → `.claude/agents/verifier.md`, `skills/model-routing/SKILL.md`, `run.sh` | **spec-runner** (5-role review), Maestro (validation hooks), arbiter | Радикально снижает стоимость ревью: дешёвый executor + frontier-judge только на диф. Для arbiter — готовое обоснование маршрутизации по ролям, а не только по задачам. |
| 7 | **Interfaces ledger + исполняемый scope-gate**: после каждого зелёного коммита проверенный публичный интерфейс пишется в `interfaces.md` и подаётся в бриф следующей stateless-задачи; allowlist путей проверяется скриптом до коммита | codex-build → `skills/codex-build/SKILL.md`, `scripts/check_scope.py` | **Maestro**, spec-runner | Механизм формализации межзадачных контрактов (текущий фокус Maestro v0.2+): агент строит на верифицированных сигнатурах, а не догадках; scope conflict prevention становится исполняемым (exit≠0), а не промптовым. |
| 8 | **Guardrails с tripwire** на input/output/каждый tool-вызов + handoffs с фильтрацией истории | openai-agents-python → `src/agents/guardrail.py`, `tool_guardrails.py`, `handoffs/history.py` | **proctor**, steward, Maestro Mode-2 | Слой контроля для автономных агентов proctor (event bus + fleets): декларативные проверки, останавливающие run. History-filtering при handoff — образец для передачи контекста между ролями spec-runner. |

### Средний приоритет

| # | Идея | Источник (репо → код) | Куда внедрять | Что даёт / как применить |
|---|------|----------------------|---------------|--------------------------|
| 9 | **PageRank repo map под токен-бюджет**: tree-sitter → граф def/ref → personalized PageRank → бинарный поиск числа тегов под `max_map_tokens`, кэш по mtime | aider → `aider/repomap.py` | **appgraph**, spec-runner | appgraph уже строит граф символов — добавить ranked-export «карта репо на N токенов» как контекст для задач spec-runner/Maestro. Закрывает и запрос на инкрементальность (mtime-кэш). |
| 10 | **Единый Phase enum + phase-transition hooks**: одна авторитетная state machine вместо 5 суб-статусов, чистые проекции (kanban, owner, runnability), подписчики на переходы | OpenOPC → `opc/layer2_organization/phase.py`, `phase_hooks.py` | **Maestro**, proctor | Анти-desync паттерн для ExecutorState (Pydantic-контракт Maestro): статусы задач, сессий и wake-сигналы деривируются из одного enum, а не синхронизируются вручную. |
| 11 | **Двухуровневая эскалация + HITL-контракт выхода**: in-team блокер будит подходящую роль, beyond-team — человека; `BLOCKED.md` + `exit 2`, удаление файла человеком = unblock | OpenOPC → `escalation.py`, `approval.py`; loopkit → `skills/hitl-escalate/SKILL.md` | **proctor**, steward, dispatcher | Готовый протокол эскалаций для fleet'ов proctor и governance-гейтов steward; dispatcher показывает `BLOCKED.md` как actionable-элемент дашборда. |
| 12 | **Content-addressable дедуп эмбеддингов** (hash=PK, ре-индекс без API-вызовов) + 3-слойный recall (snippet → expand → transcript через session anchors) + recall в fork-контексте | memsearch → `src/memsearch/store.py`, `chunker.py`, `docs/architecture.md` | **robin-runtime**, prograph-vault | Память Robin с цитатами path:line: L1/L2/L3 recall идеально ложится на требование «всегда с citations»; дедуп режет стоимость переиндексации vault. |
| 13 | **Embedded vector DB без сервера**: in-process, WAL, hybrid dense+sparse+FTS c RRF/weighted fusion, group-by top-K (диверсификация: один чанк на документ), protocol-based embedding-плагины | zvec → `src/db/reranker/reranker.cc`, `python/zvec/extension/` | **robin-runtime**, appgraph | Убирает зависимость от Milvus-сервера для памяти экосистемы (local-first, как всё в полирепо). Group-by top-K — готовый приём для разнообразия retrieved-контекста. |
| 14 | **Sprint-contract**: 3–7 script-decidable acceptance-предикатов + runtime path + out-of-scope список фиксируются ДО кода; переторговка «done» структурно заблокирована | loopkit → `skills/sprint-contract/SKILL.md` | **steward**, discovery-toolkit | Усиливает gate-артефакты (charter→acceptance): критерии приёмки обязаны быть машинно-проверяемыми — стыкуется с `gate_check.py` (GC-01..14) и `validation_cmd` ATP. |
| 15 | **Токен-экономный вывод инструментов**: cap по `--budget`, stderr-note с точным `--offset` для продолжения, `--outline`/`--locate`/`--shape` вместо сырых дампов, санитизация ANSI/OSC-инъекций из недоверенного текста | ax → `src/lib/emit.ts`, `io.ts`, `query.ts` | **devtools**, dispatcher, robin-runtime | Единый стандарт вывода CLI-инструментов экосистемы для агентов: никогда молча не обрезать, всегда давать resume-offset. Санитизация OSC/CSI — защита от prompt-injection через выводы инструментов. |
| 16 | **«Deterministic Engineering × Agent Hybrid» + delegation mode**: детерминированный код для того, что не должно падать (выбор файлов, позиционирование комментариев, матчинг правил), LLM — только для суждений; режим «отбор+правила наши, ревью — ваш агент» | open-code-review → README, `internal/delegate/`, `internal/config/rules/` | **spec-runner**, github-checker | Философия уже близка экосистеме — стоит закрепить как правило в prograph-vault/rules. Delegation mode — паттерн для spec-runner: детерминированная подготовка контекста + сменный ревью-агент (выбирает arbiter). |
| 17 | **Architect/editor split**: модель-архитектор рассуждает прозой, отдельная editor-модель делает механические правки; стоимость агрегируется через обе | aider → `aider/coders/architect_coder.py` | **spec-runner**, Maestro, arbiter | Пары «планировщик+редактор» как routable-единица arbiter вместо одного агента; дешевле и качественнее на сложных задачах. |
| 18 | **Always-on инъекция через SessionStart `additionalContext` JSON** + cost-модель «input-токены рекуррентны» + честный bench-harness (2 прогона, thinking off, реальные usage-дельты) | token-diet → `install.sh:71-142`, `SKILL.md`, `bench/bench.mjs` | **devtools** (fleet), libretto | Механика надёжной инъекции fleet-правил во все сессии всех харнессов; bench-подход — способ измерить token premium libretto числом, а не оценкой. |

### Низкий приоритет / точечные заимствования

| # | Идея | Источник (репо → код) | Куда внедрять | Что даёт |
|---|------|----------------------|---------------|----------|
| 19 | Resumable sessions ревью (`--resume <session-id>`, persist/resume/history) | open-code-review → `internal/session/` | spec-runner | Возобновление прерванного ревью-прогона без повторной оплаты пройденного. |
| 20 | E2E-шифрованный peer-обмен между агентами разных машин + push-monitor инбокса (tail NDJSON-спула, dedup по offset+id) | agent-talk → `monitors/`, `extensions/inbox-monitor.ts` | proctor | Кросс-машинный канал агентов поверх недоверенного релея; push-доставка в живую сессию — альтернатива поллингу. |
| 21 | Handover-блоки с обязательной секцией Test Result (Status/Command/Notes), которые оркестратор валидирует и требует переделать | Zenflow → `templates/agents/orchestrator.md.j2`, partials | spec-runner (roles), Maestro | Лёгкая структурная верификация свободного текста агентов без JSON-схем. |
| 22 | Один набор шаблонов → рендер под несколько харнессов (`skill_mode`, tool-aware пути) | Zenflow → `src/zenflow/deployment.py`, `guidelines.py` | robin-toolkit, discovery-toolkit | Упаковка skills-бандлов сразу под Claude Code / Copilot / OpenCode из одного источника. |
| 23 | File-state injection (содержимое state-файлов кладётся в промпт, но правится через Edit) + one-task-per-loop | ralphio → `ralphio.js:523-645` | spec-runner | Мелкая токен-экономия: не заставлять агента перечитывать только что показанные файлы. |
| 24 | AI-comments watcher: `AI!`/`AI?` в комментариях кода триггерят ход агента (watchfiles + gitignore) | aider → `aider/watch.py` | spec-runner-vscode | IDE-агностичный способ вызвать агента прямо из исходника. |
| 25 | Cost tracker на EventBus: per-task/per-agent/per-org токены+$ в SQLite, `CostEvent` подписчикам | OpenOPC → `opc/layer6_observability/cost_tracker.py` | Maestro, dispatcher | Сводный $-вид по экосистеме поверх нормализованного pricing-контракта ATP. |
| 26 | Compaction-петля памяти: retrieve → LLM-summary → append в daily.md → авто-реиндекс; maintenance-задачи с жёсткими бюджетами (`MAX_PROMPT_CHARS`, `MAX_TOOL_CALLS`) | memsearch → `compact.py`, `maintenance.py` | robin-runtime | Самосжимающаяся память дайджестов Robin с бюджетными предохранителями. |
| 27 | Progressive-disclosure референсы в skill + детерминированный рендер отчёта отдельным скриптом с санитайзерами | codex-first-customer-finder-skill → `SKILL.md`, `scripts/generate_report.py` | discovery-toolkit | Шаблон для discovery-brief: LLM пишет JSON, HTML/отчёт рендерит код. |

## Тематические кластеры (что повторяется в нескольких репо)

| Тема | Репозитории | Вывод для экосистемы |
|------|-------------|----------------------|
| Разделение generator/evaluator (дешёвый писатель + строгий судья) | loopkit, codex-build, aider (architect/editor), open-code-review | Самый подтверждённый паттерн выборки — кандидат в правило prograph-vault и в модель маршрутизации arbiter (роутить роли, не задачи). |
| JIT/progressive загрузка контекста | harness-engineering, memsearch, token-diet, codex-first-customer-finder | Экономия input-токенов важнее краткости вывода: транскрипт пересылается каждый ход. Ключ к снижению token premium libretto. |
| State-on-disk, файлы = источник истины, индексы деривируемы | loopkit, ralphio, codex-build, memsearch | Совпадает с философией экосистемы (markdown-спеки, SQLite): усиливать, а не менять. |
| Resumable runs со схемой состояния | openai-agents-python, open-code-review, codex-build, OpenOPC | Зрелые проекты все инвестируют в это; главный дефицит libretto/Maestro. |
| Исполняемые (не промптовые) гейты | codex-build (scope), loopkit (verifier JSON), Zenflow (handover-валидация), discovery-toolkit (уже есть gate_check) | Направление, в котором экосистема уже движется — таблица даёт готовые референс-реализации. |

## Рекомендуемый порядок внедрения

1. **libretto**: RunState-схема (#1) + трёхзонная компрессия (#2) + семафорный parallel (#3) — закрывают почти весь роадмап P2–P3.
2. **arbiter/ATP**: eval-методология (#4) + attributed learning (#5) — замыкают петлю benchmark→routing.
3. **spec-runner/Maestro**: haiku-verifier (#6) + interfaces ledger и scope-gate (#7) — снижают стоимость и формализуют контракты.
4. **proctor/steward**: guardrails (#8) + эскалации (#11).
5. **robin-runtime**: memsearch-паттерны (#12) поверх zvec (#13) — local-first память с цитатами.
