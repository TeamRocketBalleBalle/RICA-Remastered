#include "utilities.h"

#include "CONFIG.h"
#include "GLOBALS.h"
#include "LOG.h"
#include "PINS.h"
#include "networking_globals.h"
#include "wifi_funcs.h"

#include <Preferences.h>

/* Utility Functions */

bool credentials_exist() {
    // check for SSID only, since SSID implies password
    bool        exist;
    Preferences preferences;
    preferences.begin(RICA_PREF_NAMESPACE, true);
    exist = preferences.isKey(RICA_PREF_SSID_KEY);
    preferences.end();

    return exist;
}

bool load_credentials(String *SSID, String *PASS) {
    Preferences preferences;
    preferences.begin(RICA_PREF_NAMESPACE);
    log_trace("loading creds");
    *SSID = preferences.getString(RICA_PREF_SSID_KEY, "");
    *PASS = preferences.getString(RICA_PREF_PASS_KEY, "");
    preferences.end();
    return true;
}

/**
 * Based on NETWORKING_STATE, decide if hotspot should be started or not
 * @return boolean, whether CLOSE_SERVER should be true/false
 */
bool should_i_start_hotspot(bool start_hotspot_val) {
    /*
    When hotspot should be started:
        - when NO_CREDS exist
        - when INVALID_PASS is detected
        - *(opt) when NO_SSID is detected

    TODO: When hotspot should NOT be started:
        - when
    TODO: When no change should be made:
    */
    bool unknown_error = NETWORKING_STATE == UNKNOWN_ERROR;
    bool hotspot_should_be_started =
        NO_CREDS <= NETWORKING_STATE && NETWORKING_STATE < NO_SSID;
    if (hotspot_should_be_started || unknown_error) {
        return true;
    } else if (NETWORKING_STATE == NO_SSID &&
               millis() - __last_disconnected_millis >=
                   RICA_WIFI_OFF_TIMEOUT_ms) {
        return true;
    } else {
        return false;
    }
}

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
    BLINK_LED        = false;
    // give a visual cue with short blinks that esp has connected
    blinkLed(PIN_INBUILT_LED, 100, 3);
}
