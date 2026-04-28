[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / ThrottleStore

# Interface: ThrottleStore

Defined in: packages/bananajs/src/lib/Security/ThrottleStore.interface.ts:21

Contract for a distributed throttle store used by `@Throttle`.

Implement this interface against any backend (Redis, Memcached, database, etc.)
and pass it as `store` in `ThrottleOptions` to enable multi-instance rate limiting.

## Example

```typescript
const redisStore: ThrottleStore = {
  async consume(key) {
    // increment counter in Redis; throw if limit exceeded
  },
  async reset(key) {
    // delete counter key in Redis
  },
}

@Throttle({ windowMs: 60_000, max: 10, store: redisStore })
```

## Methods

### consume()

> **consume**(`key`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Security/ThrottleStore.interface.ts:27

Record one request for the given key.
Implementations MUST throw (or reject) when the limit is exceeded so the
framework can return 429 Too Many Requests.

#### Parameters

##### key

`string`

#### Returns

`Promise`\<`void`\>

***

### reset()

> **reset**(`key`): `Promise`\<`void`\>

Defined in: packages/bananajs/src/lib/Security/ThrottleStore.interface.ts:32

Reset the counter for the given key (e.g. when the window expires or for testing).

#### Parameters

##### key

`string`

#### Returns

`Promise`\<`void`\>
