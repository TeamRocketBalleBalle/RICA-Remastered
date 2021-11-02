#ifndef __server_global_vars_h
#define __server_global_vars_h

extern uint8_t SENSOR_AUTH_FAIL_REASON;

typedef enum {
    NONE     = -1,
    NO_CREDS = 0,
    INVALID_PASS,
    NO_SSID,
    CONNECTING,
    CONNECTED
} networking_state_t;

extern networking_state_t NETWORKING_STATE;

extern bool CHECK_CREDENTIALS;
extern bool CONNECT_TO_WIFI;
extern bool CLOSE_SERVER;

#endif
