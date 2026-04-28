[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BadGatewayResponse

# Class: BadGatewayResponse

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:170

## Extends

- [`ApiResponse`](ApiResponse.md)

## Constructors

### Constructor

> **new BadGatewayResponse**(`message?`): `BadGatewayResponse`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:176

Constructs a new instance of BadGatewayResponse.

#### Parameters

##### message?

`string` = `'Bad Gateway'`

A descriptive message accompanying the response. Defaults to 'Bad Gateway'.

#### Returns

`BadGatewayResponse`

#### Overrides

[`ApiResponse`](ApiResponse.md).[`constructor`](ApiResponse.md#constructor)

## Properties

### message

> `protected` **message**: `string`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:35

A message providing additional information about the response.

#### Inherited from

[`ApiResponse`](ApiResponse.md).[`message`](ApiResponse.md#message)

***

### status

> `protected` **status**: [`ResponseStatus`](../enumerations/ResponseStatus.md)

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:34

The HTTP response status associated with this response.

#### Inherited from

[`ApiResponse`](ApiResponse.md).[`status`](ApiResponse.md#status)

***

### statusCode

> `protected` **statusCode**: [`StatusCode`](../enumerations/StatusCode.md)

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:33

The status code indicating the success or failure of the operation.

#### Inherited from

[`ApiResponse`](ApiResponse.md).[`statusCode`](ApiResponse.md#statuscode)

## Methods

### prepare()

> `protected` **prepare**\<`T`\>(`res`, `response`, `headers`): `Response`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:38

#### Type Parameters

##### T

`T` *extends* [`ApiResponse`](ApiResponse.md)

#### Parameters

##### res

`Response`

##### response

`T`

##### headers

#### Returns

`Response`

#### Inherited from

[`ApiResponse`](ApiResponse.md).[`prepare`](ApiResponse.md#prepare)

***

### send()

> **send**(`res`, `headers?`): `Response`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:47

#### Parameters

##### res

`Response`

##### headers?

#### Returns

`Response`

#### Inherited from

[`ApiResponse`](ApiResponse.md).[`send`](ApiResponse.md#send)
