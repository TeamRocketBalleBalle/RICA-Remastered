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

#include "default_wifi_creds.h"
#include "led_functions.h"

#include <Arduino.h>
#include <PINS.h>
#include <WiFi.h>

/*
 * general function that will be called from main to start all wifi
 * functionalities like AP + STA functions
 *
 * blocking
 */
bool Networking::start_networking() {
  WiFi.mode(WIFI_MODE_APSTA);
  __default_connect_to_wifi();

  return true;
}
// demo function to check connection wifi network
bool Networking::__default_connect_to_wifi() {
  return __connect_to_wifi(DEFAULT_WIFI_SSID, DEFAULT_WIFI_PASS);
}
// TODO: return false if credentials are wrong
bool Networking::__connect_to_wifi(const char *SSID, const char *PASSWORD) {

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(SSID);
  pinMode(PIN_INBUILT_LED, OUTPUT);

  WiFi.begin(SSID, PASSWORD);

  while (WiFi.status() != WL_CONNECTED) { // give loading like look with the LED
                                          // blink when connecting
    digitalWrite(PIN_INBUILT_LED, HIGH);
    delay(500);
    digitalWrite(PIN_INBUILT_LED, LOW);
    delay(50);
    Serial.print(".");
  }
  // give a visual cue with short blinks that esp has connected
  blinkLed(PIN_INBUILT_LED, 100, 3);

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  return true;
}
