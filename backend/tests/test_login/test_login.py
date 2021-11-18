import pytest

from backend.tests.utility import make_cookie


class Test_common_login:
    base_url = '/api/v1/common'

    @pytest.mark.parametrize('username, password, expected_error_code',
                             [
                                 pytest.param(
                                     'gonerogued@gmail.com', 'Hello', 401),
                                 pytest.param('hello@gmail.com',
                                              'randomuser', 404),
                                 pytest.param(
                                     'catsarecute@gmail.com', 'v4tsal', 200),
                                 pytest.param('gonerogued@gmail.com', '', 401),
                                 pytest.param('', 'hello', 404),
                                 pytest.param(
                                     'codespicer@gmail.com', 'codespicer', 200),
                                 pytest.param("windy@gmail.com", 'windy', 200),
                                 pytest.param(
                                     "gonerogued@gmail.com", 'roguedbear', 200),
                                 pytest.param("valo@gmail.com",
                                              "aaaayuushhhh", 200),
                                 pytest.param(
                                     "LoremIpsum@lorem.ipsum", "lorem", 200)
                             ])
    def test_error_code_msg(self, client, username, password, expected_error_code):
        url = self.base_url + '/login'
        data = {
            "email": username,
            "password": password,
        }

        response = client.post(url, data=data)
        print("response.data", response.data)
        print("username, password", username, password)
        assert response.status_code == expected_error_code
