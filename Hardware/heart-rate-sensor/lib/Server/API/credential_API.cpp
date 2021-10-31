/*
  Code for the credential-only API endpoints
*/
#include "API_list.h"
#include "LOG.h"

#include <WiFi.h>

String __encryption_type(uint8_t type);
/**
 * Scan wifi networks and reply with json results of scan
 */
void scan_wifi(AsyncWebServerRequest *request) {
    // taken from:
    // https://github.com/me-no-dev/ESPAsyncWebServer#scanning-for-available-wifi-networks

    log_debug("scan started");

    int n = WiFi.scanComplete();
    if (n == -2) {
        n = WiFi.scanNetworks();
    }

    log_debug("scan found: %d networks", n);

    String json = "[";
    for (int i = 0; i < n; ++i) {
        if (i)
            json += ",";
        json += "{";
        json += "\"RSSI\":" + String(WiFi.RSSI(i));
        json += ",\"SSID\":\"" + WiFi.SSID(i) + "\"";
        json += ",\"secure_type\":\"" +
                __encryption_type(WiFi.encryptionType(i)) + "\"";
        json += "}";
    }
    WiFi.scanDelete();

    json += "]";
    request->send(200, "application/json", json);
    json = String();
}

String __encryption_type(uint8_t type) {
    const char *result;
    if (type == 0) {
        result = "open";
    } else if (type == 1) {
        result = "WEP";
    } else if (type == 2) {
        result = "WPA_PSK";
    } else if (type == 3) {
        result = "WPA2_PSK";
    } else if (type == 4) {
        result = "WPA_WPA2_PSK";
    } else if (type == 5) {
        result = "WPA2_ENTERPRISE";
    } else {
        result = "MAX";
    }

    return String(result);
}

void accept_credentials(AsyncWebServerRequest *request) {

    int         params = request->params();
    bool        valid  = true;
    const char *reason;
    log_trace("len of params: %d", params);

    if (params != 2) {
        valid  = false;
        reason = "request parameters should only be 2";
    }
    log_trace("len check success");
    if (valid && !request->hasParam("SSID")) {
        valid  = false;
        reason = "required parameter 'SSID' not present";
    }
    log_trace("SSID check success");
    if (valid && !request->hasParam("PASS")) {
        valid  = false;
        reason = "required parameter 'PASS' not present";
    }
    log_trace("PASS check success");

    if (!valid) {
        log_info("client sent bad request: %s", reason);
        request->send(400, "text/plain", String(reason));
        return;
    }

    log_info("Received credentials: \"%s\"/\"%s\"",
             request->getParam("SSID")->value().c_str(),
             request->getParam("PASS")->value().c_str());

    request->send(200, "application/plain", "OK");
}
