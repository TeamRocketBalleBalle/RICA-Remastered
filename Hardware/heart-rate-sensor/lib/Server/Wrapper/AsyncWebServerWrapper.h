/*
  ESP Async Web Server Wrapper

  This Wrapper class is designed to be used by Networking module to temporarily
  enable/disable certain API endpoints, and also to load in default
  configurations for the server.

*/
#ifndef __Async_WebServer_Wrapper_h
#define __Async_WebServer_Wrapper_h

#include <ESPAsyncWebServer.h>

class AsyncWebServerWrapper {
  private:
    AsyncWebServer *__server;

  public:
    AsyncWebServerWrapper(AsyncWebServer *server);

    void default_config();
    void register_default_API();
    void regiser_credential_only_API();
    void end();
};

#endif
