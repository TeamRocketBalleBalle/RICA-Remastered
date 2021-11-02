/*
  This Header file contains a list of ALL APIs.
  Mainly sorted into 2 categories.
    - Default: API endpoints that will be registered regardless the state of
      wifi credentials
    - AUTH_ONLY: API endpoints that are required when ESP requires credentials.
*/
#ifndef __SERVER_API_LIST_h
#define __SERVER_API_LIST_h

#include <ESPAsyncWebServer.h>

/* DEFAULT API ENDPOINTS */
void help(AsyncWebServerRequest *request);
void ping(AsyncWebServerRequest *request);

/* CREDENTIAL-ONLY API ENDPOINTS */

void scan_wifi(AsyncWebServerRequest *request);
void accept_credentials(AsyncWebServerRequest *request);
void show_credentials(AsyncWebServerRequest *request);
void client_ack(AsyncWebServerRequest *request);
void networking_state(AsyncWebServerRequest *request);

#endif
