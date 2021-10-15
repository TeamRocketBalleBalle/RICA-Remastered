#ifndef LED_FUNCS_h
#define LED_FUNCS_h

#include "Arduino.h"

void blinkLed(uint8_t pin, uint32_t delay_ms);
void blinkLed(uint8_t pin, uint32_t delay_ms, uint8_t count);

#endif
