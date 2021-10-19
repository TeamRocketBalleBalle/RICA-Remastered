/*
 *  This is the main file that will have these components working together.
 *  - Networking: dealing with all conditions, storing credentials, dynamically
 *    getting credentials if not found.
 *  - Websocket support: instead of having RESTful API to send biometric values,
 *    use websockets instead
 */
#include "wifi_funcs.h"

#include <Arduino.h>

Networking networking;

void setup() {
    Serial.begin(115200);
    delay(10);
    networking.start_networking();
}

void loop() {}
