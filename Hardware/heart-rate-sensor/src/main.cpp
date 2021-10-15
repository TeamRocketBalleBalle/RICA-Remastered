/*
 *  This sketch demonstrates how to scan WiFi networks.
 *  The API is almost the same as with the WiFi Shield library,
 *  the most obvious difference being the different file you need to include:
 */
#include "WiFi.h"
#include "wifi_funcs.h"

void setup() {
  Serial.begin(115200);
  delay(10);
  __default_connect_to_wifi();
}

void loop() {}
