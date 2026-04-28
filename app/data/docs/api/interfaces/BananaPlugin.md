[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BananaPlugin

# Interface: BananaPlugin

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:15

## Properties

### name

> **name**: `string`

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:16

## Methods

### onReady()?

> `optional` **onReady**(`ctx`): `void` \| `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:18

#### Parameters

##### ctx

[`AppContext`](AppContext.md)

#### Returns

`void` \| `Promise`\<`void`\>

***

### onShutdown()?

> `optional` **onShutdown**(): `void` \| `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:19

#### Returns

`void` \| `Promise`\<`void`\>

***

### register()

> **register**(`ctx`): `void` \| `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:17

#### Parameters

##### ctx

[`AppContext`](AppContext.md)

#### Returns

`void` \| `Promise`\<`void`\>
