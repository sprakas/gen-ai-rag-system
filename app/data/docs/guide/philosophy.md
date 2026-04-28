# Philosophy

<p class="phil-lead">
Express is excellent. But every Express codebase eventually diverges: routes defined differently across files, validation scattered or missing, error shapes inconsistent between endpoints, no shared vocabulary between services. Teams spend energy on glue code instead of product logic.
</p>

**BananaJS is the one shape your team agrees on.** It sits on top of Express — familiar runtime, same deployment model — and adds decorator routing, automatic validation, typed error handling, and a DI-ready module system. The result: every endpoint in every service looks the same, behaves the same, and can be tested the same way.

## Four ideas drive the product

<div class="phil-principles">
<div class="phil-card phil-teal">

**⚡ Conventions over configuration**

A `@Controller` class, Validation schema, a `createModule` binding — that is the full mental model. You do not configure a router, register error middleware manually, or wire validators to handlers. The framework does it; you write business logic.

</div>
<div class="phil-card phil-gold">

**🧩 Heavy is optional**

The core is lean — routing, validation, responses, errors, DI. Everything heavier (ORMs, observability, auth, caching, rate limiting, multi-tenancy, WebSocket) is a plugin or a decorator behind a peer dependency. You install what you need; nothing else is in your bundle.

</div>
<div class="phil-card phil-purple">

**🏛️ DDD when you want it**

Start with a flat controller. When the model warrants it, introduce `createModule` feature slices with domain entities, repository ports, and infrastructure adapters — no forced ceremony. The `@banana-universe/ddd` package and `bjs generate module` scaffold exactly this layered structure; you adopt at your own pace.

</div>
<div class="phil-card phil-coral">

**🤖 AI as a first-class citizen**

The `bjs` CLI ships AI-assisted workflows: generate a layered module from a description or schema, review and scaffold tests, explain code, and more. The LLM layer supports Ollama (default), llama.cpp, OpenAI, and Anthropic. See [AI commands](/tooling/ai-commands).

</div>
</div>

## What BananaJS is not

<div class="phil-nolist">

- **A full-stack framework.** It does not include templating, SSR, a built-in database, or opinionated auth. It gives you the HTTP layer and lets you choose everything else.
- **A NestJS replacement.** BananaJS is intentionally smaller. If you need its full reflection-based DI, module graph, interceptors, and pipes, NestJS is the right tool. If you want NestJS-style DX on a fraction of the dependency surface, BananaJS is built for that.

</div>

---

Read the [Quickstart](/guide/quickstart) to see these ideas in code in five minutes.
