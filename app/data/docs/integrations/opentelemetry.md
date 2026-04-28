# OpenTelemetry (`@banana-universe/plugin-otel`)

Exports **`OpenTelemetryPlugin(options)`** returning a **`BananaPlugin`** that:

1. Lazy-loads **`@opentelemetry/sdk-node`** and **`@opentelemetry/auto-instrumentations-node`**
2. Starts a **`NodeSDK`** with **`serviceName`**
3. Optionally configures an **OTLP HTTP** exporter when **`exporterUrl`** is set and **`@opentelemetry/exporter-trace-otlp-http`** is installed
4. Mounts middleware in **`register()`** to annotate the active span with **`request.id`** (from request context / `x-request-id`)
5. Shuts down the SDK in **`onShutdown`**

## Install

```bash
npm install @banana-universe/plugin-otel \
  @opentelemetry/sdk-node \
  @opentelemetry/auto-instrumentations-node \
  @opentelemetry/exporter-trace-otlp-http
```

## Options

```typescript
OpenTelemetryPlugin({
  serviceName: 'my-api',
  exporterUrl: 'http://localhost:4318/v1/traces', // optional
})
```

If the exporter package is missing, the plugin logs a warning and may fall back to default behavior.

## Initialization order

Initialize tracing **before** heavy imports if you need full coverage — same guidance as any Node OTel setup. The plugin itself runs during **`BananaApp.create`** plugin registration.
