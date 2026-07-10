<!-- prograph:generated -->

---
indexed_at: "2026-07-10T12:31:55Z"
kind: js
name: spec-runner-vscode
prograph: project
root: ./spec-runner-vscode
snapshot: 4
---

# spec-runner-vscode

> A thin VSCode extension over [spec-runner](../spec-runner)'s existing CLI/JSON contracts. It surfaces the full lifecycle — gated-spec governance and task execution — natively inside the IDE, without…

## Manifest

- declared package: `spec-runner-vscode` version `0.1.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

- [[https---github-com-andrei-shtanakov-spec-runner-schemas-costs-schema-json]] (json_schema) — `out/schemas/costs.schema.json` — `https://github.com/andrei-shtanakov/spec-runner/schemas/costs.schema.json`
- [[https---github-com-andrei-shtanakov-spec-runner-schemas-json-result-schema-json]] (json_schema) — `out/schemas/json-result.schema.json` — `https://github.com/andrei-shtanakov/spec-runner/schemas/json-result.schema.json`
- [[https---github-com-andrei-shtanakov-spec-runner-schemas-spec-frontmatter-schema-json]] (json_schema) — `out/schemas/spec-frontmatter.schema.json` — `https://github.com/andrei-shtanakov/spec-runner/schemas/spec-frontmatter.schema.json`
- [[https---github-com-andrei-shtanakov-spec-runner-schemas-status-schema-json]] (json_schema) — `out/schemas/status.schema.json` — `https://github.com/andrei-shtanakov/spec-runner/schemas/status.schema.json`

### Public symbols

- `buildArgs` (function) — `src/cli.ts:33`
- `splitCommand` (function) — `src/config.ts:27`
- `resolveConfig` (function) — `src/config.ts:64`
- `deactivate` (function) — `src/extension.ts:106`
- `normalizeStatus` (function) — `src/model.ts:12`
- `tasksFromCosts` (function) — `src/model.ts:49`
- `summaryFromStatus` (function) — `src/model.ts:71`
- `isRunnable` (function) — `src/model.ts:84`
- `ValidateFunction` (const) — `src/schemas.ts:17`
- `validateFrontmatter` (const) — `src/schemas.ts:18`
- `validateJsonResult` (const) — `src/schemas.ts:19`
- `minSpecRunnerVersion` (function) — `src/schemas.ts:49`
- `loadVendoredSchema` (function) — `src/schemas.ts:54`
- `stageFileName` (function) — `src/specState.ts:52`
- `readStage` (function) — `src/specState.ts:57`
- `readStages` (function) — `src/specState.ts:109`
- `SpecStageItem` (class) — `src/trees/specTree.ts:14`
- `TaskTreeItem` (class) — `src/trees/tasksTree.ts:16`

## Modules

_36 files, 18 public symbols, 45 internal imports._

- `esbuild.js` (js)
- `out/src/cli.js` (js)
- `out/src/commands.js` (js)
- `out/src/config.js` (js)
- `out/src/controller.js` (js)
- `out/src/extension.js` (js)
- `out/src/model.js` (js)
- `out/src/output.js` (js)
- `out/src/schemas.js` (js)
- `out/src/specState.js` (js)
- `out/src/trees/runTree.js` (js)
- `out/src/trees/specTree.js` (js)
- `out/src/trees/tasksTree.js` (js)
- `out/src/types.js` (js)
- `out/src/watchers.js` (js)
- `out/test-integration/extension.test.js` (js)
- `src/cli.ts` (js)
- `src/commands.ts` (js)
- `src/config.ts` (js)
- `src/controller.ts` (js)
- `src/extension.ts` (js)
- `src/model.ts` (js)
- `src/output.ts` (js)
- `src/schemas.ts` (js)
- `src/specState.ts` (js)
- `src/trees/runTree.ts` (js)
- `src/trees/specTree.ts` (js)
- `src/trees/tasksTree.ts` (js)
- `src/types.ts` (js)
- `src/watchers.ts` (js)
- `test-integration/extension.test.ts` (js)
- `test-integration/fixtures/workspace/bin/fake-spec-runner.js` (js)
- `test/cli.test.ts` (js)
- `test/model.test.ts` (js)
- `test/specState.test.ts` (js)
- `vitest.config.ts` (js)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

- ↔ [[https---github-com-andrei-shtanakov-spec-runner-schemas-costs-schema-json]] · `contract_link` · `json_schema`
- ↔ [[https---github-com-andrei-shtanakov-spec-runner-schemas-json-result-schema-json]] · `contract_link` · `json_schema`
- ↔ [[https---github-com-andrei-shtanakov-spec-runner-schemas-spec-frontmatter-schema-json]] · `contract_link` · `json_schema`
- ↔ [[https---github-com-andrei-shtanakov-spec-runner-schemas-status-schema-json]] · `contract_link` · `json_schema`

## Inbound edges

_None._

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
