# Security Hardening

BananaJS ships several security primitives. This guide maps each one to the
[OWASP Top 10](https://owasp.org/Top10/) category it addresses and shows the
recommended production configuration.

## Quick checklist

| Concern | Primitive | Default safe? |
|---|---|---|
| HTTP security headers | `helmet` | ✅ enabled by default |
| CORS origin restriction | `cors` + `createCorsOptions` | ⚠️ warns if no `origin` set |
| Request body size limit | `bodyLimit` | ✅ `1mb` default |
| URL-encoded prototype pollution | `urlencoded extended` | ✅ `false` by default |
| Rate limiting (global) | `rateLimit` option | ⚠️ opt-in |
| Per-route throttling | `@Throttle` | ⚠️ opt-in |
| Authentication | `AuthGuard` + `@Auth` | ⚠️ opt-in |
| Role-based access | `RolesGuard` + `@Roles` | ⚠️ opt-in |
| Resource/action access | `AbacGuard` + `@Can` | ⚠️ opt-in |
| Input validation | `@Body` / `@Query` (validation) | ⚠️ opt-in per route |
| HTML sanitisation | `@Sanitize` | ⚠️ opt-in per route |
| Secret management | `BananaConfig` `sensitive` | ⚠️ opt-in per field |
| Log redaction | `PinoLogger` default paths | ✅ enabled by default |
| Dependency CVEs | `npm audit` + Dependabot | ✅ CI enforced |

---

## A05 — Security Misconfiguration

### HTTP security headers (Helmet)

Helmet is enabled by default. For production, configure Content Security Policy and
HSTS preload:

```typescript
import { BananaApp, type HelmetOptions } from '@banana-universe/bananajs'

const helmetConfig: HelmetOptions = {
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },
  hsts: {
    maxAge: 31536000,       // 1 year
    includeSubDomains: true,
    preload: true,
  },
}

new BananaApp({
  controllers: [...],
  security: { helmet: helmetConfig },
})
```

To disable helmet entirely (testing only — never in production):

```typescript
security: { helmet: false }
```

### CORS — explicit origin allowlist

BananaJS logs a warning at startup when CORS is enabled without an explicit `origin`,
because the default allows all origins. Use `createCorsOptions` in production:

```typescript
import { BananaApp, createCorsOptions } from '@banana-universe/bananajs'

new BananaApp({
  controllers: [...],
  security: {
    cors: createCorsOptions([
      'https://app.example.com',
      'https://admin.example.com',
    ]),
  },
})
```

### Request body size limit

The default is `1mb`. Lower it for APIs that only handle small payloads:

```typescript
new BananaApp({
  controllers: [...],
  bodyLimit: '100kb',
})
```

Requests that exceed `bodyLimit` are rejected with `413 Payload Too Large` before
they reach any controller.

---

## A03 — Injection

### Input validation

Validate every external input at the boundary using `@Body`, `@Query`, `@Params`,
or `@Headers`. The decorator parses the request through the schema and replaces
`req.body` (etc.) with the validated, type-safe value — downstream code never
touches raw unvalidated input.

```typescript
import { z } from 'zod'
import { Controller, Post, Body } from '@banana-universe/bananajs'

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
})

@Controller('users')
export class UserController {
  @Post('')
  create(@Body(CreateUserSchema) body: z.infer<typeof CreateUserSchema>) {
    // body is guaranteed to match the schema
  }
}
```

### HTML sanitisation

Use `@Sanitize` on handlers that accept HTML content (rich text editors, CMS
fields). Requires `sanitize-html` peer:

```typescript
import { Sanitize } from '@banana-universe/bananajs'

@Post('articles')
@Sanitize({ allowedTags: ['b', 'i', 'em', 'strong', 'a'], allowedAttributes: { a: ['href'] } })
createArticle(@Body(ArticleSchema) body: ArticleDto) { ... }
```

### SQL / NoSQL injection prevention

**TypeORM** — always use query builder parameters or the ORM's entity methods.
Never interpolate user input into raw query strings:

```typescript
// ✅ safe
await repo.findOne({ where: { email: userInput } })
await repo.createQueryBuilder('u').where('u.email = :email', { email: userInput }).getOne()

// ❌ unsafe
await dataSource.query(`SELECT * FROM users WHERE email = '${userInput}'`)
```

**Mongoose** — avoid passing raw query objects from `req.body` directly to Mongoose
operators (`$where`, `$regex`). Validate shapes before querying:

```typescript
// ✅ validated first
const parsed = QuerySchema.parse(req.query)
await UserModel.findOne({ email: parsed.email })
```

---

## A07 — Authentication Failures

### AuthGuard

Implement `AuthGuard` and pass it to `BananaApp`. See [Authentication](/integrations/auth)
for the full API. Key points:

- Sign JWTs with a strong secret stored in an environment variable, never in source code.
- Use short expiry (`15m` – `1h`) and implement refresh token rotation.
- Attach `user` to `req` inside `canActivate` — the framework stores it in `RequestContext`.

```typescript
new BananaApp({
  controllers: [...],
  auth: { guard: jwtAuthGuard },
})
```

### ABAC with `@Can`

For resource/action access control that goes beyond roles, implement `AbacGuard`:

```typescript
import type { AbacGuard } from '@banana-universe/bananajs'

export const abacGuard: AbacGuard = {
  can(action, resource, req) {
    const user = (req as any).user
    // e.g. 'delete' on 'document' requires ownership or admin role
    if (action === 'delete' && resource === 'document') {
      return user?.roles?.includes('admin') ?? false
    }
    return true
  },
}

new BananaApp({
  controllers: [...],
  auth: { guard: jwtAuthGuard },
  abac: { guard: abacGuard },
})
```

Decorate routes with `@Can(action, resource)` — runs after authentication:

```typescript
@Delete('documents/:id')
@Auth()
@Can('delete', 'document')
deleteDocument(@Params(ParamsSchema) params: { id: string }) { ... }
```

---

## A02 — Cryptographic Failures

### Secret management with `BananaConfig`

Mark sensitive configuration fields with `sensitive: true`. The framework:
- Validates that required secrets are present at startup (fail-fast).
- Prevents accidentally leaking them via `JSON.stringify` (e.g. in an error response).

```typescript
import { BananaConfig } from '@banana-universe/bananajs'

export const config = BananaConfig({
  jwtSecret: { env: 'JWT_SECRET', required: true, sensitive: true },
  dbPassword: { env: 'DB_PASSWORD', required: true, sensitive: true },
  appName:    { env: 'APP_NAME',   default: 'MyApp' },
})

// Safe: returns real value for code use
const secret = config.get().jwtSecret

// Safe: '[REDACTED]' in JSON output — never leaks in logs or error responses
JSON.stringify(config.get())
// => '{"jwtSecret":"[REDACTED]","dbPassword":"[REDACTED]","appName":"MyApp"}'
```

---

## A09 — Security Logging and Monitoring Failures

### PinoLogger default redaction

`PinoLogger` redacts the following field paths from log output by default:

- `password`, `token`, `authorization`, `cookie`
- `*.secret`, `*.apiKey`, `*.api_key`, `*.accessToken`, `*.access_token`

You can extend the list via the constructor:

```typescript
import { PinoLogger } from '@banana-universe/bananajs'

const logger = new PinoLogger({
  redact: {
    paths: ['*.ssn', '*.creditCard'],
    censor: '[REDACTED]',
  },
})
```

Custom paths are merged with the defaults — they do not replace them.

---

## A06 — Vulnerable and Outdated Components

The repository enforces:

- **`npm audit --audit-level=high`** on every PR and push to `main` (`.github/workflows/security-audit.yml`).
- **Dependabot weekly security PRs** for all npm packages and GitHub Actions (`.github/dependabot.yml`).
- **CodeQL static analysis** on every PR (`.github/workflows/codeql.yml`).

---

## Rate limiting

### Global rate limiting

Apply a default limit to all routes:

```typescript
new BananaApp({
  controllers: [...],
  rateLimit: { windowMs: 60_000, max: 100 },
})
```

Requires `express-rate-limit` peer: `npm install express-rate-limit`.

### Per-route throttling with `@Throttle`

`@Throttle` supports per-user or per-IP keying and an optional distributed store
for multi-instance deployments:

```typescript
import { Throttle } from '@banana-universe/bananajs'

@Post('login')
@Throttle({ windowMs: 60_000, max: 5, keyBy: 'ip', message: 'Too many login attempts' })
login(@Body(LoginSchema) body: LoginDto) { ... }
```

For distributed environments, implement `ThrottleStore` and pass it as `store`:

```typescript
import type { ThrottleStore } from '@banana-universe/bananajs'

const redisThrottleStore: ThrottleStore = {
  async consume(key) { /* increment in Redis, throw on limit */ },
  async reset(key)   { /* delete key in Redis */ },
}

@Post('login')
@Throttle({ windowMs: 60_000, max: 5, keyBy: 'ip', store: redisThrottleStore })
login(@Body(LoginSchema) body: LoginDto) { ... }
```
