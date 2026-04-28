# Error types

All framework errors extend **`ApiError`** and carry an **`ErrorType`** enum value. Use **`ApiError.handle(err, res)`** inside custom middleware, or rely on **`ErrorMiddleware`** / **`createErrorMiddleware`** from the framework.

::: tip Spelling
The class for HTTP **401** is **`UnauthorisedError`** (UK spelling), consistent with the `ErrorType.UNAUTHORISED` constant.
:::

## Classes and typical HTTP status

| Class                     | Status | Use case                      |
| ------------------------- | ------ | ----------------------------- |
| `BadRequestError`         | 400    | Invalid input / business rule |
| `UnauthorisedError`       | 401    | Missing or bad credentials    |
| `PaymentRequiredError`    | 402    | Payment required              |
| `ForbiddenError`          | 403    | Authenticated but not allowed |
| `NotFoundError`           | 404    | Resource missing              |
| `ConflictError`           | 409    | Version / uniqueness conflict |
| `TooManyRequestsError`    | 429    | Rate limit / quota            |
| `InternalError`           | 500    | Unexpected failure            |
| `BadGatewayError`         | 502    | Upstream failure              |
| `ServiceUnavailableError` | 503    | Maintenance / overload        |
| `GatewayTimeoutError`     | 504    | Upstream timeout              |

## Production behavior

For **`InternalError`**, user-facing messages may be replaced in **production** to avoid leaking internals (`NODE_ENV === 'production'` path in `ApiError.handle`).

## Related

- [TypeDoc: `ApiError`](/api/classes/ApiError)
- [Basic concepts](/guide/basic-concepts)
