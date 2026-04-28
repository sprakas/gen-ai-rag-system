[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / PinoLogger

# Class: PinoLogger

Defined in: packages/bananajs/src/lib/Logger/PinoLogger.ts:16

## Implements

- [`Logger`](../interfaces/Logger.md)

## Constructors

### Constructor

> **new PinoLogger**(`options?`): `PinoLogger`

Defined in: packages/bananajs/src/lib/Logger/PinoLogger.ts:19

#### Parameters

##### options?

`LoggerOptions`\<`never`, `boolean`\>

#### Returns

`PinoLogger`

## Methods

### debug()

> **debug**(`message`, `meta?`): `void`

Defined in: packages/bananajs/src/lib/Logger/PinoLogger.ts:46

#### Parameters

##### message

`string`

##### meta?

`Record`\<`string`, `unknown`\>

#### Returns

`void`

#### Implementation of

[`Logger`](../interfaces/Logger.md).[`debug`](../interfaces/Logger.md#debug)

***

### error()

> **error**(`message`, `meta?`): `void`

Defined in: packages/bananajs/src/lib/Logger/PinoLogger.ts:42

#### Parameters

##### message

`string`

##### meta?

`Record`\<`string`, `unknown`\>

#### Returns

`void`

#### Implementation of

[`Logger`](../interfaces/Logger.md).[`error`](../interfaces/Logger.md#error)

***

### info()

> **info**(`message`, `meta?`): `void`

Defined in: packages/bananajs/src/lib/Logger/PinoLogger.ts:34

#### Parameters

##### message

`string`

##### meta?

`Record`\<`string`, `unknown`\>

#### Returns

`void`

#### Implementation of

[`Logger`](../interfaces/Logger.md).[`info`](../interfaces/Logger.md#info)

***

### warn()

> **warn**(`message`, `meta?`): `void`

Defined in: packages/bananajs/src/lib/Logger/PinoLogger.ts:38

#### Parameters

##### message

`string`

##### meta?

`Record`\<`string`, `unknown`\>

#### Returns

`void`

#### Implementation of

[`Logger`](../interfaces/Logger.md).[`warn`](../interfaces/Logger.md#warn)
