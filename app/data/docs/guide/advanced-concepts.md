# Advanced Concepts

BananaJS ships a **wide** enterprise surface—auth, OpenAPI, plugins, cache, metrics, multi-tenancy, ABAC, security decorators—not a "basic" framework with a few extras. This page maps every major option with executable code. For full type signatures, see [TypeDoc](/api/).

## Bootstrap: `new` vs `BananaApp.create`

```typescript
// Sync-only bootstrap (no async plugins)
new BananaApp({ modules: [userModule] })

// Async bootstrap — required when plugins do async work (DB connect, etc.)
const app = await BananaApp.create({
  modules: [userModule],
  plugins: [mongoosePlugin],
})
```

**Rule:** use `BananaApp.create` whenever any plugin's `register` hook is `async`. The `onReady` hook fires after all routes are mounted; `onShutdown` fires on SIGINT/SIGTERM.

## `BananaAppOptions` overview

One object drives all of BananaJS. Highlights:

| Area              | Options                                                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------- |
| **HTTP**          | `middlewares` — extra Express handlers before routes                                                                 |
| **Security**      | `security.helmet`, `security.cors` — both on by default; disable or pass config                                     |
| **Request ID**    | `requestId` — default `true`                                                                                         |
| **Logging**       | `logger` — `Logger` instance or `false`                                                                              |
| **DI**            | `container` — tsyringe `DependencyContainer` ([Dependency injection](/guide/dependency-injection))                   |
| **Modules**       | `modules` — `createModule({ id, controller, providers })` descriptors ([Layered architecture](/guide/layered-architecture)) |
| **Shutdown**      | `gracefulShutdown` — SIGINT/SIGTERM hooks                                                                            |
| **Auth**          | `auth.guard` — `AuthGuard` for `@Auth` / `@Roles` / `@Public`                                                       |
| **Swagger**       | `swagger.enabled`, `path`, `title`, `version`                                                                        |
| **Rate limit**    | `rateLimit` — global rate limiting (optional peer `express-rate-limit`)                                              |
| **Health**        | `health.enabled`, `path`, `checks` — `GET /health`                                                                  |
| **Plugins**       | `plugins` — `BananaPlugin[]`; use `BananaApp.create` for async                                                       |
| **Cache**         | `cache.store` — `'memory'` (default) or custom `CacheStore`                                                          |
| **DevTools**      | `devTools` — `GET /_banana/routes` in non-production                                                                 |
| **Metrics**       | `metrics.enabled`, `path` — Prometheus via optional peer `prom-client`                                               |
| **ABAC**          | `abac.guard` — `AbacGuard` for `@Can`                                                                                |
| **Multi-tenancy** | `tenant` — tenant resolution and `TenantContext`                                                                     |
| **Performance**   | `lazyControllers` — defer controller instantiation until first request                                               |

Exact field types and defaults: [BananaAppOptions reference](/reference/bananaapp-options).

## Authentication decorators

Configure a guard once; apply decorators anywhere.

```typescript
import type { AuthGuard } from '@banana-universe/bananajs'

class JwtGuard implements AuthGuard {
  async authenticate(req: Request): Promise<AuthenticatedUser | null> {
    const token = req.headers.authorization?.split(' ')[1]
    if (!token) return null
    return verifyJwt(token)   // your JWT verify logic
  }
}

new BananaApp({ auth: { guard: new JwtGuard() }, modules: [userModule] })
```

```typescript
@Auth()                          // whole class requires auth
@Controller('admin')
class AdminController extends BaseController {
  @Roles('admin', 'superuser')   // further narrow by role
  @Get('users')
  async list(req: Request, res: Response) { ... }

  @Public()                      // opt out for one route
  @Get('status')
  async status(_req: Request, res: Response) {
    return this.ok(res, 'ok', { status: 'up' })
  }
}
```

## OpenAPI / Swagger

Decorators feed the schema extractor. Enable Swagger at startup:

```typescript
new BananaApp({
  swagger: { enabled: true, title: 'My API', version: '1.0.0', path: '/api-docs' },
  modules: [userModule],
})
```

Annotate controllers:

```typescript
import { ApiTags, ApiOperation, ApiResponseDoc } from '@banana-universe/bananajs'

@ApiTags('Users')
@Controller('users')
class UserController extends BaseController {
  @ApiOperation({ summary: 'Get user by ID' })
  @ApiResponseDoc({ status: 200, type: UserDto })
  @Params(idSchema)
  @Get('items/:id')
  async getById(req: Request, res: Response) {
    const { id } = req.params as { id: string }
    const user = await this.service.findById(id)
    if (!user) throw new NotFoundError('User not found')
    return this.ok(res, 'ok', user)
  }
}
```

Apps created with `bananajs new` turn on `swagger.enabled` by default and include `swagger-ui-express` — `GET /api-docs` works out of the box.

For the full decorator reference, inferred-schema details, CLI export, and auth integration, see the dedicated guide: **[OpenAPI / Swagger reference](/reference/openapi)**.

## Health checks

Implement the `HealthCheck` interface and pass checks under `health.checks`:

```typescript
import { BananaApp } from '@banana-universe/bananajs'
import type { HealthCheck } from '@banana-universe/bananajs'

const dbCheck: HealthCheck = {
  name: 'database',
  async check() {
    try {
      await dataSource.query('SELECT 1')
      return { status: 'ok' }
    } catch {
      return { status: 'down', detail: 'DB unreachable' }
    }
  },
}

new BananaApp({
  health: { enabled: true, path: '/health', checks: [dbCheck] },
  modules: [userModule],
})
```

`GET /health` returns:

```json
{
  "status": "ok",
  "checks": { "database": { "status": "ok" } },
  "timestamp": "2026-03-29T10:00:00.000Z"
}
```

HTTP `200` when `ok` or `degraded`; `503` when any check returns `down`.

## Metrics (Prometheus)

Install the optional peer `prom-client`, then enable:

```bash
npm install prom-client
```

```typescript
new BananaApp({
  metrics: { enabled: true, path: '/metrics' },
  modules: [userModule],
})
```

`GET /metrics` returns Prometheus text-format. Counters tracked automatically:

| Metric                     | Labels                      |
| -------------------------- | --------------------------- |
| `http_requests_total`      | `method`, `route`, `status` |
| `http_request_duration_ms` | `method`, `route`, `status` |
| `http_errors_total`        | `method`, `route`, `status` |

If `prom-client` is not installed, the framework logs a warning and continues — no crash.

## DevTools

Enable in non-production to expose a route inspector:

```typescript
new BananaApp({ devTools: true, modules: [userModule] })
```

`GET /_banana/routes` returns:

```json
{
  "routes": [
    { "method": "GET", "path": "/users/:id", "controller": "UserController", "handler": "getById" }
  ],
  "count": 1,
  "timestamp": "2026-03-29T10:00:00.000Z"
}
```

Returns `404` in `NODE_ENV=production`. Also available as an instance method:

```typescript
const app = new BananaApp({ ... })
const table = app.getRouteTable()
```

## Performance: lazy controllers

By default, all controllers are resolved (and their DI graphs built) at startup. For large apps with many modules, defer instantiation to first request:

```typescript
new BananaApp({ lazyControllers: true, modules: [...manyModules] })
```

Trade-off: faster cold-start, slightly higher latency on the first hit per controller. Useful for serverless-style environments.

## Graceful shutdown

```typescript
new BananaApp({ gracefulShutdown: true, modules: [userModule] })
```

Hooks `SIGINT` and `SIGTERM`. Calls `plugin.onShutdown()` on every registered plugin — use it to flush connections, drain queues, or close DB pools cleanly.

## Caching

`@Cache` and `@CacheEvict` use the `CacheManager` singleton. The in-memory store is built-in; swap to Redis or any custom backend at startup.

```typescript
import { Cache, CacheEvict } from '@banana-universe/bananajs'

@Controller('products')
class ProductController extends BaseController {
  @Cache({ ttl: 120, key: (req) => `products:${req.params.id}` })
  @Params(idSchema)
  @Get('items/:id')
  async getById(req: Request, res: Response) {
    const { id } = req.params as { id: string }
    return this.ok(res, 'ok', await this.service.findById(id))
  }

  @CacheEvict({ pattern: 'products:*' })
  @Params(idSchema)
  @Delete('items/:id')
  async delete(req: Request, res: Response) {
    const { id } = req.params as { id: string }
    await this.service.delete(id)
    return this.ok(res, 'deleted', null)
  }
}
```

Custom store (e.g. Redis):

```typescript
new BananaApp({ cache: { store: new RedisCacheStore(redisClient) }, modules: [...] })
```

See [Caching reference](/reference/caching) for the full `CacheStore` interface.

## File uploads

`@Upload` integrates **multer** as an optional peer:

```bash
npm install multer
npm install -D @types/multer
```

```typescript
import { Upload } from '@banana-universe/bananajs'

@Post('avatar')
@Upload({ field: 'file', maxSizeMb: 5, allowedMimeTypes: ['image/jpeg', 'image/png'] })
async uploadAvatar(req: Request, res: Response) {
  const file = req.file    // typed by multer
  const url = await this.storage.save(file)
  return this.ok(res, 'created', { url })
}
```

## Rate limiting & throttle

`@RateLimit` and `@Throttle` work independently and can be stacked:

```typescript
import { RateLimit, Throttle } from '@banana-universe/bananajs'

@RateLimit({ windowMs: 60_000, max: 300 })    // 300 req/min — whole controller
@Controller('api')
class ApiController extends BaseController {
  @Throttle({ windowMs: 1_000, max: 5, keyBy: 'userId' })   // 5/sec per user
  @Body(searchSchema)
  @Post('search')
  async search(req: Request, res: Response) { ... }
}
```

Global rate limiting (applies before routes):

```typescript
new BananaApp({ rateLimit: { windowMs: 60_000, max: 1000 }, modules: [...] })
// opt out globally:
new BananaApp({ rateLimit: false, modules: [...] })
```

See [Security reference](/reference/security) for `@Throttle` vs `@RateLimit` comparison.

## Security helpers

```typescript
import { Sanitize, Can } from '@banana-universe/bananajs'

@Sanitize()    // strip HTML from all string fields in @Body before the handler runs
@Body(commentSchema)
@Post('comments')
async create(req: Request, res: Response) {
  const dto = req.body as CreateCommentDto
  return this.ok(res, 'created', await this.service.create(dto))
}
```

```typescript
@Auth()
@Can('delete', 'post')    // requires abac.guard
@Params(idSchema)
@Delete('posts/:id')
async delete(req: Request, res: Response) {
  const { id } = req.params as { id: string }
  await this.service.delete(id)
  return this.ok(res, 'deleted', null)
}
```

Configure ABAC at startup:

```typescript
import type { AbacGuard } from '@banana-universe/bananajs'

class MyAbacGuard implements AbacGuard {
  async can(user: AuthenticatedUser, action: string, resource: string): Promise<boolean> {
    return user.permissions.includes(`${action}:${resource}`)
  }
}

new BananaApp({ abac: { guard: new MyAbacGuard() }, modules: [...] })
```

See [Security reference](/reference/security) for the full guide.

## Multi-tenancy

BananaJS resolves a tenant ID per request via `AsyncLocalStorage` so any downstream code can call `getTenantId()` without threading the ID through every function signature:

```typescript
import { getTenantId } from '@banana-universe/bananajs'

new BananaApp({
  tenant: { extract: (req) => req.headers['x-tenant-id'] as string },
  modules: [userModule],
})
```

Inside any handler or service:

```typescript
async getAll(req: Request, res: Response) {
  const tenantId = getTenantId()    // reads from AsyncLocalStorage
  const users = await this.repo.findAll(tenantId)
  return this.ok(res, 'ok', users)
}
```

See [Multi-tenancy reference](/reference/multi-tenancy) for data isolation patterns (row-level, database-per-tenant, schema-per-tenant).

## Framework adapter

`FrameworkAdapter` and `RouteDefinition` provide a contracts layer for non-Express HTTP stacks. `@banana-universe/adapter-fastify` is an experimental stub. The current stable target is Express v5.

## Incremental migration via `BananaRouter`

Mount BananaJS-decorated routes into an **existing** Express app without a full rewrite:

```typescript
import express from 'express'
import { BananaRouter, ErrorMiddleware } from '@banana-universe/bananajs'
import { UserController } from './user/UserController'

const existing = express()
existing.use('/api', BananaRouter([UserController]))
existing.use(ErrorMiddleware)   // required — catches thrown ApiError instances
existing.listen(3000)
```

See [From Express](/migration/from-express) for the full step-by-step migration guide.

## WebSocket

Real-time features use `@banana-universe/plugin-websocket`. It is a `BananaPlugin` and requires `attachToServer(httpServer)` after the HTTP server starts:

```typescript
import { WebSocketPlugin } from '@banana-universe/plugin-websocket'

const app = await BananaApp.create({
  modules: [chatModule],
  plugins: [new WebSocketPlugin()],
})

const server = app.listen(3000)
WebSocketPlugin.attachToServer(server)
```

See [WebSocket plugin](/plugins/websocket).

## Next

- [Plugins overview](/plugins/overview)
- [Layered architecture & DDD](/guide/layered-architecture)
- [Recipes](/recipes/)
