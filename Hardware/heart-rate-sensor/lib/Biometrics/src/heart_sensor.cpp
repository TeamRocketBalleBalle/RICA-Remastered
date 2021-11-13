#include "heart_sensor.h"

#include "CONFIG.h"
#include "LOG.h"
#include "biometric_vars.h"

const byte RATE_SIZE = 4;    // Increase this for more averaging. 4 is good.
byte       rates[RATE_SIZE]; // Array of heart rates
byte       rateSpot = 0;     // rates array index
long       lastBeat = 0;     // Time at which the last beat occurred
float      beatsPerMinute;
int        beatAvg;

unsigned long last_active_time     = 0;
bool          NO_HUMAN_INTERACTING = false;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
MAX30105         particleSensor;

bool __setup_display() {
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    log_trace("display begined");
    display.display();
    log_trace("display displayed");
    return true;
}

bool __setup_sensor() {
    // Use default I2C port, 400kHz speed
    particleSensor.begin(Wire, I2C_SPEED_FAST);
    particleSensor.setup(); // Configure sensor with default settings
    // Turn Red LED to low to indicate sensor is running
    particleSensor.setPulseAmplitudeRed(0x0A);
    return true;
}

void __sleep_esp() {
#if !RICA_DO_NOT_SLEEP_DEBUG
    // shutdown sensor and display
    particleSensor.shutDown();
    display.clearDisplay();
    display.display();

    // reference: https://esp32.com/viewtopic.php?t=3083
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);
    esp_deep_sleep_start();
#else
    log_info("not going to sleep as debug flag on");
#endif
}

void HeartSensor::start_sensing() {
    while (true) {
        long irValue =
            particleSensor.getIR(); // Reading the IR value it will permit us to
                                    // know if there's a finger on the sensor or
                                    // not Also detecting a heartbeat
        if (irValue > 7000) {       // If a finger is detected
            if (NO_HUMAN_INTERACTING) {
                NO_HUMAN_INTERACTING = false;
            }

            display.clearDisplay(); // Clear the display
            display.drawBitmap(
                5, 5, logo2_bmp, 24, 21,
                WHITE);             // Draw the first bmp picture (little heart)
            display.setTextSize(2); // Near it display the average BPM you can
                                    // display the BPM if you want
            display.setTextColor(WHITE);
            display.setCursor(50, 0);
            display.println("BPM");
            display.setCursor(50, 18);
            display.println(beatAvg);

            if (checkForBeat(irValue) == true) // If a heart beat is detected
            {
                display.clearDisplay(); // Clear the display
                display.drawBitmap(
                    0, 0, logo3_bmp, 32, 32,
                    WHITE); // Draw the second picture (bigger heart)
                display.setTextSize(2); // And still displays the average BPM
                display.setTextColor(WHITE);
                display.setCursor(50, 0);
                display.println("BPM");
                display.setCursor(50, 18);
                display.println(beatAvg);
                display.display();
                //    tone(3,1000);                                        //And
                //    tone the buzzer for a 100ms you can reduce it it will be
                //    better
                delay(100);
                //    noTone(3); //Deactivate the buzzer to have the effect of a
                //    "bip"
                // We sensed a beat!
                long delta =
                    millis() - lastBeat; // Measure duration between two beats
                lastBeat = millis();

                beatsPerMinute = 60 / (delta / 1000.0); // Calculating the BPM

                if (beatsPerMinute < 255 &&
                    beatsPerMinute >
                        20) // To calculate the average we store some values
                            // (4) then do some math to calculate the average
                {
                    rates[rateSpot++] =
                        (byte)beatsPerMinute; // Store this reading in the array
                    rateSpot %= RATE_SIZE;    // Wrap variable

                    // Take average of readings
                    beatAvg = 0;
                    for (byte x = 0; x < RATE_SIZE; x++)
                        beatAvg += rates[x];
                    beatAvg /= RATE_SIZE;
                }
            }
        }
        if (irValue < 7000) { // If no finger is detected it inform the user and
                              // put the average BPM to 0 or it will be stored
                              // for the next measure

            if (!NO_HUMAN_INTERACTING) {
                NO_HUMAN_INTERACTING = true;
                last_active_time     = millis();
            }

            beatAvg = 0;
            display.clearDisplay();
            display.setTextSize(1);
            display.setTextColor(WHITE);
            display.setCursor(30, 5);
            display.println("Please Place ");
            display.setCursor(30, 15);
            display.println("your finger ");
        }

        bool go_to_sleep =
            NO_HUMAN_INTERACTING &&
            millis() - last_active_time >= RICA_SENSOR_SLEEP_TIMEOUT_ms;
        if (go_to_sleep) {
            log_info("going to sleep after inactivity");
            __sleep_esp();
        }
        if (NO_HUMAN_INTERACTING) {
            int countdown =
                (RICA_SENSOR_SLEEP_TIMEOUT_ms - (millis() - last_active_time)) /
                1000;
            display.setCursor(0, SCREEN_HEIGHT - 20);
            display.printf("sleeping in %ds", countdown);
        }
        display.display();
    }
}
