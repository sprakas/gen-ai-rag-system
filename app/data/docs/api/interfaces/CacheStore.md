[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / CacheStore

# Interface: CacheStore

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:1

## Methods

### del()

> **del**(`key`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:4

#### Parameters

##### key

`string`

#### Returns

`Promise`\<`void`\>

***

### get()

> **get**(`key`): `Promise`\<`unknown`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:2

#### Parameters

##### key

`string`

#### Returns

`Promise`\<`unknown`\>

***

### keys()

> **keys**(`pattern`): `Promise`\<`string`[]\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:5

#### Parameters

##### pattern

`string`

#### Returns

`Promise`\<`string`[]\>

***

### set()

> **set**(`key`, `value`, `ttl?`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Cache/CacheManager.ts:3

#### Parameters

##### key

`string`

##### value

`unknown`

##### ttl?

`number`

#### Returns

`Promise`\<`void`\>
