#include "heart_sensor.h"

#include "LOG.h"

void sensor_task(void *param) {
    log_info("running on core: %d", xPortGetCoreID());
    heart_sensor.start_sensing();
    vTaskDelete(NULL); // TODO: temporary fix, remove when hr loop is added
}

void HeartSensor::start_sensing() { log_info("hello world"); }
