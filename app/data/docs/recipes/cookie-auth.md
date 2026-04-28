# Recipe: Cookie-Based Authentication

A complete `AuthGuard` implementation using secure, `HttpOnly` session cookies.

## Prerequisites

```bash
npm install cookie-parser express-session
npm install --save-dev @types/cookie-parser @types/express-session
```

## 1. Configure session middleware

```typescript
// src/bootstrap.ts
import { BananaApp } from '@banana-universe/bananajs'
import cookieParser from 'cookie-parser'
import session from 'express-session'
import { cookieAuthGuard } from './auth/cookie.guard.js'

export const app = new BananaApp({
  controllers: [...],
  middlewares: [
    cookieParser(),
    session({
      secret: process.env['SESSION_SECRET']!,
      resave: false,
      saveUninitialized: false,
      cookie: {
        httpOnly: true,      // Prevent client-side JavaScript access
        secure: process.env['NODE_ENV'] === 'production',   // HTTPS only in prod
        sameSite: 'strict',  // Block cross-site request forgery
        maxAge: 30 * 60 * 1000,  // 30 minutes
      },
    }),
  ],
  auth: { guard: cookieAuthGuard },
})
```

::: warning Secure cookie in production
`secure: true` requires HTTPS. Behind a load balancer or reverse proxy,
set `app.set('trust proxy', 1)` so Express reads the correct protocol
from the `X-Forwarded-Proto` header.
:::

## 2. Define a guard

```typescript
// src/auth/cookie.guard.ts
import type { Request } from 'express'
import type { AuthGuard, RolesGuard } from '@banana-universe/bananajs'

interface SessionUser {
  id: string
  roles: string[]
}

// Extend express-session typings
declare module 'express-session' {
  interface SessionData {
    user?: SessionUser
  }
}

export const cookieAuthGuard: AuthGuard & RolesGuard = {
  async canActivate(req: Request): Promise<boolean> {
    const user = req.session?.user
    if (!user) return false

    // Make user available to downstream code via RequestContext
    ;(req as unknown as Record<string, unknown>)['user'] = user
    return true
  },

  async extractRoles(req: Request): Promise<string[]> {
    return req.session?.user?.roles ?? []
  },
}
```

## 3. Login and logout handlers

```typescript
// src/modules/auth/auth.controller.ts
import { Controller, Post, Body, Public } from '@banana-universe/bananajs'
import { z } from 'zod'
import type { Request, Response } from 'express'
import { userService } from '../users/user.service.js'

const LoginSchema = z.object({
  email:    z.string().email(),
  password: z.string().min(1),
})

@Controller('auth')
export class AuthController {
  @Post('login')
  @Public()
  async login(
    @Body(LoginSchema) body: z.infer<typeof LoginSchema>,
    req: Request,
    res: Response,
  ) {
    const user = await userService.verifyCredentials(body.email, body.password)
    if (!user) {
      return res.status(401).json({ message: 'Invalid credentials' })
    }

    // Regenerate session to prevent session fixation
    await new Promise<void>((resolve, reject) => {
      req.session.regenerate((err) => (err ? reject(err) : resolve()))
    })

    req.session.user = { id: user.id, roles: user.roles }
    return res.json({ message: 'Logged in' })
  }

  @Post('logout')
  async logout(req: Request, res: Response) {
    await new Promise<void>((resolve, reject) => {
      req.session.destroy((err) => (err ? reject(err) : resolve()))
    })
    res.clearCookie('connect.sid')
    return res.json({ message: 'Logged out' })
  }
}
```

## Security notes

- Always call `req.session.regenerate()` after a successful login to prevent **session fixation**.
- Set `httpOnly: true` — prevents client-side JS from reading the cookie (mitigates XSS impact).
- Set `secure: true` in production — cookie transmitted over HTTPS only.
- Set `sameSite: 'strict'` — blocks the cookie from being sent in cross-site requests (CSRF mitigation).
- Rotate `SESSION_SECRET` periodically; store it in a secrets manager, not in source code.
- Use short `maxAge` and implement sliding session renewal for sensitive operations.
- Store sessions server-side (Redis, database) in production, not in-memory (lost on restart).

## Testing

```typescript
import { BananaTestApp } from '@banana-universe/bananajs/testing'
import cookieParser from 'cookie-parser'
import session from 'express-session'

// Provide a always-pass guard in tests to avoid session middleware complexity
const testGuard: AuthGuard = {
  async canActivate(req) {
    ;(req as any).user = { id: 'test-1', roles: ['user'] }
    return true
  },
}

const app = BananaTestApp.create({
  controllers: [AuthController],
  middlewares: [cookieParser(), session({ secret: 'test-secret', resave: false, saveUninitialized: false })],
  auth: { guard: testGuard },
})
```
