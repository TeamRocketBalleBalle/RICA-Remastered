#ifndef RICA_WS_h
#define RICA_WS_h

#include <ESPAsyncWebServer.h>

bool init_websocket(AsyncWebServer *server);
void __onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client,
               AwsEventType type, void *arg, uint8_t *data, size_t len);

void text_all_IR_value(long irVal);
void text_all_BPM(byte *rate_arr, const byte rate_len, float beatsPerMinute,
                  int beatsAvg);

extern AsyncWebSocket ws;
#endif
