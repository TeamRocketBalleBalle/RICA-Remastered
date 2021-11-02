#ifndef RICA_UTILITIES_h
#define RICA_UTILITIES_h

#include <WiFi.h>
// wifi event handlers

void sta_disconnect_handler(WiFiEvent_t *event, WiFiEventInfo_t *info);
void sta_connect_handler(WiFiEvent_t *event, WiFiEventInfo_t *info);

#endif
