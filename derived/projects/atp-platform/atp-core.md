<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: python
name: atp-core
parent: atp-platform
prograph: project
root: ./atp-platform/packages/atp-core
snapshot: 4
---

# atp-core

## Manifest

- declared package: `atp-core` version `1.0.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `logger` (const) — `atp/chaos/concurrency.py:13`
- `stress_test_async` (function) — `atp/chaos/concurrency.py:32`
- `stress_test_sync` (function) — `atp/chaos/concurrency.py:70`
- `logger` (const) — `atp/chaos/injectors.py:24`
- `ChaosError` (class) — `atp/chaos/injectors.py:27`
- `ToolFailureError` (class) — `atp/chaos/injectors.py:41`
- `RateLimitError` (class) — `atp/chaos/injectors.py:59`
- `TokenLimitError` (class) — `atp/chaos/injectors.py:71`
- `ChaosInjector` (class) — `atp/chaos/injectors.py:85`
- `RateLimiter` (class) — `atp/chaos/injectors.py:438`
- `LatencyInjector` (class) — `atp/chaos/injectors.py:507`
- `ToolFailureInjector` (class) — `atp/chaos/injectors.py:547`
- `TokenLimitInjector` (class) — `atp/chaos/injectors.py:596`
- `PartialResponseInjector` (class) — `atp/chaos/injectors.py:630`
- `ErrorType` (class) — `atp/chaos/models.py:9`
- `ToolFailureConfig` (class) — `atp/chaos/models.py:20`
- `LatencyConfig` (class) — `atp/chaos/models.py:43`
- `TokenLimitConfig` (class) — `atp/chaos/models.py:63`
- `PartialResponseConfig` (class) — `atp/chaos/models.py:74`
- `RateLimitConfig` (class) — `atp/chaos/models.py:100`
- `ChaosConfig` (class) — `atp/chaos/models.py:113`
- `ChaosProfile` (class) — `atp/chaos/models.py:159`
- `DEFAULT_ERROR_MESSAGES` (const) — `atp/chaos/models.py:173`
- `get_profile` (function) — `atp/chaos/profiles.py:15`
- `list_profiles` (function) — `atp/chaos/profiles.py:39`
- `get_profile_description` (function) — `atp/chaos/profiles.py:48`
- `ATPError` (class) — `atp/core/exceptions.py:4`
- `LoaderError` (class) — `atp/core/exceptions.py:8`
- `ValidationError` (class) — `atp/core/exceptions.py:12`
- `ParseError` (class) — `atp/core/exceptions.py:43`
- `ATP_VERSION` (const) — `atp/core/logging.py:42`
- `SENSITIVE_KEY_PATTERNS` (const) — `atp/core/logging.py:54`
- `generate_correlation_id` (function) — `atp/core/logging.py:73`
- `get_correlation_id` (function) — `atp/core/logging.py:82`
- `set_correlation_id` (function) — `atp/core/logging.py:91`
- `correlation_context` (class) — `atp/core/logging.py:100`
- `bind_context` (class) — `atp/core/logging.py:141`
- `add_correlation_id` (function) — `atp/core/logging.py:176`
- `add_bound_context` (function) — `atp/core/logging.py:186`
- `add_common_fields` (function) — `atp/core/logging.py:207`
- `redact_sensitive_data` (function) — `atp/core/logging.py:222`
- `sanitize_event` (function) — `atp/core/logging.py:264`
- `filter_by_module_level` (function) — `atp/core/logging.py:274`
- `set_module_log_level` (function) — `atp/core/logging.py:319`
- `get_module_log_level` (function) — `atp/core/logging.py:333`
- `clear_module_log_levels` (function) — `atp/core/logging.py:345`
- `StructlogHandler` (class) — `atp/core/logging.py:392`
- `configure_logging` (function) — `atp/core/logging.py:454`
- `configure_logging_from_settings` (function) — `atp/core/logging.py:549`
- `get_logger` (function) — `atp/core/logging.py:567`
- `log_with_context` (function) — `atp/core/logging.py:588`
- `create_test_logger` (function) — `atp/core/logging.py:611`
- `reset_logging` (function) — `atp/core/logging.py:642`
- `logger` (const) — `atp/core/metrics.py:54`
- `MetricsSettings` (class) — `atp/core/metrics.py:66`
- `ATPMetrics` (class) — `atp/core/metrics.py:107`
- `configure_metrics` (function) — `atp/core/metrics.py:354`
- `reset_metrics` (function) — `atp/core/metrics.py:410`
- `get_metrics` (function) — `atp/core/metrics.py:467`
- `get_registry` (function) — `atp/core/metrics.py:479`
- `generate_metrics` (function) — `atp/core/metrics.py:490`
- `record_llm_call` (function) — `atp/core/metrics.py:619`
- `record_adapter_error` (function) — `atp/core/metrics.py:643`
- `logger` (const) — `atp/core/observer.py:13`
- `Observer` (class) — `atp/core/observer.py:34`
- `LoggingObserver` (class) — `atp/core/observer.py:42`
- `ErrorCollector` (class) — `atp/core/observer.py:60`
- `CompositeObserver` (class) — `atp/core/observer.py:104`
- `get_observer` (function) — `atp/core/observer.py:123`
- `set_observer` (function) — `atp/core/observer.py:128`
- `EvalCheck` (class) — `atp/core/results.py:33`
- `CaseVerdict` (class) — `atp/core/results.py:43`
- `EvalResult` (class) — `atp/core/results.py:66`
- `ProgressEventType` (class) — `atp/core/results.py:133`
- `ProgressEvent` (class) — `atp/core/results.py:147`
- `ProgressCallback` (const) — `atp/core/results.py:173`
- `TestReport` (class) — `atp/core/results.py:333`
- `SuiteReport` (class) — `atp/core/results.py:355`
- `rebuild_report_models` (function) — `atp/core/results.py:429`
- `logger` (const) — `atp/core/security.py:24`
- `audit_logger` (const) — `atp/core/security.py:25`
- `SECRET_PATTERNS` (const) — `atp/core/security.py:34`
- `SENSITIVE_ENV_PATTERNS` (const) — `atp/core/security.py:148`
- `SAFE_ENV_ALLOWLIST` (const) — `atp/core/security.py:172`
- `ALLOWED_URL_SCHEMES` (const) — `atp/core/security.py:205`
- `INTERNAL_IP_RANGES` (const) — `atp/core/security.py:208`
- `METADATA_ENDPOINTS` (const) — `atp/core/security.py:220`
- `DOCKER_IMAGE_PATTERN` (const) — `atp/core/security.py:228`
- `VALID_NETWORK_MODES` (const) — `atp/core/security.py:235`
- `MAX_MEMORY_BYTES` (const) — `atp/core/security.py:238`
- `MAX_CPU_CORES` (const) — `atp/core/security.py:239`
- `MAX_TIMEOUT_SECONDS` (const) — `atp/core/security.py:240`
- `MAX_PATH_LENGTH` (const) — `atp/core/security.py:241`
- `MAX_DESCRIPTION_LENGTH` (const) — `atp/core/security.py:242`
- `MAX_REQUEST_SIZE_BYTES` (const) — `atp/core/security.py:245`
- `MAX_RESPONSE_SIZE_BYTES` (const) — `atp/core/security.py:246`
- `MAX_ARTIFACTS_COUNT` (const) — `atp/core/security.py:247`
- `MAX_ENV_VARS_COUNT` (const) — `atp/core/security.py:248`
- `MAX_OBJECT_DEPTH` (const) — `atp/core/security.py:249`
- `MAX_ARRAY_SIZE` (const) — `atp/core/security.py:250`
- `REDACTED` (const) — `atp/core/security.py:253`
- `SAFE_COMMAND_BINARIES` (const) — `atp/core/security.py:256`
- `SecurityEventType` (class) — `atp/core/security.py:277`
- `SecurityValidationError` (class) — `atp/core/security.py:294`
- `log_security_event` (function) — `atp/core/security.py:328`
- `validate_request_size` (function) — `atp/core/security.py:373`
- `validate_object_depth` (function) — `atp/core/security.py:395`
- `validate_artifacts_count` (function) — `atp/core/security.py:436`
- `validate_env_vars_count` (function) — `atp/core/security.py:454`
- `validate_path_within_workspace` (function) — `atp/core/security.py:478`
- `open_file_safely` (function) — `atp/core/security.py:577`
- `sanitize_filename` (function) — `atp/core/security.py:629`
- `validate_url` (function) — `atp/core/security.py:665`
- `validate_url_with_dns` (function) — `atp/core/security.py:765`
- `validate_docker_image` (function) — `atp/core/security.py:842`
- `validate_docker_network` (function) — `atp/core/security.py:876`
- `validate_volume_mount` (function) — `atp/core/security.py:902`
- `parse_memory_limit` (function) — `atp/core/security.py:964`
- `validate_cpu_limit` (function) — `atp/core/security.py:1024`
- `validate_timeout` (function) — `atp/core/security.py:1066`
- `redact_secrets` (function) — `atp/core/security.py:1101`
- `is_sensitive_env_var` (function) — `atp/core/security.py:1126`
- `filter_environment_variables` (function) — `atp/core/security.py:1146`
- `sanitize_env_value` (function) — `atp/core/security.py:1202`
- `redact_dict_secrets` (function) — `atp/core/security.py:1240`
- `validate_task_description` (function) — `atp/core/security.py:1289`
- `validate_command` (function) — `atp/core/security.py:1317`
- `escape_shell_arg` (function) — `atp/core/security.py:1391`
- `validate_task_id` (function) — `atp/core/security.py:1406`
- `SecureFormatter` (class) — `atp/core/security.py:1449`
- `sanitize_log_message` (function) — `atp/core/security.py:1458`
- `sanitize_error_message` (function) — `atp/core/security.py:1486`
- `setup_secure_logging` (function) — `atp/core/security.py:1527`
- `logger` (const) — `atp/core/settings.py:33`
- `CONFIG_FILE_NAMES` (const) — `atp/core/settings.py:36`
- `DashboardSettings` (class) — `atp/core/settings.py:110`
- `RunnerSettings` (class) — `atp/core/settings.py:200`
- `LLMSettings` (class) — `atp/core/settings.py:234`
- `LoggingSettings` (class) — `atp/core/settings.py:271`
- `ATPSettings` (class) — `atp/core/settings.py:302`
- `get_settings` (function) — `atp/core/settings.py:534`
- `generate_json_schema` (function) — `atp/core/settings.py:588`
- `generate_example_config` (function) — `atp/core/settings.py:618`
- `logger` (const) — `atp/core/telemetry.py:64`
- `P` (const) — `atp/core/telemetry.py:67`
- `R` (const) — `atp/core/telemetry.py:68`
- `TelemetrySettings` (class) — `atp/core/telemetry.py:80`
- `InMemorySpanExporter` (class) — `atp/core/telemetry.py:164`
- `get_debug_exporter` (function) — `atp/core/telemetry.py:321`
- `configure_telemetry` (function) — `atp/core/telemetry.py:340`
- `reset_telemetry` (function) — `atp/core/telemetry.py:463`
- `add_exporter_to_provider` (function) — `atp/core/telemetry.py:486`
- `ensure_debug_exporter` (function) — `atp/core/telemetry.py:509`
- `get_tracer` (function) — `atp/core/telemetry.py:567`
- `get_current_span` (function) — `atp/core/telemetry.py:579`
- `set_span_attribute` (function) — `atp/core/telemetry.py:588`
- `set_span_attributes` (function) — `atp/core/telemetry.py:603`
- `add_span_event` (function) — `atp/core/telemetry.py:615`
- `record_exception` (function) — `atp/core/telemetry.py:633`
- `inject_trace_context` (function) — `atp/core/telemetry.py:656`
- `extract_trace_context` (function) — `atp/core/telemetry.py:674`
- `span` (function) — `atp/core/telemetry.py:692`
- `create_test_span` (function) — `atp/core/telemetry.py:770`
- `create_adapter_span` (function) — `atp/core/telemetry.py:804`
- `create_evaluator_span` (function) — `atp/core/telemetry.py:834`
- `set_test_result_attributes` (function) — `atp/core/telemetry.py:864`
- `set_adapter_response_attributes` (function) — `atp/core/telemetry.py:891`
- `set_evaluator_result_attributes` (function) — `atp/core/telemetry.py:916`
- `USAGE_CONTRACT` (const) — `atp/cost/cloud_pricer.py:22`
- `PRICING_INSTALL_HINT` (const) — `atp/cost/cloud_pricer.py:23`
- `PricingDependencyError` (class) — `atp/cost/cloud_pricer.py:29`
- `CloudPricer` (class) — `atp/cost/cloud_pricer.py:157`
- `logger` (const) — `atp/cost/models.py:14`
- `logger` (const) — `atp/cost/tracker.py:13`
- `CostPersistenceBackend` (class) — `atp/cost/tracker.py:16`
- `CostTracker` (class) — `atp/cost/tracker.py:37`
- `get_cost_tracker` (function) — `atp/cost/tracker.py:294`
- `set_cost_tracker` (function) — `atp/cost/tracker.py:306`
- `shutdown_cost_tracker` (function) — `atp/cost/tracker.py:312`
- `TagFilter` (class) — `atp/loader/filters.py:6`
- `logger` (const) — `atp/loader/format_dispatch.py:20`
- `SuiteFormatDetector` (const) — `atp/loader/format_dispatch.py:23`
- `SuiteFormatHandler` (const) — `atp/loader/format_dispatch.py:27`
- `SuiteFormatRegistry` (class) — `atp/loader/format_dispatch.py:30`
- `get_suite_format_registry` (function) — `atp/loader/format_dispatch.py:90`
- `TestLoader` (class) — `atp/loader/loader.py:14`
- `MultiAgentMode` (class) — `atp/loader/models.py:11`
- `CollaborationConfig` (class) — `atp/loader/models.py:19`
- `HandoffTrigger` (class) — `atp/loader/models.py:44`
- `ContextAccumulationMode` (class) — `atp/loader/models.py:54`
- `HandoffConfig` (class) — `atp/loader/models.py:63`
- `ComparisonConfig` (class) — `atp/loader/models.py:91`
- `TaskDefinition` (class) — `atp/loader/models.py:106`
- `Constraints` (class) — `atp/loader/models.py:122`
- `Assertion` (class) — `atp/loader/models.py:139`
- `ScoringWeights` (class) — `atp/loader/models.py:153`
- `TestDefinition` (class) — `atp/loader/models.py:162`
- `AgentConfig` (class) — `atp/loader/models.py:269`
- `ChaosSettings` (class) — `atp/loader/models.py:279`
- `TestDefaults` (class) — `atp/loader/models.py:304`
- `TestSuite` (class) — `atp/loader/models.py:320`
- `YAMLParser` (class) — `atp/loader/parser.py:14`
- `VariableSubstitution` (class) — `atp/loader/parser.py:90`
- `COLLABORATION_CONFIG_SCHEMA` (const) — `atp/loader/schema.py:6`
- `HANDOFF_CONFIG_SCHEMA` (const) — `atp/loader/schema.py:27`
- `COMPARISON_CONFIG_SCHEMA` (const) — `atp/loader/schema.py:53`
- `TEST_SUITE_SCHEMA` (const) — `atp/loader/schema.py:67`
- `validate_schema` (function) — `atp/loader/schema.py:254`
- `logger` (const) — `atp/loader/suite_source.py:20`
- `SuiteSourceDetector` (const) — `atp/loader/suite_source.py:23`
- `SuiteSourceLoader` (const) — `atp/loader/suite_source.py:25`
- `SuiteSourceRegistry` (class) — `atp/loader/suite_source.py:28`
- `get_suite_source_registry` (function) — `atp/loader/suite_source.py:68`
- `CatalogError` (class) — `atp/model_catalog/errors.py:10`
- `CatalogNotConfiguredError` (class) — `atp/model_catalog/errors.py:14`
- `CatalogTOMLError` (class) — `atp/model_catalog/errors.py:22`
- `CatalogSchemaError` (class) — `atp/model_catalog/errors.py:26`
- `logger` (const) — `atp/model_catalog/loader.py:30`
- `resolve_catalog_path` (function) — `atp/model_catalog/loader.py:49`
- `load_catalog` (function) — `atp/model_catalog/loader.py:78`
- `resolve_default_model` (function) — `atp/model_catalog/loader.py:93`
- `read_template` (function) — `atp/model_catalog/loader.py:118`
- `ModelEntry` (class) — `atp/model_catalog/schema.py:16`
- `HarnessEntry` (class) — `atp/model_catalog/schema.py:26`
- `AgentEntry` (class) — `atp/model_catalog/schema.py:38`
- `CatalogDefaults` (class) — `atp/model_catalog/schema.py:49`
- `ModelCatalog` (class) — `atp/model_catalog/schema.py:57`
- `PROTOCOL_VERSION` (const) — `atp/protocol/_version.py:3`
- `SUPPORTED_VERSIONS` (const) — `atp/protocol/_version.py:5`
- `MAX_TASK_ID_LENGTH` (const) — `atp/protocol/models.py:14`
- `MAX_DESCRIPTION_LENGTH` (const) — `atp/protocol/models.py:15`
- `MAX_PATH_LENGTH` (const) — `atp/protocol/models.py:16`
- `MAX_ERROR_LENGTH` (const) — `atp/protocol/models.py:17`
- `MAX_CONTENT_LENGTH` (const) — `atp/protocol/models.py:18`
- `MAX_ARTIFACTS_COUNT` (const) — `atp/protocol/models.py:19`
- `MAX_ENV_VARS_COUNT` (const) — `atp/protocol/models.py:20`
- `MAX_METADATA_KEYS` (const) — `atp/protocol/models.py:21`
- `TASK_ID_PATTERN` (const) — `atp/protocol/models.py:24`
- `ResponseStatus` (class) — `atp/protocol/models.py:27`
- `EventType` (class) — `atp/protocol/models.py:37`
- `Task` (class) — `atp/protocol/models.py:47`
- `Context` (class) — `atp/protocol/models.py:94`
- `ATPRequest` (class) — `atp/protocol/models.py:162`
- `Metrics` (class) — `atp/protocol/models.py:216`
- `ArtifactFile` (class) — `atp/protocol/models.py:237`
- `ArtifactStructured` (class) — `atp/protocol/models.py:285`
- `ArtifactReference` (class) — `atp/protocol/models.py:310`
- `Artifact` (const) — `atp/protocol/models.py:332`
- `ATPResponse` (class) — `atp/protocol/models.py:335`
- `ToolCallPayload` (class) — `atp/protocol/models.py:389`
- `LLMRequestPayload` (class) — `atp/protocol/models.py:401`
- `ReasoningPayload` (class) — `atp/protocol/models.py:412`
- `ErrorPayload` (class) — `atp/protocol/models.py:420`
- `ProgressPayload` (class) — `atp/protocol/models.py:428`
- `EventPayload` (const) — `atp/protocol/models.py:438`
- `ATPEvent` (class) — `atp/protocol/models.py:448`
- `generate_request_schema` (function) — `atp/protocol/schema.py:8`
- `generate_response_schema` (function) — `atp/protocol/schema.py:13`
- `generate_event_schema` (function) — `atp/protocol/schema.py:18`
- `generate_all_schemas` (function) — `atp/protocol/schema.py:23`
- `ScoreAggregator` (class) — `atp/scoring/aggregator.py:18`
- `NormalizationConfig` (class) — `atp/scoring/models.py:8`
- `ComponentScore` (class) — `atp/scoring/models.py:33`
- `ScoreBreakdown` (class) — `atp/scoring/models.py:50`
- `ScoredTestResult` (class) — `atp/scoring/models.py:109`
- `CV_STABLE_THRESHOLD` (const) — `atp/statistics/calculator.py:14`
- `CV_MODERATE_THRESHOLD` (const) — `atp/statistics/calculator.py:15`
- `CV_UNSTABLE_THRESHOLD` (const) — `atp/statistics/calculator.py:16`
- `T_CRITICAL_VALUES` (const) — `atp/statistics/calculator.py:20`
- `StatisticsCalculator` (class) — `atp/statistics/calculator.py:72`
- `StabilityLevel` (class) — `atp/statistics/models.py:9`
- `StabilityAssessment` (class) — `atp/statistics/models.py:18`
- `StatisticalResult` (class) — `atp/statistics/models.py:33`
- `MetricStatistics` (class) — `atp/statistics/models.py:69`
- `TestRunStatistics` (class) — `atp/statistics/models.py:78`
- `StatisticalReporter` (class) — `atp/statistics/reporter.py:13`
- `logger` (const) — `atp/streaming/buffer.py:11`
- `DEFAULT_MAX_EVENTS` (const) — `atp/streaming/buffer.py:13`
- `EventBuffer` (class) — `atp/streaming/buffer.py:16`
- `EventReplayIterator` (class) — `atp/streaming/buffer.py:202`
- `BufferingEventIterator` (class) — `atp/streaming/buffer.py:268`
- `EventOrderingError` (class) — `atp/streaming/validation.py:10`
- `EventValidator` (class) — `atp/streaming/validation.py:34`
- `validate_event_sequence` (function) — `atp/streaming/validation.py:120`
- `ValidatingEventIterator` (class) — `atp/streaming/validation.py:178`

## Modules

_45 files, 285 public symbols, 14 internal imports._

- `atp/chaos/__init__.py` (python)
- `atp/chaos/concurrency.py` (python)
- `atp/chaos/injectors.py` (python)
- `atp/chaos/models.py` (python)
- `atp/chaos/profiles.py` (python)
- `atp/core/__init__.py` (python)
- `atp/core/exceptions.py` (python)
- `atp/core/logging.py` (python)
- `atp/core/metrics.py` (python)
- `atp/core/observer.py` (python)
- `atp/core/result.py` (python)
- `atp/core/results.py` (python)
- `atp/core/security.py` (python)
- `atp/core/settings.py` (python)
- `atp/core/telemetry.py` (python)
- `atp/cost/__init__.py` (python)
- `atp/cost/cloud_pricer.py` (python)
- `atp/cost/models.py` (python)
- `atp/cost/tracker.py` (python)
- `atp/loader/__init__.py` (python)
- `atp/loader/filters.py` (python)
- `atp/loader/format_dispatch.py` (python)
- `atp/loader/loader.py` (python)
- `atp/loader/models.py` (python)
- `atp/loader/parser.py` (python)
- `atp/loader/schema.py` (python)
- `atp/loader/suite_source.py` (python)
- `atp/model_catalog/__init__.py` (python)
- `atp/model_catalog/errors.py` (python)
- `atp/model_catalog/loader.py` (python)
- `atp/model_catalog/schema.py` (python)
- `atp/protocol/__init__.py` (python)
- `atp/protocol/_version.py` (python)
- `atp/protocol/models.py` (python)
- `atp/protocol/schema.py` (python)
- `atp/scoring/__init__.py` (python)
- `atp/scoring/aggregator.py` (python)
- `atp/scoring/models.py` (python)
- `atp/statistics/__init__.py` (python)
- `atp/statistics/calculator.py` (python)
- `atp/statistics/models.py` (python)
- `atp/statistics/reporter.py` (python)
- `atp/streaming/__init__.py` (python)
- `atp/streaming/buffer.py` (python)
- `atp/streaming/validation.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

- ← [[atp-adapters]] · `package_dep` · `atp-core`
- ← [[atp-dashboard]] · `package_dep` · `atp-core`
- ← [[atp-platform]] · `package_dep` · `atp-core`

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
