/*
    Test wifi functionalities
 */
#include <unity.h>
#include <wifi_funcs.h>

Networking networking;
/*
this test requires a known wifi network to be there and defined in
"default_wifi_creds.h", otherwise this test will fail
*/
void test_default_wifi_connect() {
  TEST_ASSERT_EQUAL(true, networking.__default_connect_to_wifi());
}

bool run_test() {
  UNITY_BEGIN();
  RUN_TEST(test_default_wifi_connect);
  UNITY_END();

  return 0;
}

void setup() { run_test(); }
void loop() {}
