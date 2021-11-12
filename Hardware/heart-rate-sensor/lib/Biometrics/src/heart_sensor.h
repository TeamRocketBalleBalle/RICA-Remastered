#ifndef RICA_HEART_SENSOR_h
#define RICA_HEART_SENSOR_h
class HeartSensor {
  public:
    void start_sensing();
};
void sensor_task(void *param);

extern HeartSensor heart_sensor;
#endif
