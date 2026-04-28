# Core concepts

This page builds a mental model for the five pillars of every BananaJS app: **controllers**, **routing**, **validation**, **responses**, and **errors**. If you ran the [Quickstart](/guide/quickstart), you've already seen these in action — this page explains the "why" behind each decision.

## What is a controller?

A **controller** is a TypeScript class whose methods map to HTTP endpoints. Think of it as a router file that self-describes what it handles — no separate route registration needed.

```typescript
import { Controller, Get } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

@Controller('users')           // Base path: /users
export class UserController {
  @Get('')                     // GET /users
  list(_req: Request, res: Response) {
    res.json({ users: [] })
  }

  @Get(':id')                  // GET /users/:id
  getOne(req: Request, res: Response) {
    res.json({ id: req.params.id })
  }
}
```

**Key rule:** Both `@Controller` and route decorators use **slash-free segments**. The framework joins them into Express paths automatically. Write `'users'`, not `'/users'`.

### Registering controllers

Controllers live inside **modules**. A module is a feature slice that groups a controller with its providers:

```typescript
import { createModule, BananaApp } from '@banana-universe/bananajs'

export const userModule = createModule({
  id: 'user',
  controller: UserController,
  providers: [],              // services, repos, etc. added here
})

await BananaApp.create({ modules: [userModule] })
```

BananaJS reads the decorator metadata at startup, creates an Express Router per controller, and wires everything together. You never call `new UserController()` yourself.

## HTTP method decorators

| Decorator | Method | Example path |
|-----------|--------|-------------|
| `@Get(path)` | GET | `@Get('list')` → `GET /users/list` |
| `@Post(path)` | POST | `@Post('')` → `POST /users` |
| `@Put(path)` | PUT | `@Put(':id')` → `PUT /users/:id` |
| `@Patch(path)` | PATCH | `@Patch(':id/status')` → `PATCH /users/:id/status` |
| `@Delete(path)` | DELETE | `@Delete(':id')` → `DELETE /users/:id` |

All five accept optional **per-route middlewares** as additional arguments:

```typescript
@Get('protected', authMiddleware, logMiddleware)
protectedRoute(req: Request, res: Response) { ... }
```

## Validation {#validation}

BananaJS validates request data **declaratively** using **validation schemas**. Add a decorator and the framework runs validation before your handler — you never write `if (!req.body.email) return res.status(400)...` manually.

```typescript
import { Body, Params, Query } from '@banana-universe/bananajs'
import { z } from 'zod'

// --- Schemas ---
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.coerce.number().int().min(0).optional(),
})

const UserIdSchema = z.object({
  id: z.string().uuid(),
})

const SearchSchema = z.object({
  q: z.string().optional(),
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
})

// --- Controller ---
@Controller('users')
export class UserController extends BaseController {

  @Get('')
  @Query(SearchSchema)          // Validates req.query
  list(req: Request, res: Response) {
    const { q, page, limit } = req.query as z.infer<typeof SearchSchema>
    // page and limit are already numbers, not strings
    return this.ok(res, 'Users fetched', { q, page, limit })
  }

  @Post('')
  @Body(CreateUserSchema)       // Validates req.body
  create(req: Request, res: Response) {
    const data = req.body as z.infer<typeof CreateUserSchema>
    // data.email, data.name, data.age are fully typed
    return this.ok(res, 'User created', data)
  }

  @Get(':id')
  @Params(UserIdSchema)         // Validates req.params
  getOne(req: Request, res: Response) {
    const { id } = req.params as z.infer<typeof UserIdSchema>
    return this.ok(res, 'User found', { id })
  }
}
```

**What happens when validation fails?** BananaJS throws a `BadRequestError` automatically. Your handler never runs. The response shape is consistent:

```json
{
  "statusCode": "error",
  "status": 400,
  "message": "Validation failed: email: Invalid email"
}
```

**`@Headers(schema)`** works the same way for request headers.

::: tip Schema coercion for query params
Query string values are always strings in Express. Use `z.coerce.number()` instead of `z.number()` for numeric query params — it converts `"42"` to `42` before passing to your handler.
:::

## Responses

BananaJS response types enforce a **single JSON shape** across every endpoint. That predictability is what lets frontend clients and API consumers behave reliably.

### BaseController helpers

Extend **`BaseController`** to get `this.ok()` and `this.error()`:

```typescript
import { Controller, Get, BaseController } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

@Controller('products')
export class ProductController extends BaseController {

  @Get(':id')
  async getProduct(req: Request, res: Response) {
    const product = await fetchProduct(req.params.id)
    if (!product) {
      return this.error(res, new NotFoundError('Product not found'))
    }
    return this.ok(res, 'Product found', product)
    //   ↑ statusCode: "success", status: 200, message: ..., data: product
  }
}
```

**`this.ok(res, message, data)`** calls `SuccessResponse` under the hood.

### Pagination

For paginated lists, use **`PaginatedResponse`** and **`PaginationQuerySchema`**:

```typescript
import { PaginatedResponse, PaginationQuerySchema, Query } from '@banana-universe/bananajs'
import { z } from 'zod'

@Get('list')
@Query(PaginationQuerySchema)
async list(req: Request, res: Response) {
  const { page, limit } = req.query as z.infer<typeof PaginationQuerySchema>
  const [items, total] = await getItems(page, limit)

  const response = new PaginatedResponse(
    'Items fetched',
    items,
    { page, limit, total, totalPages: Math.ceil(total / limit) },
  )
  response.send(res)
}
```

Response shape includes a `meta` object: `{ page, limit, total, totalPages }`.

## Errors

BananaJS uses typed error classes so every error produces an **expected, consistent HTTP response**. The pattern: **throw a specific error class**; **`ErrorMiddleware` catches it**.

### Throwing errors

```typescript
import {
  NotFoundError,
  BadRequestError,
  UnauthorisedError,
  ForbiddenError,
  ConflictError,
} from '@banana-universe/bananajs'

// Inside any controller method or async handler:
throw new NotFoundError('User not found')         // → 404
throw new BadRequestError('Email already exists') // → 400
throw new UnauthorisedError()                      // → 401
throw new ForbiddenError('Admin only')             // → 403
throw new ConflictError('Duplicate entry')         // → 409
```

### Wiring the error middleware

Add **`ErrorMiddleware`** **after** all routes. BananaJS does this for you when using `BananaApp`, but if you're using `BananaRouter` for incremental adoption, you must add it yourself:

```typescript
import { ErrorMiddleware } from '@banana-universe/bananajs'

// After all routes:
app.use(ErrorMiddleware)
```

### Error response shape

Every error follows the same envelope:

```json
{
  "statusCode": "error",
  "status": 404,
  "message": "User not found"
}
```

In **production** (`NODE_ENV=production`), `InternalError` messages are masked to prevent leaking stack traces or sensitive internals.

Full error class list: [Error types reference](/reference/error-types).

## App bootstrap: `new BananaApp` vs `BananaApp.create`

| Method | When to use |
|--------|-------------|
| `new BananaApp(options)` | Synchronous-only apps with no plugins needing async setup |
| `await BananaApp.create(options)` | Whenever you use **plugins** (TypeORM, Mongoose, OTel, WebSocket) |

```typescript
// Simple sync bootstrap
new BananaApp({
  modules: [userModule],
})

// Async bootstrap with plugins
const app = await BananaApp.create({
  modules: [userModule],
  plugins: [TypeOrmPlugin({ ... })],
})
```

::: tip One options object, always
Whether you use `new BananaApp` or `BananaApp.create`, the argument is always **one plain object**. There is no second argument or method chaining for configuration.
:::

## How it all connects

```
Request → Express HTTP pipeline
       → Validation middleware (@Body / @Query / @Params / @Headers)
            ↓ invalid: BadRequestError → ErrorMiddleware → 400 JSON
            ↓ valid: req.body / req.query / req.params updated with parsed data
       → Your controller method
            ↓ business logic
       → this.ok(res, ...) OR throw ApiError subclass
            ↓ thrown: ErrorMiddleware → typed JSON response
            ↓ ok: SuccessResponse JSON
```

## Next steps

- Continue to [Getting started](/guide/getting-started) for full project setup with the CLI
- Jump to [Authentication](/integrations/auth) to add guards
- See [Dependency injection](/guide/dependency-injection) when you need services and modules
- Browse the [Decorator reference](/reference/decorators) for the full public API surface

