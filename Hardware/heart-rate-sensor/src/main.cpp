/*
 *  This is the main file that will have these components working together.
 *  - Networking: dealing with all conditions, storing credentials, dynamically
 *    getting credentials if not found.
 *  - Websocket support: instead of having RESTful API to send biometric values,
 *    use websockets instead
 */
#include "LOG.h"
#include "wifi_funcs.h"

#include <Arduino.h>

Networking networking;

void setup() {
    Serial.begin(115200);
    setupLogging(&Serial);
    delay(10);
    log_debug("Starting networking...");
    networking.start_networking();
    log_trace("done networking");
}

void loop() {}
