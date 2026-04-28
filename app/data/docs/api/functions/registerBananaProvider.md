[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / registerBananaProvider

# Function: registerBananaProvider()

> **registerBananaProvider**(`container`, `p`): `void`

Defined in: packages/bananajs/src/lib/DI/registerProviders.ts:15

## Parameters

### container

`DependencyContainer`

### p

[`Constructor`](../type-aliases/Constructor.md) \| \{ `token`: `InjectionToken`\<`unknown`\>; `useClass`: [`Constructor`](../type-aliases/Constructor.md); \} \| \{ `token`: `InjectionToken`\<`unknown`\>; `useFactory`: (`c`) => `unknown`; \} \| \{ `token`: `InjectionToken`\<`unknown`\>; `useValue`: `unknown`; \} \| \{ `token`: `InjectionToken`\<`unknown`\>; `useClass`: [`Constructor`](../type-aliases/Constructor.md); \} \| \{ `token`: `InjectionToken`\<`unknown`\>; `useFactory`: (`c`) => `unknown`; \} \| \{ `token`: `InjectionToken`\<`unknown`\>; `useValue`: `unknown`; \}

## Returns

`void`
