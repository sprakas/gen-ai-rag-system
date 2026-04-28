[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / PaginationQuerySchema

# Variable: PaginationQuerySchema

> `const` **PaginationQuerySchema**: `ZodObject`\<\{ `limit`: `ZodDefault`\<`ZodOptional`\<`ZodNumber`\>\>; `page`: `ZodDefault`\<`ZodOptional`\<`ZodNumber`\>\>; \}, `"strip"`, `ZodTypeAny`, \{ `limit`: `number`; `page`: `number`; \}, \{ `limit?`: `number`; `page?`: `number`; \}\>

Defined in: packages/bananajs/src/lib/Pagination/Pagination.ts:30

Default Zod schema for `page` / `limit` query validation with `@Query`.
