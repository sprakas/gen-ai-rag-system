# CLI reference

The **`bjs`** CLI (package **`@banana-universe/bananajs-cli`**) is a **first-class product surface**: scaffolding, codegen, static analysis, DB/OpenAPI tooling, and **AI** flows—including **`.bananarc.json`**, **`ai setup`**, and **`ai generate --module`** for DDD layouts ([Philosophy](/guide/philosophy), [AI module generation](/tooling/ai-module-generation)).

Package: **`@banana-universe/bananajs-cli`** · Binaries: **`bjs`** (shortcut), **`bananajs`**. Source: **`packages/bananajs-cli/src/index.ts`** (Commander.js).

## Global

```bash
bjs --help
bjs --version
```

## `bjs new [appName]`

Scaffolds an app from **built-in presets** (MongoDB/Mongoose or SQL/TypeORM). Writes files under **`./<appName>`**—**no git** and no remote template.

- Prompts for app name if omitted (default suggestion: **`my-bananajs-app`**)
- Interactive terminal: prompts for **MongoDB** vs **SQL** preset, then **Flat** vs **DDD layered** folder structure (default: **flat**)
- **`--preset <id>`** — **`mongodb`** \| **`sql`** — skip the preset prompt (use in CI/scripts)
- Non-interactive stdin (no TTY): defaults to **`sql`** preset and **flat** structure; pass **`--preset`** explicitly to choose MongoDB

**Scaffold defaults** (both presets):

- **Swagger** — **`swagger.enabled: true`** in bootstrap; **`swagger-ui-express`** in **`dependencies`** so **`/api-docs`** works; OpenAPI JSON at **`/api-docs.json`**.
- **Lint / format** — ESLint 9 flat config + Prettier (**tab width 4**), **`.editorconfig`**, **`npm run lint`** / **`npm run format`**.
- **DB** — Connection/options live in **`src/db/`** (**`mongo.ts`** or **`typeorm-options.ts`**) with explicit error handling or validation; **`main.ts`** wraps startup in **`try/catch`**.
- **Types** — **`@types/node`**, **`@types/express`**, **`@types/swagger-ui-express`** as dev dependencies.
- **Timestamps** — Mongoose **`timestamps: true`** on sample schemas; TypeORM **`@CreateDateColumn`** / **`@UpdateDateColumn`** on sample entities where shown.

Details: [Getting started](/guide/getting-started) (section **What the generated app includes**).

## `bjs generate [type] [name]` (alias: `g`)

**Types:** `controller` | `dto` | `middleware` | **`module`**

- Omit **`type`** and **`name`** in a **TTY** to be prompted (resource kind, then name).
- **`controller` / `dto` / `middleware`** — writes **`cwd/<name>.controller.ts`** (or `.dto.ts` / `.middleware.ts`).
- **`module`** — feature layout aligned with **`bjs new`**: **`src/modules/<kebab>/`** with **`createModule`** in **`index.ts`** and tsyringe **`@injectable` / `@inject`**. Two structure modes (prompted interactively; default: **flat**):
  - **Flat** *(default)* — controller, service, repository (interface + ORM impl), and DTO all at the module root; no subdirectories.
  - **DDD layered** — **`domain/`** (entity + repository token), **`application/`**, **`infrastructure/`**, **`<Pascal>.dto.ts`** and **`<Pascal>.controller.ts`** at the module root.
  - After a successful write (not **`--dry-run`**), the CLI **registers** the module in **`bootstrap.ts`** and, for TypeORM, appends the ORM entity to **`entities[]`**.
  - **`--structure ddd|flat`** — override the default (**`flat`**); omit to be prompted in a TTY.
  - **`--orm typeorm|mongoose|none`** — infrastructure adapter (default: **`typeorm`** when non-interactive). **`--orm`** wins over **`--preset`**.
  - **`--preset mongodb|sql`** — default ORM mapping.
  - **`--out <dir>`** — base directory (default **`./src`**).
  - **`--skip-bootstrap`** — do not patch **`bootstrap.ts`** or TypeORM **`entities[]`**.
- **`--dry-run`** — print content without writing.

See [Layered architecture & DDD](/guide/layered-architecture).

## `bjs routes`

Static scan for `@Controller` and HTTP decorators — prints a colored route table. **`--root <dir>`** sets the tree to scan (default **`src`**). In a **TTY** without **`--root`**, you are prompted for the directory.

## `bjs migrate`

**Express → BananaJS** codemod. In a **TTY**, confirms before running.

## `bjs db`

- **`--status`** — runs **`typeorm migration:show`** when a TypeORM config is present; if **`mongoose`** is in `package.json`, prints a short note (no migrate CLI).
- With **no flags** in a **TTY**, choose an action from a short menu.

## `bjs openapi export`

- **`--out <path>`** — OpenAPI spec output (default **`./openapi.json`** when unspecified).
- **`--client typescript`** — optional client generation (`openapi-typescript`).
- In a **TTY**, you may be prompted for output path and whether to generate TypeScript types.

## `bjs ai`

Subcommands have **one-letter aliases** (e.g. **`bjs ai g`** = **`bjs ai generate`**). Full table: **[AI hub](/ai/)**.

| Command           | Alias   | Purpose                                                                                                                                                                                                                                                 |
| ----------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`ai setup`**    | **`s`** | Configure provider + **`.bananarc.json`**                                                                                                                                                                                                               |
| **`ai generate`** | **`g`** | Flat module scaffold *(default)* or DDD **`--module`** (LLM extraction); **TTY** walks through flat-module → DDD → legacy flat, then schema vs text. After write, registers bootstrap / TypeORM **`entities[]`** when applicable—same as **`bjs generate module`**. |
| **`ai doc`**      | **`d`** | JSDoc on controllers; **`--file`**, **`--dry-run`**                                                                                                                                                                                                     |
| **`ai review`**   | **`r`** | Structured LLM review; **`--file`**, **`--module`**, or positional path; **`--format json`**, **`--sarif`**                                                                                                                                             |
| **`ai wire`**     | **`w`** | Bootstrap wiring hints (dry-run); optional **`--llm`**                                                                                                                                                                                                  |
| **`ai test`**     | **`t`** | Scaffold **`node:test` + supertest**                                                                                                                                                                                                                    |
| **`ai explain`**  | **`e`** | Short file summary                                                                                                                                                                                                                                      |

Shared: **`--out <dir>`**, **`--dry-run`** where applicable.

::: info Flat and DDD modules
Both **`bjs generate module`** and **`bjs ai generate`** support two folder structures — **flat** (default) and **DDD layered**:

- **Flat** *(default)* — controller, service, repository, and DTO live at **`src/modules/<feature>/`** root; no `domain/` / `application/` / `infrastructure/` subdirs.
- **DDD layered** — full **`domain/`**, **`application/`**, **`infrastructure/`** subdirectory layout with DDD `Entity<Props>` base class and repository port pattern.

Pass **`--structure flat`** (default) or **`--structure ddd`** to skip the interactive prompt. In a TTY, the prompt shows **Flat** first.

**`bjs ai generate --module`** accepts **`--orm`** and **`--preset mongodb|sql`**. In **`.bananarc.json`**, **`generate.preset`** sets the default ORM when **`generate.defaultOrm`** is omitted (**`mongodb`** → mongoose, **`sql`** → typeorm).
:::

## Related

- [AI commands](/tooling/ai-commands)
- [AI module generation](/tooling/ai-module-generation)
- [Benchmarks](/tooling/benchmarks)
