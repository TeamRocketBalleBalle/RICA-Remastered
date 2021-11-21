> to be expanded later

## Files you need to setup for development:

-   ### `default_wifi_creds.h`

    location: `lib/Constants/` \
    content:

    ```cpp
    #ifndef DEFAULT_WIFI_CREDS
    #define DEFAULT_WIFI_CREDS
    const char *DEFAULT_WIFI_SSID = "YOUR SSID";
    const char *DEFAULT_WIFI_PASS = "YOUR PASSWORD";
    #endif
    ```

## list of APIs:

-   `/scan_wifi` [GET] Output:

    ```json
    [{"RSSI":-46,"SSID":"wifi 1 🥳 (2.4GHz)", "secure_type":"WPA_WPA2_PSK"}, ...]
    ```

    where `...` is if more wifis are detected they will be added in the same
    format

-   `/accept_credentials` [POST]

    Usage: `/accept_credentials?SSID=<ssid here>&PASS=<pass here>` use this
    javascript code to urlencode SSID (handles emojis)

    ```js
    escape(unescape(encodeURIComponent(ssid)));
    ```

    error messages and reason are sent via status code `400` and reason in
    response

-   `/status` [GET]

    used to get the status of client. could be any from the image attached
    example Output:

    ```json
    { "status": 4, "code": null }
    ```

    where `status` corresponds to enum code in the screenshot, and `code`
    corresponds to some internal error number inside esp library. `code` being
    useful for me, `status` is what you need for your logic

-   `/get_ip` [GET]

    returns the ip address of esp so you can store it in localstorage. **ONLY
    CALL AFTER ESP RETURNS `status: 4` aka esp is connected to wifi**

-   `/client_ack` [POST]

    **you** use this to give your acknowledgement to esp that you have the data
    you need and now esp can turn its hotspot off and client will move on their
    original wifi network response: `200, OK`
