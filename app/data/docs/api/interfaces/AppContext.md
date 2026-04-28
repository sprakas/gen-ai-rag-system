[**@banana-universe/bananajs**](../index.md)

***

[@banana-universe/bananajs](../index.md) / AppContext

# Interface: AppContext

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:6

## Properties

### app

> **app**: `Application`

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:7

***

### container?

> `optional` **container?**: `DependencyContainer`

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:10

Root tsyringe container — plugins register shared infrastructure here; per-module providers use child containers.

***

### controllerClasses?

> `optional` **controllerClasses?**: [`Constructor`](../type-aliases/Constructor.md)[]

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:12

Classes registered as HTTP controllers (from `controllers` or `modules`) for plugins that scan constructors.

***

### logger?

> `optional` **logger?**: [`Logger`](Logger.md)

Defined in: packages/bananajs/src/lib/Plugin/Plugin.interface.ts:8
