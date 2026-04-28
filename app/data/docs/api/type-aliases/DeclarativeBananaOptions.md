[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / DeclarativeBananaOptions

# Type Alias: DeclarativeBananaOptions

> **DeclarativeBananaOptions** = `Omit`\<[`BananaAppOptions`](../interfaces/BananaAppOptions.md), `"container"`\> & `object`

Defined in: packages/bananajs/src/lib/DI/bananaBootstrap.ts:28

## Type Declaration

### container?

> `optional` **container?**: `DependencyContainer`

### providers?

> `optional` **providers?**: [`BananaProviderRegistration`](BananaProviderRegistration.md)[]

Merged into a new DependencyContainer, or into `container` when both are set.
Replaces legacy Awilix `services` registrations.
