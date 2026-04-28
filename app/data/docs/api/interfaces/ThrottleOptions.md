[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / ThrottleOptions

# Interface: ThrottleOptions

Defined in: packages/bananajs/src/lib/Security/Throttle.decorator.ts:4

## Properties

### keyBy?

> `optional` **keyBy?**: `"userId"` \| `"ip"`

Defined in: packages/bananajs/src/lib/Security/Throttle.decorator.ts:7

***

### max

> **max**: `number`

Defined in: packages/bananajs/src/lib/Security/Throttle.decorator.ts:6

***

### message?

> `optional` **message?**: `string`

Defined in: packages/bananajs/src/lib/Security/Throttle.decorator.ts:8

***

### store?

> `optional` **store?**: [`ThrottleStore`](ThrottleStore.md)

Defined in: packages/bananajs/src/lib/Security/Throttle.decorator.ts:14

Optional external store for distributed deployments (e.g. Redis).
Must implement the `ThrottleStore` interface from `@banana-universe/bananajs`.
Defaults to in-memory counting when omitted.

***

### windowMs

> **windowMs**: `number`

Defined in: packages/bananajs/src/lib/Security/Throttle.decorator.ts:5
