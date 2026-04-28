# Domain & persistence

**The one-line idea:** business rules live in one place (the domain), database code lives somewhere else (infrastructure), and they talk through a simple interface (the port). Neither side needs to know how the other is built.

This is what makes it easy to test your logic without a real database, and to swap databases without rewriting business rules.

## Why separate them?

Imagine you write your article-saving logic directly with Mongoose:

```typescript
// ❌ Business logic tangled with database code
async function createArticle(title: string, body: string) {
  const doc = await ArticleModel.create({ title, body })
  return doc
}
```

This is fine at first. But now:
- To test it, you need a running MongoDB
- To switch to PostgreSQL, you rewrite this function
- Business rules (e.g. "title must not be empty") sit next to `await ArticleModel.create`

The solution is to separate *what an Article is* from *how it gets stored*.

## The three-part pattern

| Part | What it is | Example |
|---|---|---|
| **Domain entity** | Plain TypeScript class — your business model | `Article` with title, body, rules |
| **Port** | TypeScript interface — describes what you need from storage | `findById`, `save`, `delete` |
| **Adapter** | Class that implements the port using a real ORM | `ArticleMongooseRepo` |

The service calls the port. The adapter fulfills it. The two never import each other directly.

## Step by step

### 1. Domain entity — pure business model

No Express. No ORM. Just the data and its rules.

```typescript
// domain/Article.entity.ts
import { Entity } from '@banana-universe/ddd'

export interface ArticleProps {
  id: string
  title: string
  body: string
  createdAt: Date
  updatedAt: Date
}

export class Article extends Entity<ArticleProps> {
  get title() { return this.props.title }
  get body()  { return this.props.body  }
}
```

### 2. Port — the storage contract

An interface + a DI token. The service will depend on this, not on any real DB class.

```typescript
// domain/Article.repository.ts
import type { Repository } from '@banana-universe/ddd'
import type { InjectionToken } from 'tsyringe'
import type { Article } from './Article.entity.js'

// Repository<T> gives you: findById, findAll, save, delete
export type ArticleRepository = Repository<Article>

export const ArticleRepositoryToken = Symbol(
  'ArticleRepository',
) as InjectionToken<ArticleRepository>
```

### 3. Service — uses the port, knows nothing about the DB

```typescript
// application/Article.service.ts
import { injectable, inject } from 'tsyringe'
import type { ArticleRepository } from '../domain/Article.repository.js'
import { ArticleRepositoryToken } from '../domain/Article.repository.js'
import { Article } from '../domain/Article.entity.js'

@injectable()
export class ArticleService {
  constructor(
    @inject(ArticleRepositoryToken)
    private readonly repo: ArticleRepository,
  ) {}

  async create(title: string, body: string): Promise<Article> {
    return this.repo.save(new Article({ id: '', title, body,
      createdAt: new Date(), updatedAt: new Date() }))
  }

  async getAll(): Promise<Article[]> {
    return this.repo.findAll()
  }
}
```

### 4. Adapter — the real database code

Two options — TypeORM or Mongoose.

**TypeORM**

```typescript
// infrastructure/Article.typeorm-repo.ts
import { injectable, inject } from 'tsyringe'
import { DataSource } from 'typeorm'
import { TypeOrmRepositoryAdapter } from '@banana-universe/plugin-typeorm'
import { Article } from '../domain/Article.entity.js'
import { ArticleOrmEntity } from './Article.orm-entity.js'

@injectable()
export class ArticleTypeOrmRepo
  extends TypeOrmRepositoryAdapter<Article, ArticleOrmEntity>
{
  constructor(@inject('dataSource') ds: DataSource) {
    super(ds, ArticleOrmEntity)
  }

  // DB row → domain object
  toDomain(row: ArticleOrmEntity): Article {
    return new Article({ id: row.id, title: row.title, body: row.body,
      createdAt: row.createdAt, updatedAt: row.updatedAt })
  }

  // Domain object → DB row
  toPersistence(article: Article): ArticleOrmEntity {
    const row = new ArticleOrmEntity()
    row.title = article.title
    row.body  = article.body
    return row
  }
}
```

**Mongoose**

```typescript
// infrastructure/Article.mongoose-repo.ts
import { injectable, inject } from 'tsyringe'
import { MongooseRepositoryAdapter } from '@banana-universe/plugin-mongoose'
import { Article } from '../domain/Article.entity.js'
import { getArticleModel, type ArticleDoc } from './Article.mongoose-model.js'

@injectable()
export class ArticleMongooseRepo
  extends MongooseRepositoryAdapter<Article, ArticleDoc>
{
  constructor(@inject('mongooseConnection') connection: Connection) {
    super(getArticleModel(connection))
  }

  toDomain(doc: ArticleDoc): Article {
    return new Article({ id: String(doc._id), title: doc.title, body: doc.body,
      createdAt: doc.createdAt, updatedAt: doc.updatedAt })
  }

  toPersistence(article: Article): Partial<ArticleDoc> {
    return { title: article.title, body: article.body }
  }
}
```

### 5. Bind token → adapter in the module

```typescript
// index.ts
import { createModule } from '@banana-universe/bananajs'
import { ArticleController } from './Article.controller.js'
import { ArticleService } from './application/Article.service.js'
import { ArticleMongooseRepo } from './infrastructure/Article.mongoose-repo.js'
import { ArticleRepositoryToken } from './domain/Article.repository.js'

export const articlesModule = createModule({
  id: 'articles',
  controller: ArticleController,
  providers: [
    { token: ArticleRepositoryToken, useClass: ArticleMongooseRepo },  // ← swap here
    ArticleService,
  ],
})
```

**Switching from Mongoose to TypeORM?** Change `useClass: ArticleMongooseRepo` to `useClass: ArticleTypeOrmRepo`. Nothing else changes.

## Plugin order matters

Plugins register the DB connection on the root container **before** feature modules run. If a module can't find its `dataSource` or `mongooseConnection` at startup, the plugin is either missing or listed after the module.

```typescript
// bootstrap.ts
const app = await BananaApp.create({
  plugins: [TypeOrmPlugin({ entities: [ArticleOrmEntity], ...dbConfig })],  // runs first
  modules: [articlesModule],                                                 // resolves after
})
```

## Testing without a database

Because the service depends on the **token** (not the concrete adapter), tests can plug in a fake implementation:

```typescript
// __tests__/article.test.ts
import { BananaTestApp } from '@banana-universe/bananajs/testing'
import { articlesModule } from '../index.js'
import { ArticleRepositoryToken } from '../domain/Article.repository.js'

class FakeArticleRepo implements ArticleRepository {
  private items = new Map<string, Article>()
  async findById(id: string) { return this.items.get(id) ?? null }
  async findAll() { return [...this.items.values()] }
  async save(a: Article) { this.items.set(a.id, a); return a }
  async delete(id: string) { this.items.delete(id) }
}

const fake = new FakeArticleRepo()

const app = await BananaTestApp.create({
  modules: [articlesModule],
  testOverrides: [{ token: ArticleRepositoryToken, useValue: fake }],
})

test('POST /articles creates an article', async () => {
  const res = await app.inject({
    method: 'POST', url: '/articles',
    body: { title: 'Hello', body: 'World' },
  })
  expect(res.statusCode).toBe(200)
  expect(fake.items.size).toBe(1)
})
```

No running database. Tests finish in milliseconds. See [Testing reference](/reference/testing) for the full guide.

## Learn more

- [Layered architecture & DDD](/guide/layered-architecture) — full step-by-step example with all four layers
- [Dependency injection](/guide/dependency-injection) — containers, providers, `testOverrides`
- [TypeORM integration](/integrations/typeorm) — ORM entity setup and plugin config
- [Mongoose integration](/integrations/mongoose) — schema, model, and plugin config
- [Recipes](/recipes/) — runnable apps with real module and adapter examples
