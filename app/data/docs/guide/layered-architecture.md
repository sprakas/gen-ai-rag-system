# Layered architecture & DDD

**The short version:** organize each feature into layers so that business rules, HTTP wiring, and database code never get mixed together.

You don't need this on day one. A flat controller + service works fine for simple apps. This page describes the structure the CLI scaffolds when your app starts to grow.

## Why bother? A quick analogy

Think of a restaurant:

| Restaurant | Your code |
|---|---|
| **Waiter** | **Controller** — takes the HTTP request, returns a response |
| **Chef** | **Service** — runs the business logic |
| **Recipe book** | **Domain** — the rules about what your data *is* and what it *can do* |
| **Fridge / pantry** | **Infrastructure** — the actual database adapter |

The chef doesn't care whether the food is in a fridge or a freezer. The recipe book has no idea what SQL is. That separation is the whole idea — each layer has one job and doesn't peek into the others.

## The four layers at a glance

```
src/modules/article/
  Article.controller.ts    ← Waiter: HTTP only, no business logic
  Article.dto.ts           ← Request/response shapes (schema)
  application/
    Article.service.ts     ← Chef: orchestrates the use case
  domain/
    Article.entity.ts      ← Recipe: what an Article IS
    Article.repository.ts  ← What we need from storage (no DB specifics)
  infrastructure/
    Article.typeorm-repo.ts   ← Fridge: actual database code
    Article.orm-entity.ts     ← Table/document shape for the ORM
  index.ts                 ← Wires everything together
```

| Layer | One job | Must NOT |
|---|---|---|
| **Controller** | Parse request → call service → return response | Contain business rules |
| **Service** | Orchestrate the use case | Import Express or query the DB directly |
| **Domain** | Hold your model and rules | Import Express, any ORM, or any framework |
| **Infrastructure** | Implement storage adapters (map DB rows ↔ domain objects) | Contain business logic |

## A complete example — blog articles

Let's walk through a real `Article` feature layer by layer.

### Step 1 — Domain: what is an Article?

The entity holds your data shape and business rules. No database, no HTTP — just the plain idea of what an article is.

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

### Step 2 — Domain: what do we need from storage?

Instead of calling the database directly, the domain declares a **port** — a TypeScript interface that says *"I need to store and retrieve Articles, but I don't care how."*

```typescript
// domain/Article.repository.ts
import type { Repository } from '@banana-universe/ddd'
import type { InjectionToken } from 'tsyringe'
import type { Article } from './Article.entity.js'

// Four methods out of the box: findById, findAll, save, delete
export type ArticleRepository = Repository<Article>

export const ArticleRepositoryToken = Symbol(
  'ArticleRepository',
) as InjectionToken<ArticleRepository>
```

### Step 3 — Service: the business logic

The service calls the domain and the port. It has no idea whether the database is Postgres or MongoDB.

```typescript
// application/Article.service.ts
import { randomUUID } from 'node:crypto'
import { injectable, inject } from 'tsyringe'
import type { ArticleRepository } from '../domain/Article.repository.js'
import { ArticleRepositoryToken } from '../domain/Article.repository.js'
import { Article } from '../domain/Article.entity.js'

@injectable()
export class ArticleService {
  constructor(
    @inject(ArticleRepositoryToken)
    private readonly repo: ArticleRepository,  // the interface, not a real DB class
  ) {}

  async create(title: string, body: string): Promise<Article> {
    return this.repo.save(new Article({ id: randomUUID(), title, body,
      createdAt: new Date(), updatedAt: new Date() }))
  }

  async getAll(): Promise<Article[]> {
    return this.repo.findAll()
  }
}
```

### Step 4 — Infrastructure: the actual database

This is the only layer where TypeORM or Mongoose appears. It implements the port by translating between domain objects and DB rows/documents.

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

### Step 5 — Controller: HTTP wiring

Thin. Validates input with schemas, calls the service, returns the response.

```typescript
// Article.controller.ts
import type { Request, Response } from 'express'
import { Controller, Post, Get, Body, BaseController } from '@banana-universe/bananajs'
import { injectable, inject } from 'tsyringe'
import { ArticleService } from './application/Article.service.js'
import { CreateArticleDto } from './Article.dto.js'

@Controller('articles')
@injectable()
export class ArticleController extends BaseController {
  constructor(@inject(ArticleService) private readonly service: ArticleService) {
    super()
  }

  @Post('')
  @Body(CreateArticleDto)
  async create(req: Request, res: Response) {
    const { title, body } = req.body as { title: string; body: string }
    return this.ok(res, 'created', await this.service.create(title, body))
  }

  @Get('')
  async list(_req: Request, res: Response) {
    return this.ok(res, 'ok', await this.service.getAll())
  }
}
```

### Step 6 — Wire it all together

```typescript
// index.ts
import { createModule } from '@banana-universe/bananajs'
import { ArticleController } from './Article.controller.js'
import { ArticleService } from './application/Article.service.js'
import { ArticleTypeOrmRepo } from './infrastructure/Article.typeorm-repo.js'
import { ArticleRepositoryToken } from './domain/Article.repository.js'

export const articlesModule = createModule({
  id: 'articles',
  controller: ArticleController,
  providers: [
    { token: ArticleRepositoryToken, useClass: ArticleTypeOrmRepo },  // ← swap DB here
    ArticleService,
  ],
})
```

**Want to switch from TypeORM to Mongoose?** Change the `useClass` line above. The service and domain are untouched.

## Do I need all four layers?

No. Start flat:

```
src/modules/article/
  Article.controller.ts   ← validation + HTTP
  Article.service.ts      ← logic lives here too, totally fine for simple features
  Article.dto.ts
  index.ts
```

Add the full split when:
- You want to **test business logic** without a running database
- You want to **swap databases** without rewriting use cases
- Your feature has **real business rules** that deserve their own home

## Generate the full structure

```bash
bjs generate module article --orm typeorm
# or
bjs generate module article --orm mongoose
```

This scaffolds the complete folder layout above. See [CLI docs](/tooling/cli) for all options.

## Quick reference — `Repository<T>` methods

```typescript
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>
  findAll(criteria?: FindCriteria<T>): Promise<T[]>
  save(entity: T): Promise<T>
  delete(id: ID): Promise<void>
}
```

Filter with `FindCriteria` — no raw SQL leaking into services:

```typescript
const recent = await this.repo.findAll({
  where:   { title: { like: 'BananaJS' } },
  orderBy: { field: 'createdAt', direction: 'desc' },
  limit:   20,
})
// Supported operators: eq, in, like, gt, lt
```

## Learn more

- [Domain & persistence](/guide/domain-and-persistence) — deep dive into ports, adapters, and plugin wiring
- [Dependency injection](/guide/dependency-injection) — `createModule`, `providers`, scoped containers
- [Philosophy](/guide/philosophy) — why structure helps teams scale
- [TypeORM integration](/integrations/typeorm) — ORM entity and adapter setup
- [Mongoose integration](/integrations/mongoose) — schema, model, and adapter setup
- [Recipes](/recipes/) — runnable apps with `createModule` and layered folders
