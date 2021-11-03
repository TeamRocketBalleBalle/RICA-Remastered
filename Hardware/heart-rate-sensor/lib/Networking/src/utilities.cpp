#include "utilities.h"

#include "GLOBALS.h"
#include "LOG.h"
#include "PINS.h"
#include "networking_globals.h"
#include "wifi_funcs.h"

#include <Preferences.h>

/* STA Event handlers */

void sta_disconnect_handler(WiFiEvent_t *event, WiFiEventInfo_t *info) {
    uint8_t *reason = &info->disconnected.reason;

    if (*reason != SENSOR_AUTH_FAIL_REASON) {
        SENSOR_AUTH_FAIL_REASON = *reason;
        log_error("can't connect to WiFi. reason: %d", *reason);

        if (*reason == 15 || *reason == 202) {
            NETWORKING_STATE = INVALID_PASS;
        } else if (*reason == 201) {
            NETWORKING_STATE = NO_SSID;
        } else {
            NETWORKING_STATE = UNKNOWN_ERROR;
        }
        __last_disconnected_millis = millis();
    }
}

void sta_connect_handler(WiFiEvent_t *event, WiFiEventInfo_t *info) {
    log_debug("wifi connected");
    NETWORKING_STATE = CONNECTED;
    // give a visual cue with short blinks that esp has connected
    blinkLed(PIN_INBUILT_LED, 100, 3);
}
