import json

import pytest

from backend.tests.utility import make_cookie


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

        assert response.status_code == 400, "/appointment endpoint does not exist"

    @pytest.mark.parametrize("id_value, expected_error",
                             [
                                 pytest.param("OneTwoThree", 400,
                                              id="id is string"),
                                 pytest.param("120.0", 400),
                                 pytest.param(2, 200),  # patient with id 2
                                 pytest.param(3, 200),  # doc with id 3
                                 # forbidden for chemist utype
                                 pytest.param(5, 403)
                             ])
    def test_ID_param_values(self, client, id_value: int, expected_error: int):
        url = self.base_url + "/appointment"

        cookie = make_cookie(id=id_value)
        client.set_cookie("localhost", "session", cookie)
        response = client.get(url)

        assert response.status_code == expected_error

    @pytest.mark.parametrize("user_id, expected_no_of_bookings",
                             [
                                 # patient 1 has no bookings
                                 pytest.param(1, 0, id="zero booking"),
                                 # patient 7 has 1 booking
                                 pytest.param(7, 1, id="one booking"),
                                 # patient 2 has 2 bookings
                                 pytest.param(2, 2, id="two bookings")
                             ])
    def test_number_of_booking_returned(self, client, user_id, expected_no_of_bookings):
        url = self.base_url + "/appointment"

        cookie = make_cookie(id=user_id)
        client.set_cookie("localhost", "session", cookie)

        response = client.get(url)
        actual_no_of_appointments = len(json.loads(
            response.data.decode())["appointments"])
        print(response.data.decode())
        assert actual_no_of_appointments == expected_no_of_bookings
