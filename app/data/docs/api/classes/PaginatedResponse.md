[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / PaginatedResponse

# Class: PaginatedResponse\<T\>

Defined in: packages/bananajs/src/lib/Pagination/Pagination.ts:12

## Extends

- [`SuccessResponse`](SuccessResponse.md)\<`T`[]\>

## Type Parameters

### T

`T`

## Constructors

### Constructor

> **new PaginatedResponse**\<`T`\>(`message`, `data`, `meta`): `PaginatedResponse`\<`T`\>

Defined in: packages/bananajs/src/lib/Pagination/Pagination.ts:13

#### Parameters

##### message

`string`

##### data

`T`[]

##### meta

[`PaginationMeta`](../interfaces/PaginationMeta.md)

#### Returns

`PaginatedResponse`\<`T`\>

#### Overrides

[`SuccessResponse`](SuccessResponse.md).[`constructor`](SuccessResponse.md#constructor)

## Properties

### message

> `protected` **message**: `string`

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:35

A message providing additional information about the response.

#### Inherited from

[`SuccessResponse`](SuccessResponse.md).[`message`](SuccessResponse.md#message)

***

### meta

> `readonly` **meta**: [`PaginationMeta`](../interfaces/PaginationMeta.md)

Defined in: packages/bananajs/src/lib/Pagination/Pagination.ts:13

***

### status

> `protected` **status**: [`ResponseStatus`](../enumerations/ResponseStatus.md)

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:34

The HTTP response status associated with this response.

#### Inherited from

[`SuccessResponse`](SuccessResponse.md).[`status`](SuccessResponse.md#status)

***

### statusCode

> `protected` **statusCode**: [`StatusCode`](../enumerations/StatusCode.md)

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:33

The status code indicating the success or failure of the operation.

#### Inherited from

[`SuccessResponse`](SuccessResponse.md).[`statusCode`](SuccessResponse.md#statuscode)

## Methods

### getData()

> **getData**(): `T`[]

Defined in: packages/bananajs/src/lib/Response/ApiResponse.ts:71

#### Returns

`T`[]

#### Inherited from

[`SuccessResponse`](SuccessResponse.md).[`getData`](SuccessResponse.md#getdata)

***

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

[`SuccessResponse`](SuccessResponse.md).[`prepare`](SuccessResponse.md#prepare)

***

### send()

> **send**(`res`, `headers?`): `Response`

Defined in: packages/bananajs/src/lib/Pagination/Pagination.ts:17

#### Parameters

##### res

`Response`

##### headers?

#### Returns

`Response`

#### Overrides

[`SuccessResponse`](SuccessResponse.md).[`send`](SuccessResponse.md#send)
