# Security

BananaJS provides four security layers: **rate limiting**, **per-user throttling**, **ABAC authorization**, and **input sanitization**. Most are decorator-based and composable with auth guards.

## Rate limiting

Rate limiting rejects requests that exceed a threshold. Two decorators cover different use cases.

### `@RateLimit` — IP-based limiting

Uses `express-rate-limit` (optional peer) to limit requests per IP:

```bash
npm install express-rate-limit
```

```typescript
import { RateLimit, Controller, Get } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

// Class-level: 100 requests per 15 minutes for all routes in this controller
@Controller('api')
@RateLimit({ windowMs: 15 * 60 * 1000, max: 100 })
export class ApiController {
  @Get('data')
  getData(req: Request, res: Response) { ... }
}

// Method-level: stricter limit for expensive operations
@Controller('auth')
export class AuthController {
  @Post('login')
  @RateLimit({ windowMs: 60 * 1000, max: 5 })   // 5 attempts per minute
  login(req: Request, res: Response) { ... }
}
```

When the limit is exceeded, BananaJS returns `TooManyRequestsError` (429).

### Global rate limiting via `BananaAppOptions`

Apply a limit across the entire app:

```typescript
new BananaApp({
  controllers: defineBananaControllers(UserController),
  rateLimit: {
    windowMs: 15 * 60 * 1000,
    max: 1000,
  },
})
```

Disable globally with `rateLimit: false` (useful in tests — `BananaTestApp` sets this by default).

### `@Throttle` — user-based throttling

`@Throttle` limits per **user** (via JWT `sub` claim) rather than per IP. This prevents a single authenticated user from hammering an endpoint even from different IPs:

```typescript
import { Throttle } from '@banana-universe/bananajs'

@Controller('ai')
@Auth()
export class AiController {
  @Post('generate')
  @Throttle({ windowMs: 60_000, max: 10, keyBy: 'user' })  // 10 per minute per user
  async generate(req: Request, res: Response) { ... }
}
```

**Options:**

| Option | Type | Description |
|---|---|---|
| `windowMs` | `number` | Time window in milliseconds |
| `max` | `number` | Maximum requests in the window |
| `keyBy` | `'user' \| 'ip'` | `'user'` uses JWT `sub`; `'ip'` uses remote IP |

## ABAC authorization with `@Can`

ABAC (attribute-based access control) is more granular than role checks — it asks "can _this_ user perform _this action_ on _this resource_?" You implement the `AbacGuard` interface; BananaJS runs it after authentication.

### 1. Implement `AbacGuard`

```typescript
import type { AbacGuard } from '@banana-universe/bananajs'
import type { Request } from 'express'

export const resourceGuard: AbacGuard = {
  async can(action: string, resource: string, req: Request): Promise<boolean> {
    const user = (req as any).user   // set by AuthGuard.canActivate
    if (!user) return false

    if (action === 'delete' && resource === 'post') {
      // Only admins or the post owner can delete
      const post = await Post.findById(req.params.id)
      return user.roles.includes('admin') || post?.authorId === user.id
    }

    if (action === 'read' && resource === 'user') {
      // Users can read their own record; admins can read all
      return user.roles.includes('admin') || req.params.id === user.id
    }

    return false  // deny by default
  },
}
```

### 2. Register the guard

```typescript
new BananaApp({
  controllers: defineBananaControllers(PostController),
  auth: { guard: bearerAuthGuard },
  abac: { guard: resourceGuard },
})
```

### 3. Apply `@Can` to routes

```typescript
import { Can, Auth, Controller, Delete, Get } from '@banana-universe/bananajs'

@Controller('posts')
@Auth()
export class PostController extends BaseController {

  @Get(':id')
  @Can('read', 'post')          // runs resourceGuard.can('read', 'post', req)
  async getPost(req: Request, res: Response) { ... }

  @Delete(':id')
  @Can('delete', 'post')        // checks ownership or admin role
  async deletePost(req: Request, res: Response) { ... }
}
```

`@Can` runs **after** `@Auth` — the caller is already authenticated when ABAC runs.

**Failure:** Returns `ForbiddenError` (403) when `AbacGuard.can` returns `false`.

### ABAC vs role checks

| Use | When the question is |
|---|---|
| `@Roles('admin')` | "Does the user have this role?" — simple membership check |
| `@Can('action', 'resource')` | "Is this user allowed to do this to _that specific thing_?" — ownership or attribute-based |

Use both: `@Auth() @Roles('editor') @Can('publish', 'post')` chains naturally.

## Input sanitization with `@Sanitize`

`@Sanitize` strips dangerous HTML from string fields in `req.body` before the handler runs. It uses `sanitize-html` (optional peer):

```bash
npm install sanitize-html
npm install -D @types/sanitize-html
```

```typescript
import { Sanitize } from '@banana-universe/bananajs'

@Post('comment')
@Body(CreateCommentSchema)
@Sanitize()
async createComment(req: Request, res: Response) {
  // req.body.content is sanitized — <script> tags and onclick handlers removed
  const comment = await this.service.create(req.body)
  return this.ok(res, 'Comment added', comment)
}
```

**What it strips:** `<script>`, `<iframe>`, `onclick`, `onerror`, and other XSS vectors. Safe tags like `<b>`, `<em>`, `<p>` are preserved by default.

**Customizing:**

```typescript
@Sanitize({
  allowedTags: ['b', 'i', 'em', 'strong'],   // only allow formatting
  allowedAttributes: {},                       // no attributes at all
})
@Post('bio')
async updateBio(req: Request, res: Response) { ... }
```

Options are passed directly to `sanitize-html`. See the [sanitize-html docs](https://github.com/apostrophecms/sanitize-html) for the full option set.

**Scope:** `@Sanitize` operates on all **string** fields in `req.body`. Non-string fields are untouched.

::: warning @Body runs first
Run `@Body(schema)` before `@Sanitize` — validation ensures the body shape is correct, then sanitization cleans the string content. The decorator apply order in TypeScript is bottom-to-top at runtime, but both frameworks handle this correctly when stacked together.
:::

## Helmet and CORS

BananaJS applies `helmet` and `cors` by default. Customize or disable per-app:

```typescript
new BananaApp({
  controllers: defineBananaControllers(UserController),
  security: {
    helmet: {
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", 'cdn.example.com'],
        },
      },
    },
    cors: {
      origin: ['https://app.example.com', 'https://mobile.example.com'],
      credentials: true,
    },
  },
})

// Disable both (for development only):
security: { helmet: false, cors: false }
```

## Security checklist

| Layer | How BananaJS covers it |
|---|---|
| Input validation | `@Body`, `@Query`, `@Params` with validation schemas — rejects malformed input before handlers |
| HTML injection / XSS | `@Sanitize` strips unsafe HTML from string fields |
| SQL / ORM injection | Use TypeORM/Mongoose query builders, not raw string concatenation |
| Auth | `@Auth`, `@Roles`, `AuthGuard` — pluggable identity verification |
| Authorization | `@Can`, `AbacGuard` — resource-level access decisions |
| Rate limiting | `@RateLimit`, `@Throttle` — IP and user-based limits |
| HTTP header hardening | `security.helmet` — defaults on |
| CORS | `security.cors` — configurable origins |
| Secret leakage | `InternalError` messages are masked in production |
| Error details | `errorMiddleware` never exposes stack traces in production |

## Related

- [Authentication](/integrations/auth) — `@Auth`, `@Roles`, `AuthGuard` setup
- [Advanced concepts](/guide/advanced-concepts) — `rateLimit`, `abac` options in `BananaAppOptions`
- [Decorators reference](/reference/decorators) — `@RateLimit`, `@Throttle`, `@Sanitize`, `@Can`
- TypeDoc: [`AbacGuard`](/api/interfaces/AbacGuard)
