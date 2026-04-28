[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BaseController

# Abstract Class: BaseController

Defined in: packages/bananajs/src/lib/Controller/BaseController.ts:9

Base class for HTTP controllers: standardized success responses and error propagation.
Throw [ApiError](ApiError.md) subclasses from handlers; [error](#error) is a convenience re-throw.

## Constructors

### Constructor

> **new BaseController**(): `BaseController`

#### Returns

`BaseController`

## Methods

### error()

> `protected` **error**(`err`): `never`

Defined in: packages/bananajs/src/lib/Controller/BaseController.ts:14

#### Parameters

##### err

[`ApiError`](ApiError.md)

#### Returns

`never`

***

### ok()

> `protected` **ok**\<`T`\>(`res`, `message`, `data`): `Response`

Defined in: packages/bananajs/src/lib/Controller/BaseController.ts:10

#### Type Parameters

##### T

`T`

#### Parameters

##### res

`Response`

##### message

`string`

##### data

`T`

#### Returns

`Response`
