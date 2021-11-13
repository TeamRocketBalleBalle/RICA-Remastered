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
bool CONNECT_TO_WIFI   = false;
bool CLOSE_SERVER      = false;
bool START_HOTSPOT     = false;
bool HOTSPOT_STARTED   = false;
bool BLINK_LED         = false;

bool CLIENT_ACK_RECIEVED = false;

bool __WIFI_EVENT_HANDLER_REGISTERED = false;
bool __LED_CUE_STATE                 = LOW;
bool __wifi_off                      = false;

unsigned long __PREV_LED_MILLIS          = 0;
unsigned long __last_disconnected_millis = 0;

// end global variable definitions

// networking task
void networking_task(void *param) {
    log_info("running on core: %d", xPortGetCoreID());

    log_debug("Starting networking...");
    networking.start_networking();
    log_trace("done networking");

    vTaskDelete(NULL);
}

/**
 * general function that will be called from main to start all wifi
 * functionalities like AP + STA functions
 *
 * blocking method
 */
bool Networking::start_networking() {
    WiFi.mode(WIFI_MODE_APSTA);

    __handle_networking();
    return true;
}

#if RICA_SENSOR_DEBUG
// demo function to check connection wifi network
bool Networking::__default_connect_to_wifi() {
    return __connect_to_wifi(DEFAULT_WIFI_SSID, DEFAULT_WIFI_PASS);
}
#endif

/**
 * Connects to wifi
 * @param SSID the SSID of the wifi network
 * @param PASSWORD the password of the wifi network
 * @return true if connection was successful
 */
bool Networking::__connect_to_wifi(const char *SSID, const char *PASSWORD) {
    log_info("Connecting to \"%s\"", SSID);

    WiFi.setHostname(RICA_SENSOR_HOSTNAME);
    wl_status_t return_code = WiFi.begin(SSID, PASSWORD);
    if (return_code == WL_CONNECT_FAILED) {
        START_HOTSPOT    = true;
        NETWORKING_STATE = UNKNOWN_ERROR;
        log_error("wifi connection failed");
    }
    return true;
}

bool Networking::__start_web_server(bool register_creds_API) {
    AsyncWebServerWrapper server_wrapper(&server);

    log_trace("Configuring Server");
    server_wrapper.default_config();
    server_wrapper.register_default_API();

    if (register_creds_API) {
        server_wrapper.regiser_credential_only_API();
        log_trace("registering credential API");
    }

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

/**
 * Blocking method that decides based on credentials the sensor has and their
 * validity, should hotspot be started or resume normal server operations with
 * websockets
 */
void Networking::__handle_networking() {
    unsigned long prev_time = millis();

    uint8_t variable_state = CHECK_CREDENTIALS + CLOSE_SERVER + CONNECT_TO_WIFI;
    uint8_t prev_var_state = variable_state;
    while (true) {
        // run loop every NETWORKING_LOOP_DELAY milliseconds
        while (NETWORKING_LOOP_DELAY < millis() - prev_time) {
            prev_time = millis();

            variable_state = CHECK_CREDENTIALS + CLOSE_SERVER +
                             CONNECT_TO_WIFI + START_HOTSPOT + HOTSPOT_STARTED +
                             CLIENT_ACK_RECIEVED;
            if (prev_var_state != variable_state) {
                log_debug(
                    "Variable state changed! CHECK_CREDENTIALS: %d | "
                    "CLOSE_SERVER: %d | CONNECT_TO_WIFI: %d | START_HOTSPOT: "
                    "%d | HOTSPOT_STARTED: %d | CLIENT_ACK_RECEIVED: %d",
                    CHECK_CREDENTIALS, CLOSE_SERVER, CONNECT_TO_WIFI,
                    START_HOTSPOT, HOTSPOT_STARTED, CLIENT_ACK_RECIEVED);
                prev_var_state = variable_state;
            }

            if (CHECK_CREDENTIALS) {
                CHECK_CREDENTIALS = false;
                bool creds_exist  = credentials_exist();

                log_trace("checking credentials.... they%s exist",
                          creds_exist ? "" : " do not");

                if (creds_exist) {
                    CONNECT_TO_WIFI = true;
                } else {
                    NETWORKING_STATE = NO_CREDS;
                }
            }

            if (CONNECT_TO_WIFI) {
                log_trace("connecting to wifi");
                CONNECT_TO_WIFI  = false;
                NETWORKING_STATE = CONNECTING;
                BLINK_LED        = true;
                __wifi_off       = false;
                /* Pseudocode:
                   - register event handlers in connect to wifi
                   - set status to connecting
                   - load creds from preferences
                   - pass those creds to __connect_to_wifi
                */
                if (!__WIFI_EVENT_HANDLER_REGISTERED) {
                    __WIFI_EVENT_HANDLER_REGISTERED = true;
                    __register_auth_events();
                }
                log_trace("registered auth events");

                // load creds
                String SSID, PASS;
                load_credentials(&SSID, &PASS);
                __connect_to_wifi(SSID.c_str(), PASS.c_str());
            }

            // if hotspot is not started and we are connected, we dont need user
            // confirmation to close the hotspot
            if (HOTSPOT_STARTED) {
                CLOSE_SERVER =
                    CLIENT_ACK_RECIEVED && NETWORKING_STATE == CONNECTED;
            } else {
                CLOSE_SERVER =
                    !HOTSPOT_STARTED && NETWORKING_STATE == CONNECTED;
            }
            if (CLOSE_SERVER) {
                START_HOTSPOT   = false;
                HOTSPOT_STARTED = false;

                server.end();
                log_trace("served end");
                WiFi.enableAP(false);
                WiFi.mode(WIFI_MODE_STA);
                log_trace("AP disconnect");

                // register new server and start it
                // server = AsyncWebServer(HTTP_PORT);
                __start_web_server(false); // NOTE: true for debugging purpose,
                                           // set it to false otherwise

                return; // <----- this is where this method exits
            }

            START_HOTSPOT = should_i_start_hotspot(START_HOTSPOT);
            if (START_HOTSPOT && !HOTSPOT_STARTED) {
                HOTSPOT_STARTED = true;
                WiFi.softAP(DEFAULT_HOTSPOT_SSID, NULL);
                log_trace("Hotspot started");
                __start_web_server(true);
            }

            // micro managing stuff

            // turn off wifi if timeout ms have passed
            if (!__wifi_off && NETWORKING_STATE == NO_SSID &&
                RICA_WIFI_OFF_TIMEOUT_ms <=
                    prev_time - __last_disconnected_millis) {
                BLINK_LED  = false;
                __wifi_off = true;
                log_trace("on error 201, wifi disconnected");
                WiFi.disconnect();
            }

            // if, CONNECTING then blink led using reference from arduino sketch
            bool toggle_led =
                BLINK_LED && prev_time - __PREV_LED_MILLIS >= RICA_LED_DELAY_ms;

            if (toggle_led) {
                __PREV_LED_MILLIS = prev_time;
                __LED_CUE_STATE   = !__LED_CUE_STATE;
                digitalWrite(PIN_INBUILT_LED, __LED_CUE_STATE);
            }
        }
    }
}
