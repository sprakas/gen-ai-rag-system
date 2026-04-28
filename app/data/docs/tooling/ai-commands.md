# AI commands

This page is the **reference**: flags, aliases, and copy-paste examples for every **`bjs ai`** subcommand. For the narrative—why the CLI exists, and how **setup → generate → wire → review** fits your workflow—read the **[AI hub](/ai/)** first; come here when you need the full option matrix.

Commands run under **`bjs ai`** (or **`bananajs ai`**).

## Command aliases

Each subcommand has a **one-letter alias** (see **`bjs ai --help`**):

| Command    | Alias |
| ---------- | ----- |
| `setup`    | `s`   |
| `generate` | `g`   |
| `doc`      | `d`   |
| `review`   | `r`   |
| `wire`     | `w`   |
| `test`     | `t`   |
| `explain`  | `e`   |

Examples: **`bjs ai g --module "…"`**, **`bjs ai r widgets`**, **`bjs ai w --llm`**.

::: warning Note
**`bjs ai g`** is **AI** `generate`. The top-level **`bjs g`** is the non-AI **`bjs generate`** (controller, dto, module, …)—different command.
:::

## `bjs ai setup` (`bjs ai s`)

Interactive wizard: LLM provider, model, and **`.bananarc.json`** (including optional **`project`** context for wire/codegen).

```bash
bjs ai setup
bjs ai s
```

## `bjs ai generate` (`bjs ai g`)

| Option                                                        | Description                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **`--from-schema <file>`**                                    | JSON Schema or OpenAPI (flat); with **`--module`**, DDD extraction        |
| **`--from-prompt <text>`**                                    | Natural language flat scaffold (uses shared LLM rules + `.bananarc.json`) |
| **`--module [description]`**                                  | Layered DDD module; pair with **`--from-schema`** or a description        |
| **`--orm`**, **`--preset`**                                   | ORM choice (same semantics as **`ban new`**)                              |
| **`--out`**, **`--dry-run`**, **`--detailed`**, **`--debug`** | Output dir, preview, second LLM pass for bodies, raw LLM logging          |

After a successful DDD write (not **`--dry-run`**), the CLI **registers** the module in bootstrap and **patches TypeORM `entities[]`** when applicable—same behavior as **`bjs generate module`**.

With **no flags** in a TTY, **`bjs ai generate`** first asks whether you want a **DDD module** or **flat** scaffold, then runs the appropriate prompts (schema path vs description, ORM, optional **`--detailed`**, etc.). Non-interactive environments should use explicit flags.

```bash
# DDD: description + ORM
bjs ai generate --module "Invoices with line items" --orm typeorm
bjs ai g --module "Invoices with line items" --orm typeorm --preset sql

# Flat: schema file
bjs ai g --from-schema ./specs/api.json

# Dry-run preview
bjs ai g --module "Tags" --dry-run
```

Details: **[AI module generation](/tooling/ai-module-generation)**.

## `bjs ai review` (`bjs ai r`)

Structured review (JSON with **`schemaVersion`**, human-readable summary in text mode). **Non-interactive** — you must pass a target.

| Option                      | Description                                                                               |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| **`--file <path>`**         | Single TypeScript file                                                                    |
| **`--module <path>`**       | Directory — all **`.ts`** files (non-declaration)                                         |
| **`[target]`** (positional) | Same as file or directory; bare name **`widgets`** → **`src/modules/widgets`** if present |
| **`--format text \| json`** | Default **text**                                                                          |
| **`--sarif`**               | SARIF 2.1.0 instead of text/json                                                          |
| **`--fix`**                 | Reserved; safe auto-fix not applied yet                                                   |

```bash
bjs ai review --file src/modules/orders/Order.controller.ts
bjs ai review --module src/modules/widgets
bjs ai review widgets
bjs ai r widgets --format json
```

Schema: **`ai-review.schema.json`** in **`@banana-universe/bananajs-cli`**.

## `bjs ai wire` (`bjs ai w`)

Bootstrap wiring hints (**dry-run**; does not modify files). Optional **`--llm`** for narrative. Reads **`project`** from **`.bananarc.json`** when present.

```bash
bjs ai wire
bjs ai w --llm
```

## `bjs ai test` (`bjs ai t`)

Scaffolds a minimal **`node:test` + supertest** file (BananaTestApp-style). **`--out`** overrides default path.

```bash
bjs ai test
bjs ai t --out src/__tests__/api-smoke.test.ts
```

## `bjs ai explain [file]` (`bjs ai e`)

Short LLM summary of a file (PR descriptions, onboarding).

```bash
bjs ai explain src/bootstrap.ts
bjs ai e src/bootstrap.ts
```

## `bjs ai doc` (`bjs ai d`)

**Deprecation path:** JSDoc-only rewrites are lower signal than **types + OpenAPI**. The command still runs but prints a yellow notice; prefer **`openapi export`** and hand-written API docs. Timeline and alternatives: **[AI hub](/ai/)**.

## `bjs ai context` (`bjs ai ctx`)

Generates project-tailored AI context files embedding the shared BananaJS rules, discovered module layout, and installed plugin list. No LLM call required — reads `.bananarc.json` and scans `src/modules/` statically.

| Output file                       | IDE / agent                       |
| --------------------------------- | --------------------------------- |
| `CLAUDE.md`                       | Claude Code, Claude.ai projects   |
| `.cursor/rules/bananajs.mdc`      | Cursor (current MDC format)       |
| `.cursorrules`                    | Cursor (legacy backwards compat)  |
| `.github/copilot-instructions.md` | GitHub Copilot                    |
| `AGENTS.md`                       | OpenAI Codex CLI and other agents |

| Option               | Description                                                     |
| -------------------- | --------------------------------------------------------------- |
| **`--format <fmt>`** | `claude \| cursor \| copilot \| agents \| all` (default: `all`) |
| **`--out <dir>`**    | Output directory (default: project root)                        |
| **`--dry-run`**      | Preview files without writing                                   |

```bash
# Generate all context files in the project root
bjs ai context

# Generate only the Claude file
bjs ai context --format claude

# Preview what would be written
bjs ai context --dry-run

# Write to a specific folder
bjs ai context --out .ai-context
```

::: tip Commit these files
Commit the generated context files so every team member's IDE agent follows the same BananaJS conventions without manual prompt engineering.
:::

## `bjs ai mock`

Generates TypeScript fixture factories and JSON sample files from validation schemas in a controller, DTO, or module directory.

| Option                  | Description                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| **`--schema <file>`**   | Path to a TypeScript file containing a validation schema                     |
| **`--module <path>`**   | Directory — generates fixtures for all validation schema files found         |
| **`--out <dir>`**       | Base directory for `__fixtures__/` output (default: alongside input)         |
| **`--format ts\|json`** | TypeScript factory functions (`ts`) or JSON samples (`json`) (default: `ts`) |
| **`--dry-run`**         | Preview without writing                                                      |

Output format for `--format ts` (with `@faker-js/faker` installed):

```typescript
// __fixtures__/create-user.dto.fixtures.ts  (generated)
import { faker } from '@faker-js/faker'
import type { CreateUserDto } from '../create-user.dto.js'

export const buildCreateUserDto = (overrides?: Partial<CreateUserDto>): CreateUserDto => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  ...overrides,
})
```

::: info Optional peer: @faker-js/faker
When `@faker-js/faker` is not installed, the command falls back to hardcoded type-based literals (`'value'`, `1`, `true`, etc.) and prints an install hint. Install it for richer fixture data:

```bash
npm install --save-dev @faker-js/faker
```

:::

```bash
# Generate from a single DTO file
bjs ai mock --schema src/modules/users/create-user.dto.ts

# Generate for an entire module
bjs ai mock --module src/modules/users

# JSON format (useful as input to `bjs ai openapi enrich` fixtures)
bjs ai mock --schema src/modules/users/create-user.dto.ts --format json

# Dry-run preview
bjs ai mock --module src/modules/orders --dry-run
```

## `bjs ai openapi enrich`

Takes an existing `openapi.json` (from `bjs openapi export`) and fills in missing operation summaries, parameter descriptions, response descriptions, and tags using the configured LLM.

| Option                | Description                                                       |
| --------------------- | ----------------------------------------------------------------- |
| **`--in <spec>`**     | Input OpenAPI JSON file (**required**)                            |
| **`--out <spec>`**    | Output OpenAPI JSON file — must differ from `--in` (**required**) |
| **`--dry-run`**       | Show a diff of proposed additions without writing                 |
| **`--skip-examples`** | Do not enrich response descriptions                               |
| **`--skip-tags`**     | Do not add missing tags                                           |

::: warning Safety contract
`--out` is always required. The command never overwrites `--in` in place. The enriched spec includes `x-enriched-by: bananajs-cli@<version>` so the source is traceable. Use `--dry-run` to review changes before committing them to your spec.
:::

```bash
# Export spec first, then enrich
bjs openapi export --out openapi.json
bjs ai openapi enrich --in openapi.json --out openapi.enriched.json

# Dry-run: see what would be added
bjs ai openapi enrich --in openapi.json --out openapi.enriched.json --dry-run

# Skip tags if your spec already has them
bjs ai openapi enrich --in openapi.json --out openapi.enriched.json --skip-tags
```

## Command alias table (full)

| Command          | Alias |
| ---------------- | ----- |
| `setup`          | `s`   |
| `generate`       | `g`   |
| `doc`            | `d`   |
| `review`         | `r`   |
| `wire`           | `w`   |
| `test`           | `t`   |
| `explain`        | `e`   |
| `context`        | `ctx` |
| `mock`           | —     |
| `openapi enrich` | —     |
| `debug`          | —     |
| `perf`           | —     |
| `upgrade`        | —     |
| `changelog`      | —     |

---

## Horizon B — Developer-experience depth

### `bjs ai debug [input]`

Analyze a BananaJS runtime error or stack trace and receive a structured root-cause explanation and concrete fix. Reads from **stdin** (pipe), `--input <file>`, or an inline string argument.

Output schema — `AiDebugJson` (`schemaVersion: "1.0.0"`, separate versioning from `ai review`):

```json
{
  "schemaVersion": "1.0.0",
  "error": "Cannot inject token 'IUserRepository'",
  "rootCause": "Provider not registered in createModule() providers[]",
  "location": { "file": "src/modules/user/index.ts", "hint": "providers array" },
  "fix": "Add { token: IUserRepository, useClass: TypeOrmUserRepository } to providers",
  "severity": "error"
}
```

| Option                     | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| **`[input]`** (positional) | Inline error text or path to a file with the stack trace     |
| **`--input <path>`**       | Path to stack trace file (alternative to stdin / positional) |
| **`--file <path>`**        | Optional source file to attach as additional context         |
| **`--format text\|json`**  | Default: `text`                                              |
| **`--debug`**              | Print raw LLM output                                         |

```bash
# Pipe stderr output
npm start 2>&1 | bjs ai debug

# From a saved stack trace file
bjs ai debug --input crash.log

# With a source file for extra context
bjs ai debug --input crash.log --file src/modules/orders/index.ts

# JSON output for CI
bjs ai debug --input crash.log --format json
```

::: tip Coverage
`ai debug` understands tsyringe DI token errors, missing `reflect-metadata`, decorator metadata failures, TypeORM entity registration gaps, and Mongoose schema resolution errors.
:::

---

### `bjs ai perf`

Scan controller or service files for performance antipatterns. **Static-first** — most checks (N+1, unbounded queries, Mongoose `.lean()`, missing `@Cache`) run without an LLM, making this safe for CI pipelines with no configured provider. An optional LLM pass supplements static results with deeper analysis.

Findings are emitted in the same `AiReviewJson` format as `bjs ai review`, so existing JSON parsers and CI tooling work immediately.

| Option                    | Description                                                          |
| ------------------------- | -------------------------------------------------------------------- |
| **`--file <path>`**       | Single TypeScript file                                               |
| **`--module <path>`**     | Directory or bare module name (e.g. `orders` → `src/modules/orders`) |
| **`--format text\|json`** | Default: `text`                                                      |
| **`--debug`**             | Print raw LLM output                                                 |

Static checks included (no LLM required):

| Pattern                                              | Severity |
| ---------------------------------------------------- | -------- |
| ORM call inside `.forEach`/`.map`/for-of loop (N+1)  | `error`  |
| `findAll()` with no `take`/`limit` (unbounded query) | `warn`   |
| `@Get` route with no `@Cache` decorator              | `warn`   |
| Mongoose `find()` without `.lean()`                  | `warn`   |
| `JSON.stringify`/`JSON.parse` per request            | `info`   |

```bash
# Analyze a single controller
bjs ai perf --file src/modules/orders/order.controller.ts

# Analyze an entire module
bjs ai perf --module src/modules/orders

# JSON output for CI gates
bjs ai perf --module src/modules/catalog --format json
```

---

### `bjs ai upgrade`

Scan the codebase for deprecated BananaJS patterns and generate migration hints or patch files. Detection is **static regex-first** — no LLM call required for scanning. An optional LLM pass provides migration hints for patterns that require manual intervention.

Pattern manifest is seeded from [`docs/MIGRATION.md`](/migration/from-express) — covers all breaking changes across BananaJS versions.

| Option               | Description                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **`--to <version>`** | Target BananaJS version (e.g. `0.6.0`); checks only patterns deprecated by that version. Default: all patterns.                                |
| **`--apply`**        | Apply **safe mechanical** fixes in-place (leading-slash removal, `@ZodBody` → `@Body`, etc.). Requires explicit flag — never applied silently. |
| **`--out <dir>`**    | Output directory for `.patch` files (for ambiguous patterns that need manual review).                                                          |
| **`--dry-run`**      | Print all findings without modifying any file.                                                                                                 |
| **`--debug`**        | Print raw LLM hints.                                                                                                                           |

Pattern tags:

- **`[safe-apply]`** — safe mechanical transform; applied by `--apply`
- **`[manual]`** — requires developer judgment; emits `.patch` or LLM hint

```bash
# Full scan (all patterns, dry-run)
bjs ai upgrade --dry-run

# Scan for v0.6.0-specific patterns
bjs ai upgrade --to 0.6.0

# Apply safe fixes in-place
bjs ai upgrade --to 0.6.0 --apply

# Output patches for manual review
bjs ai upgrade --out ./upgrade-patches
```

::: warning Safe-apply scope
`--apply` only transforms patterns marked **`[safe-apply]`** (e.g., remove leading slashes, `@ZodBody` → `@Body`). Patterns requiring DI rewrites, API shape changes, or business logic judgment emit `.patch` files and are never silently rewritten. `--apply` is not exposed in the MCP server transport.
:::

---

### `bjs ai changelog`

Generate a structured developer changelog from git commits, optionally enriched with an OpenAPI spec diff between two snapshots.

| Option                  | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| **`--from <ref>`**      | Start git ref (tag, commit, branch). Default: previous tag. |
| **`--to <ref>`**        | End git ref (default: `HEAD`).                              |
| **`--before <spec>`**   | OpenAPI JSON snapshot before the range (for diff).          |
| **`--after <spec>`**    | OpenAPI JSON snapshot after the range (for diff).           |
| **`--format md\|json`** | Output format (default: `md`).                              |
| **`--out <file>`**      | Write to file instead of stdout.                            |
| **`--debug`**           | Print raw LLM output.                                       |

Output sections (only non-empty sections are included):

- **Breaking Changes** — removed APIs, renamed exports, incompatible signatures
- **New Features** — new commands, endpoints, decorators, plugins
- **Bug Fixes** — observable behavior fixes
- **Deprecated** — still works, removal scheduled
- **Internal** — CI, deps, infra (collapsed, max 3 bullets)

```bash
# Changelog since previous tag
bjs ai changelog

# Specific range
bjs ai changelog --from v0.5.0 --to v0.6.0

# With OpenAPI diff to surface breaking API changes
bjs ai changelog --from v0.5.0 --before openapi-v0.5.json --after openapi-v0.6.json

# Write markdown to file
bjs ai changelog --out CHANGELOG.md

# JSON output (for tooling integration)
bjs ai changelog --format json --out changelog.json
```

---

## PRPAV pipeline

Every `bjs ai` command runs through the same five-stage pipeline. Understanding the stages makes `--debug` output and error messages easier to read.

| Stage        | What happens                                                                                                                                                                |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prepare**  | Load `.bananarc.json`, resolve the LLM provider, validate that required inputs (files, specs, git refs, flags) exist. Fails fast — nothing else runs if inputs are missing. |
| **Research** | Read source files, scan for patterns, load OpenAPI specs, collect git log, load schemas. All local I/O; no LLM calls yet. Static checks in `ai perf` run here.              |
| **Plan**     | Build LLM prompts and determine operation targets. No network I/O.                                                                                                          |
| **Act**      | Execute LLM calls. Automatically skipped for `ai wire` when `--llm` is not passed — so `bjs ai wire` always produces output even without a configured model.                |
| **Validate** | Write files, apply patches, emit results to stdout. `--dry-run` short-circuits here — everything up to and including Act ran, but nothing lands on disk.                    |

When a stage fails, the error message includes the stage name:

```
ai perf failed [research]: Cannot read file: src/modules/orders/order.service.ts
ai contract failed [act]: Ollama HTTP 404: model 'llama3.2' not found
ai upgrade failed [prepare]: No bananarc.json found — run `bjs ai setup` first
```

Pass **`--debug`** to any LLM command to log per-stage timings and raw LLM output to stderr.

## Implementation note

Source lives in **`packages/bananajs-cli`** (`ai.ts`, `ai-module.ts`, `ai-review-run.ts`, `ai-context.ts`, `ai-mock.ts`, `ai-openapi-enrich.ts`, `ai-debug.ts`, `ai-debug-schema.ts`, `ai-perf.ts`, `ai-upgrade.ts`, `ai-upgrade-manifest.ts`, `ai-changelog.ts`, `ai-contract.ts`, `mcp-server.ts`, `lib/llm/`, …). Pipeline contract: **`lib/llm/pipeline.ts`**. Shared rules: **`lib/llm/bananajs-ai-rules.ts`**.

---

## Horizon C — Ecosystem and runtime

### `bjs ai contract`

Generate **Pact-compatible consumer contract tests** from an exported OpenAPI spec. Produces TypeScript test files that define consumer expectations per endpoint and can be run against the live provider in CI.

| Option                      | Description                                                                              |
| --------------------------- | ---------------------------------------------------------------------------------------- |
| **`--spec <openapi.json>`** | Input OpenAPI JSON file from `bjs openapi export` (**required**)                         |
| **`--consumer <name>`**     | Consumer name for the Pact contract, e.g. `frontend` (**required**)                      |
| **`--provider <name>`**     | Provider name for the Pact contract, e.g. `api` (**required**)                           |
| **`--fixtures <dir>`**      | Directory with JSON files from `bjs ai mock --format json`; skips LLM payload generation |
| **`--out <dir>`**           | Output directory (default: `src/__tests__/contract`)                                     |
| **`--dry-run`**             | Preview generated test files without writing                                             |
| **`--debug`**               | Print raw LLM output                                                                     |

**Workflow: combine `ai mock` + `ai contract` to minimize LLM calls:**

```bash
# Generate JSON fixtures from validation schemas
bjs ai mock --module src/modules/users --format json --out src/__fixtures__

# Generate contract tests reusing those fixtures
bjs openapi export --out openapi.json
bjs ai contract --spec openapi.json --consumer frontend --provider api \
  --fixtures src/__fixtures__

# Dry-run preview
bjs ai contract --spec openapi.json --consumer frontend --provider api --dry-run
```

::: info @pact-foundation/pact peer
The generated test files import from `@pact-foundation/pact`. Install it as a dev dependency:

```bash
npm install --save-dev @pact-foundation/pact
```

:::

---

### `bjs mcp start` — MCP server

Start the BananaJS **Model Context Protocol** server over stdio. IDE agents (Claude Code, Cursor, GitHub Copilot Workspace, etc.) can invoke BananaJS capabilities as native tools — no shell script wrapper required.

```bash
# Start the MCP server (stdio transport)
bananajs mcp start
# or
npx @banana-universe/bananajs-cli mcp start
```

**VS Code / Claude Code config (`.mcp.json` or `claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "bananajs": {
      "command": "npx",
      "args": ["@banana-universe/bananajs-cli", "mcp", "start"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

**Tools exposed:**

| Tool                | Maps to                       | Notes                                                       |
| ------------------- | ----------------------------- | ----------------------------------------------------------- |
| `bananajs_routes`   | `bjs routes`                  | Returns route table for the scanned project                 |
| `bananajs_explain`  | `bjs ai explain <file>`       | LLM file summary                                            |
| `bananajs_review`   | `bjs ai review --format json` | Returns `AiReviewJson`                                      |
| `bananajs_generate` | `bjs ai generate --module`    | DDD module generation; defaults to `--dry-run` via MCP      |
| `bananajs_mock`     | `bjs ai mock --schema`        | Fixture factory generation; defaults to `--dry-run` via MCP |
| `bananajs_debug`    | `bjs ai debug --format json`  | Returns `AiDebugJson`                                       |
| `bananajs_perf`     | `bjs ai perf --format json`   | Returns `AiReviewJson`                                      |
| `bananajs_upgrade`  | `bjs ai upgrade --dry-run`    | Dry-run **only** — `--apply` is intentionally not exposed   |

::: warning Security: --apply not exposed via MCP
The `bananajs_upgrade` tool always runs in dry-run mode. File-mutating operations must be run via the CLI directly after reviewing the output.
:::

---

### `@banana-universe/plugin-ai` — `BananaAiPlugin`

Framework plugin that registers a configured `LlmProvider` on the tsyringe root container under the `"AiProvider"` injection token. Full reference: [Plugin AI](/plugins/overview).

```typescript
import { BananaApp } from '@banana-universe/bananajs'
import { BananaAiPlugin, AI_PROVIDER_TOKEN } from '@banana-universe/plugin-ai'

await BananaApp.create({
  plugins: [BananaAiPlugin({ provider: myOllamaProvider })],
  modules: [catalogModule],
})
```

Inject in controllers via `@inject(AI_PROVIDER_TOKEN)`.

::: danger Prompt injection
`BananaAiPlugin` does **not** sanitize user input. Always validate input with `@Body` schemas, cap string lengths, and never pass raw `req.headers` / `req.params` into LLM prompts. See the plugin README for full security guidance.
:::

---

### `@banana-universe/ai-provider-core`

Shared publishable package containing the `LlmProvider` interface and `AI_PROVIDER_TOKEN` constant. Both `bananajs-cli` and `plugin-ai` import from this package instead of duplicating the type.

```typescript
import type { LlmProvider, LlmGenerateOptions } from '@banana-universe/ai-provider-core'
import { AI_PROVIDER_TOKEN } from '@banana-universe/ai-provider-core'

class MyProvider implements LlmProvider {
  async generate(prompt: string, options?: LlmGenerateOptions): Promise<string> {
    // ...
  }
}
```
