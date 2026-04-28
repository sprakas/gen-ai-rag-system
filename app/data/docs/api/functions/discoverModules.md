[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / discoverModules

# Function: discoverModules()

> **discoverModules**(`_opts`): `Promise`\<[`BananaModuleDescriptor`](../interfaces/BananaModuleDescriptor.md)[]\>

Defined in: packages/bananajs/src/lib/DI/BananaModule.ts:47

Optional convention-based module loading. **Not implemented** in core — use explicit `modules: [...]`
or generate a manifest at build time. When implemented, results must be sorted by `id` for stable route order.

## Parameters

### \_opts

[`DiscoverModulesOptions`](../interfaces/DiscoverModulesOptions.md)

## Returns

`Promise`\<[`BananaModuleDescriptor`](../interfaces/BananaModuleDescriptor.md)[]\>
