# Testing

BananaJS provides `BananaTestApp` — a first-class testing utility that runs your app in-process without binding a real port. This makes integration tests fast, isolated, and CI-safe.

## Install

`BananaTestApp` lives in the `testing` subpath export:

```bash
# No extra install needed if @banana-universe/bananajs is already installed
# Test runner of your choice:
npm install -D vitest
# or: jest, node:test
```

## Basic integration test

```typescript
import { BananaTestApp } from '@banana-universe/bananajs/testing'
import { defineBananaControllers } from '@banana-universe/bananajs'
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { UserController } from '../src/User.controller.js'

describe('UserController', () => {
  let app: BananaTestApp

  beforeAll(async () => {
    app = await BananaTestApp.create({
      controllers: defineBananaControllers(UserController),
    })
  })

  afterAll(async () => {
    await app.close()
  })

  it('GET /users returns 200', async () => {
    const res = await app.request().get('/users')
    expect(res.status).toBe(200)
    expect(res.body.statusCode).toBe('success')
  })

  it('POST /users with invalid body returns 400', async () => {
    const res = await app.request().post('/users').send({ email: 'not-email' })
    expect(res.status).toBe(400)
    expect(res.body.statusCode).toBe('error')
  })
})
```

`app.request()` returns a [supertest](https://github.com/ladjs/supertest)-compatible agent. No port is bound.

## Testing with modules and fake repositories

The `testOverrides` option replaces token bindings after all module providers are resolved — injecting fakes without changing production code:

```typescript
import { BananaTestApp } from '@banana-universe/bananajs/testing'
import { defineBananaAppOptions } from '@banana-universe/bananajs'
import { userModule } from '../src/modules/users/index.js'
import { USER_REPO_TOKEN } from '../src/modules/users/domain/User.repository.js'

class InMemoryUserRepository {
  private store = new Map()
  async findById(id: string) { return this.store.get(id) ?? null }
  async save(user: any) { this.store.set(user.id, user) }
  async delete(id: string) { this.store.delete(id) }
  async findAll() { return [...this.store.values()] }
}

const fakeRepo = new InMemoryUserRepository()

const app = await BananaTestApp.create(
  defineBananaAppOptions({
    modules: [userModule],
    testOverrides: [
      // Replace the real TypeORM repository with our fake
      { token: USER_REPO_TOKEN, useValue: fakeRepo },
    ],
  })
)
```

`testOverrides` is applied **after** all modules resolve — it wins over module-level providers for the same token.

## Testing with authentication

`BananaTestApp` ships fluent helpers for auth headers:

```typescript
// Set a Bearer token for all subsequent requests
app.withAuth('my-test-token')

// Test a protected route
const res = await app.request().get('/admin/users')
expect(res.status).toBe(200)

// Clear auth headers when done
app.clearHeaders()

// Test that an unauthenticated request is rejected
const unauth = await app.request().get('/admin/users')
expect(unauth.status).toBe(401)
```

`withAuth` sets `Authorization: Bearer <token>` on every request until `clearHeaders()` is called.

For setting arbitrary headers:

```typescript
app.withHeaders({
  'x-tenant-id': 'tenant-123',
  'x-request-id': 'test-req-001',
})
```

## Test-safe defaults

`BananaTestApp` applies sensible defaults so tests don't fail on security middleware:

| Default | Why |
|---|---|
| `rateLimit: false` | Prevents rate limiting from interfering with test loops |
| `security.helmet: false` | Avoids CSP headers that can block test assertions |
| `security.cors: false` | CORS headers are irrelevant in process-local test calls |

Override any of these by passing them explicitly in the options object. The test defaults use a **deep merge** so you can selectively re-enable individual options.

## Bypassing auth in tests

Two approaches:

### Option 1 — Fake guard in `testOverrides`

```typescript
import type { AuthGuard } from '@banana-universe/bananajs'

const alwaysPassGuard: AuthGuard = {
  async canActivate(req) {
    // Simulate a logged-in user
    ;(req as any).user = { id: 'test-user', roles: ['admin'] }
    return true
  },
}

const app = await BananaTestApp.create({
  controllers: defineBananaControllers(UserController),
  auth: { guard: alwaysPassGuard },
})
```

### Option 2 — `withAuth` + real guard

If your guard validates real JWTs, generate a short-lived test token signed with your test secret:

```typescript
import jwt from 'jsonwebtoken'

const TEST_SECRET = 'test-secret-not-for-production'
const testToken = jwt.sign({ sub: 'user-1', roles: ['admin'] }, TEST_SECRET)

app.withAuth(testToken)
```

## API snapshot tests

Test the full response shape to catch unintended API changes:

```typescript
it('GET /users/:id returns consistent shape', async () => {
  await fakeRepo.save({ id: '123', name: 'Alice', email: 'alice@example.com' })

  const res = await app.request().get('/users/123')
  expect(res.body).toMatchSnapshot()
  // or assert specific shape:
  expect(res.body).toEqual({
    statusCode: 'success',
    status: 200,
    message: expect.any(String),
    data: {
      id: '123',
      name: 'Alice',
      email: 'alice@example.com',
    },
  })
})
```

## Unit testing services

Services don't need `BananaTestApp` — inject fakes directly in the constructor:

```typescript
import { describe, it, expect } from 'vitest'
import { UserService } from '../src/modules/users/application/User.service.js'
import { InMemoryUserRepository } from './helpers/InMemoryUserRepository.js'

describe('UserService', () => {
  let service: UserService
  let repo: InMemoryUserRepository

  beforeEach(() => {
    repo = new InMemoryUserRepository()
    service = new UserService(repo)
  })

  it('createUser stores a user and returns it', async () => {
    const user = await service.createUser({ name: 'Bob', email: 'bob@example.com' })
    expect(user.id).toBeDefined()
    expect(await repo.findById(user.id)).not.toBeNull()
  })

  it('createUser with existing email throws ConflictError', async () => {
    await service.createUser({ name: 'Bob', email: 'bob@example.com' })
    await expect(service.createUser({ name: 'Bob 2', email: 'bob@example.com' }))
      .rejects.toThrow('Email already in use')
  })
})
```

Unit tests are cheaper than integration tests and should cover most service logic. Use `BananaTestApp` for HTTP-level concerns (routing, validation middleware, auth middleware behavior).

## Testing with plugins

When testing code that uses plugins (TypeORM, Mongoose), you have two options:

**Option A — Use a test database** (slower, tests real SQL):
```typescript
const app = await BananaTestApp.create({
  modules: [userModule],
  plugins: [
    TypeOrmPlugin({
      type: 'sqlite',
      database: ':memory:',
      entities: [UserOrmEntity],
      synchronize: true,    // creates tables from entities
    }),
  ],
})
```

**Option B — Fake the repository** (faster, no database):
```typescript
const app = await BananaTestApp.create({
  modules: [userModule],
  testOverrides: [
    { token: USER_REPO_TOKEN, useValue: new InMemoryUserRepository() },
  ],
})
```

Option B is usually preferred for unit/integration tests. Reserve Option A for database-specific behavior (migrations, constraints, JSON columns).

## `BananaApp.getRouteTable()` in tests

Use the route table to assert that routes were registered correctly:

```typescript
const app = await BananaTestApp.create({
  controllers: defineBananaControllers(UserController),
})

const table = app.getRouteTable()
expect(table).toContainEqual(
  expect.objectContaining({ method: 'GET', path: '/users/:id' })
)
```

## Related

- [Dependency injection](/guide/dependency-injection) — `testOverrides`, container model
- [Authentication](/integrations/auth) — testing guards and auth flows
- [BananaAppOptions](/reference/bananaapp-options) — `testOverrides` field
- TypeDoc: [`BananaTestApp`](/api/)
