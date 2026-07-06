<!-- prograph:generated -->

---
indexed_at: "2026-05-27T12:45:37Z"
kind: python
name: proctor-a
prograph: project
root: ./proctor-a
snapshot: 48
---

# proctor-a

> Distributed autonomous agent system with microkernel architecture. Version 0.1.0.

## Manifest

- declared package: `proctor` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `logger` (const) — `src/proctor/__main__.py:15`
- `main` (function) — `src/proctor/__main__.py:18`
- `logger` (const) — `src/proctor/core/bootstrap.py:25`
- `LLMCall` (const) — `src/proctor/core/bootstrap.py:27`
- `Application` (class) — `src/proctor/core/bootstrap.py:56`
- `EventBus` (class) — `src/proctor/core/bus.py:21`
- `logger` (const) — `src/proctor/core/config.py:15`
- `LLMConfig` (class) — `src/proctor/core/config.py:18`
- `NATSConfig` (class) — `src/proctor/core/config.py:29`
- `EventsConfig` (class) — `src/proctor/core/config.py:63`
- `ScheduleItemConfig` (class) — `src/proctor/core/config.py:71`
- `RouteRule` (class) — `src/proctor/core/config.py:97`
- `SchedulerConfig` (class) — `src/proctor/core/config.py:115`
- `TelegramConfig` (class) — `src/proctor/core/config.py:122`
- `HMACAuthConfig` (class) — `src/proctor/core/config.py:130`
- `BearerAuthConfig` (class) — `src/proctor/core/config.py:146`
- `NoneAuthConfig` (class) — `src/proctor/core/config.py:155`
- `AuthConfig` (const) — `src/proctor/core/config.py:162`
- `WebhookPathConfig` (class) — `src/proctor/core/config.py:168`
- `WebhookConfig` (class) — `src/proctor/core/config.py:179`
- `ProctorConfig` (class) — `src/proctor/core/config.py:228`
- `load_config` (function) — `src/proctor/core/config.py:319`
- `logger` (const) — `src/proctor/core/memory.py:12`
- `EpisodicMemory` (class) — `src/proctor/core/memory.py:94`
- `TaskStatus` (class) — `src/proctor/core/models.py:12`
- `Event` (class) — `src/proctor/core/models.py:30`
- `Task` (class) — `src/proctor/core/models.py:71`
- `Episode` (class) — `src/proctor/core/models.py:86`
- `Envelope` (class) — `src/proctor/core/models.py:97`
- `LLMCallRecord` (class) — `src/proctor/core/models.py:111`
- `logger` (const) — `src/proctor/core/router.py:19`
- `Router` (class) — `src/proctor/core/router.py:56`
- `logger` (const) — `src/proctor/core/state.py:13`
- `StateManager` (class) — `src/proctor/core/state.py:100`
- `Handler` (const) — `src/proctor/core/transport/base.py:15`
- `ConnectionState` (class) — `src/proctor/core/transport/base.py:18`
- `DisconnectCallback` (const) — `src/proctor/core/transport/base.py:56`
- `EventTransport` (class) — `src/proctor/core/transport/base.py:59`
- `TransportError` (class) — `src/proctor/core/transport/errors.py:12`
- `TransportConnectionError` (class) — `src/proctor/core/transport/errors.py:16`
- `TransportLifecycleError` (class) — `src/proctor/core/transport/errors.py:20`
- `TransportUnavailableError` (class) — `src/proctor/core/transport/errors.py:24`
- `TransportDrainingError` (class) — `src/proctor/core/transport/errors.py:28`
- `InvalidSubjectError` (class) — `src/proctor/core/transport/errors.py:32`
- `EventTooLargeError` (class) — `src/proctor/core/transport/errors.py:40`
- `EventSchemaError` (class) — `src/proctor/core/transport/errors.py:44`
- `HandlerTimeoutError` (class) — `src/proctor/core/transport/errors.py:54`
- `logger` (const) — `src/proctor/core/transport/local.py:36`
- `LocalEventTransport` (class) — `src/proctor/core/transport/local.py:232`
- `logger` (const) — `src/proctor/core/transport/nats.py:46`
- `SCHEMA_VERSION` (const) — `src/proctor/core/transport/nats.py:48`
- `Decoder` (const) — `src/proctor/core/transport/nats.py:50`
- `register_decoder` (function) — `src/proctor/core/transport/nats.py:61`
- `NATSEventTransport` (class) — `src/proctor/core/transport/nats.py:110`
- `Trigger` (class) — `src/proctor/triggers/base.py:8`
- `logger` (const) — `src/proctor/triggers/scheduler.py:16`
- `SchedulerTrigger` (class) — `src/proctor/triggers/scheduler.py:19`
- `logger` (const) — `src/proctor/triggers/telegram.py:16`
- `TELEGRAM_API_BASE` (const) — `src/proctor/triggers/telegram.py:18`
- `INITIAL_RETRY_DELAY` (const) — `src/proctor/triggers/telegram.py:19`
- `MAX_RETRY_DELAY` (const) — `src/proctor/triggers/telegram.py:20`
- `RETRY_BACKOFF_FACTOR` (const) — `src/proctor/triggers/telegram.py:21`
- `TelegramTrigger` (class) — `src/proctor/triggers/telegram.py:24`
- `logger` (const) — `src/proctor/triggers/terminal.py:12`
- `QUIT_COMMANDS` (const) — `src/proctor/triggers/terminal.py:14`
- `TerminalTrigger` (class) — `src/proctor/triggers/terminal.py:17`
- `logger` (const) — `src/proctor/triggers/webhook.py:27`
- `InflightLimiter` (class) — `src/proctor/triggers/webhook.py:114`
- `WebhookTrigger` (class) — `src/proctor/triggers/webhook.py:160`
- `logger` (const) — `src/proctor/workers/llm.py:23`
- `task_id_ctx` (const) — `src/proctor/workers/llm.py:35`
- `step_id_ctx` (const) — `src/proctor/workers/llm.py:36`
- `episode_id_ctx` (const) — `src/proctor/workers/llm.py:37`
- `LLMCall` (const) — `src/proctor/workers/llm.py:39`
- `build_llm_call` (function) — `src/proctor/workers/llm.py:42`
- `logger` (const) — `src/proctor/workers/runtime.py:13`
- `LLMFn` (const) — `src/proctor/workers/runtime.py:18`
- `ToolDef` (class) — `src/proctor/workers/runtime.py:24`
- `ToolResult` (class) — `src/proctor/workers/runtime.py:32`
- `AgentResult` (class) — `src/proctor/workers/runtime.py:40`
- `AgentRuntime` (class) — `src/proctor/workers/runtime.py:48`
- `logger` (const) — `src/proctor/workflow/dag.py:17`
- `StepResult` (class) — `src/proctor/workflow/dag.py:20`
- `StepRunner` (const) — `src/proctor/workflow/dag.py:28`
- `topo_sort` (function) — `src/proctor/workflow/dag.py:31`
- `DAGExecutor` (class) — `src/proctor/workflow/dag.py:64`
- `logger` (const) — `src/proctor/workflow/engine.py:16`
- `LLMCall` (const) — `src/proctor/workflow/engine.py:18`
- `WorkflowResult` (class) — `src/proctor/workflow/engine.py:21`
- `WorkflowEngine` (class) — `src/proctor/workflow/engine.py:30`
- `WorkflowMode` (class) — `src/proctor/workflow/spec.py:13`
- `StepType` (class) — `src/proctor/workflow/spec.py:22`
- `StepRetry` (class) — `src/proctor/workflow/spec.py:32`
- `Step` (class) — `src/proctor/workflow/spec.py:39`
- `WorkflowPolicies` (class) — `src/proctor/workflow/spec.py:53`
- `WorkflowSpec` (class) — `src/proctor/workflow/spec.py:62`
- `pytest_collection_modifyitems` (function) — `tests/conftest.py:12`
- `pytestmark` (const) — `tests/integration/test_llm_ollama.py:17`
- `pytestmark` (const) — `tests/integration/test_transport_contract.py:24`
- `TestContract` (class) — `tests/integration/test_transport_contract.py:107`
- `pytestmark` (const) — `tests/integration/test_transport_nats_reconnect.py:32`
- `test_disconnect_transitions_to_reconnecting` (function) — `tests/integration/test_transport_nats_reconnect.py:180`
- `test_reconnect_transitions_back_to_connected` (function) — `tests/integration/test_transport_nats_reconnect.py:190`
- `test_delivery_resumes_after_reconnect` (function) — `tests/integration/test_transport_nats_reconnect.py:202`
- `pytestmark` (const) — `tests/test_core/test_bootstrap.py:25`
- `TestInit` (class) — `tests/test_core/test_bootstrap.py:62`
- `TestStartStop` (class) — `tests/test_core/test_bootstrap.py:79`
- `TestSetLLMCall` (class) — `tests/test_core/test_bootstrap.py:168`
- `TestEventBusFunctional` (class) — `tests/test_core/test_bootstrap.py:179`
- `TestHandleTerminal` (class) — `tests/test_core/test_bootstrap.py:234`
- `TestTelegramTriggerBootstrap` (class) — `tests/test_core/test_bootstrap.py:402`
- `TestSchedulerIntegration` (class) — `tests/test_core/test_bootstrap.py:461`
- `TestPublicExports` (class) — `tests/test_core/test_bootstrap.py:570`
- `TestContextVarWiring` (class) — `tests/test_core/test_bootstrap.py:582`
- `TestRouterIntegration` (class) — `tests/test_core/test_bootstrap.py:631`
- `TestWebhookBootstrap` (class) — `tests/test_core/test_bootstrap.py:753`
- `TestApplicationDI` (class) — `tests/test_core/test_bootstrap.py:832`
- `pytestmark` (const) — `tests/test_core/test_bus.py:9`
- `TestEventBus` (class) — `tests/test_core/test_bus.py:17`
- `TestLLMConfig` (class) — `tests/test_core/test_config.py:21`
- `TestLLMConfigExtended` (class) — `tests/test_core/test_config.py:44`
- `TestNATSConfig` (class) — `tests/test_core/test_config.py:68`
- `TestSchedulerConfig` (class) — `tests/test_core/test_config.py:96`
- `TestTelegramConfig` (class) — `tests/test_core/test_config.py:111`
- `TestScheduleItemConfig` (class) — `tests/test_core/test_config.py:142`
- `TestProctorConfig` (class) — `tests/test_core/test_config.py:186`
- `TestLoadConfig` (class) — `tests/test_core/test_config.py:264`
- `TestRouteRule` (class) — `tests/test_core/test_config.py:424`
- `TestWorkflowCatalog` (class) — `tests/test_core/test_config.py:468`
- `TestRoutes` (class) — `tests/test_core/test_config.py:493`
- `TestShadowDetection` (class) — `tests/test_core/test_config.py:529`
- `test_is_strictly_broader_direct` (function) — `tests/test_core/test_config.py:592`
- `TestPublicExports` (class) — `tests/test_core/test_config.py:602`
- `TestAuthConfig` (class) — `tests/test_core/test_config.py:625`
- `TestEventsConfig` (class) — `tests/test_core/test_config.py:676`
- `TestSourceNameTightened` (class) — `tests/test_core/test_config.py:697`
- `TestWebhookConfigValidation` (class) — `tests/test_core/test_config.py:738`
- `TestTransportResolution` (class) — `tests/test_core/test_config.py:876`
- `pytestmark` (const) — `tests/test_core/test_memory.py:13`
- `TestEpisodeModel` (class) — `tests/test_core/test_memory.py:42`
- `TestInitializeAndClose` (class) — `tests/test_core/test_memory.py:71`
- `TestSaveAndGetEpisode` (class) — `tests/test_core/test_memory.py:109`
- `TestListEpisodes` (class) — `tests/test_core/test_memory.py:149`
- `TestSearchEpisodes` (class) — `tests/test_core/test_memory.py:173`
- `TestSaveEpisodeDuplicate` (class) — `tests/test_core/test_memory.py:198`
- `TestSearchWildcardEscape` (class) — `tests/test_core/test_memory.py:209`
- `TestLLMCallsTable` (class) — `tests/test_core/test_memory.py:225`
- `TestTaskStatus` (class) — `tests/test_core/test_models.py:17`
- `TestEvent` (class) — `tests/test_core/test_models.py:33`
- `TestTask` (class) — `tests/test_core/test_models.py:78`
- `TestEnvelope` (class) — `tests/test_core/test_models.py:136`
- `TestLLMCallRecord` (class) — `tests/test_core/test_models.py:193`
- `TestPublicExports` (class) — `tests/test_core/test_models.py:230`
- `TestEventValidators` (class) — `tests/test_core/test_models.py:240`
- `pytestmark` (const) — `tests/test_core/test_rate_limited_logger.py:9`
- `TestRateLimitedLogger` (class) — `tests/test_core/test_rate_limited_logger.py:17`
- `TestResolvePath` (class) — `tests/test_core/test_router.py:16`
- `TestRouterHappyPath` (class) — `tests/test_core/test_router.py:77`
- `TestRouterUnmatched` (class) — `tests/test_core/test_router.py:217`
- `TestRouterBindingFailed` (class) — `tests/test_core/test_router.py:274`
- `pytestmark` (const) — `tests/test_core/test_state.py:13`
- `TestInitialize` (class) — `tests/test_core/test_state.py:31`
- `TestSaveAndGetTask` (class) — `tests/test_core/test_state.py:51`
- `TestUpdateTask` (class) — `tests/test_core/test_state.py:106`
- `TestListTasks` (class) — `tests/test_core/test_state.py:133`
- `TestGetNonexistent` (class) — `tests/test_core/test_state.py:165`
- `TestConfigOverrides` (class) — `tests/test_core/test_state.py:173`
- `TestPublicExports` (class) — `tests/test_core/test_state.py:210`
- `TestConnectionState` (class) — `tests/test_core/test_transport_base.py:13`
- `TestEventTransportAbstract` (class) — `tests/test_core/test_transport_base.py:23`
- `TestProtocols` (class) — `tests/test_core/test_transport_base.py:48`
- `TestDedupCache` (class) — `tests/test_core/test_transport_dedup.py:16`
- `TestDedupTTL` (class) — `tests/test_core/test_transport_dedup.py:103`
- `TestDedupEviction` (class) — `tests/test_core/test_transport_dedup.py:120`
- `TestExceptionHierarchy` (class) — `tests/test_core/test_transport_errors.py:18`
- `pytestmark` (const) — `tests/test_core/test_transport_local.py:17`
- `TestLifecycle` (class) — `tests/test_core/test_transport_local.py:25`
- `TestPublish` (class) — `tests/test_core/test_transport_local.py:65`
- `TestWildcardDelivery` (class) — `tests/test_core/test_transport_local.py:97`
- `TestDrainAndCancel` (class) — `tests/test_core/test_transport_local.py:129`
- `TestWildcardMatcher` (class) — `tests/test_core/test_transport_matcher.py:9`
- `TestSubjectValidation` (class) — `tests/test_core/test_transport_matcher.py:43`
- `pytestmark` (const) — `tests/test_core/test_transport_nats_wire.py:26`
- `TestHandCraftedDecode` (class) — `tests/test_core/test_transport_nats_wire.py:68`
- `TestSchemaVersion` (class) — `tests/test_core/test_transport_nats_wire.py:105`
- `TestMalformedHeaders` (class) — `tests/test_core/test_transport_nats_wire.py:182`
- `TestPublishHeaders` (class) — `tests/test_core/test_transport_nats_wire.py:263`
- `pytestmark` (const) — `tests/test_integration.py:28`
- `TestTerminalToResult` (class) — `tests/test_integration.py:55`
- `TestSchedulerTriggerIntegration` (class) — `tests/test_integration.py:249`
- `TestWebhookIntegration` (class) — `tests/test_integration.py:325`
- `test_version_exists` (function) — `tests/test_scaffold.py:12`
- `test_package_importable` (function) — `tests/test_scaffold.py:21`
- `test_main_module_exists` (function) — `tests/test_scaffold.py:27`
- `test_main_is_coroutine` (function) — `tests/test_scaffold.py:33`
- `test_entry_point_runs` (function) — `tests/test_scaffold.py:42`
- `TestScheduleItemConfigValidation` (class) — `tests/test_triggers/test_scheduler.py:60`
- `TestSchedulerTriggerInit` (class) — `tests/test_triggers/test_scheduler.py:109`
- `TestIntervalScheduling` (class) — `tests/test_triggers/test_scheduler.py:131`
- `TestCronScheduling` (class) — `tests/test_triggers/test_scheduler.py:187`
- `TestDisabledSchedules` (class) — `tests/test_triggers/test_scheduler.py:293`
- `TestLifecycle` (class) — `tests/test_triggers/test_scheduler.py:350`
- `TestPublicExports` (class) — `tests/test_triggers/test_scheduler.py:419`
- `TestTelegramTriggerInit` (class) — `tests/test_triggers/test_telegram.py:70`
- `TestHandleUpdate` (class) — `tests/test_triggers/test_telegram.py:94`
- `TestGetUpdates` (class) — `tests/test_triggers/test_telegram.py:246`
- `TestPollLoop` (class) — `tests/test_triggers/test_telegram.py:381`
- `TestStartStop` (class) — `tests/test_triggers/test_telegram.py:511`
- `TestTelegramConfigDefaults` (class) — `tests/test_triggers/test_telegram.py:563`
- `TestPublicExports` (class) — `tests/test_triggers/test_telegram.py:569`
- `TestProcessLine` (class) — `tests/test_triggers/test_terminal.py:17`
- `TestQuitCommands` (class) — `tests/test_triggers/test_terminal.py:172`
- `TestTriggerABC` (class) — `tests/test_triggers/test_terminal.py:184`
- `TestTerminalTriggerState` (class) — `tests/test_triggers/test_terminal.py:200`
- `TestPublicExports` (class) — `tests/test_triggers/test_terminal.py:215`
- `pytestmark` (const) — `tests/test_triggers/test_webhook.py:36`
- `TestInflightLimiter` (class) — `tests/test_triggers/test_webhook.py:39`
- `TestSafeHeaders` (class) — `tests/test_triggers/test_webhook.py:78`
- `TestVerifyAuthHMAC` (class) — `tests/test_triggers/test_webhook.py:138`
- `TestVerifyAuthBearer` (class) — `tests/test_triggers/test_webhook.py:192`
- `TestVerifyAuthNone` (class) — `tests/test_triggers/test_webhook.py:225`
- `TestLifecycle` (class) — `tests/test_triggers/test_webhook.py:232`
- `TestHappyPathHMAC` (class) — `tests/test_triggers/test_webhook.py:361`
- `TestStatusCodes` (class) — `tests/test_triggers/test_webhook.py:402`
- `TestHappyPathBearer` (class) — `tests/test_triggers/test_webhook.py:504`
- `TestHeaderWhitelistE2E` (class) — `tests/test_triggers/test_webhook.py:520`
- `TestUnauthenticatedOpenPath` (class) — `tests/test_triggers/test_webhook.py:547`
- `TestInflightCap` (class) — `tests/test_triggers/test_webhook.py:558`
- `TestBusPublishFailure` (class) — `tests/test_triggers/test_webhook.py:612`
- `TestCancelledErrorPassthrough` (class) — `tests/test_triggers/test_webhook.py:633`
- `TestOuterErrorGuard` (class) — `tests/test_triggers/test_webhook.py:654`
- `TestDrainOnStop` (class) — `tests/test_triggers/test_webhook.py:678`
- `pytestmark` (const) — `tests/test_workers/test_llm.py:15`
- `TestHappyPath` (class) — `tests/test_workers/test_llm.py:62`
- `TestRetry` (class) — `tests/test_workers/test_llm.py:112`
- `TestFallback` (class) — `tests/test_workers/test_llm.py:149`
- `TestNonTransient` (class) — `tests/test_workers/test_llm.py:298`
- `TestContextVars` (class) — `tests/test_workers/test_llm.py:332`
- `TestUsageExtraction` (class) — `tests/test_workers/test_llm.py:383`
- `TestTelemetryMechanics` (class) — `tests/test_workers/test_llm.py:431`
- `TestPersistenceIsNonFatal` (class) — `tests/test_workers/test_llm.py:474`
- `make_text_response` (function) — `tests/test_workers/test_runtime.py:17`
- `make_tool_call` (function) — `tests/test_workers/test_runtime.py:22`
- `TestToolDef` (class) — `tests/test_workers/test_runtime.py:36`
- `TestToolResult` (class) — `tests/test_workers/test_runtime.py:53`
- `TestAgentResult` (class) — `tests/test_workers/test_runtime.py:66`
- `TestAgentRuntimeNoTools` (class) — `tests/test_workers/test_runtime.py:83`
- `TestAgentRuntimeToolCalls` (class) — `tests/test_workers/test_runtime.py:144`
- `TestAgentRuntimeMaxTurns` (class) — `tests/test_workers/test_runtime.py:276`
- `TestAgentRuntimeUnknownTool` (class) — `tests/test_workers/test_runtime.py:337`
- `TestAgentRuntimeEdgeCases` (class) — `tests/test_workers/test_runtime.py:391`
- `TestAgentRuntimeToolErrors` (class) — `tests/test_workers/test_runtime.py:465`
- `TestPublicExports` (class) — `tests/test_workers/test_runtime.py:497`
- `TestTopoSortLinearChain` (class) — `tests/test_workflow/test_dag.py:14`
- `TestTopoSortParallel` (class) — `tests/test_workflow/test_dag.py:38`
- `TestTopoSortCycleDetection` (class) — `tests/test_workflow/test_dag.py:67`
- `TestDAGExecutorSingleStep` (class) — `tests/test_workflow/test_dag.py:123`
- `TestDAGExecutorLinear` (class) — `tests/test_workflow/test_dag.py:135`
- `TestDAGExecutorParallel` (class) — `tests/test_workflow/test_dag.py:161`
- `TestDAGExecutorFailurePropagation` (class) — `tests/test_workflow/test_dag.py:196`
- `TestDAGExecutorResults` (class) — `tests/test_workflow/test_dag.py:258`
- `TestStepResultModel` (class) — `tests/test_workflow/test_dag.py:294`
- `TestImports` (class) — `tests/test_workflow/test_dag.py:315`
- `TestWorkflowResultModel` (class) — `tests/test_workflow/test_engine.py:53`
- `TestSimpleWorkflow` (class) — `tests/test_workflow/test_engine.py:84`
- `TestDAGWorkflow` (class) — `tests/test_workflow/test_engine.py:133`
- `TestUnsupportedModes` (class) — `tests/test_workflow/test_engine.py:225`
- `TestStepIdContext` (class) — `tests/test_workflow/test_engine.py:256`
- `TestImports` (class) — `tests/test_workflow/test_engine.py:302`
- `TestWorkflowMode` (class) — `tests/test_workflow/test_spec.py:15`
- `TestStepType` (class) — `tests/test_workflow/test_spec.py:26`
- `TestStepRetry` (class) — `tests/test_workflow/test_spec.py:38`
- `TestStep` (class) — `tests/test_workflow/test_spec.py:50`
- `TestWorkflowPolicies` (class) — `tests/test_workflow/test_spec.py:108`
- `TestWorkflowSpec` (class) — `tests/test_workflow/test_spec.py:129`

## Modules

_64 files, 275 public symbols, 367 internal imports._

- `src/proctor/__init__.py` (python)
- `src/proctor/__main__.py` (python)
- `src/proctor/core/__init__.py` (python)
- `src/proctor/core/bootstrap.py` (python)
- `src/proctor/core/bus.py` (python)
- `src/proctor/core/config.py` (python)
- `src/proctor/core/memory.py` (python)
- `src/proctor/core/models.py` (python)
- `src/proctor/core/router.py` (python)
- `src/proctor/core/state.py` (python)
- `src/proctor/core/transport/__init__.py` (python)
- `src/proctor/core/transport/base.py` (python)
- `src/proctor/core/transport/errors.py` (python)
- `src/proctor/core/transport/local.py` (python)
- `src/proctor/core/transport/nats.py` (python)
- `src/proctor/triggers/__init__.py` (python)
- `src/proctor/triggers/base.py` (python)
- `src/proctor/triggers/scheduler.py` (python)
- `src/proctor/triggers/telegram.py` (python)
- `src/proctor/triggers/terminal.py` (python)
- `src/proctor/triggers/webhook.py` (python)
- `src/proctor/workers/__init__.py` (python)
- `src/proctor/workers/llm.py` (python)
- `src/proctor/workers/runtime.py` (python)
- `src/proctor/workflow/__init__.py` (python)
- `src/proctor/workflow/dag.py` (python)
- `src/proctor/workflow/engine.py` (python)
- `src/proctor/workflow/spec.py` (python)
- `tests/__init__.py` (python)
- `tests/conftest.py` (python)
- `tests/integration/__init__.py` (python)
- `tests/integration/conftest.py` (python)
- `tests/integration/test_llm_ollama.py` (python)
- `tests/integration/test_transport_contract.py` (python)
- `tests/integration/test_transport_nats_reconnect.py` (python)
- `tests/test_core/__init__.py` (python)
- `tests/test_core/test_bootstrap.py` (python)
- `tests/test_core/test_bus.py` (python)
- `tests/test_core/test_config.py` (python)
- `tests/test_core/test_memory.py` (python)
- `tests/test_core/test_models.py` (python)
- `tests/test_core/test_rate_limited_logger.py` (python)
- `tests/test_core/test_router.py` (python)
- `tests/test_core/test_state.py` (python)
- `tests/test_core/test_transport_base.py` (python)
- `tests/test_core/test_transport_dedup.py` (python)
- `tests/test_core/test_transport_errors.py` (python)
- `tests/test_core/test_transport_local.py` (python)
- `tests/test_core/test_transport_matcher.py` (python)
- `tests/test_core/test_transport_nats_wire.py` (python)
- `tests/test_integration.py` (python)
- `tests/test_scaffold.py` (python)
- `tests/test_triggers/__init__.py` (python)
- `tests/test_triggers/test_scheduler.py` (python)
- `tests/test_triggers/test_telegram.py` (python)
- `tests/test_triggers/test_terminal.py` (python)
- `tests/test_triggers/test_webhook.py` (python)
- `tests/test_workers/__init__.py` (python)
- `tests/test_workers/test_llm.py` (python)
- `tests/test_workers/test_runtime.py` (python)
- `tests/test_workflow/__init__.py` (python)
- `tests/test_workflow/test_dag.py` (python)
- `tests/test_workflow/test_engine.py` (python)
- `tests/test_workflow/test_spec.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-05-26T08:18:45Z): project added (added)

## Drift findings

_None._
