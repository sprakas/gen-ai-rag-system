# BananaConfig

**`BananaConfig`** validates **environment variables** against a **schema** you define. It returns a **frozen** config object plus **reload** and **secret rotation** hooks.

## Define a schema

```typescript
import { BananaConfig } from '@banana-universe/bananajs'

const schema = {
  port: { env: 'PORT', type: 'number', default: 3000 },
  nodeEnv: { env: 'NODE_ENV', default: 'development' },
  databaseUrl: { env: 'DATABASE_URL', required: true },
  apiSecret: { env: 'API_SECRET', required: true, sensitive: true },
} as const

export const config = BananaConfig(schema)
```

## Access values

- **Direct properties** — `config.port`, `config.databaseUrl` (typed from schema)
- **`.get()`** — returns readonly snapshot: `config.get().port`

## Reload & secrets

- **`config.reload()`** — re-read env and replace frozen values
- **`config.onSecretRotated(handler)`** / **`offSecretRotated`** — notification when sensitive keys change (for rotation workflows)

## Validation errors

If required variables are missing or types do not parse, **`BananaConfig`** throws at startup with a list of problems — fail fast before listening on a port.

## Types

- **`ConfigFieldDef`** — `env`, `type?`, `default?`, `required?`, `sensitive?`
- **`ConfigSchema`** — record of field definitions
- **`ConfigResult<S>`** — inferred readonly result type
- **`BananaConfigInstance<T>`** — `get`, `reload`, rotation hooks

## Related

- [TypeDoc: `BananaConfig`](/api/functions/BananaConfig)
