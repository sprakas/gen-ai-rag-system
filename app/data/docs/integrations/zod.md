# Validation

**BananaJS** ships with built-in validation: use **`@Body`**, **`@Query`**, **`@Params`**, and **`@Headers`** with a schema and the framework validates the incoming data automatically.

## Install

```bash
npm install zod
```

The validation library is a **dependency** of `@banana-universe/bananajs` — your app should list it for direct schema imports.

## Plugin status

`@banana-universe/plugin-zod` is decommissioned and removed from this monorepo.

Use the validation decorators directly from `@banana-universe/bananajs`:

- `Body`
- `Query`
- `Params`
- `Headers`

## OpenAPI

Request body documentation is generated from your schemas via **`zod-to-json-schema`** (and from explicit **`@ApiBody({ schema })`** when provided).
