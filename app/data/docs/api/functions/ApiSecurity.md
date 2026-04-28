[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / ApiSecurity

# Function: ApiSecurity()

> **ApiSecurity**(...`schemes`): `MethodDecorator` & `ClassDecorator`

Defined in: packages/bananajs/src/lib/OpenAPI/ApiDoc.decorators.ts:80

Declares that a route requires a specific OpenAPI security scheme.

## Parameters

### schemes

...`string`[]

## Returns

`MethodDecorator` & `ClassDecorator`

## Example

```typescript
@Get('profile')
@Auth()
@ApiSecurity('BearerAuth')
profile() { ... }
```
