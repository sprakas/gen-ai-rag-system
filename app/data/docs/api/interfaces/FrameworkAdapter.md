[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / FrameworkAdapter

# Interface: FrameworkAdapter

Defined in: packages/bananajs/src/lib/Adapter/FrameworkAdapter.ts:14

Abstract adapter interface for framework independence.
Implement this to swap Express for another HTTP framework (e.g., Fastify).
Currently in exploration phase — only Express is fully supported.

## Methods

### addRoute()

> **addRoute**(`route`): `void`

Defined in: packages/bananajs/src/lib/Adapter/FrameworkAdapter.ts:15

#### Parameters

##### route

[`RouteDefinition`](RouteDefinition.md)

#### Returns

`void`

***

### getInstance()

> **getInstance**(): `unknown`

Defined in: packages/bananajs/src/lib/Adapter/FrameworkAdapter.ts:18

#### Returns

`unknown`

***

### listen()

> **listen**(`port`, `callback?`): `void`

Defined in: packages/bananajs/src/lib/Adapter/FrameworkAdapter.ts:17

#### Parameters

##### port

`number`

##### callback?

() => `void`

#### Returns

`void`

***

### use()

> **use**(`middleware`): `void`

Defined in: packages/bananajs/src/lib/Adapter/FrameworkAdapter.ts:16

#### Parameters

##### middleware

`RequestHandler`

#### Returns

`void`
