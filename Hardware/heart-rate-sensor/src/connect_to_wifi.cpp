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
#include "PINS.h"
#include "default_wifi_creds.h"
#include "led_functions.h"
#include "wifi_funcs.h"

#include <Arduino.h>
#include <WiFi.h>

bool __default_connect_to_wifi() {
  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(DEFAULT_WIFI_SSID);
  pinMode(PIN_INBUILT_LED, OUTPUT);

  WiFi.begin(DEFAULT_WIFI_SSID, DEFAULT_WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) { // give loading like look with the LED
                                          // blink when connecting
    digitalWrite(PIN_INBUILT_LED, HIGH);
    delay(500);
    digitalWrite(PIN_INBUILT_LED, LOW);
    delay(50);
    Serial.print(".");
  }
  blinkLed(PIN_INBUILT_LED, 100, 3);

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  return true;
}
