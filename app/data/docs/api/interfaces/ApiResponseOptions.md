[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / ApiResponseOptions

# Interface: ApiResponseOptions

Defined in: packages/bananajs/src/lib/OpenAPI/ApiDoc.decorators.ts:17

## Properties

### description

> **description**: `string`

Defined in: packages/bananajs/src/lib/OpenAPI/ApiDoc.decorators.ts:19

***

### schema?

> `optional` **schema?**: `ZodType`\<`any`, `ZodTypeDef`, `any`\>

Defined in: packages/bananajs/src/lib/OpenAPI/ApiDoc.decorators.ts:21

Optional Zod schema for the response body — auto-included in the generated OpenAPI spec.

***

### status

> **status**: `number`

Defined in: packages/bananajs/src/lib/OpenAPI/ApiDoc.decorators.ts:18

***

### type?

> `optional` **type?**: (...`args`) => `unknown`

Defined in: packages/bananajs/src/lib/OpenAPI/ApiDoc.decorators.ts:22

#### Parameters

##### args

...`unknown`[]

#### Returns

`unknown`
