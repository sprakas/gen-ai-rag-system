[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / BananaProviderRegistration

# Type Alias: BananaProviderRegistration

> **BananaProviderRegistration** = [`Constructor`](Constructor.md) \| \{ `token`: `InjectionToken`\<`unknown`\> \| `string` \| `symbol`; `useClass`: [`Constructor`](Constructor.md); \} \| \{ `token`: `InjectionToken`\<`unknown`\> \| `string` \| `symbol`; `useFactory`: (`c`) => `unknown`; \} \| \{ `token`: `InjectionToken`\<`unknown`\> \| `string` \| `symbol`; `useValue`: `unknown`; \}

Defined in: packages/bananajs/src/lib/DI/registerProviders.ts:6

Top-level or module-level provider registration compatible with [defineBananaAppOptions](../functions/defineBananaAppOptions.md).
