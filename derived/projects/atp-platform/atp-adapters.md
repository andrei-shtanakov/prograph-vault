<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: python
name: atp-adapters
parent: atp-platform
prograph: project
root: ./atp-platform/packages/atp-adapters
snapshot: 1
---

# atp-adapters

## Manifest

- declared package: `atp-adapters` version `1.0.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `logger` (const) — `atp/adapters/autogen.py:27`
- `AutoGenAdapterConfig` (class) — `atp/adapters/autogen.py:30`
- `AutoGenAdapter` (class) — `atp/adapters/autogen.py:52`
- `AzureOpenAIAdapter` (class) — `atp/adapters/azure_openai/adapter.py:31`
- `get_openai_client` (function) — `atp/adapters/azure_openai/auth.py:13`
- `get_azure_ad_token_provider` (function) — `atp/adapters/azure_openai/auth.py:69`
- `AzureOpenAIAdapterConfig` (class) — `atp/adapters/azure_openai/models.py:10`
- `logger` (const) — `atp/adapters/base.py:25`
- `tracer` (const) — `atp/adapters/base.py:26`
- `AdapterConfig` (class) — `atp/adapters/base.py:29`
- `AgentAdapter` (class) — `atp/adapters/base.py:46`
- `track_response_cost` (function) — `atp/adapters/base.py:312`
- `BedrockAdapter` (class) — `atp/adapters/bedrock/adapter.py:30`
- `create_boto3_client` (function) — `atp/adapters/bedrock/auth.py:10`
- `BedrockAdapterConfig` (class) — `atp/adapters/bedrock/models.py:10`
- `logger` (const) — `atp/adapters/cli.py:31`
- `CLIAdapterConfig` (class) — `atp/adapters/cli.py:34`
- `CLIAdapter` (class) — `atp/adapters/cli.py:58`
- `ContainerResources` (class) — `atp/adapters/container.py:41`
- `ContainerAdapterConfig` (class) — `atp/adapters/container.py:55`
- `ContainerAdapter` (class) — `atp/adapters/container.py:121`
- `CrewAIAdapterConfig` (class) — `atp/adapters/crewai.py:27`
- `CrewAIAdapter` (class) — `atp/adapters/crewai.py:42`
- `AdapterError` (class) — `atp/adapters/exceptions.py:6`
- `AdapterTimeoutError` (class) — `atp/adapters/exceptions.py:20`
- `AdapterConnectionError` (class) — `atp/adapters/exceptions.py:33`
- `AdapterResponseError` (class) — `atp/adapters/exceptions.py:47`
- `AdapterNotFoundError` (class) — `atp/adapters/exceptions.py:62`
- `logger` (const) — `atp/adapters/fallback.py:11`
- `FallbackAdapter` (class) — `atp/adapters/fallback.py:14`
- `HTTPAdapterConfig` (class) — `atp/adapters/http.py:25`
- `HTTPAdapter` (class) — `atp/adapters/http.py:85`
- `LangGraphAdapterConfig` (class) — `atp/adapters/langgraph.py:27`
- `LangGraphAdapter` (class) — `atp/adapters/langgraph.py:47`
- `logger` (const) — `atp/adapters/mcp/adapter.py:33`
- `MCPTool` (class) — `atp/adapters/mcp/adapter.py:36`
- `MCPResource` (class) — `atp/adapters/mcp/adapter.py:46`
- `MCPPrompt` (class) — `atp/adapters/mcp/adapter.py:55`
- `MCPServerInfo` (class) — `atp/adapters/mcp/adapter.py:65`
- `MCPAdapterConfig` (class) — `atp/adapters/mcp/adapter.py:76`
- `MCPAdapter` (class) — `atp/adapters/mcp/adapter.py:150`
- `TransportState` (class) — `atp/adapters/mcp/transport.py:21`
- `TransportConfig` (class) — `atp/adapters/mcp/transport.py:31`
- `JSONRPCMessage` (class) — `atp/adapters/mcp/transport.py:57`
- `JSONRPCError` (class) — `atp/adapters/mcp/transport.py:90`
- `create_jsonrpc_request` (function) — `atp/adapters/mcp/transport.py:100`
- `create_jsonrpc_response` (function) — `atp/adapters/mcp/transport.py:123`
- `parse_jsonrpc_message` (function) — `atp/adapters/mcp/transport.py:146`
- `MCPTransport` (class) — `atp/adapters/mcp/transport.py:175`
- `StdioTransportConfig` (class) — `atp/adapters/mcp/transport.py:375`
- `StdioTransport` (class) — `atp/adapters/mcp/transport.py:406`
- `SSETransportConfig` (class) — `atp/adapters/mcp/transport.py:702`
- `SSETransport` (class) — `atp/adapters/mcp/transport.py:727`
- `logger` (const) — `atp/adapters/registry.py:12`
- `AdapterRegistry` (class) — `atp/adapters/registry.py:89`
- `get_registry` (function) — `atp/adapters/registry.py:318`
- `create_adapter` (function) — `atp/adapters/registry.py:331`
- `logger` (const) — `atp/adapters/sdk_adapter.py:21`
- `SDKAdapterConfig` (class) — `atp/adapters/sdk_adapter.py:24`
- `SDKAdapter` (class) — `atp/adapters/sdk_adapter.py:34`
- `VertexAdapter` (class) — `atp/adapters/vertex/adapter.py:30`
- `get_vertexai_module` (function) — `atp/adapters/vertex/auth.py:13`
- `initialize_vertexai` (function) — `atp/adapters/vertex/auth.py:36`
- `VertexAdapterConfig` (class) — `atp/adapters/vertex/models.py:10`

## Modules

_27 files, 64 public symbols, 26 internal imports._

- `atp/adapters/__init__.py` (python)
- `atp/adapters/autogen.py` (python)
- `atp/adapters/azure_openai/__init__.py` (python)
- `atp/adapters/azure_openai/adapter.py` (python)
- `atp/adapters/azure_openai/auth.py` (python)
- `atp/adapters/azure_openai/models.py` (python)
- `atp/adapters/base.py` (python)
- `atp/adapters/bedrock/__init__.py` (python)
- `atp/adapters/bedrock/adapter.py` (python)
- `atp/adapters/bedrock/auth.py` (python)
- `atp/adapters/bedrock/models.py` (python)
- `atp/adapters/cli.py` (python)
- `atp/adapters/container.py` (python)
- `atp/adapters/crewai.py` (python)
- `atp/adapters/exceptions.py` (python)
- `atp/adapters/fallback.py` (python)
- `atp/adapters/http.py` (python)
- `atp/adapters/langgraph.py` (python)
- `atp/adapters/mcp/__init__.py` (python)
- `atp/adapters/mcp/adapter.py` (python)
- `atp/adapters/mcp/transport.py` (python)
- `atp/adapters/registry.py` (python)
- `atp/adapters/sdk_adapter.py` (python)
- `atp/adapters/vertex/__init__.py` (python)
- `atp/adapters/vertex/adapter.py` (python)
- `atp/adapters/vertex/auth.py` (python)
- `atp/adapters/vertex/models.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

- → [[atp-core]] · `package_dep` · `atp-core` `>=1.0.0`

## Inbound edges

- ← [[atp-platform]] · `package_dep` · `atp-adapters`

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
