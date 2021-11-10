import json

import pytest


class TestDoctors_get_booking:
    """
    Arguments: user ID
    Test Cases:
        - 401 on missing arguments
        - 401 on invalid ID (bad ID values)
        - testing appointments
            - 202, valid return for patients and doctors
            - 403, if usertype chemist
        - test number of appointments returned
            - 0 bookings
            - 1 bookings
            - 2 bookings
            - expired bookings
        - TODO: test actual appointment content returned
    """
    base_url = "/api/v1/doctors"

    def test_get_booking_missing_arg(self, client):
        response = client.get(self.base_url + "/appointment")

        assert response.status_code == 401, "/appointment endpoint does not exist"

    @pytest.mark.parametrize("id_value, expected_error",
                             [
                                 pytest.param("OneTwoThree", 401,
                                              id="id is string"),
                                 pytest.param("120.0", 401),
                                 pytest.param("P02", 200),
                                 pytest.param("D02", 200),
                                 # forbidden for chemist utype
                                 pytest.param("C02", 403)
                             ])
    def test_ID_param_values(self, client, id_value: str, expected_error):
        url = self.base_url + "/appointment?id=" + id_value
        response = client.get(url)

        assert response.status_code == expected_error

    @pytest.mark.parametrize("user_id, expected_no_of_bookings",
                             [
                                 pytest.param("P03", 0, id="zero booking"),
                                 pytest.param("P02", 1, id="one booking"),
                                 pytest.param("P01", 2, id="two bookings")
                             ])
    def test_number_of_booking_returned(self, client, user_id, expected_no_of_bookings):
        url = self.base_url + "/appointment?id=" + user_id

        response = client.get(url)
        actual_no_of_appointments = len(json.loads(response.data.decode()))
        print(response.data.decode())
        assert actual_no_of_appointments == expected_no_of_bookings
