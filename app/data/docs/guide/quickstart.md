# Quickstart

Build a working REST API in 5 minutes. No theory — just a controller, a validation schema, and a running server.

**Prerequisites:** Node.js 20+ and npm (or pnpm / yarn).

<div class="guide-steps">

## 1. Install

```bash
npm install @banana-universe/bananajs reflect-metadata express zod
npm install -D typescript @types/node @types/express
```

## 2. Configure TypeScript

Create `tsconfig.json` in your project root:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "experimentalDecorators": true,
    "outDir": "dist",
    "strict": true
  }
}
```

## 3. Write your first controller

Create `src/hello.controller.ts`:

```typescript
import { Controller, Get, Post, Body, BaseController } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'
import { z } from 'zod'

// Define the request body schema
const GreetSchema = z.object({
  name: z.string().min(1),
})

@Controller('hello')          // Routes under /hello/...
export class HelloController extends BaseController {

  @Get('')                    // GET /hello
  greet(_req: Request, res: Response) {
    return this.ok(res, 'Hello!', { message: 'Welcome to BananaJS' })
  }

  @Post('greet')              // POST /hello/greet
  @Body(GreetSchema)          // Validates req.body — 400 on failure, auto
  greetUser(req: Request, res: Response) {
    const { name } = req.body as z.infer<typeof GreetSchema>
    return this.ok(res, `Hello, ${name}!`, { name })
  }
}
```

## 4. Bootstrap the app

Create `src/main.ts`:

```typescript
import 'reflect-metadata'     // Must be the very first import
import { BananaApp, defineBananaControllers } from '@banana-universe/bananajs'
import { HelloController } from './hello.controller.js'

const app = new BananaApp({
  controllers: defineBananaControllers(HelloController),
})

app.getInstance().listen(3000, () => {
  console.log('Running at http://localhost:3000')
})
```

::: warning Import order matters
`import 'reflect-metadata'` must come **before** any file that uses decorators. In larger projects, put it at the very top of your entry file.
:::

## 5. Run it

```bash
npx tsc && node dist/main.js
```

Then test:

```bash
# Returns: { statusCode: "success", status: 200, message: "Hello!", data: { message: "Welcome to BananaJS" } }
curl http://localhost:3000/hello

# Returns: { statusCode: "success", status: 200, message: "Hello, Alice!", data: { name: "Alice" } }
curl -X POST http://localhost:3000/hello/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# Returns: { statusCode: "error", status: 400, message: "Validation failed: ..." }
curl -X POST http://localhost:3000/hello/greet \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
```

That's it. You have:
- **Decorator-based routing** — no `router.get()` boilerplate
- **Automatic validation** — validation schema on `@Body`, bad input → 400 automatically
- **Consistent responses** — every success and error uses the same JSON shape

</div>

## What just happened?

```
POST /hello/greet  →  @Body(GreetSchema) validates  →  your handler  →  this.ok(res, ...)
                            ↓ if invalid
                       400 BadRequestError (handled automatically)
```

The decorator system works at startup — BananaJS reads the `@Controller` and `@Get`/`@Post` metadata, builds an Express Router, and registers error middleware. You write class methods; the framework handles wiring.

## Next steps

| Want to… | Go to |
|----------|-------|
| Understand decorators, responses, errors deeply | [Core concepts](/guide/basic-concepts) |
| Add more routes, params, query strings | [Core concepts — validation](/guide/basic-concepts#validation) |
| Use the CLI to scaffold a full project | [Getting started](/guide/getting-started) |
| Add auth to your routes | [Authentication](/integrations/auth) |
| Connect a database | [TypeORM](/integrations/typeorm) or [Mongoose](/integrations/mongoose) |

::: tip Use the CLI
`npx @banana-universe/bananajs-cli new my-app` sets up a full project — TypeScript, ESLint, Prettier, database, Swagger — in one command. The manual setup above teaches the fundamentals; the CLI saves 20 minutes on a real project.
:::
