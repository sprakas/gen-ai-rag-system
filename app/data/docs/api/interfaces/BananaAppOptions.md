[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BananaAppOptions

# Interface: BananaAppOptions

Defined in: packages/bananajs/src/lib/Core/App.ts:50

## Extended by

- [`CreateBananaApplicationOptions`](CreateBananaApplicationOptions.md)

## Properties

### abac?

> `optional` **abac?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:109

#### guard

> **guard**: [`AbacGuard`](AbacGuard.md)

***

### apiPrefix?

> `optional` **apiPrefix?**: `string`

Defined in: packages/bananajs/src/lib/Core/App.ts:68

Prepended to every controller base path (e.g. `v1` → `/v1/...`). Use URI versioning per enterprise DX docs.

***

### auth?

> `optional` **auth?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:75

#### guard

> **guard**: [`AuthGuard`](AuthGuard.md)

***

### bodyLimit?

> `optional` **bodyLimit?**: `string`

Defined in: packages/bananajs/src/lib/Core/App.ts:60

Maximum request body size accepted by the JSON and URL-encoded body parsers.
Uses the same format as the `bytes` package (e.g. `'1mb'`, `'500kb'`). Defaults to `'1mb'`.

***

### cache?

> `optional` **cache?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:100

#### store?

> `optional` **store?**: `"memory"` \| [`CacheStore`](CacheStore.md)

***

### container?

> `optional` **container?**: `DependencyContainer`

Defined in: packages/bananajs/src/lib/Core/App.ts:64

Root tsyringe container; optional — created when using `modules` without an explicit container.

***

### devTools?

> `optional` **devTools?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:103

***

### gracefulShutdown?

> `optional` **gracefulShutdown?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:73

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

***

### lazyControllers?

> `optional` **lazyControllers?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:113

***

### logger?

> `optional` **logger?**: `false` \| [`Logger`](Logger.md)

Defined in: packages/bananajs/src/lib/Core/App.ts:62

***

### metrics?

> `optional` **metrics?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:104

#### enabled

> **enabled**: `boolean`

#### path?

> `optional` **path?**: `string`

***

### middlewares?

> `optional` **middlewares?**: `RequestHandler`\<`ParamsDictionary`, `any`, `any`, `ParsedQs`, `Record`\<`string`, `any`\>\>[]

Defined in: packages/bananajs/src/lib/Core/App.ts:51

***

### plugins?

> `optional` **plugins?**: [`BananaPlugin`](BananaPlugin.md)[]

Defined in: packages/bananajs/src/lib/Core/App.ts:99

***

### rateLimit?

> `optional` **rateLimit?**: `false` \| \{ `max?`: `number`; `message?`: `string`; `windowMs?`: `number`; \}

Defined in: packages/bananajs/src/lib/Core/App.ts:86

***

### requestId?

> `optional` **requestId?**: `boolean`

Defined in: packages/bananajs/src/lib/Core/App.ts:61

***

### security?

> `optional` **security?**: `object`

Defined in: packages/bananajs/src/lib/Core/App.ts:52

#### cors?

> `optional` **cors?**: `false` \| `CorsOptions`

#### helmet?

> `optional` **helmet?**: `boolean` \| `Readonly`\<`HelmetOptions`\>

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

***

### tenant?

> `optional` **tenant?**: [`TenantOptions`](TenantOptions.md)

Defined in: packages/bananajs/src/lib/Core/App.ts:112

***

### testOverrides?

> `optional` **testOverrides?**: [`BananaProviderRegistration`](../type-aliases/BananaProviderRegistration.md)[]

Defined in: packages/bananajs/src/lib/Core/App.ts:72

Applied to the root container after plugin/module setup — for tests (e.g. swap a repository port for a fake).
