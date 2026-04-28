[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / CreateBananaApplicationOptions

# Interface: CreateBananaApplicationOptions

Defined in: packages/bananajs/src/lib/Core/App.ts:611

Options for [createBananaApplication](../functions/createBananaApplication.md) — extends [BananaAppOptions](BananaAppOptions.md) with optional listen helpers.

## Extends

- [`BananaAppOptions`](BananaAppOptions.md)

## Properties

### abac?

> `optional` **abac?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:109

#### guard

> **guard**: [`AbacGuard`](AbacGuard.md)

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`abac`](BananaAppOptions.md#abac)

***

### apiPrefix?

> `optional` **apiPrefix?**: `string`

Defined in: packages/bananajs/src/lib/Core/App.ts:68

Prepended to every controller base path (e.g. `v1` → `/v1/...`). Use URI versioning per enterprise DX docs.

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`apiPrefix`](BananaAppOptions.md#apiprefix)

***

### auth?

> `optional` **auth?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:75

#### guard

> **guard**: [`AuthGuard`](AuthGuard.md)

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`auth`](BananaAppOptions.md#auth)

***

### bodyLimit?

> `optional` **bodyLimit?**: `string`

Defined in: packages/bananajs/src/lib/Core/App.ts:60

Maximum request body size accepted by the JSON and URL-encoded body parsers.
Uses the same format as the `bytes` package (e.g. `'1mb'`, `'500kb'`). Defaults to `'1mb'`.

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`bodyLimit`](BananaAppOptions.md#bodylimit)

***

### cache?

> `optional` **cache?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:100

#### store?

> `optional` **store?**: `"memory"` \| [`CacheStore`](CacheStore.md)

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`cache`](BananaAppOptions.md#cache)

***

### container?

> `optional` **container?**: `DependencyContainer`

Defined in: packages/bananajs/src/lib/Core/App.ts:64

Root tsyringe container; optional — created when using `modules` without an explicit container.

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`container`](BananaAppOptions.md#container)

***

### devTools?

> `optional` **devTools?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:103

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`devTools`](BananaAppOptions.md#devtools)

***

### gracefulShutdown?

> `optional` **gracefulShutdown?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:73

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`gracefulShutdown`](BananaAppOptions.md#gracefulshutdown)

***

### health?

> `optional` **health?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:93

#### checks?

> `optional` **checks?**: [`HealthCheck`](HealthCheck.md)[]

#### enabled

> **enabled**: `boolean`

#### path?

> `optional` **path?**: `string`

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`health`](BananaAppOptions.md#health)

***

### hostname?

> `optional` **hostname?**: `string`

Defined in: packages/bananajs/src/lib/Core/App.ts:614

***

### lazyControllers?

> `optional` **lazyControllers?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:113

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`lazyControllers`](BananaAppOptions.md#lazycontrollers)

***

### logger?

> `optional` **logger?**: `false` \| [`Logger`](Logger.md)

Defined in: packages/bananajs/src/lib/Core/App.ts:62

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`logger`](BananaAppOptions.md#logger)

***

### metrics?

> `optional` **metrics?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:104

#### enabled

> **enabled**: `boolean`

#### path?

> `optional` **path?**: `string`

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`metrics`](BananaAppOptions.md#metrics)

***

### middlewares?

> `optional` **middlewares?**: `RequestHandler`\<`ParamsDictionary`, `any`, `any`, `ParsedQs`, `Record`\<`string`, `any`\>\>[]

Defined in: packages/bananajs/src/lib/Core/App.ts:51

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`middlewares`](BananaAppOptions.md#middlewares)

***

### onListening?

> `optional` **onListening?**: (`info`) => `void`

Defined in: packages/bananajs/src/lib/Core/App.ts:615

#### Parameters

##### info

###### hostname?

`string`

###### port

`number`

#### Returns

`void`

***

### plugins?

> `optional` **plugins?**: [`BananaPlugin`](BananaPlugin.md)[]

Defined in: packages/bananajs/src/lib/Core/App.ts:99

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`plugins`](BananaAppOptions.md#plugins)

***

### port?

> `optional` **port?**: `number`

Defined in: packages/bananajs/src/lib/Core/App.ts:613

When set, calls `Application.listen` after the app is created.

***

### rateLimit?

> `optional` **rateLimit?**: `false` \| \{ `max?`: `number`; `message?`: `string`; `windowMs?`: `number`; \}

Defined in: packages/bananajs/src/lib/Core/App.ts:86

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`rateLimit`](BananaAppOptions.md#ratelimit)

***

### requestId?

> `optional` **requestId?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:61

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`requestId`](BananaAppOptions.md#requestid)

***

### security?

> `optional` **security?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:52

#### cors?

> `optional` **cors?**: `false` \| `CorsOptions`

#### helmet?

> `optional` **helmet?**: `boolean` \| `Readonly`\<`HelmetOptions`\>

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`security`](BananaAppOptions.md#security)

***

### swagger?

> `optional` **swagger?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:78

#### description?

> `optional` **description?**: `string`

#### enabled?

> `optional` **enabled?**: `boolean`

Defaults to `true` — omit or set to `false` to disable.

#### path?

> `optional` **path?**: `string`

#### title?

> `optional` **title?**: `string`

#### version?

> `optional` **version?**: `string`

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`swagger`](BananaAppOptions.md#swagger)

***

### tenant?

> `optional` **tenant?**: [`TenantOptions`](TenantOptions.md)

Defined in: packages/bananajs/src/lib/Core/App.ts:112

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`tenant`](BananaAppOptions.md#tenant)

***

### testOverrides?

> `optional` **testOverrides?**: [`BananaProviderRegistration`](../type-aliases/BananaProviderRegistration.md)[]

Defined in: packages/bananajs/src/lib/Core/App.ts:72

Applied to the root container after plugin/module setup — for tests (e.g. swap a repository port for a fake).

#### Inherited from

[`BananaAppOptions`](BananaAppOptions.md).[`testOverrides`](BananaAppOptions.md#testoverrides)
