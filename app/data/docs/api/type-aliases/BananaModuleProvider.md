[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BananaModuleProvider

# Type Alias: BananaModuleProvider

> **BananaModuleProvider** = [`Constructor`](Constructor.md) \| \{ `token`: `InjectionToken`\<`unknown`\> \| `string` \| `symbol`; `useClass`: [`Constructor`](Constructor.md); \} \| \{ `token`: `InjectionToken`\<`unknown`\> \| `string` \| `symbol`; `useFactory`: (`c`) => `unknown`; \} \| \{ `token`: `InjectionToken`\<`unknown`\> \| `string` \| `symbol`; `useValue`: `unknown`; \}

Defined in: packages/bananajs/src/lib/DI/BananaModule.ts:9

Provider entry for [createModule](../functions/createModule.md) — a class, or an explicit token binding.
The module **`controller`** is registered on the child container automatically — **do not** list it in **`providers`**.
