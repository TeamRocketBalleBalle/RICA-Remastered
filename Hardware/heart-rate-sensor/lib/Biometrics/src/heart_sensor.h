#ifndef RICA_HEART_SENSOR_h
#define RICA_HEART_SENSOR_h

#include <Adafruit_SSD1306.h>
#include <MAX30105.h>
#include <Wire.h>
#include <heartRate.h>

class HeartSensor {
  public:
    void start_sensing();
};

bool __setup_display();
bool __setup_sensor();
void __sleep_esp();

extern HeartSensor      heart_sensor;
extern Adafruit_SSD1306 display;
extern MAX30105         particleSensor;
#endif
