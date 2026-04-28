# Caching

BananaJS provides method-level caching via `@Cache` and `@CacheEvict` decorators backed by `CacheManager`. The built-in store is in-memory with TTL support; plug in Redis or any custom backend via the `CacheStore` interface.

## Setup

No extra install needed for in-memory caching. Pass `cache` in `BananaAppOptions`:

```typescript
import { BananaApp, defineBananaControllers } from '@banana-universe/bananajs'

new BananaApp({
  controllers: defineBananaControllers(ProductController),
  cache: {
    store: 'memory',    // default — in-process LRU with TTL
  },
})
```

For Redis, install a Redis CacheStore adapter and pass it:

```typescript
import { RedisCacheStore } from './cache/RedisCacheStore.js'  // your adapter

new BananaApp({
  controllers: defineBananaControllers(ProductController),
  cache: { store: new RedisCacheStore({ url: process.env.REDIS_URL }) },
})
```

## `@Cache(options)` — cache the return value

Caches the method's return value under a key for a specified TTL. On subsequent calls within the TTL, the method is not invoked and the cached value is returned.

```typescript
import { Cache, Controller, Get, BaseController } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

@Controller('products')
export class ProductController extends BaseController {

  // Cache each product by its ID for 5 minutes
  @Get(':id')
  @Cache({ ttl: 300, key: (req) => `product:${req.params.id}` })
  async getProduct(req: Request, res: Response) {
    const product = await this.service.findById(req.params.id)
    if (!product) throw new NotFoundError('Product not found')
    return this.ok(res, 'Product found', product)
  }

  // Cache the full product list for 1 minute
  @Get('')
  @Cache({ ttl: 60, key: 'products:list' })
  async listProducts(_req: Request, res: Response) {
    const products = await this.service.findAll()
    return this.ok(res, 'Products fetched', products)
  }
}
```

**Options:**

| Option | Type | Description |
|---|---|---|
| `ttl` | `number` | Seconds until expiry |
| `key` | `string \| ((req: Request) => string)` | Cache key or factory function |

## `@CacheEvict(options)` — invalidate on mutation

Clears cache entries matching a key or glob pattern after the method completes successfully.

```typescript
@Controller('products')
export class ProductController extends BaseController {

  // Evict the specific product and the list on update
  @Put(':id')
  @Body(UpdateProductSchema)
  @CacheEvict({ pattern: `product:*` })    // clears all product:* keys
  async updateProduct(req: Request, res: Response) {
    const updated = await this.service.update(req.params.id, req.body)
    return this.ok(res, 'Updated', updated)
  }

  // Evict just the list cache on create
  @Post('')
  @Body(CreateProductSchema)
  @CacheEvict({ key: 'products:list' })
  async createProduct(req: Request, res: Response) {
    const product = await this.service.create(req.body)
    return this.ok(res, 'Created', product)
  }

  // Evict everything on bulk delete
  @Delete('')
  @CacheEvict({ pattern: '*' })
  async clearAll(req: Request, res: Response) {
    await this.service.deleteAll()
    return this.ok(res, 'Cleared', null)
  }
}
```

**Options:**

| Option | Type | Description |
|---|---|---|
| `key` | `string` | Exact key to evict |
| `pattern` | `string` | Glob pattern — `product:*` evicts all keys starting with `product:` |

Use `key` for precise invalidation. Use `pattern` when a write affects multiple cached entries.

## `CacheManager` — programmatic access

Use `CacheManager` directly in services when the decorator approach doesn't fit (e.g. conditional caching based on business logic):

```typescript
import { CacheManager } from '@banana-universe/bananajs'

@injectable()
export class ProductService {
  private cache = CacheManager.getInstance()

  async findById(id: string): Promise<Product | null> {
    const cacheKey = `product:${id}`
    const cached = await this.cache.get<Product>(cacheKey)
    if (cached) return cached

    const product = await this.repo.findById(id)
    if (product) {
      await this.cache.set(cacheKey, product, 300)  // ttl in seconds
    }
    return product
  }

  async update(id: string, data: Partial<Product>): Promise<Product> {
    const product = await this.repo.update(id, data)
    await this.cache.delete(`product:${id}`)
    return product
  }
}
```

**`CacheManager` API:**

| Method | Signature | Description |
|---|---|---|
| `get<T>` | `(key: string) => Promise<T \| null>` | Retrieve cached value |
| `set` | `(key, value, ttl?) => Promise<void>` | Store value; `ttl` seconds or no expiry |
| `delete` | `(key: string) => Promise<void>` | Remove one key |
| `evict` | `(pattern: string) => Promise<void>` | Remove all keys matching glob pattern |
| `clear` | `() => Promise<void>` | Remove all entries |

## Custom `CacheStore`

Implement `CacheStore` to use Redis, Memcached, or any other backend:

```typescript
import type { CacheStore } from '@banana-universe/bananajs'
import { createClient } from 'redis'

export class RedisCacheStore implements CacheStore {
  private client = createClient({ url: process.env.REDIS_URL })

  async connect() {
    await this.client.connect()
  }

  async get<T>(key: string): Promise<T | null> {
    const raw = await this.client.get(key)
    return raw ? (JSON.parse(raw) as T) : null
  }

  async set(key: string, value: unknown, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(value)
    if (ttl) {
      await this.client.setEx(key, ttl, serialized)
    } else {
      await this.client.set(key, serialized)
    }
  }

  async delete(key: string): Promise<void> {
    await this.client.del(key)
  }

  async evict(pattern: string): Promise<void> {
    const keys = await this.client.keys(pattern)
    if (keys.length > 0) await this.client.del(keys)
  }

  async clear(): Promise<void> {
    await this.client.flushDb()
  }
}
```

Pass to `BananaApp`:
```typescript
const redisStore = new RedisCacheStore()
await redisStore.connect()

new BananaApp({
  controllers: defineBananaControllers(ProductController),
  cache: { store: redisStore },
})
```

## Multi-tenant cache isolation

When using `@Tenant()`, cache keys are **automatically namespaced** by tenant ID. Cached data from `tenant-A` is never returned to `tenant-B`:

```typescript
@Controller('products')
@Tenant()
export class ProductController extends BaseController {
  @Get(':id')
  @Cache({ ttl: 300, key: (req) => `product:${req.params.id}` })
  async getProduct(req: Request, res: Response) {
    // Key is stored as `<tenantId>:product:<id>` — no cross-tenant leakage
  }
}
```

For manual keys via `CacheManager`, use `getTenantId()` to namespace:

```typescript
import { getTenantId } from '@banana-universe/bananajs'

const key = `${getTenantId()}:product:${id}`
```

## Related

- [Multi-tenancy](/reference/multi-tenancy) — cache key namespacing by tenant
- [Advanced concepts](/guide/advanced-concepts) — `cache` option in `BananaAppOptions`
- TypeDoc: [`CacheManager`](/api/classes/CacheManager), [`CacheStore`](/api/interfaces/CacheStore)
