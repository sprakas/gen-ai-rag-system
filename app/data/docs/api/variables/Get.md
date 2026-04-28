[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / Get

# Variable: Get

> `const` **Get**: (`path`, `middlewares?`) => `MethodDecorator`

Defined in: packages/bananajs/src/lib/Router/Route.decorator.ts:45

Method decorator for HTTP GET requests.

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
