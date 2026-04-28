# Mongoose (`@banana-universe/plugin-mongoose`)

Registers a **Mongoose `Connection`** with the app context, exposes **`mongooseConnection`** on the **tsyringe** root container (via **`registerInstance('mongooseConnection', connection)`**) when **`MongoosePlugin`** runs, and provides **`@Transactional()`** using MongoDB **sessions** with **`session.withTransaction`** (requires a replica set or sharded cluster for multi-document transactions).

## Install

```bash
npm install @banana-universe/plugin-mongoose mongoose
```

## Usage

```typescript
import mongoose from 'mongoose'
import { BananaApp, defineBananaAppOptions } from '@banana-universe/bananajs'
import { MongoosePlugin } from '@banana-universe/plugin-mongoose'
import { articlesModule } from './modules/articles/index.js'

await mongoose.connect(process.env.DATABASE_URL!)

const app = await BananaApp.create(
  defineBananaAppOptions({
    modules: [articlesModule],
    plugins: [MongoosePlugin(mongoose.connection)],
    // ...other BananaAppOptions
  }),
)
```

For the minimal **`controllers`**-only style, you can still use **`defineBananaControllers(...)`** with **`MongoosePlugin`**; prefer **`modules`** + **`createModule`** for vertical slices ([Recipes](/recipes/), [example-rest-mongodb](https://github.com/surya-manne/banana-universe/tree/main/apps/example-rest-mongodb)).

- **`MongoosePlugin(connection)`** — stores the connection, registers **`mongooseConnection`** on the app container when present, **`onShutdown`** calls **`connection.close()`**
- **`@Transactional()`** — runs the method inside **`startSession` → `withTransaction`**; use **`MongooseTransactionContext.getSession()`** to pass `{ session }` to model operations inside the transaction
- Standalone `mongod` does **not** support transactions; use a replica set for **`@Transactional`**

For domain-style repositories, **`MongooseRepositoryAdapter`** implements the domain port—see [Layered architecture](/guide/layered-architecture) and the **`Article.mongoose-repository`** / **`Article.mongoose-model`** split under **`apps/example-rest-mongodb`**.
