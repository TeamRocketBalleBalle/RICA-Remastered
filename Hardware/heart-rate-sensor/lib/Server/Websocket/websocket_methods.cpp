#include "CONFIG.h"
#include "GLOBALS.h"
#include "LOG.h"

#include <Websocket/websocket_methods.h>

AsyncWebSocket ws("/ws");

unsigned long last_message_millis = 0;

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

void text_all_IR_value(long irVal) {
    if (NETWORKING_STATE == CONNECTED &&
        millis() - last_message_millis >= RICA_WEBSOCKET_DELAY_ms) {
        last_message_millis = millis();
        String json         = String();
        json += "{\"ir_val\":" + String(irVal);
        json += "}";
        ws.textAll(json);
        json = String();
    }
}
