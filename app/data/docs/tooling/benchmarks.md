# Benchmarks

**`apps/benchmarks`** contains an **autocannon**-based suite against a small BananaJS app. It measures throughput and latency and compares results to a **baseline** with a regression threshold.

## Run locally

From the **repository root**:

```bash
npm ci
npx tsc -p packages/bananajs/tsconfig.lib.json
cd apps/benchmarks
node --loader ts-node/esm src/benchmark.ts
node --loader ts-node/esm src/report.ts
```

**`results.json`** is produced for inspection; **`baseline.json`** holds reference numbers.

## CI

- **`.github/workflows/benchmarks.yml`** — runs on pushes to **`main`** when **`packages/bananajs`** or **`apps/benchmarks`** change
- **`.github/workflows/ci.yml`** — can run the same benchmark job as part of the unified gate (see workflow comments in-repo)

Tune thresholds and scenarios in **`apps/benchmarks`** sources — not in this docs page.

## Related

- [CLI reference](/tooling/cli) — local development and workspace commands
