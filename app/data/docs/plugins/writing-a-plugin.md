# Writing a plugin

Implement **`BananaPlugin`** from **`@banana-universe/bananajs`** (re-exported types are stable).

## Minimal example

```typescript
import type { BananaPlugin, AppContext } from '@banana-universe/bananajs'

export function RequestTimingPlugin(): BananaPlugin {
  return {
    name: 'request-timing',
    register(ctx: AppContext) {
      ctx.app.use((req, res, next) => {
        const start = Date.now()
        res.on('finish', () => {
          ctx.logger?.info(`${req.method} ${req.url} ${res.statusCode} ${Date.now() - start}ms`)
        })
        next()
      })
    },
  }
}
```

## Async registration

Use **`async register`** for dynamic imports or network checks — consumers must use **`BananaApp.create`**.

## Container integration

If **`ctx.container`** (tsyringe) exists, register shared singletons with **`registerInstance(token, value)`** or **`register(token, { useClass })`** so controllers resolved from the container receive dependencies.

## Peer dependencies

Declare optional integrations as **`peerDependencies`** with **`peerDependenciesMeta.optional: true`** so consumers only install what they use.

## Related

- [Plugins overview](/plugins/overview)
- [TypeDoc: `BananaPlugin`](/api/interfaces/BananaPlugin)
