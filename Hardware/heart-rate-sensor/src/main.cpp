/*
 *  This is the main file that will have these components working together.
 *  - Networking: dealing with all conditions, storing credentials, dynamically
 *    getting credentials if not found.
 *  - Websocket support: instead of having RESTful API to send biometric values,
 *    use websockets instead
 */
#include "CONFIG.h"
#include "GLOBALS.h"
#include "LOG.h"
#include "PINS.h"
#include "heart_sensor.h"
#include "wifi_funcs.h"

#include <Arduino.h>

Networking     networking;
AsyncWebServer server = AsyncWebServer(HTTP_PORT);

HeartSensor  heart_sensor;
TaskHandle_t networking_task_handle;

void setup() {
    Serial.begin(115200);
    pinMode(PIN_INBUILT_LED, OUTPUT);
    setupLogging(&Serial);
    xTaskCreatePinnedToCore(networking_task, "networking", 5000, NULL, 2,
                            &networking_task_handle, 0);
    delay(10);
}

void loop() {
    __setup_sensor();
    __setup_display();
    heart_sensor.start_sensing();
}
