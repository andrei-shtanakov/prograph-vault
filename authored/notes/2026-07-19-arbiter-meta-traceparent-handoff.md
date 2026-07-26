# Handoff: arbiter должен читать `params._meta.traceparent` (M3-obs, вторая половина)

Дата: 2026-07-19. Контекст: Maestro M3-obs (план
`Maestro/docs/superpowers/plans/2026-07-19-m3-obs-traceparent-mcp.md`).

## Что уже сделано на стороне Maestro

С PR `feat/m3-obs-traceparent-mcp` каждый MCP `tools/call` из Maestro
(route_task, report_outcome, get_agent_status, report_benchmark) несёт
W3C trace-контекст в MCP-санкционированном слоте `params._meta`:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "route_task",
    "arguments": { "...": "..." },
    "_meta": { "traceparent": "00-<32hex trace_id>-<16hex span_id>-01" }
  }
}
```

Гарантии отправителя:

- Формат строго `00-<trace_id>-<span_id>-01` (W3C traceparent v00).
- Нулевой trace-id (`0`*32) НИКОГДА не отправляется — при отсутствии
  реального trace-контекста ключ `_meta` целиком опускается.
- Текущий arbiter (pin f3c955c) поле игнорирует: server.rs парсит params
  как сырой `Value` и читает только `name`/`arguments` — подтверждено
  e2e-тестом `test_pinned_arbiter_tolerates_meta_traceparent` в
  `Maestro/tests/test_arbiter_real_subprocess.py`.

## Что нужно сделать в arbiter (владелец — репо arbiter)

1. В диспетчере `tools/call` (`arbiter-mcp/src/server.rs`, район :458-490)
   извлекать `params._meta.traceparent`, парсить по существующему
   `_TRACEPARENT_RE`-аналогу в `arbiter-core/src/obs.rs` (там уже есть
   парсер для env `TRACEPARENT`).
2. Биндить `trace_id` (и `parent_span_id` = span_id из traceparent) в
   obs-контекст на время обработки этого запроса, чтобы
   `route.decision`, `outcome.recorded`, `benchmark_runs`-INSERT и пр.
   получали TraceId вызывающего Maestro вместо собственного корневого.
3. Отсутствие/невалидность `_meta.traceparent` — не ошибка: молча
   продолжать с текущим поведением (собственный trace root).
4. После релиза: Maestro может поднять пин и убрать оговорку «until
   arbiter reads it» в комментарии `_call_tool_once`.

Ценность: сквозная корреляция maestro-спанов `task.route` /
`benchmark.report.*` с arbiter-side записями по `trace_id` — исходный
мотив TODO «M3-obs / arbiter trace» (Maestro/TODO.md).
