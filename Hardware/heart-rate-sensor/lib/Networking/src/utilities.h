#ifndef RICA_UTILITIES_h
#define RICA_UTILITIES_h

#include <WiFi.h>

bool credentials_exist();
bool load_credentials(String *SSID, String *PASS);

bool should_i_start_hotspot(bool start_hotspot_value);

// wifi event handlers

void sta_disconnect_handler(WiFiEvent_t *event, WiFiEventInfo_t *info);
void sta_connect_handler(WiFiEvent_t *event, WiFiEventInfo_t *info);

#endif
