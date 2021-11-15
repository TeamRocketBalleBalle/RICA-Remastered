#include "websocket_methods.h"

#include "LOG.h"

AsyncWebSocket ws("/ws");

bool init_websocket(AsyncWebServer *server) {
    ws.onEvent(__onEvent);
    server->addHandler(&ws);
    return true;
}

void __onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client,
               AwsEventType type, void *arg, uint8_t *data, size_t len) {
    switch (type) {
    case WS_EVT_CONNECT:
        ws.cleanupClients();
        Serial.printf("WebSocket client #%u connected from %s\n", client->id(),
                      client->remoteIP().toString().c_str());
        break;
    case WS_EVT_DISCONNECT:
        Serial.printf("WebSocket client #%u disconnected\n", client->id());
        break;
    case WS_EVT_PONG:
        log_info("Client #%u/%s pinged!", client->id(),
                 client->remoteIP().toString().c_str());
        break;
    case WS_EVT_DATA:
    case WS_EVT_ERROR:
        break;
    }
}
