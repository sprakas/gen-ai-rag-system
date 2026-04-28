[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / Post

# Variable: Post

> `const` **Post**: (`path`, `middlewares?`) => `MethodDecorator`

Defined in: packages/bananajs/src/lib/Router/Route.decorator.ts:53

Method decorator for HTTP POST requests.

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
