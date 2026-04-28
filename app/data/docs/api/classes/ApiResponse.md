[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / ApiResponse

# Abstract Class: ApiResponse

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:23

## Extended by

- [`SuccessResponse`](SuccessResponse.md)
- [`BadRequestResponse`](BadRequestResponse.md)
- [`UnauthorizedResponse`](UnauthorizedResponse.md)
- [`PaymentRequiredErrorResponse`](PaymentRequiredErrorResponse.md)
- [`ForbiddenResponse`](ForbiddenResponse.md)
- [`NotFoundResponse`](NotFoundResponse.md)
- [`ConflictResponse`](ConflictResponse.md)
- [`TooManyRequestsResponse`](TooManyRequestsResponse.md)
- [`InternalErrorResponse`](InternalErrorResponse.md)
- [`BadGatewayResponse`](BadGatewayResponse.md)
- [`ServiceUnavailableResponse`](ServiceUnavailableResponse.md)
- [`GatewayTimeoutResponse`](GatewayTimeoutResponse.md)

## Constructors

### Constructor

> **new ApiResponse**(`statusCode`, `status`, `message`): `ApiResponse`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:32

Constructs an instance of ApiResponse.

#### Parameters

##### statusCode

[`StatusCode`](../enumerations/StatusCode.md)

The status code indicating the success or failure of the operation.

##### status

[`ResponseStatus`](../enumerations/ResponseStatus.md)

The HTTP response status associated with this response.

##### message

`string`

A message providing additional information about the response.

#### Returns

`ApiResponse`

## Properties

### message

> `protected` **message**: `string`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:35

A message providing additional information about the response.

***

### status

> `protected` **status**: [`ResponseStatus`](../enumerations/ResponseStatus.md)

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:34

The HTTP response status associated with this response.

***

### statusCode

> `protected` **statusCode**: [`StatusCode`](../enumerations/StatusCode.md)

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:33

The status code indicating the success or failure of the operation.

## Methods

### prepare()

> `protected` **prepare**\<`T`\>(`res`, `response`, `headers`): `Response`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:38

#### Type Parameters

##### T

`T` *extends* `ApiResponse`

#### Parameters

##### res

`Response`

##### response

`T`

##### headers

#### Returns

`Response`

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
