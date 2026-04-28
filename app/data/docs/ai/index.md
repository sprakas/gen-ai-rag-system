---
outline: [2, 3]
---

# AI with BananaJS

Most AI workflows follow the same rut: a blob of code from a chat window, hard to review and impossible to script. BananaJS turns that around. The **`bjs ai`** commands are a **contract**: the CLI talks to your LLM, but what lands on disk stays **ordinary TypeScript**—diffable in PRs, repeatable in CI, and aligned with the same DDD layout you get from **`bjs new`** and **`bjs generate module`**.

This page is the **story and the overview**. Every flag, edge case, and subcommand reference lives under **Tooling**—use the left sidebar to jump straight there.

## The arc: from blank repo to reviewable output

You are not “vibe coding” a monolith. You are **configuring a tool**, **generating a slice**, **checking wiring**, then **reviewing** before merge.


<div class="ai-steps">
<div class="ai-step"><div class="step-badge">1</div><code class="step-cmd">ai setup</code><p>Configure provider, model and project hints in <code>.bananarc.json</code></p></div>
<div class="ai-step"><div class="step-badge">2</div><code class="step-cmd">ai generate</code><p>Scaffold a flat bundle or full DDD module tree — text or OpenAPI in, TypeScript out, auto-wired</p></div>
<div class="ai-step"><div class="step-badge">3</div><code class="step-cmd">ai review</code><p>Structured findings for CI — JSON, SARIF, or human-readable summary</p></div>
<div class="ai-step"><div class="step-badge">4</div><code class="step-cmd">ai context</code><p>Publish BananaJS conventions to every teammate's IDE agent — one commit, zero prompts</p></div>
<div class="ai-step"><div class="step-badge">5</div><code class="step-cmd">ai debug</code><p>Parse a runtime stack trace into root cause, source location hint, and a concrete fix</p></div>
<div class="ai-step"><div class="step-badge">6</div><code class="step-cmd">ai upgrade</code><p>Detect deprecated patterns before a version bump — auto-fix safe ones, patch files for the rest</p></div>
<div class="ai-step"><div class="step-badge">7</div><code class="step-cmd">ai perf</code><p>Static-first scan for N+1 queries, unbounded cursors, missing <code>.lean()</code>, and missing <code>@Cache</code></p></div>
<div class="ai-step"><div class="step-badge">8</div><code class="step-cmd">ai contract</code><p>Generate Pact consumer contract tests from your OpenAPI spec</p></div>
<a href="#mcp-server" class="ai-step ai-step--full ai-step--link"><div class="step-badge">9</div><code class="step-cmd">mcp start</code><p>Expose the full CLI as an MCP server — <code>bananajs_routes</code>, <code>bananajs_review</code>, <code>bananajs_generate</code>, and more available as native tools in Cursor, Claude Desktop, and any MCP-compatible IDE <span class="step-link-hint">→ see real-world usage</span></p></a>
</div>

::: info How every command runs internally
Every `bjs ai` command follows the same **Prepare → Research → Plan → Act → Validate** pipeline. **Prepare** loads config and validates inputs. **Research** reads files and runs static checks locally — no LLM yet. **Plan** builds prompts. **Act** calls the LLM (skipped for `ai wire` without `--llm`, which is why wire always produces output). **Validate** writes results or previews with `--dry-run`. Pass `--debug` to see per-stage timings. Full reference: [PRPAV pipeline](/tooling/ai-commands#prpav-pipeline).
:::

## Where the deep docs live (Tooling)

| You want…                                           | Open in Tooling                                           |
| --------------------------------------------------- | --------------------------------------------------------- |
| Every flag, alias, and copy-paste example           | [**AI commands**](/tooling/ai-commands)                   |
| DDD layout, extraction, and **`--module`** behavior | [**AI module generation**](/tooling/ai-module-generation) |
| **`bjs ai`** in context of the whole CLI            | [**CLI reference — `bjs ai`**](/tooling/cli#bjs-ai)       |
| IDE context files, fixture factories, OpenAPI enrich | [**AI commands — V2 additions**](/tooling/ai-commands#bjs-ai-context-bjs-ai-ctx) |
| Runtime debug, performance scan, upgrade readiness, release changelog | [**AI commands — Horizon B**](/tooling/ai-commands#horizon-b-developer-experience-depth) |
| Pact contract tests, MCP server, `BananaAiPlugin`, `ai-provider-core` | [**AI commands — Horizon C**](/tooling/ai-commands#horizon-c-ecosystem-bridges) |

The sidebar under **AI** lists the same destinations so one click always lands in **Tooling** for reference material.

## Binaries

- **`bjs`** — short name (used in these docs)
- **`bananajs`** — full name

::: tip Two different `g` commands
**`bjs ai g`** runs **AI** codegen. **`bjs g`** (top-level) runs **`bjs generate`** (controller, dto, **non-AI** module scaffold). Same letter, different verbs.
:::

For the full alias table and all flags, see [AI commands](/tooling/ai-commands).

## Guided examples

These are **moments in a real workflow**—onboarding, a new slice, a gate before merge—not an exhaustive flag list. For every option (including **CI-safe** invocations), use [**AI commands**](/tooling/ai-commands).

::: info How to read this section
Each scenario has a **short story** (who you are, what you need), a **command** you can paste, and **what you get** so nothing feels like a black box. Where it helps, tabs show the **full subcommand** next to its **one-letter alias**—same tool, fewer keystrokes.
:::

<div class="ai-guided-examples">

<div class="ai-scenario">

### 1 · First run: introduce the CLI to your LLM

**Scene:** You opened the repo for the first time. Nothing knows whether you use Ollama on your laptop or an API key in the cloud.

**Run** (from the app root):

::: code-group

```bash [bjs ai setup]
cd my-app
bjs ai setup
```

```bash [bjs ai s]
cd my-app
bjs ai s
```

:::

**You get:** a **`.bananarc.json`** with provider, model, retries/timeouts, and optional **`project`** hints (`bootstrap`, `apiPrefix`, …) that **`ai generate`** and **`ai wire`** reuse later.

</div>

<div class="ai-scenario">

### 2 · From a backlog line to a DDD module tree

**Scene:** Product gave you a sentence—“catalog with SKU and stock”—and you want **`src/modules/...`** with domain, application, and infrastructure, not three ad-hoc files in the repo root.

**Run:**

::: code-group

```bash [Long form]
bjs ai generate --module "Product catalog with SKU, price, and stock" --orm typeorm
```

```bash [Alias]
bjs ai g --module "Product catalog with SKU, price, and stock" --orm typeorm
```

:::

**You get:** generated files under **`src/modules/<kebab>/`**, plus—when not **`--dry-run`**—bootstrap registration and a best-effort TypeORM **`entities[]`** patch, same contract as **`bjs generate module`**. Deeper pipeline notes: [**AI module generation**](/tooling/ai-module-generation).

</div>

<div class="ai-scenario">

### 3 · OpenAPI in hand; ship a flat scaffold

**Scene:** Design exported **`petstore.yaml`**. You want a matching controller + DTO + service bundle without hand-copying types.

**Run:**

```bash
bjs ai generate --from-schema ./openapi/petstore.yaml
```

**You get:** deterministic **flat** files next to your workflow (see [**generate**](/tooling/ai-commands#bjs-ai-generate-bjs-ai-g))—use **`--dry-run`** first if you only want a preview.

</div>

<div class="ai-scenario">

### 4 · Review before the PR lands (or in CI)

**Scene:** You are about to open a PR, or a job needs machine-readable output.

**Human-readable** (summary + severities):

::: code-group

```bash [Path]
bjs ai review src/modules/widgets
```

```bash [Bare module name]
bjs ai r widgets
```

:::

A **bare** name like `widgets` resolves to **`src/modules/widgets`** when that folder exists—you can skip the long path on repeat runs.

**JSON** (scripts, dashboards):

```bash
bjs ai review widgets --format json
bjs ai r widgets --format json
```

**You get:** structured findings with **`schemaVersion`**; optional [**`--sarif`**](/tooling/ai-commands#bjs-ai-review-bjs-ai-r) for tools that speak SARIF.

</div>

<div class="ai-scenario">

### 5 · After a merge: did bootstrap fall behind?

**Scene:** You rebased or pulled **`main`**. New **`export const …Module`** entries exist under **`src/modules/`**, but you are not sure **`bootstrap.ts`** lists them all.

**Run:**

::: code-group

```bash [Hints only]
bjs ai wire
```

```bash [+ LLM narrative]
bjs ai w --llm
```

:::

**You get:** **dry-run** text only—the CLI **never** edits files. It tells you what import and **`modules: [...]`** lines to consider. Optional **`--llm`** adds a short narrative; still no writes.

</div>

<div class="ai-scenario">

### 6 · One file, one paragraph for reviewers

**Scene:** The PR template asks “what changed in the controller?” and you want a tight summary without rereading the diff.

::: code-group

```bash [Long form]
bjs ai explain src/modules/orders/Order.controller.ts
```

```bash [Alias]
bjs ai e src/modules/orders/Order.controller.ts
```

:::

**You get:** a concise LLM summary of that file—handy for descriptions and onboarding notes.

</div>

<div class="ai-scenario">

### 7 · Smoke-test scaffold

**Scene:** You need a **`node:test` + supertest** starting point that matches BananaTestApp-style recipes.

::: code-group

```bash [Default path]
bjs ai test
```

```bash [Custom output]
bjs ai t --out src/__tests__/api-smoke.test.ts
```

:::

**You get:** a minimal test file you can extend; adjust **`--out`** to match your layout.

</div>

<div class="ai-scenario">

### 8 · Share BananaJS rules with every IDE agent on the team

**Scene:** Your team uses Cursor, Claude Code, and GitHub Copilot. Every developer has slightly different context files — or none at all. You want one commit that covers all of them.

**Run** (from the app root):

```bash
bjs ai context
```

**You get:** four files generated from `.bananarc.json` + discovered module layout:

| File | Who reads it |
|---|---|
| `CLAUDE.md` | Claude Code, Claude.ai |
| `.cursor/rules/bananajs.mdc` | Cursor |
| `.cursorrules` | Cursor (backwards compat) |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `AGENTS.md` | OpenAI Codex CLI and others |

No LLM call needed. Commit the files and every agent immediately learns your module layout, ORM choice, and the shared framework rules.

One format only? Use `--format`:

```bash
bjs ai context --format copilot
```

</div>

<div class="ai-scenario">

### 9 · Generate fixture factories for a module

**Scene:** You have a `Users` module with typed DTOs and want type-safe factory functions for tests and Storybook — without hard-coding fragile object literals everywhere.

**Run:**

```bash
bjs ai mock --module src/modules/users
```

**You get:** a `__fixtures__/` folder next to your module with one `*.fixtures.ts` file per validation schema found. Each export follows the `build<Type>(overrides?)` pattern so you can override specific fields per test.

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

No `@faker-js/faker`? The command falls back to hardcoded literals and prints an install hint.

Use `--format json` when you need raw JSON samples (e.g. for manual testing or as input to `bjs ai openapi enrich`).

</div>

<div class="ai-scenario">

### 10 · Make your OpenAPI spec more useful for SDK generation

**Scene:** You exported `openapi.json` and noticed every operation has an empty `summary`. You're about to generate a TypeScript client and the resulting function names will be meaningless.

**Run:**

```bash
bjs openapi export --out openapi.json
bjs ai openapi enrich --in openapi.json --out openapi.enriched.json
```

**You get:** `openapi.enriched.json` with `summary`, `description`, `tags`, and `paramDescription` fields filled in by the configured LLM. The original `openapi.json` is never modified.

Preview changes without writing with `--dry-run`:

```bash
bjs ai openapi enrich --in openapi.json --out openapi.enriched.json --dry-run
```

</div>


<div class="ai-scenario">

### 11 · Debug a DI token error at runtime

**Scene:** You ran `npm start` and the process crashed with a tsyringe injection error. You saved the output to `crash.log` and want to know the root cause and the exact fix without manually re-reading the DI wiring.

**Run:**

```bash
# Pipe stderr directly
npm start 2>&1 | bjs ai debug

# Or from a saved file
bjs ai debug --input crash.log
```

**You get:** a structured `AiDebugJson` response — root cause, source location hint, and a concrete fix — printed as readable text or as JSON with `--format json`. No guesswork about which provider or token is missing.

</div>

<div class="ai-scenario">

### 12 · Catch N+1 queries before the PR lands

**Scene:** Code review flagged a service that loops over orders and calls the database inside the loop. You want the check to run automatically — without an LLM configured in CI — so it blocks the merge if the pattern recurs.

**Run:**

```bash
bjs ai perf --module src/modules/orders --format json
```

**You get:** `AiReviewJson` output — the same schema as `bjs ai review`. N+1, unbounded queries, missing `.lean()`, and missing `@Cache` patterns are caught statically (no LLM required). Pipe the exit code to gate your pipeline.

</div>

<div class="ai-scenario">

### 13 · Prepare an upgrade report before bumping the version

**Scene:** You are migrating a project from BananaJS 0.5 to 0.6. You want to know which files still use deprecated patterns (class-validator imports, old DI helpers, leading slashes in route decorators) before you start editing.

**Run:**

```bash
# See what needs to change (no files written)
bjs ai upgrade --to 0.6.0 --dry-run

# Apply safe mechanical fixes (slash removal, @ZodBody → @Body)
bjs ai upgrade --to 0.6.0 --apply

# Write .patch files for patterns that need manual review
bjs ai upgrade --to 0.6.0 --out ./upgrade-patches
```

**You get:** a grouped report by file. `[safe-apply]` patterns are auto-fixable. `[manual]` patterns emit `.patch` files or LLM hints. Nothing is ever silently rewritten without `--apply`.

</div>

<div class="ai-scenario">

### 14 · Generate Pact consumer tests from your OpenAPI spec

**Scene:** Your team just added three new POST endpoints. You want consumer-driven contract tests that verify the shape of every request body before a dependency goes live — without hand-writing Pact interactions.

**Run:**

```bash
bjs openapi export --out openapi.json
bjs ai contract --spec openapi.json --consumer my-app --provider orders-api
```

**You get:** `src/__tests__/contract/my-app-orders-api.contract.test.ts` — one Pact interaction per path/method, payloads built from JSON Schema validators (or your own `--fixtures` folder from `bjs ai mock`). Install `@pact-foundation/pact` once and the file is CI-ready.

Use `--dry-run` to preview how many interactions will be generated without writing anything to disk.

</div>

<div class="ai-scenario">

### 15 · Connect your IDE agent to the CLI (MCP)

**Scene:** You use Cursor, Claude Desktop, or another IDE that supports the Model Context Protocol. You want `bjs routes`, `bjs ai review`, and six other BananaJS CLI tools available as native agent tools — without copy-pasting commands back and forth.

**Run once** (add to your IDE config, then start the server):

```json
// .mcp.json  (or claude_desktop_config.json)
{
  "mcpServers": {
    "bananajs": {
      "command": "node",
      "args": ["/path/to/bjs", "mcp", "start"]
    }
  }
}
```

**You get:** 8 tools — `bananajs_routes`, `bananajs_explain`, `bananajs_review`, `bananajs_generate`, `bananajs_mock`, `bananajs_debug`, `bananajs_perf`, `bananajs_upgrade` — surfaced directly in your IDE's agent sidebar. `bananajs_upgrade` always adds `--dry-run`; no files are rewritten without your Go-Ahead.

</div>

<div class="ai-scenario">

### 16 · Inject an LLM provider at runtime via `BananaAiPlugin`

**Scene:** You are building an endpoint that calls an LLM as part of the request handler — summarise, classify, or enrich — and you want the provider wired via tsyringe DI so it's easy to swap in tests.

**Install:**

```bash
npm install @banana-universe/plugin-ai @banana-universe/ai-provider-core
```

**Bootstrap:**

```typescript
import { BananaApp } from '@banana-universe/bananajs'
import { BananaAiPlugin } from '@banana-universe/plugin-ai'
import type { LlmProvider } from '@banana-universe/ai-provider-core'

const myProvider: LlmProvider = {
  generate: async (prompt) => callYourLlmApi(prompt),
}

await BananaApp.create({ plugins: [BananaAiPlugin({ provider: myProvider })] })
```

**Inject in a controller:**

```typescript
import { inject } from '@banana-universe/bananajs'
import { AI_PROVIDER_TOKEN } from '@banana-universe/ai-provider-core'
import type { LlmProvider } from '@banana-universe/ai-provider-core'

@injectable()
export class SummaryService {
  constructor(@inject(AI_PROVIDER_TOKEN) private ai: LlmProvider) {}

  summarise(text: string) {
    return this.ai.generate(`Summarise: ${text}`)
  }
}
```

In tests, override the token with a stub — no network calls ever leave your test suite.

</div>

</div>

## Command index (at a glance)

<div class="ai-cmd-grid">
<div class="ai-cmd-card"><code class="cmd-name">ai setup</code><p>Create <code>.bananarc.json</code> and provider defaults</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai generate</code><p>Flat or DDD codegen; optional <code>--detailed</code> second pass</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai review</code><p>Structured findings; <code>--format json</code>, <code>--sarif</code>, module or file scope</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai wire</code><p>Dry-run bootstrap hints; optional <code>--llm</code></p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai test</code><p><code>node:test</code> + supertest scaffold</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai explain [file]</code><p>Short LLM summary of one file</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai context</code><p>Generate IDE context files (CLAUDE.md, Cursor rules, Copilot instructions, AGENTS.md)</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai mock</code><p>TypeScript fixture factories and JSON samples from validation schemas</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai openapi enrich</code><p>Fill missing summaries, descriptions, tags in an OpenAPI spec</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai doc</code><p>Legacy JSDoc path — prefer OpenAPI + <a href="/tooling/cli#bjs-openapi-export">docs</a></p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai debug [input]</code><p>Parse a runtime stack trace into root cause + fix (<code>AiDebugJson</code>)</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai perf</code><p>Static-first performance scan (N+1, unbounded queries, Mongoose .lean, @Cache); optional LLM pass</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai upgrade</code><p>Detect deprecated patterns; <code>--apply</code> for safe fixes, <code>--out</code> for patch files</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai changelog</code><p>Structured changelog from <code>git log</code>; optional OpenAPI diff enrichment</p></div>
<div class="ai-cmd-card"><code class="cmd-name">ai contract</code><p>Pact consumer contract tests from OpenAPI spec; <code>--fixtures</code> from <code>ai mock</code></p></div>
<div class="ai-cmd-card"><code class="cmd-name">mcp start</code><p>Expose all 8 CLI tools as MCP server for Cursor, Claude Desktop, and other IDE agents</p></div>
</div>

## Shared LLM rules

Every call prepends the same **versioned** rules (layout, ORM boundaries, HTTP, security, review severity). Source: `packages/bananajs-cli/src/lib/llm/bananajs-ai-rules.ts`; contract tests under `packages/bananajs-cli/src/__tests__/`.

## Project context (`.bananarc.json`)

Optional **`project`** block documents bootstrap for codegen and **`ai wire`**: **`apiPrefix`**, **`bootstrap`**, **`main`**. Types live in `packages/bananajs-cli/src/lib/llm/bananarc.ts`; **`generate`** holds **`defaultOrm`**, **`preset`**, **`outDir`**, **`structure`**.

## Structured review schema

JSON output carries **`schemaVersion`**. Published schema: **`ai-review.schema.json`** in **`@banana-universe/bananajs-cli`**.

## MCP server: CLI tools in your IDE {#mcp-server}

`bjs mcp start` launches a long-running **JSON-RPC server** that any MCP-compatible IDE can discover. Instead of copying terminal commands back and forth, your agent sidebar calls BananaJS operations as native tools — with typed inputs, structured outputs, and no human in the loop for routine steps.

### Exposed tools

| Tool | What it does |
|------|--------------|
| `bananajs_routes` | List every registered route and its HTTP method |
| `bananajs_explain` | Return a concise LLM summary of any source file |
| `bananajs_review` | Run a structured convention review; returns `AiReviewJson` |
| `bananajs_generate` | Scaffold a flat bundle or full DDD module tree |
| `bananajs_mock` | Generate `build<Type>()` fixture factories from validation schemas |
| `bananajs_debug` | Parse a stack trace into root cause + fix (`AiDebugJson`) |
| `bananajs_perf` | Static-first N+1 and performance scan |
| `bananajs_upgrade` | Upgrade readiness check — **always dry-run**, no files written |

### Finding your `bjs` binary

The MCP server process must be a **persistent executable** — not a hot-reload dev server. Three ways to reference it:

| Approach | `command` | `args[0]` | When to use |
|---|---|---|---|
| **npx** (recommended) | `npx` | `-y`, `@banana-universe/bananajs-cli` | No install needed; always uses the right version |
| **Local install** | `node` | `./node_modules/.bin/bjs` | Already in `dependencies`; fastest startup |
| **Global install** | `bjs` | _(inline below)_ | Run `npm i -g @banana-universe/bananajs-cli` first |

The tabs below use the **`npx`** form throughout. Swap the `command`/`args` block if you prefer the local or global approach.

### One-time setup per IDE

::: code-group

```json [Cursor · .mcp.json]
// File: <project-root>/.mcp.json
// Or globally: ~/.cursor/mcp.json
{
  "mcpServers": {
    "bananajs": {
      "command": "npx",
      "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
    }
  }
}
```

```json [VS Code · GitHub Copilot]
// File: <project-root>/.vscode/mcp.json
// Requires VS Code ≥ 1.99 with Copilot extension
{
  "servers": {
    "bananajs": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
    }
  }
}
```

```json [Claude Desktop]
// macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
// Windows: %APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "bananajs": {
      "command": "npx",
      "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
    }
  }
}
```

```bash [Claude Code CLI]
# One command — no config file editing needed
claude mcp add bananajs -- npx -y @banana-universe/bananajs-cli mcp start

# Verify it registered
claude mcp list
```

```json [Windsurf]
// File: ~/.codeium/windsurf/mcp_server_config.json
{
  "mcpServers": {
    "bananajs": {
      "command": "npx",
      "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
    }
  }
}
```

```json [OpenCode]
// File: <project-root>/opencode.json  (or ~/.config/opencode/config.json globally)
{
  "mcp": {
    "bananajs": {
      "command": "npx",
      "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
    }
  }
}
```

```json [Zed]
// File: ~/.config/zed/settings.json  — merge into the existing object
{
  "context_servers": {
    "bananajs": {
      "command": {
        "path": "npx",
        "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
      }
    }
  }
}
```

```json [Continue]
// File: <project-root>/.continue/config.json
{
  "mcpServers": [
    {
      "name": "bananajs",
      "command": "npx",
      "args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start"]
    }
  ]
}
```

:::

::: tip Restart once, use everywhere
After saving the config, **restart the IDE** (or reload the MCP server from its settings panel). The server registers all 8 tools automatically — no further setup needed until you change the config file.
:::

::: warning Working directory matters
The MCP server resolves your project root from the directory it starts in. If your IDE launches it from the wrong folder, pass `--cwd` explicitly:

```json
"args": ["-y", "@banana-universe/bananajs-cli", "mcp", "start", "--cwd", "/absolute/path/to/my-app"]
```
:::


### Real-world use cases

<div class="mcp-use-cases">

<details class="ai-scenario ai-scenario--collapsible">
<summary><strong>Use case 1 &middot; Generate, review, and iterate — without leaving the chat</strong><span class="uc-tag">generate · review</span></summary>

**Scene:** You are in Cursor's agent sidebar. You type: *"Add a Payments module with Stripe webhook handling."* You want the files generated, wired, and reviewed in a single flow — no terminal, no tab-switching.

**What happens:**

1. The agent calls `bananajs_generate` with your prompt and the `typeorm` ORM detected from `.bananarc.json`.
2. Files land in `src/modules/payments/` — controller, service, DTOs, entities, bootstrap registration — all in one pass.
3. The agent immediately calls `bananajs_review payments --format json`.
4. Findings come back inline: one `warning` about a missing `@Catch` decorator on the webhook handler, one `info` about an unbounded query. You fix both in the same chat turn.

**Why this matters:** The loop that normally spans three terminal commands and two file opens collapses into one conversation turn. The review findings are attached to the same context as the generated code, so the agent can apply fixes with precise line references.

</details>

<details class="ai-scenario ai-scenario--collapsible">
<summary><strong>Use case 2 &middot; Debug a production crash in Claude Desktop</strong><span class="uc-tag">debug</span></summary>

**Scene:** You get paged. Your app threw a tsyringe `Cannot inject the dependency at position #0` error in production. You copy the stack trace into Claude Desktop and ask: *"What is wrong and how do I fix it?"*

**What happens:**

1. Claude calls `bananajs_debug` with the stack trace text.
2. The tool returns an `AiDebugJson` object: the root cause (`OrderService` is not decorated with `@injectable()`), the exact file and line, and a one-line fix.
3. You ask a follow-up: *"Are there any other modules with the same issue?"*
4. Claude calls `bananajs_review src/modules --format json`, filters findings by `injection` severity, and lists two more candidates.

**Why this matters:** A crash that previously meant reading stack traces manually and grepping the codebase takes under a minute. The agent retains context across both tool calls, so follow-up questions cost nothing.

</details>

<details class="ai-scenario ai-scenario--collapsible">
<summary><strong>Use case 3 &middot; Pre-PR performance scan from the IDE sidebar</strong><span class="uc-tag">perf</span></summary>

**Scene:** You just finished a new Orders service. Before opening the PR you want to check for N+1 queries and missing `.lean()` calls — without switching to a terminal.

**What happens:**

1. You type in Cursor: *"Run a performance scan on the orders module."*
2. The agent calls `bananajs_perf` with `module: "src/modules/orders"` and `format: "json"`.
3. Results appear inline: two N+1 findings in `OrderService.findAll`, one missing `.lean()` in a Mongoose query. Each includes file path and line number.
4. You ask: *"Fix the N+1 in findAll."* The agent reads the file, applies the eager-load fix, and calls `bananajs_perf` again to confirm clean output.

**Why this matters:** The scan runs statically — no LLM required — so it's instant and free. Catching it before the PR saves a review round-trip.

</details>

<details class="ai-scenario ai-scenario--collapsible">
<summary><strong>Use case 4 &middot; Explore live routes without opening any file</strong><span class="uc-tag">routes</span></summary>

**Scene:** You joined a project mid-sprint. You want to know what HTTP endpoints exist and which module owns each one — without reading through bootstrap and every controller.

**What happens:**

1. You type: *"What routes does this app expose?"*
2. The agent calls `bananajs_routes` with no arguments.
3. A structured list comes back: method, path, controller class, and handler method for every registered route.
4. You follow up: *"Which of these don't have authentication middleware?"* The agent reasons over the route list and flags the unguarded ones.

**Why this matters:** `bananajs_routes` reflects the actual registered state of the app — not just what's in source files. It's the fastest orienteering tool when you're new to a codebase.

</details>

<details class="ai-scenario ai-scenario--collapsible">
<summary><strong>Use case 5 &middot; Generate test fixtures while writing a test</strong><span class="uc-tag">mock</span></summary>

**Scene:** You are mid-way through writing a unit test for `CreateOrderUseCase`. You need a realistic `CreateOrderDto` object but don't want to hand-code a literal or leave a `TODO`.

**What happens:**

1. You type in the chat: *"Generate fixture factories for the orders module."*
2. The agent calls `bananajs_mock` with `module: "src/modules/orders"`.
3. A `__fixtures__/create-order.dto.fixtures.ts` file is written alongside your module with a `buildCreateOrderDto(overrides?)` export.
4. You import it at the top of your test — one line — and override only the fields your test cares about.

**Why this matters:** Factories stay in sync with your validation schema automatically on the next `bjs ai mock` run. No more stale object literals causing type errors three sprints later.

</details>

</div>

## Recipes and samples

- [Recipes](/recipes/) — single-ORM apps.
- [example-rest-dual-orm](https://github.com/surya-manne/banana-universe/tree/main/apps/example-rest-dual-orm) — TypeORM + Mongoose in one codebase.

## Read next

- [Philosophy — AI-first](/guide/philosophy)
- [AI commands (full reference)](/tooling/ai-commands)
- [AI module generation (DDD)](/tooling/ai-module-generation)
- [CLI reference](/tooling/cli)
- Roadmap: `plans/AIRoadmapV1.md` and `plans/AIRoadmapV2.md` in the repo
