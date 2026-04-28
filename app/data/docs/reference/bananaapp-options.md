# BananaAppOptions

`BananaApp` is created with **one object**: either **`controllers`** (via **`defineBananaControllers`**) or **`modules`** (from **`createModule`**) plus **`BananaAppOptions`** fields.

```typescript
import { BananaApp, defineBananaControllers } from '@banana-universe/bananajs'

new BananaApp({
  controllers: defineBananaControllers(UserController),
  // ...BananaAppOptions
})
```

Use **`BananaApp.create({ ... })`** when you need **async plugin registration** (`plugins` array).

## Declarative bootstrap (optional)

- **`defineBananaControllers(...controllers)`** — returns the controller list for the **`controllers`** property
- **`defineBananaAppOptions({ modules: [...], plugins, ... })`** — preferred for feature slices: each module supplies **`controller`**, **`providers`**, and **`id`**; do not list the controller class again inside **`providers`**
- **`defineBananaAppOptions({ controllers: defineBananaControllers(...), providers, ... })`** — merges **`providers`** (tsyringe-style registrations: classes and `{ token, useClass | useFactory | useValue }`) into a container and returns a **`BananaApp.create`**-ready input
- **`createBananaProviderContainer(providers)`** — isolated child container + registrations in one call (see **`bananaBootstrap.ts`**)

See **`packages/bananajs/src/lib/DI/bananaBootstrap.ts`**.

## `BananaAppOptions` fields (summary)

The interface is defined in **`packages/bananajs/src/lib/Core/App.ts`**. Below is a **conceptual** grouping; see TypeDoc for exact optional/required fields.

### Core

- **`middlewares`** — `RequestHandler[]` applied after framework defaults and before controller routes
- **`security`** — `{ helmet?: boolean \| HelmetOptions; cors?: CorsOptions \| false }` — helmet and CORS are applied by default unless disabled
- **`requestId`** — boolean, default `true`; enables `X-Request-ID` handling
- **`logger`** — `Logger` instance or `false` to disable built-in logging
- **`container`** — **tsyringe** `DependencyContainer` (optional; created when using `providers` / `modules`)
- **`apiPrefix`** — optional segment prepended to all controller base paths (e.g. `v1` for `/v1/...`)
- **`testOverrides`** — extra registrations merged onto the **root** container after modules (for tests / fakes)
- **`gracefulShutdown`** — register signal handlers for clean process exit

### Auth & docs

- **`auth`** — `{ guard: AuthGuard }` for `@Auth` / `@Roles` / `@Public`
- **`swagger`** — OpenAPI JSON + UI (`enabled`, `path`, `title`, `version`, `description`, …)

### Operational

- **`rateLimit`** — global rate limit config or `false`
- **`health`** — `{ enabled, path?, checks? }` for **`GET /health`**
- **`metrics`** — Prometheus metrics endpoint (`prom-client` peer)
- **`devTools`** — expose **`GET /_banana/routes`** in non-production

### Plugins & cache

- **`plugins`** — `BananaPlugin[]`; register in order; async work in `register()` requires **`BananaApp.create`**
- **`cache`** — `{ store?: 'memory' \| CacheStore }` for `@Cache` / `@CacheEvict`

### Security, tenancy, and performance

- **`abac`** — `{ guard: AbacGuard }` for `@Can`
- **`tenant`** — tenant resolution options (see `TenantOptions` in TypeDoc)
- **`lazyControllers`** — defer controller instantiation until first request

## `RouteInfo`

`BananaApp.prototype.getRouteTable(): RouteInfo[]` returns `{ method, path, controller, handler }` for tooling.

## Related

- [Advanced concepts](/guide/advanced-concepts)
- [TypeDoc: `BananaApp`](/api/classes/BananaApp), [`BananaAppOptions`](/api/interfaces/BananaAppOptions)
