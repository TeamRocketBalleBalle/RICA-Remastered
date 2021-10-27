#include "AsyncWebServerWrapper.h"

#include "../API/API_list.h"
#include "CONFIG.h"

AsyncWebServerWrapper::AsyncWebServerWrapper(AsyncWebServer *server)
    : __server(server) {}

/**
 * close the AsyncWebServer by calling `server.end()`
 */
void AsyncWebServerWrapper::end() {
    __server->end();
    delete __server;
}

void AsyncWebServerWrapper::default_config() {

    // Catch-All Handler
    __server->onNotFound([](AsyncWebServerRequest *request) {
        // handle unknown request
        request->send(404);
    });
}

/**
 * Registers all the functions in API/API_list
 */
void AsyncWebServerWrapper::register_default_API() {
    __server->on("/help", HTTP_ANY, help);
    __server->on("/ping", HTTP_GET,
                 [](AsyncWebServerRequest *request) { ping(request); });
}

/**
 * Registers credentials only API  in the API/API_list
 */
void AsyncWebServerWrapper::regiser_credential_only_API() {
    __server->on("/scan_wifi", HTTP_GET, scan_wifi);
}
