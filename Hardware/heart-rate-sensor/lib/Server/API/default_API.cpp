/*
  Code for the default API endpoints
*/
#include "API_list.h"
#include "LOG.h"

// Easter egg
void help(AsyncWebServerRequest *request) {
    request->redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ");
}

// Ping check
void ping(AsyncWebServerRequest *request) {
    log_debug("ping request received");
    request->send(200, "text/plain", "pong");
}
