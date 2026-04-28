[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / InternalError

# Class: InternalError

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:146

## Extends

- [`ApiError`](ApiError.md)

## Constructors

### Constructor

> **new InternalError**(`message?`): `InternalError`

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:152

Creates a new instance of InternalError.

#### Parameters

##### message?

`string` = `'Internal Server Error'`

A descriptive message accompanying the error. Defaults to 'Internal Server Error'.

#### Returns

`InternalError`

#### Overrides

[`ApiError`](ApiError.md).[`constructor`](ApiError.md#constructor)

## Properties

### cause?

> `optional` **cause?**: `unknown`

Defined in: docs-site/node\_modules/typescript/lib/lib.es2022.error.d.ts:26

#### Inherited from

[`ApiError`](ApiError.md).[`cause`](ApiError.md#cause)

***

### message

> **message**: `string` = `'error'`

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:31

#### Inherited from

[`ApiError`](ApiError.md).[`message`](ApiError.md#message)

***

### name

> **name**: `string`

Defined in: docs-site/node\_modules/typescript/lib/lib.es5.d.ts:1076

#### Inherited from

[`ApiError`](ApiError.md).[`name`](ApiError.md#name)

***

### stack?

> `optional` **stack?**: `string`

Defined in: docs-site/node\_modules/typescript/lib/lib.es5.d.ts:1078

#### Inherited from

[`ApiError`](ApiError.md).[`stack`](ApiError.md#stack)

***

### type

> **type**: [`ErrorType`](../enumerations/ErrorType.md)

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:31

#### Inherited from

[`ApiError`](ApiError.md).[`type`](ApiError.md#type)

***

### prepareStackTrace?

> `static` `optional` **prepareStackTrace?**: (`err`, `stackTraces`) => `any`

Defined in: node\_modules/@types/node/globals.d.ts:11

Optional override for formatting stack traces

#### Parameters

##### err

`Error`

##### stackTraces

`CallSite`[]

#### Returns

`any`

#### See

https://v8.dev/docs/stack-trace-api#customizing-stack-traces

#### Inherited from

[`ApiError`](ApiError.md).[`prepareStackTrace`](ApiError.md#preparestacktrace)

***

### stackTraceLimit

> `static` **stackTraceLimit**: `number`

Defined in: node\_modules/@types/node/globals.d.ts:13

#### Inherited from

[`ApiError`](ApiError.md).[`stackTraceLimit`](ApiError.md#stacktracelimit)

## Methods

### captureStackTrace()

> `static` **captureStackTrace**(`targetObject`, `constructorOpt?`): `void`

Defined in: node\_modules/@types/node/globals.d.ts:4

Create .stack property on a target object

#### Parameters

##### targetObject

`object`

##### constructorOpt?

`Function`

#### Returns

`void`

#### Inherited from

[`ApiError`](ApiError.md).[`captureStackTrace`](ApiError.md#capturestacktrace)

***

### handle()

> `static` **handle**(`err`, `res`): `Response`

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:35

#### Parameters

##### err

[`ApiError`](ApiError.md)

##### res

`Response`

#### Returns

`Response`

#### Inherited from

[`ApiError`](ApiError.md).[`handle`](ApiError.md#handle)
