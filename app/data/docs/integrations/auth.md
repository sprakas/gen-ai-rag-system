# Authentication

BananaJS does **not** ship a built-in identity provider. It ships a **small contract**: you implement an **`AuthGuard`** (and optionally **`RolesGuard`**), pass it through **`BananaAppOptions.auth`**, and mark routes with **`@Auth`**, **`@Public`**, and **`@Roles`**. The framework wires **Express middleware** in the right order and maps failures to **`401`** / **`403`** consistently.

That separation matters in production: you keep **Passport**, **JWT**, **session cookies**, **mTLS**, or **API keys** behind one guard implementation—your controllers stay declarative.

## Mental model

```mermaid
flowchart TB
  subgraph req [Incoming request]
    H[Headers / cookies]
  end
  subgraph guard [Your AuthGuard]
    C[canActivate]
    R[extractRoles — optional]
  end
  subgraph fw [Framework]
    M[Auth middleware]
    RC[RequestContext user]
    H2[Handler]
  end
  H --> C
  C -->|false| U401[UnauthorisedError 401]
  C -->|true| R
  R -->|no matching role| U403[ForbiddenError 403]
  R -->|ok| M
  M --> RC
  RC --> H2
  style C fill:#0f2440,stroke:#fdb913,color:#f8fafc
  style R fill:#132a45,stroke:#5b7a8c,color:#f8fafc
  style M fill:#132a45,stroke:#fdb913,color:#f8fafc
  style U401 fill:#1a0a0a,stroke:#a0a9b8,color:#f8fafc
  style U403 fill:#1a0a0a,stroke:#a0a9b8,color:#f8fafc
```

1. **`canActivate(req)`** — return **`true`** only when the caller is authenticated (or your policy allows the request). Return **`false`** → **`401`**.
2. **`@Roles('admin', …)`** — if present, the guard must also implement **`extractRoles(req)`** ( **`RolesGuard`** ). If any required role is missing → **`403`**. If the guard has no **`extractRoles`**, **`@Roles`** cannot be satisfied → **`403`**.
3. **`req.user`** — if you attach **`user`** on the Express request, BananaJS copies it into **`RequestContext`** for the duration of the request (async-local), so downstream code can read the same identity without threading **`req`** everywhere.

## 1. Implement a guard

Implement **`AuthGuard`** from **`@banana-universe/bananajs`**. For **`@Roles`**, add **`extractRoles`** so the same object satisfies **`RolesGuard`**.

```typescript
import type { Request } from 'express'
import type { AuthGuard, RolesGuard } from '@banana-universe/bananajs'

// Example: Bearer token present; your verify() calls your IdP or JWT library.
async function verifyBearer(req: Request): Promise<{ sub: string; roles: string[] } | null> {
  const auth = req.headers.authorization
  if (typeof auth !== 'string' || !auth.startsWith('Bearer ')) return null
  const token = auth.slice(7)
  // Replace with your real verification (jwt.verify, introspection, etc.)
  if (token.length < 10) return null
  return { sub: 'user-1', roles: ['user'] }
}

export const bearerAuthGuard: AuthGuard & RolesGuard = {
  async canActivate(req: Request): Promise<boolean> {
    const session = await verifyBearer(req)
    if (!session) return false
    ;(req as unknown as { user: unknown }).user = { id: session.sub, roles: session.roles }
    return true
  },

  async extractRoles(req: Request): Promise<string[]> {
    const u = (req as unknown as { user?: { roles?: string[] } }).user
    return u?.roles ?? []
  },
}
```

::: tip Keep secrets out of the framework
Guard code runs in **your** app; load signing keys and issuer URLs from **environment** or **`BananaConfig`**, not from the docs.
:::

## 2. Register the guard on `BananaApp`

Pass **`auth: { guard: bearerAuthGuard }`** (or your factory) in **`BananaAppOptions`**. Without **`auth.guard`**, routes decorated with **`@Auth`** log a **warning** and **do not** run auth middleware—**`@Public`** is still honored for opting out.

```typescript
import { BananaApp, defineBananaControllers } from '@banana-universe/bananajs'
import { bearerAuthGuard } from './auth/bearer-guard.js'
import { ApiController } from './Api.controller.js'

export const app = new BananaApp({
  controllers: defineBananaControllers(ApiController),
  auth: { guard: bearerAuthGuard },
  swagger: { enabled: true, title: 'API', version: '1.0.0', path: '/api-docs' },
})
```

See [**BananaAppOptions**](/reference/bananaapp-options) for the full surface area.

## 3. Decorate controllers

| Decorator                       | Scope           | Meaning                                                                                                     |
| ------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------- |
| **`@Auth()`**                   | Class or method | This route is protected; requires **`canActivate`** unless overridden.                                      |
| **`@Public()`**                 | Method          | Skip auth for this handler **even if** the class is **`@Auth`** (use for health, login callback, webhooks). |
| **`@Roles('admin', 'editor')`** | Method          | After auth, require at least one of the listed roles.                                                       |

```typescript
import { Controller, Get, Auth, Public, Roles } from '@banana-universe/bananajs'

@Controller('api')
@Auth()
export class ApiController {
  @Get('health')
  @Public()
  health() {
    return { ok: true }
  }

  @Get('profile')
  profile() {
    // user was attached in the guard and mirrored to RequestContext
    return { message: 'authenticated' }
  }

  @Get('admin')
  @Roles('admin')
  adminOnly() {
    return { role: 'admin' }
  }
}
```

## Errors and HTTP status

| Failure                               | HTTP    | Error type              |
| ------------------------------------- | ------- | ----------------------- |
| **`canActivate`** returns **`false`** | **401** | **`UnauthorisedError`** |
| **`@Roles`** not satisfied            | **403** | **`ForbiddenError`**    |

These flow through **`ErrorMiddleware`** like other **`ApiError`** subclasses.

## OpenAPI (Swagger)

When **`auth`** is set on **`BananaApp`**, the generated spec includes **`BearerAuth`** (HTTP bearer, JWT-style) and marks protected operations with **`security: [{ BearerAuth: [] }]`** (unless the handler is **`@Public`**). See **`packages/bananajs/src/lib/OpenAPI/swagger.setup.ts`**.

Install **`@scalar/express-api-reference`** or **`swagger-ui-express`** to get a UI; otherwise the JSON spec is still served at **`/api-docs.json`** (path defaults—see **`swagger`** options).
## OpenAPI security schemes

When `auth` is set on `BananaApp`, the generated spec includes a `BearerAuth` scheme
(HTTP bearer, JWT-style). You can declare additional schemes and mark individual routes
using `@ApiSecurity`:

```typescript
import { Controller, Get, Auth, ApiSecurity } from '@banana-universe/bananajs'

@Controller('payments')
@Auth()
export class PaymentController {
  // Inherits BearerAuth from the auth guard
  @Get('invoices')
  listInvoices() { ... }

  // Requires an additional API-key scheme for machine-to-machine calls
  @Get('webhook-status')
  @ApiSecurity('ApiKeyAuth', 'BearerAuth')
  webhookStatus() { ... }
}
```

Declare the scheme definitions in the raw OpenAPI `components.securitySchemes` block
(pass it through `swagger.components` once that option is exposed, or extend the spec
in a plugin):

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

The `@ApiSecurity` decorator accepts one or more scheme names. Without arguments it
marks the route with the globally configured scheme (`BearerAuth` when auth guard is set).
## Beyond auth: ABAC with `@Can`

If you need **resource/action** checks (e.g. “can delete **this** document”), use **`@Can(action, resource)`** and provide **`abac: { guard: AbacGuard }`** in **`BananaAppOptions`**. That runs **after** authentication. See [**Advanced concepts**](/guide/advanced-concepts) and TypeDoc for **`AbacGuard`**.

## Testing

### Option 1 — Fake guard via `auth` option

Provide an always-pass guard in `BananaTestApp.create`:

```typescript
import { BananaTestApp } from '@banana-universe/bananajs/testing'
import type { AuthGuard, RolesGuard } from '@banana-universe/bananajs'

const testGuard: AuthGuard & RolesGuard = {
  async canActivate(req) {
    ;(req as any).user = { id: 'test-user-1', roles: ['admin'] }
    return true
  },
  async extractRoles(req) {
    return (req as any).user?.roles ?? []
  },
}

const app = await BananaTestApp.create({
  controllers: defineBananaControllers(ApiController),
  auth: { guard: testGuard },
})
```

### Option 2 — Real JWT token with test secret

If your guard verifies JWTs, sign a test token with your test key:

```typescript
import jwt from 'jsonwebtoken'

const TEST_SECRET = process.env.JWT_SECRET ?? 'test-only'
const token = jwt.sign({ sub: 'user-42', roles: ['editor'] }, TEST_SECRET, { expiresIn: '1h' })

app.withAuth(token)
const res = await app.request().get('/api/profile')
expect(res.status).toBe(200)
```

### Option 3 — Test unauthenticated behavior

```typescript
app.clearHeaders()  // remove any Bearer token set by withAuth

const res = await app.request().get('/api/admin')
expect(res.status).toBe(401)
expect(res.body.statusCode).toBe('error')
```

Full testing guide: [Testing](/reference/testing).

## Related

- [Decorators — Auth & security](/reference/decorators#auth-security)
- [Security](/reference/security) — ABAC (`@Can`), rate limiting, input sanitization
- [Testing](/reference/testing) — `BananaTestApp`, `testOverrides`, auth helpers
- [BananaAppOptions — `auth`](/reference/bananaapp-options#auth-docs)
- TypeDoc: [`AuthGuard`](/api/interfaces/AuthGuard), [`RolesGuard`](/api/interfaces/RolesGuard)
