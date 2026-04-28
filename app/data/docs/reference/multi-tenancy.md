# Multi-tenancy

BananaJS ships a complete multi-tenancy system based on `AsyncLocalStorage`. The tenant ID is extracted from each request, stored in a context that persists through the async call chain, and optionally used to namespace cache keys. No request object is threaded through service code.

## Mental model

```mermaid
flowchart LR
  R[Incoming request] --> M[createTenantMiddleware]
  M -->|x-tenant-id header OR JWT tid claim| S[TenantContext.run]
  S --> C[Controller]
  C --> SVC[Service]
  SVC -->|getTenantId| T[Tenant ID from context]
  style M fill:#0f2440,stroke:#fdb913,color:#f8fafc
  style S fill:#132a45,stroke:#5b7a8c,color:#f8fafc
  style T fill:#0f2440,stroke:#fdb913,color:#f8fafc
```

The middleware establishes the tenant scope. Every `await` in the request handler runs inside that scope. `getTenantId()` reads from it — no `req` argument needed.

## Setup

### 1. Add the tenant option

```typescript
import { BananaApp, defineBananaControllers } from '@banana-universe/bananajs'

new BananaApp({
  controllers: defineBananaControllers(NoteController),
  tenant: {
    header: 'x-tenant-id',   // extract from this header (default)
    // OR:
    jwtClaim: 'tid',          // extract from JWT payload claim
    // OR both — header takes precedence
  },
})
```

`BananaApp` registers `createTenantMiddleware()` automatically when `tenant` is set.

### 2. Use `@Tenant()` to mark controllers

`@Tenant()` is a marker that documents tenant-awareness and enables automatic cache key namespacing:

```typescript
import { Controller, Get, Tenant, getTenantId, BaseController } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

@Controller('notes')
@Tenant()
export class NoteController extends BaseController {

  @Get('')
  async listNotes(_req: Request, res: Response) {
    const tenantId = getTenantId()   // '42', 'acme-corp', etc.
    const notes = await this.service.findByTenant(tenantId)
    return this.ok(res, 'Notes', notes)
  }
}
```

## Extracting the tenant ID

### Via header (default)

```http
GET /notes HTTP/1.1
x-tenant-id: acme-corp
Authorization: Bearer <token>
```

### Via JWT claim

If you prefer to encode tenant identity inside the JWT:

```typescript
tenant: { jwtClaim: 'tid' }
```

The middleware decodes (but **does not verify**) the JWT to read the `tid` claim. Verification is your `AuthGuard`'s job — the tenant middleware only reads the claim value.

### Custom extraction

For non-standard schemes (subdomain, path prefix, database lookup), implement your own tenant middleware using `runWithTenant`:

```typescript
import { runWithTenant } from '@banana-universe/bananajs'
import type { RequestHandler } from 'express'

export const subdomainTenantMiddleware: RequestHandler = (req, _res, next) => {
  // e.g. acme.example.com → 'acme'
  const tenantId = req.hostname.split('.')[0]
  if (!tenantId || tenantId === 'www') {
    return next(new BadRequestError('Cannot determine tenant'))
  }
  runWithTenant(tenantId, next)
}
```

Register as a global middleware:

```typescript
new BananaApp({
  controllers: defineBananaControllers(NoteController),
  middlewares: [subdomainTenantMiddleware],
})
```

## `TenantContext` API

| Export | Signature | Description |
|---|---|---|
| `getTenantId()` | `() => string \| undefined` | Current tenant from `AsyncLocalStorage` |
| `runWithTenant(id, fn)` | `(tenantId: string, fn: () => void) => void` | Run `fn` inside a tenant scope |
| `TenantContext` | class | `AsyncLocalStorage`-backed context; advanced use |
| `createTenantMiddleware(options?)` | `() => RequestHandler` | Factory for the built-in middleware |
| `@Tenant(options?)` | class/method decorator | Mark controller as tenant-scoped; enables cache namespacing |

## Data isolation patterns

Multi-tenancy is only meaningful when data is actually isolated. Three common patterns:

### Pattern 1 — Row-level isolation (shared database)

Add a `tenantId` column to every tenant-scoped table:

```typescript
// TypeORM entity
@Entity()
export class Note {
  @PrimaryGeneratedColumn('uuid')
  id: string

  @Column()
  tenantId: string       // every query must filter by this

  @Column('text')
  content: string
}
```

In the repository adapter, always include the tenant filter:

```typescript
async findByTenant(tenantId: string): Promise<Note[]> {
  return this.ds.getRepository(NoteOrmEntity).find({
    where: { tenantId },
  })
}

// Even findById should filter by tenant to prevent cross-tenant access
async findById(id: string, tenantId: string): Promise<Note | null> {
  return this.ds.getRepository(NoteOrmEntity).findOne({
    where: { id, tenantId },   // tenant filter prevents data leakage
  })
}
```

### Pattern 2 — Database-per-tenant

Create a separate database (or schema) per tenant and switch connections per request:

```typescript
import { getTenantId } from '@banana-universe/bananajs'

@injectable()
export class TenantDataSourceFactory {
  private sources = new Map<string, DataSource>()

  async getForTenant(): Promise<DataSource> {
    const tenantId = getTenantId()!
    if (!this.sources.has(tenantId)) {
      const ds = new DataSource({
        type: 'postgres',
        database: `tenant_${tenantId}`,
        entities: [NoteOrmEntity],
      })
      await ds.initialize()
      this.sources.set(tenantId, ds)
    }
    return this.sources.get(tenantId)!
  }
}
```

### Pattern 3 — Schema-per-tenant (PostgreSQL)

Set the `search_path` per request for full schema isolation without separate databases. See `docs/MULTI-TENANCY.md` in the repository for the full PostgreSQL schema isolation guide.

## Cache isolation

When `@Tenant()` is applied, `@Cache` decorators automatically prefix keys with the tenant ID:

```typescript
@Controller('products')
@Tenant()
export class ProductController {
  @Get(':id')
  @Cache({ ttl: 300, key: (req) => `product:${req.params.id}` })
  async getProduct(req: Request, res: Response) {
    // Stored as 'acme-corp:product:123', not 'product:123'
    // tenant-B cannot see tenant-A's cached products
  }
}
```

For programmatic caching via `CacheManager`, namespace keys manually:

```typescript
import { getTenantId } from '@banana-universe/bananajs'

const key = `${getTenantId()}:product:${productId}`
await CacheManager.getInstance().set(key, product, 300)
```

## Testing with tenants

Use `withHeaders` on `BananaTestApp` to set the tenant header:

```typescript
import { BananaTestApp } from '@banana-universe/bananajs/testing'

const app = await BananaTestApp.create({ ... })

// Scope all next requests to tenant 'acme'
app.withHeaders({ 'x-tenant-id': 'acme' })
const res = await app.request().get('/notes')

// Switch tenant
app.withHeaders({ 'x-tenant-id': 'globex' })
const res2 = await app.request().get('/notes')
```

## Security considerations

- **Never trust client-provided tenant IDs without validation** — verify that the authenticated user belongs to the claimed tenant in your `AuthGuard` before the tenant middleware runs, or validate inside the guard.
- **Filter all queries by tenant** — a missing `WHERE tenantId = $1` leaks data. Use base repository classes or interceptors to enforce this automatically where possible.
- **Audit cross-tenant operations** — admin endpoints that can access all tenants should log access and require elevated roles.

## Related

- [Caching](/reference/caching) — automatic cache key namespacing with `@Tenant`
- [Authentication](/integrations/auth) — combine with `@Auth` for authenticated tenant access
- [Advanced concepts](/guide/advanced-concepts) — `tenant` option in `BananaAppOptions`
- [Recipes](/recipes/) — `example-multitenant` app with per-tenant data and `@Can`
- `docs/MULTI-TENANCY.md` in the repository — PostgreSQL schema isolation, Mongoose per-tenant connections, and deep patterns
