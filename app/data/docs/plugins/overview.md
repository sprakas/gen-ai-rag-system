# Plugins overview

Plugins are the primary extension point in BananaJS. They wire middleware, open external connections, and register DI tokens — all before your controllers are mounted. Each plugin is a plain object that implements **`BananaPlugin`** from `@banana-universe/bananajs`.

## The interface

```typescript
interface BananaPlugin {
  name: string
  register(ctx: AppContext): void | Promise<void>
  onReady?(ctx: AppContext): void | Promise<void>
  onShutdown?(): void | Promise<void>
}
```

**`AppContext`** gives plugins access to:

| Property            | Type                             | Purpose                                                   |
| ------------------- | -------------------------------- | --------------------------------------------------------- |
| `app`               | `express.Application`            | Mount middleware, set headers, configure Express           |
| `logger`            | `Logger` (optional)              | Structured log output via the app's logger                |
| `container`         | `DependencyContainer` (optional) | tsyringe root container — register tokens here            |
| `controllerClasses` | `Function[]` (optional)          | Resolved controller classes, for post-route introspection |

## Lifecycle

Hooks run in this order for every plugin (sequentially by plugin array index):

```
BananaApp.create()
  └─ for each plugin in order:
       register()        ← middleware, DB open, SDK start
  └─ controllers mounted
  └─ for each plugin in order:
       onReady()         ← post-mount work (optional)

app.close() / SIGTERM
  └─ for each plugin in reverse order:
       onShutdown()      ← clean teardown (optional)
```

::: tip Always use `BananaApp.create` with async plugins
`new BananaApp(options)` is synchronous and will **not** await `register`. Use `await BananaApp.create(options)` whenever any plugin performs async work (opening DB connections, importing dynamic modules, etc.).
:::

## Registration

Pass **`plugins: BananaPlugin[]`** inside **`BananaAppOptions`**. Plugin order matters — `register` hooks run left to right, `onShutdown` hooks run right to left.

```typescript
import { BananaApp, defineBananaControllers } from '@banana-universe/bananajs'
import { TypeOrmPlugin } from '@banana-universe/plugin-typeorm'
import { OpenTelemetryPlugin } from '@banana-universe/plugin-otel'

await BananaApp.create({
  controllers: defineBananaControllers(UserController),
  plugins: [
    OpenTelemetryPlugin({ serviceName: 'my-api' }), // register first → traces DB calls
    TypeOrmPlugin({ type: 'postgres', url: process.env.DATABASE_URL, entities: [User] }),
  ],
})
```

## Container integration

If `ctx.container` is present, plugins can register DI tokens that controllers receive via constructor injection:

```typescript
import type { BananaPlugin, AppContext } from '@banana-universe/bananajs'
import { REDIS_CLIENT } from './tokens.js'
import { createClient } from 'redis'

export function RedisPlugin(url: string): BananaPlugin {
  let client: ReturnType<typeof createClient>
  return {
    name: 'redis',
    async register(ctx: AppContext) {
      client = createClient({ url })
      await client.connect()
      ctx.container?.registerInstance(REDIS_CLIENT, client)
    },
    async onShutdown() {
      await client.quit()
    },
  }
}
```

Controllers that inject `REDIS_CLIENT` will receive the connected instance after `register` completes.

## Official plugins (monorepo)

| Package                             | Factory / class                                      | Key features                                                        | Guide                                        |
| ----------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------- |
| `@banana-universe/plugin-typeorm`   | `TypeOrmPlugin(options)`                             | DataSource lifecycle, `@InjectRepository`, `@Transactional()`       | [TypeORM](/integrations/typeorm)             |
| `@banana-universe/plugin-mongoose`  | `MongoosePlugin(connection)`                         | Registers connection in container, `@Transactional()` with sessions | [Mongoose](/integrations/mongoose)           |
| `@banana-universe/plugin-otel`      | `OpenTelemetryPlugin({ serviceName, exporterUrl? })` | NodeSDK bootstrap, auto-instrumentation, OTLP export, SDK shutdown  | [OpenTelemetry](/integrations/opentelemetry) |
| `@banana-universe/plugin-websocket` | `new WebSocketPlugin({ path?, controllers })`        | `ws` server, decorator routing, `attachToServer`, graceful close    | [WebSocket](/plugins/websocket)              |
| `@banana-universe/plugin-ai`        | `BananaAiPlugin({ provider })`                       | Registers `LlmProvider` in the DI container for use across modules  | [AI](/ai/)                                   |

### Quick install

::: code-group

```bash [TypeORM]
npm install @banana-universe/plugin-typeorm typeorm reflect-metadata pg
```

```bash [Mongoose]
npm install @banana-universe/plugin-mongoose mongoose
```

```bash [OpenTelemetry]
npm install @banana-universe/plugin-otel \
  @opentelemetry/sdk-node \
  @opentelemetry/auto-instrumentations-node
```

```bash [WebSocket]
npm install @banana-universe/plugin-websocket ws
npm install -D @types/ws
```

```bash [AI]
npm install @banana-universe/plugin-ai @banana-universe/ai-provider-core
```

:::

## Peer dependencies

Official plugins declare optional integrations as `peerDependencies` with `peerDependenciesMeta.optional: true`. This means npm will not install the underlying library automatically — you add only what you use. A missing optional peer causes a startup warning, not a crash, unless the plugin explicitly requires it.

## Related

- [Writing a plugin](/plugins/writing-a-plugin)
- [WebSocket plugin](/plugins/websocket)
- [TypeORM integration](/integrations/typeorm)
- [Mongoose integration](/integrations/mongoose)
- [OpenTelemetry integration](/integrations/opentelemetry)
