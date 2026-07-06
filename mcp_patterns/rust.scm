; .prograph/mcp_patterns/rust.scm — project-specific MCP idiom overrides.
; Appended to the bundled rust_mcp.scm at parse time.

; arbiter idiom: hand-rolled JSON-RPC server. Tools are NOT registered via
; .tool("name", ...) / register_tool() macros — they're dispatched in a
; `match tool_name { "route_task" => ..., "report_outcome" => ... }` block.
; Recognise match arms with literal-string patterns as tool decls.
;
; Predicate filters:
; - exclude strings with '/' (JSON-RPC method names like "tools/call")
; - exclude strings starting with '-' (clap CLI argument arms like "--config")
; - require at least one '_' to look identifier-shaped (tool names are
;   snake_case in this monorepo; this filters out short keywords like
;   "initialize"/"ping" and arbitrary string match arms in non-MCP code)
;
; This pattern fires on ANY Rust file with a snake_case match-arm dispatch.
; In a monorepo without other such idioms it's effectively arbiter-only.
((match_arm
   pattern: (match_pattern (string_literal) @tool_name_literal))
 (#not-match? @tool_name_literal "/")
 (#not-match? @tool_name_literal "^\"-")
 (#match? @tool_name_literal "_")) @tool_decl_match
