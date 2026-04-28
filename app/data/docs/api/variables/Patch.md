[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / Patch

# Variable: Patch

> `const` **Patch**: (`path`, `middlewares?`) => `MethodDecorator`

Defined in: packages/bananajs/src/lib/Router/Route.decorator.ts:69

Method decorator for HTTP PATCH requests.

## Parameters

### path?

`string` = `''`

The endpoint path.

### middlewares?

`RequestHandler`\<`ParamsDictionary`, `any`, `any`, `ParsedQs`, `Record`\<`string`, `any`\>\>[]

Optional middleware functions.

## Returns

`MethodDecorator`

A method decorator.
