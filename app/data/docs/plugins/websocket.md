# WebSocket plugin

**`@banana-universe/plugin-websocket`** implements **`BananaPlugin`** and uses the **`ws`** package (optional peer).

## Install

```bash
npm install @banana-universe/plugin-websocket ws
npm install -D @types/ws
```

## Construction

```typescript
import { WebSocketPlugin } from '@banana-universe/plugin-websocket'
import { ChatController } from './chat.ws-controller.js'

const wsPlugin = new WebSocketPlugin({
  path: '/ws', // HTTP upgrade path (default '/ws')
  controllers: [ChatController],
})
```

Pass **`wsPlugin`** in **`BananaAppOptions.plugins`**, then after **`listen()`**:

```typescript
const server = app.getInstance().listen(3000)
wsPlugin.attachToServer(server)
```

**`attachToServer`** wires the **`upgrade`** event on the Node HTTP server to the internal **`WebSocketServer`**.

## Decorators

Exported from the package (see `packages/plugin-websocket/src`):

- **`@WsController`** — marks a WebSocket controller class
- **`@OnConnect`**, **`@OnDisconnect`**, **`@OnMessage(event)`** — lifecycle and message routing
- **`@WsBody`** — optional DTO validation (full parity with HTTP **`@Body`** behavior is an incremental improvement area)

## Shutdown

The plugin closes the **`WebSocketServer`** in **`onShutdown`**.

## Related

- [Plugins overview](/plugins/overview)
