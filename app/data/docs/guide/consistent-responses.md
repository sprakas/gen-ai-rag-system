# Consistent Responses

BananaJS enforces a single response contract across every handler. Every response — success or error — shares the same envelope, so clients parse responses the same way regardless of route.

## The envelope

All responses carry three fields:

```typescript
{
  statusCode: 'success' | 'error'   // always present
  status:     number                 // HTTP status code
  message:    string                 // human-readable label
  data?:      T                      // success only; omitted on errors
}
```

Undefined fields are stripped before sending, so error responses never have a `data` key in the JSON.

## Success responses

### Via `BaseController.ok()`

The preferred path. Extend `BaseController` and call `this.ok(res, message, data)` from any handler:

```typescript
import { Controller, Get, BaseController } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

@Controller('users')
export class UserController extends BaseController {
  @Get(':id')
  async getOne(req: Request, res: Response) {
    const user = await UserService.findById(req.params.id)
    return this.ok(res, 'User fetched', user)
  }
}
```

The signature:

```typescript
protected ok<T>(res: Response, message: string, data: T): Response
```

JSON output:

```json
{
  "statusCode": "success",
  "status": 200,
  "message": "User fetched",
  "data": { "id": "1", "name": "Alice" }
}
```

### Via `SuccessResponse` directly

When you need more control (custom headers, use outside a `BaseController`):

```typescript
import { SuccessResponse } from '@banana-universe/bananajs'

new SuccessResponse('Export ready', { fileId: 'abc' }).send(res, {
  'x-export-id': 'abc',
})
```

`send(res, headers?)` accepts an optional `{ [key: string]: string }` headers map.

### Paginated responses

`PaginatedResponse<T>` extends `SuccessResponse<T>` and adds pagination metadata. Use it when returning list endpoints that support offset or cursor pagination. The shape and status code are identical to a plain success response — clients see the same outer envelope, with pagination fields appended inside `data` (or alongside it, depending on your list handler).

## Error responses

### Throw a typed error class

Throw any `ApiError` subclass from a handler. The `ErrorMiddleware` catches it and calls `ApiError.handle()` to produce the right response shape — you never call `res.status().json()` manually.

```typescript
import { Controller, Get, BaseController, NotFoundError } from '@banana-universe/bananajs'
import type { Request, Response } from 'express'

@Controller('users')
export class UserController extends BaseController {
  @Get(':id')
  async getOne(req: Request, res: Response) {
    const user = await UserService.findById(req.params.id)
    if (!user) throw new NotFoundError('User not found')
    return this.ok(res, 'User fetched', user)
  }
}
```

JSON output:

```json
{
  "statusCode": "error",
  "status": 404,
  "message": "User not found"
}
```

### How errors flow

```
handler throws ApiError subclass
  └─ Express passes it to ErrorMiddleware (4-arg handler)
       └─ instanceof ApiError → ApiError.handle(err, res)
            └─ switch(err.type) → correct ApiResponse subclass.send(res)
       └─ otherwise → InternalError (message masked in production)
```

### Available error classes

| Class                    | HTTP | ErrorType              | Default message                  |
| ------------------------ | ---- | ---------------------- | -------------------------------- |
| `BadRequestError`        | 400  | `BAD_REQUEST`          | `'Bad Parameters'`               |
| `UnauthorisedError`      | 401  | `UNAUTHORISED`         | —                                |
| `PaymentRequiredError`   | 402  | `PAYMENT_REQUIRED`     | —                                |
| `ForbiddenError`         | 403  | `FORBIDDEN`            | —                                |
| `NotFoundError`          | 404  | `NOT_FOUND`            | —                                |
| `ConflictError`          | 409  | `CONFLICT`             | —                                |
| `TooManyRequestsError`   | 429  | `TOO_MANY_REQUESTS`    | —                                |
| `InternalError`          | 500  | `INTERNAL_ERROR`       | `'Something wrong happened.'`    |
| `BadGatewayError`        | 502  | `BAD_GATEWAY`          | —                                |
| `ServiceUnavailableError`| 503  | `SERVICE_UNAVAILABLE`  | —                                |
| `GatewayTimeoutError`    | 504  | `GATEWAY_TIMEOUT`      | —                                |

All are exported from `@banana-universe/bananajs`.

### Production masking

In production (`NODE_ENV === 'production'`), any error not explicitly typed as an `ApiError` subclass is caught by `ErrorMiddleware`, wrapped as `InternalError`, and its message is replaced with `'Something wrong happened.'`. This prevents accidental leakage of stack traces or internal error text.

Typed `ApiError` subclasses always send their own `message` unchanged, in all environments.

## Validation errors

The validation decorators — `@Body`, `@Query`, `@Params`, `@Headers` — accept validation schemas and throw `BadRequestError` internally when parsing fails. The client receives the same envelope:

```json
{
  "statusCode": "error",
  "status": 400,
  "message": "Invalid input"
}
```

No additional work is needed to wire validation errors into the response contract.

## Best practices

- Use `this.ok()` from `BaseController` for all success responses — avoid calling `res.json()` directly.
- Throw typed `ApiError` subclasses instead of `res.status(xxx).json(...)` so the contract is enforced at the middleware level.
- Keep `message` stable and user-facing; put machine-readable details (IDs, counts, lists) inside `data`.
- Do not catch and swallow `ApiError` in handlers — let `ErrorMiddleware` handle it.
- In `catch` blocks, always `return next(error)` (the `return` is required because `noImplicitReturns` is enabled):

```typescript
@Get(':id')
async getOne(req: Request, res: Response, next: NextFunction) {
  try {
    const user = await UserService.findById(req.params.id)
    if (!user) throw new NotFoundError('User not found')
    return this.ok(res, 'User fetched', user)
  } catch (error) {
    return next(error)  // ← return is required
  }
}
```

## Related

- [Core concepts](/guide/basic-concepts)
- [Error types](/reference/error-types)
- [BananaAppOptions](/reference/bananaapp-options)
- [TypeDoc: BaseController](/api/classes/BaseController)
- [TypeDoc: ApiError](/api/classes/ApiError)
