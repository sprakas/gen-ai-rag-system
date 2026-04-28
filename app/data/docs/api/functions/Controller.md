[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / Controller

# Function: Controller()

> **Controller**(`basePath?`): `ClassDecorator`

Defined in: packages/bananajs/src/lib/Router/Controller.decorator.ts:12

A Class Decorator that marks a class as a controller.

`basePath` is a route segment without leading or trailing slashes (e.g. `'articles'`, `''` for root).
The framework joins segments when mounting routes.

## Parameters

### basePath?

`string` = `''`

The base path segment of the controller.

## Returns

`ClassDecorator`

A class decorator that marks a class as a controller.
