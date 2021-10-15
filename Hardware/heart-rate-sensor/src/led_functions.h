#ifndef LED_FUNCS_h
#define LED_FUNCS_h

#include "Arduino.h"

// Blink led on `pin` for `delay_ms` milliseconds
void blinkLed(uint8_t pin, uint32_t delay_ms);
// Blink led on `pin` for `delay_ms` milliseconds for `count` times
void blinkLed(uint8_t pin, uint32_t delay_ms, uint8_t count);

#endif
