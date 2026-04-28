[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / CacheManager

# Class: CacheManager

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:72

## Methods

### del()

> **del**(`key`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:100

#### Parameters

##### key

`string`

#### Returns

`Promise`\<`void`\>

***

### evict()

> **evict**(`pattern`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:104

#### Parameters

##### pattern

`string`

#### Returns

`Promise`\<`void`\>

***

### get()

> **get**(`key`): `Promise`\<`unknown`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:92

#### Parameters

##### key

`string`

#### Returns

`Promise`\<`unknown`\>

***

### set()

> **set**(`key`, `value`, `ttl?`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:96

#### Parameters

##### key

`string`

##### value

`unknown`

##### ttl?

`number`

#### Returns

`Promise`\<`void`\>

***

### getInstance()

> `static` **getInstance**(`store?`): `CacheManager`

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:80

#### Parameters

##### store?

[`CacheStore`](../interfaces/CacheStore.md)

#### Returns

`CacheManager`

***

### reset()

> `static` **reset**(): `void`

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:88

#### Returns

`void`
