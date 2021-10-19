#ifndef WIFI_FUNCS
#define WIFI_FUNCS

#include <led_functions.h>

class Networking {
public:
  Networking() {}
  // the abstract function to start all networking
  bool start_networking();

  // ===========================================
  // connects to wifi using default credentials
  bool __default_connect_to_wifi();
  // connects to wifi using provided credentials
  bool __connect_to_wifi(const char *SSID, const char *PASSWORD);
};
#endif
