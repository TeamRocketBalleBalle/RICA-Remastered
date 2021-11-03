/*
sample code for "default_wifi_creds.h" header file:
```cpp
#ifndef DEFAULT_WIFI_CREDS
#define DEFAULT_WIFI_CREDS
const char *DEFAULT_WIFI_SSID = "YOUR SSID";
const char *DEFAULT_WIFI_PASS = "YOUR PASSWORD";
#endif
```
*/
#include "wifi_funcs.h"

#include "CONFIG.h"
#include "GLOBALS.h"
#include "LOG.h"
#include "PINS.h"
#include "Wrapper/AsyncWebServerWrapper.h"
#include "default_wifi_creds.h"
#include "led_functions.h"
#include "networking_globals.h"
#include "utilities.h"

#include <Arduino.h>
#include <WiFi.h>

// Define global variables here
unsigned short     SENSOR_AUTH_FAIL_REASON = 0;
networking_state_t NETWORKING_STATE        = NONE;

bool CHECK_CREDENTIALS = true;
bool CONNECT_TO_WIFI   = true;
bool CLOSE_SERVER      = false;
#define START_HOTSPOT() !CLOSE_SERVER

unsigned long __last_disconnected_millis = 0;

// end global variable definitions

/**
 * general function that will be called from main to start all wifi
 * functionalities like AP + STA functions
 *
 * blocking method
 */
bool Networking::start_networking() {
    WiFi.mode(WIFI_MODE_APSTA);
    __default_connect_to_wifi();
    log_trace("Connected to wifi");
    // start the hotspot
    WiFi.softAP(DEFAULT_HOTSPOT_SSID, NULL);
    log_trace("Hotspot started");
    // start the webserver
    __start_web_server();
    return true;
}
// demo function to check connection wifi network
bool Networking::__default_connect_to_wifi() {
    return __connect_to_wifi(DEFAULT_WIFI_SSID, DEFAULT_WIFI_PASS);
}
// TODO: return false if credentials are wrong
/**
 * Connects to wifi
 * @param SSID the SSID of the wifi network
 * @param PASSWORD the password of the wifi network
 * @return true if connection was successful
 */
bool Networking::__connect_to_wifi(const char *SSID, const char *PASSWORD) {
    log_info("Connecting to \"%s\"", SSID);

    WiFi.setHostname(RICA_SENSOR_HOSTNAME);
    WiFi.begin(SSID, PASSWORD);

    return true;
}

bool Networking::__start_web_server() {
    AsyncWebServerWrapper server_wrapper(&server);

    log_trace("Configuring Server");
    server_wrapper.default_config();
    server_wrapper.register_default_API();
    server_wrapper.regiser_credential_only_API();
    server.begin();
    log_trace("Server started...");

    return true;
}

bool Networking::__register_auth_events() {
    WiFi.onEvent(
        [](WiFiEvent_t event, WiFiEventInfo_t info) {
            sta_disconnect_handler(&event, &info);
        },
        SYSTEM_EVENT_STA_DISCONNECTED);

    WiFi.onEvent(
        [](WiFiEvent_t event, WiFiEventInfo_t info) {
            sta_connect_handler(&event, &info);
        },
        SYSTEM_EVENT_STA_CONNECTED);
    return true;
}
