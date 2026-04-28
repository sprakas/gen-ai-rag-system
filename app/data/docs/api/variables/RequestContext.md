[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / RequestContext

# Variable: RequestContext

> `const` **RequestContext**: `object`

Defined in: packages/bananajs/src/lib/Context/RequestContext.ts:13

## Type Declaration

### get()

> **get**(): [`RequestContextData`](../interfaces/RequestContextData.md) \| `undefined`

#### Returns

[`RequestContextData`](../interfaces/RequestContextData.md) \| `undefined`

### getRequestId()

> **getRequestId**(): `string` \| `undefined`

#### Returns

`string` \| `undefined`

### run()

> **run**\<`T`\>(`data`, `fn`): `T`

#### Type Parameters

##### T

`T`

#### Parameters

##### data

[`RequestContextData`](../interfaces/RequestContextData.md)

##### fn

() => `T`

#### Returns

`T`

### set()

> **set**(`key`, `value`): `void`

#### Parameters

##### key

`string`

##### value

`unknown`

#### Returns

`void`
