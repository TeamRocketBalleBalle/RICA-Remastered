#ifndef RICA_WS_h
#define RICA_WS_h

#include <ESPAsyncWebServer.h>

bool init_websocket(AsyncWebServer *server);
void __onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client,
               AwsEventType type, void *arg, uint8_t *data, size_t len);

extern AsyncWebSocket ws;
#endif
