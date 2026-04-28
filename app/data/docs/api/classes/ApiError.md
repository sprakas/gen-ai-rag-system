[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / ApiError

# Abstract Class: ApiError

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:30

## Extends

- `Error`

## Extended by

- [`BadRequestError`](BadRequestError.md)
- [`UnauthorisedError`](UnauthorisedError.md)
- [`PaymentRequiredError`](PaymentRequiredError.md)
- [`ForbiddenError`](ForbiddenError.md)
- [`NotFoundError`](NotFoundError.md)
- [`ConflictError`](ConflictError.md)
- [`TooManyRequestsError`](TooManyRequestsError.md)
- [`InternalError`](InternalError.md)
- [`BadGatewayError`](BadGatewayError.md)
- [`ServiceUnavailableError`](ServiceUnavailableError.md)
- [`GatewayTimeoutError`](GatewayTimeoutError.md)

## Constructors

### Constructor

> **new ApiError**(`type`, `message?`): `ApiError`

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:31

#### Parameters

##### type

[`ErrorType`](../enumerations/ErrorType.md)

##### message?

`string` = `'error'`

#### Returns

`ApiError`

#### Overrides

`Error.constructor`

## Properties

### cause?

> `optional` **cause?**: `unknown`

Defined in: docs-site/node\_modules/typescript/lib/lib.es2022.error.d.ts:26

#### Inherited from

`Error.cause`

***

### message

> **message**: `string` = `'error'`

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:31

#### Inherited from

`Error.message`

***

### name

> **name**: `string`

Defined in: docs-site/node\_modules/typescript/lib/lib.es5.d.ts:1076

#### Inherited from

`Error.name`

***

### stack?

> `optional` **stack?**: `string`

Defined in: docs-site/node\_modules/typescript/lib/lib.es5.d.ts:1078

#### Inherited from

`Error.stack`

***

### type

> **type**: [`ErrorType`](../enumerations/ErrorType.md)

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:31

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

`Error.prepareStackTrace`

***

### stackTraceLimit

> `static` **stackTraceLimit**: `number`

Defined in: node\_modules/@types/node/globals.d.ts:13

#### Inherited from

`Error.stackTraceLimit`

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

`Error.captureStackTrace`

***

### handle()

> `static` **handle**(`err`, `res`): `Response`

Defined in: packages/bananajs/src/lib/Response/ApiError.ts:35

#### Parameters

##### err

`ApiError`

##### res

`Response`

#### Returns

`Response`
