/*
Utility functions to do effects with LED
like blinking it for a duration
*/
#include <Arduino.h>

/*
 * blinks led on given pin and for a `delay_ms` milliseconds
 */
void blinkLed(uint8_t pin, uint32_t delay_ms) {
    digitalWrite(pin, HIGH);
    delay(delay_ms);
    digitalWrite(pin, LOW);
    delay(delay_ms);
}
/*
 * blinks led for a given count
 */
void blinkLed(uint8_t pin, uint32_t delay_ms, uint8_t count) {
    for (uint8_t i = 0; i < count; i++) {
        blinkLed(pin, delay_ms);
    }
}
