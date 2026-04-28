# Migrating from Express

BananaJS runs on **Express** — middleware, `Request`/`Response`, and ecosystem packages still work. For a **step-by-step** migration strategy, the repository includes **`docs/MIGRATION.md`** (incremental adoption, `BananaRouter`, testing).

## Incremental mount with `BananaRouter`

Mount generated BananaJS routes under a prefix while legacy Express routes stay in place:

```typescript
import express from 'express'
import { BananaRouter } from '@banana-universe/bananajs'
import { UserController } from './user.controller.js'

const app = express()
app.use(express.json())

const bananaRoutes = BananaRouter([UserController])
app.use('/api/v2', bananaRoutes)

app.get('/legacy', (_req, res) => res.send('ok'))

app.listen(3000)
```

`BananaRouter` is a **function** that returns an Express **`Router`** — use it directly with `app.use`. (The longer **`docs/MIGRATION.md`** example in-repo may still say `new BananaRouter` / `.router`; prefer the pattern above.)

## What changes conceptually

| Express habit                       | BananaJS pattern                                  |
| ----------------------------------- | ------------------------------------------------- |
| Manual `router.get/post`            | `@Controller` + `@Get`/`@Post` on class methods   |
| Manual body/query validation        | `@Body(schema)` / `@Query(schema)` with validation |
| Ad-hoc `res.status().json()`        | `BaseController.ok` or `SuccessResponse` + `send` |
| Central `if (err)` in every handler | Throw `ApiError` subclasses + `ErrorMiddleware`   |

## Codemod

The CLI includes **`bananajs migrate`** — Express route codemod that emits `*.controller.ts` starters (see [CLI](/tooling/cli)).

## Tests

Use **`BananaTestApp`** from **`@banana-universe/bananajs/testing`** to hit your app over HTTP without binding a real port in every test.

## Related

- [Getting started](/guide/getting-started)
- [Advanced concepts](/guide/advanced-concepts)
