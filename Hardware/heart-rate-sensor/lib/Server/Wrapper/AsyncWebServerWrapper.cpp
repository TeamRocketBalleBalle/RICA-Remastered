#include "AsyncWebServerWrapper.h"

#include "../API/API_list.h"
#include "CONFIG.h"

#if RICA_SENSOR_DEBUG
#include <Preferences.h>
#endif

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
    __server->on("/accept_credentials", HTTP_POST, accept_credentials);
    __server->on("/client_ack", HTTP_POST, client_ack);

// debug methods
#if RICA_SENSOR_DEBUG

    __server->on("/show_credentials", HTTP_GET, show_credentials);
    __server->on("/wipe", HTTP_DELETE, [](AsyncWebServerRequest *request) {
        Preferences preferences;
        preferences.begin("config");
        bool done = preferences.clear();
        preferences.end();
        request->send(200, "text/plain", done ? "ok" : "fail");
    });
#endif
}
