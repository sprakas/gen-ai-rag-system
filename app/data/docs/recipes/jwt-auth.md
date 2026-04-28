# Recipe: JWT Authentication

A complete, production-ready `AuthGuard` implementation using signed JSON Web Tokens.

## Prerequisites

```bash
npm install jsonwebtoken
npm install --save-dev @types/jsonwebtoken
```

## 1. Define a guard

```typescript
// src/auth/jwt.guard.ts
import type { Request } from 'express'
import type { AuthGuard, RolesGuard } from '@banana-universe/bananajs'
import { BananaConfig, UnauthorisedError } from '@banana-universe/bananajs'
import jwt from 'jsonwebtoken'

// Load secret at startup — marked sensitive so it never appears in logs or JSON output
const config = BananaConfig({
  jwtSecret:  { env: 'JWT_SECRET',  required: true, sensitive: true },
  jwtIssuer:  { env: 'JWT_ISSUER',  default: 'my-api' },
  jwtAudience:{ env: 'JWT_AUDIENCE', default: 'my-client' },
})

interface JwtPayload {
  sub: string
  roles: string[]
  iss: string
  aud: string
}

function extractToken(req: Request): string | null {
  const auth = req.headers.authorization
  if (typeof auth === 'string' && auth.startsWith('Bearer ')) {
    return auth.slice(7)
  }
  return null
}

export const jwtAuthGuard: AuthGuard & RolesGuard = {
  async canActivate(req: Request): Promise<boolean> {
    const raw = extractToken(req)
    if (!raw) return false

    let payload: JwtPayload
    try {
      payload = jwt.verify(raw, config.get().jwtSecret, {
        issuer:   config.get().jwtIssuer,
        audience: config.get().jwtAudience,
      }) as JwtPayload
    } catch {
      // expired, tampered, or wrong key — do not leak details
      return false
    }

    // Attach user for downstream via RequestContext
    ;(req as unknown as Record<string, unknown>)['user'] = {
      id: payload.sub,
      roles: payload.roles ?? [],
    }
    return true
  },

  async extractRoles(req: Request): Promise<string[]> {
    const user = (req as unknown as { user?: { roles?: string[] } }).user
    return user?.roles ?? []
  },
}
```

## 2. Register the guard

```typescript
// src/bootstrap.ts
import { BananaApp } from '@banana-universe/bananajs'
import { jwtAuthGuard } from './auth/jwt.guard.js'
import { UserController } from './modules/users/user.controller.js'

export const app = new BananaApp({
  controllers: [UserController],
  auth: { guard: jwtAuthGuard },
  swagger: { enabled: true, title: 'My API', version: '1.0.0' },
})
```

## 3. Protect routes

```typescript
import { Controller, Get, Auth, Public, Roles } from '@banana-universe/bananajs'

@Controller('users')
@Auth()
export class UserController {
  @Get('me')
  profile() {
    return { message: 'Your profile' }
  }

  @Get('admin-only')
  @Roles('admin')
  adminOnly() {
    return { message: 'Admins only' }
  }

  @Get('public-ping')
  @Public()
  ping() {
    return { ok: true }
  }
}
```

## 4. Issue tokens (example)

```typescript
import jwt from 'jsonwebtoken'

// Call this in your login handler after verifying credentials
export function signToken(userId: string, roles: string[]): string {
  return jwt.sign(
    { sub: userId, roles },
    process.env['JWT_SECRET']!,
    {
      expiresIn: '15m',   // Short-lived access token
      issuer:   process.env['JWT_ISSUER'] ?? 'my-api',
      audience: process.env['JWT_AUDIENCE'] ?? 'my-client',
    },
  )
}
```

## Security notes

- Store `JWT_SECRET` in an environment variable (or secrets manager), never in source code.
- Use a minimum of 256-bit (32-byte) random secret for HMAC-SHA256.
- Keep access token expiry short (`15m`–`1h`); implement refresh token rotation.
- Always verify `iss` and `aud` to prevent token confusion attacks.
- Do not include sensitive data (passwords, PII) in the JWT payload.

## Testing

```typescript
import { BananaTestApp } from '@banana-universe/bananajs/testing'
import jwt from 'jsonwebtoken'

const TEST_SECRET = 'test-secret-at-least-32-chars-long!!'
process.env['JWT_SECRET'] = TEST_SECRET

const app = BananaTestApp.create({
  controllers: [UserController],
  auth: { guard: jwtAuthGuard },
})

const token = jwt.sign({ sub: 'user-1', roles: ['admin'] }, TEST_SECRET, { expiresIn: '1h' })
app.withAuth(token)

const res = await app.inject({ method: 'GET', url: '/users/me' })
expect(res.statusCode).toBe(200)
```
