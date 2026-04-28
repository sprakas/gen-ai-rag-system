---
layout: home

hero:
  name: BananaJS
  text: AI-first, DDD-ready Node.js framework
  tagline: DX · Express · Plugins · CLI · Type-safe APIs
  image:
    src: /banana-hero.svg
    alt: BananaJS — Express, plugins, CLI, AI
  actions:
    - theme: brand
      text: Quickstart — 5 min
      link: /guide/quickstart
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: Recipes
      link: /recipes/

features:
  - icon: 🤖
    title: AI-first CLI & codegen
    details: 'Turn specs and prompts into working endpoints and modules—generate code, improve docs, and review quality from the CLI so routine API work does not eat your week.'
    link: /ai/
    linkText: AI docs
  - icon: ✨
    title: DX — calm and productive
    details: 'Developer experience matters—one consistent way to declare routes, validate input, shape responses, and surface errors: less boilerplate, fewer surprises, faster iteration on real product logic.'
    link: /guide/basic-concepts
    linkText: Core concepts
  - icon: 🧱
    title: DDD as a destination
    details: 'Keep business rules and use cases understandable and testable—structure grows with your product instead of turning into a flat pile of handlers.'
    link: /guide/layered-architecture
    linkText: Architecture guide
  - icon: 🔌
    title: Deeply extendable
    details: 'Add databases, realtime, observability, and other integrations when you need them—the core stays lean while you opt into heavier pieces.'
    link: /plugins/overview
    linkText: Plugin docs
  - icon: 🤖
    title: MCP server
    details: '`bjs mcp start` exposes the full BananaJS CLI as a Model Context Protocol server—9 typed tools available natively in Cursor, Claude Desktop, and any MCP-compatible IDE. No copy-pasting terminal commands, no context switching.'
    link: /mcp/
    linkText: MCP docs
  - icon: 📄
    title: Automatic Swagger docs
    details: 'Your decorators are the spec. The OpenAPI doc your consumers read is built live from the same code your server runs—so the contract never drifts, and you never write YAML.'
    link: /reference/openapi
    linkText: OpenAPI docs
---

<div class="sky-scene" aria-hidden="true">
  <span class="sky-orb sky-orb-1"></span>
  <span class="sky-orb sky-orb-2"></span>
  <span class="sky-orb sky-orb-3"></span>
</div>

<div class="home-hero-section">

<br/><br/>

<p class="tagline-rich">
  <span class="gradient-text">Exceptional DX on Express</span> — structure and automation for teams that want <strong>clear APIs</strong> and a path to <strong>domain-driven design</strong>, with a CLI that fits how modern teams work—without dragging in a heavyweight runtime.
</p>

</div>

<div class="home-why">

## Why BananaJS

**Not a thin wrapper around Express** — a deliberate stack for teams who want **great DX**, **structure**, **automation**, and **maintainable domains** without adopting a monolithic platform. Invest in **tooling** so you spend time on product behavior, not repetitive files. **Plugins** let capabilities grow without bloating the core.

[Philosophy](/guide/philosophy) · [Layered architecture](/guide/layered-architecture) · [Recipes](/recipes/)

</div>

<div class="home-learning-path">

## Learning path

<div class="tracks">
<div class="track track-beginner">

**🐣 New to BananaJS**

Ship something in your first session.

- [Quickstart](/guide/quickstart) — a running API in 5 min
- [Full setup & CLI](/guide/getting-started) — scaffold and project layout
- [Core concepts](/guide/basic-concepts) — controllers, validation, responses
- [Error types](/reference/error-types) — the typed error toolkit

</div>
<div class="track track-builder">

**🔨 Building a real feature**

Make it production-shaped.

- [Modules & DI](/guide/dependency-injection) — `createModule`, scoped containers
- [Authentication](/integrations/auth) — guards, `@Auth`, `@Roles`
- [Caching](/reference/caching) — `@Cache`, `@CacheEvict`, custom store
- [Security](/reference/security) — rate limiting, ABAC, sanitization
- [Recipes](/recipes/) — runnable example apps

</div>
<div class="track track-deep">

**🏗️ Going deep**

Architecture, performance, plugin authoring.

- [Advanced concepts](/guide/advanced-concepts) — full `BananaAppOptions` surface
- [Layered architecture](/guide/layered-architecture) — DDD modules, CLI scaffold
- [Domain & persistence](/guide/domain-and-persistence) — ports, adapters, ORMs
- [Testing](/reference/testing) — `BananaTestApp`, `testOverrides`
- [Multi-tenancy](/reference/multi-tenancy) — tenant isolation patterns
- [Writing a plugin](/plugins/writing-a-plugin) — async lifecycle, DI integration

</div>
<div class="track track-ai">

**🤖 AI & MCP**

Let your IDE agent do the heavy lifting.

- [AI overview](/ai/) — `bjs ai` commands and the PRPAV pipeline
- [AI codegen](/tooling/ai-commands) — generate modules and endpoints from text
- [AI review](/tooling/ai-commands#ai-review) — structured findings for CI
- [MCP server](/mcp/) — `bjs mcp start`, 9 tools in Cursor and Claude Desktop
- [AI context](/tooling/ai-commands#ai-context) — publish conventions to every teammate's agent

</div>
</div>

</div>
