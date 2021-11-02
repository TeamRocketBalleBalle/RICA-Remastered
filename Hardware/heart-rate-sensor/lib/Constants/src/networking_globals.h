#ifndef __server_global_vars_h
#define __server_global_vars_h

extern unsigned short SENSOR_AUTH_FAIL_REASON;

typedef enum networking_state_t {
    NONE     = -1,
    NO_CREDS = 0,
    INVALID_PASS,
    NO_SSID,
    CONNECTING,
    CONNECTED,
    UNKNOWN_ERROR
} networking_state_t;

extern networking_state_t NETWORKING_STATE;

extern bool CHECK_CREDENTIALS;
extern bool CONNECT_TO_WIFI;
extern bool CLOSE_SERVER;

extern unsigned long __last_disconnected_millis;

#endif
