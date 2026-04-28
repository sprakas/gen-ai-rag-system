[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BananaConfigInstance

# Interface: BananaConfigInstance\<T\>

Defined in: packages/bananajs/src/lib/Config/BananaConfig.ts:21

## Type Parameters

### T

`T`

## Methods

### get()

> **get**(): `Readonly`\<`T`\>

Defined in: packages/bananajs/src/lib/Config/BananaConfig.ts:22

#### Returns

`Readonly`\<`T`\>

***

### offSecretRotated()

> **offSecretRotated**(`handler`): `void`

Defined in: packages/bananajs/src/lib/Config/BananaConfig.ts:25

#### Parameters

##### handler

(`key`, `newValue`) => `void`

#### Returns

`void`

***

### onSecretRotated()

> **onSecretRotated**(`handler`): `void`

Defined in: packages/bananajs/src/lib/Config/BananaConfig.ts:24

#### Parameters

##### handler

(`key`, `newValue`) => `void`

#### Returns

`void`

***

### reload()

> **reload**(): `void`

Defined in: packages/bananajs/src/lib/Config/BananaConfig.ts:23

#### Returns

`void`
