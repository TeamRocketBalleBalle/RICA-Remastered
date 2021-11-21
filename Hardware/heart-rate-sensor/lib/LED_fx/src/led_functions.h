#ifndef LED_FUNCS_h
#define LED_FUNCS_h

#include "Arduino.h"

/**
 * Blink led on `pin` for `delay_ms` milliseconds
 * @param pin the pin of the LED
 * @param delay_ms the interval to wait between LED blinks in milliseconds
 */
void blinkLed(uint8_t pin, uint32_t delay_ms);
/**
 * Blink led on `pin` for `delay_ms` milliseconds for `count` times
 * @param pin the pin of the LED
 * @param delay_ms the interval to wait between LED blinks in milliseconds
 * @param count the number of times to blink the LED
 */
void blinkLed(uint8_t pin, uint32_t delay_ms, uint8_t count);

#endif
