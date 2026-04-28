[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / createCorsOptions

# Function: createCorsOptions()

> **createCorsOptions**(`allowedOrigins`): `CorsOptions`

Defined in: packages/bananajs/src/lib/Security/cors.helper.ts:19

Creates a strict CORS configuration object from an explicit origin allowlist.

Passing a wildcard origin (`'*'`) in `allowedOrigins` is intentionally
discouraged — use `security.cors` directly for open APIs.

## Parameters

### allowedOrigins

`string`[]

## Returns

`CorsOptions`

## Example

```typescript
new BananaApp({
  controllers: [...],
  security: {
    cors: createCorsOptions(['https://app.example.com', 'https://admin.example.com']),
  },
})
```
