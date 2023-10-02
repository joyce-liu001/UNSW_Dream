import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError


@pytest.fixture()
def clear():
    requests.delete(config.url + 'clear/v1', json={})


@pytest.fixture(name='dict_list')
def create_dict_list():
    """
    Fixture function, is to pre-register four users for further tests

    Returns:
        dict_list: Dict, contain the pre-register users' information

    """
    dict_list = list()
    dict_list.append(requests.post(config.url + 'auth/register/v2',
                                   json={'email': 'pony.ma@qq.com',
                                         'password': 'PonyMa',
                                         'name_first': 'Pony',
                                         'name_last': 'Ma'}).json())
    dict_list.append(requests.post(config.url + 'auth/register/v2',
                                   json={'email': 'pony.ma2@qq.com',
                                         'password': 'PonyMa',
                                         'name_first': 'Pony',
                                         'name_last': 'Ma'}).json())
    dict_list.append(requests.post(config.url + 'auth/register/v2',
                                   json={'email': 'sundar.pichai@gmail.com',
                                         'password': 'SundarPichai',
                                         'name_first': 'Sunder',
                                         'name_last': 'Pichai'}).json())
    dict_list.append(requests.post(config.url + 'auth/register/v2',
                                   json={'email': 'jack.smith@hotmail.com',
                                         'password': 'JackSmith',
                                         'name_first': 'Jack',
                                         'name_last': 'Smith'}).json())
    return dict_list


@pytest.mark.usefixtures("clear")
class TestRegister:
    """
    Tests for the auth_register_v2 function
    """

    def test_register(self, dict_list):
        """
        Test for normal register case

        Args:
            dict_list: Dict, contain the pre-register users' information


        Returns:
            N/A

        """
        # Make sure the return type is a dict and the value type in it is int
        id_list = list()
        for id_dict in dict_list:
            assert type(id_dict).__name__ == "dict", "return type ==  dict"
            assert type(id_dict["token"]).__name__ == "str", "value type in token == str"
            assert type(id_dict["auth_user_id"]).__name__ == "int", "value type in auth_user_id == int"
            id_list.append(id_dict["auth_user_id"])
        # Check whether each return token is unique
        assert len(id_list) == len(set(id_list)), "tokens are all different"

    def test_register_invalid_email(self):
        """
        This test is to test for the user register with invalid email address

        Returns:
            N/A

        Raises:
            InputError: When the email address of the user is invalid

        """

    result = requests.post(config.url + 'auth/register/v2',
                           json={'email': '',
                                 'password': '123456',
                                 'name_first': 'Email',
                                 'name_last': 'Invalid'})
    assert result.status_code == InputError.code
    result = requests.post(config.url + 'auth/register/v2',
                           json={'email': 'email',
                                 'password': '123456',
                                 'name_first': 'Email',
                                 'name_last': 'Invalid'})
    assert result.status_code == InputError.code
    result = requests.post(config.url + 'auth/register/v2',
                           json={'email': 'email@email',
                                 'password': '123456',
                                 'name_first': 'Email',
                                 'name_last': 'Invalid'})
    assert result.status_code == InputError.code

    def test_register_email_been_used(self, dict_list):
        """
        This test is to test for the user register with email that have been used

        Returns:
            N/A

        Raises：
            InputError: When he email address of thr user is been used

        """
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma@qq.com',
                                     'password': 'PonyMa',
                                     'name_first': 'Pony',
                                     'name_last': 'Ma'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': 'PonyMa',
                                     'name_first': 'Pony',
                                     'name_last': 'Ma'})
        assert result.status_code == InputError.code

    def test_register_password_too_short(self):
        """
        This test is to test for the user register with too short password

        Returns:
            N/A

        Raises:
            InputError: When the password of the user is too short

        """
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma@qq.com',
                                     'password': '',
                                     'name_first': 'Pony',
                                     'name_last': 'Ma'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': '12345',
                                     'name_first': 'Pony',
                                     'name_last': 'Ma'})
        assert result.status_code == InputError.code

    def test_register_invalid_first_name(self):
        """
        This test is to test for the user register with invalid first name

        Returns:
            N/A

        Raises:
            InputError: When the first nof the user is invalid

        """
        too_long_name = ""
        while len(too_long_name) < 51:
            too_long_name += 'a'
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': '12345',
                                     'name_first': '',
                                     'name_last': 'Ma'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': '12345',
                                     'name_first': too_long_name,
                                     'name_last': 'Ma'})
        assert result.status_code == InputError.code

    def test_register_invalid_last_name(self):
        """
        This test is to test for the user register with invalid last name

        Returns:
            N/A

        Raises:
            InputError: When the last name of the user is invalid

        """
        too_long_name = ""
        while len(too_long_name) < 51:
            too_long_name += 'a'
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': '12345',
                                     'name_first': 'Pony',
                                     'name_last': ''})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/register/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': '12345',
                                     'name_first': 'Pony',
                                     'name_last': too_long_name})
        assert result.status_code == InputError.code


@pytest.mark.usefixtures("clear")
class TestLogin:
    """
    Tests for the auth_login_v2 function
    """

    def test_login(self, dict_list):
        """

        Test for normal login case

        Args:
            dict_list: Dict, contain the pre-register users' information


        Returns:
            N/A

        """
        comp_list = list()
        comp_list.append(requests.post(config.url + 'auth/login/v2',
                                       json={'email': 'pony.ma@qq.com',
                                             'password': 'PonyMa'}).json())
        comp_list.append(requests.post(config.url + 'auth/login/v2',
                                       json={'email': 'pony.ma2@qq.com',
                                             'password': 'PonyMa'}).json())
        comp_list.append(requests.post(config.url + 'auth/login/v2',
                                       json={'email': 'sundar.pichai@gmail.com',
                                             'password': 'SundarPichai'}).json())
        comp_list.append(requests.post(config.url + 'auth/login/v2',
                                       json={'email': 'jack.smith@hotmail.com',
                                             'password': 'JackSmith'}).json())
        for id_dict in comp_list:
            assert type(id_dict).__name__ == "dict", "return type ==  dict"
            assert type(id_dict["token"]).__name__ == "str", "value type in token == str"
            assert type(id_dict["auth_user_id"]).__name__ == "int", "value type in auth_user_id == int"
        # Check whether the token return is totally match the token return in register
        for i in range(0, len(dict_list)):
            assert dict_list[i]['auth_user_id'] == comp_list[i]['auth_user_id']

    def test_login_invalid_email(self):
        """
        Test for user login with invalid email

        Returns:
            N/A

        Raises:
            InputError: When the user login with invalid email

        """
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': '',
                                     'password': '123456'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'email',
                                     'password': '123456'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'email@email',
                                     'password': '123456'})
        assert result.status_code == InputError.code

    def test_login_incorrect_password(self, dict_list):
        """
         Test for user login with correct email but incorrect password

         Returns:
             N/A

         Raises:
             InputError: When the login password is incorrect

         """
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'pony.ma@qq.com',
                                     'password': 'PonyMa1'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': 'PonyMa1'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'sundar.pichai@gmail.com',
                                     'password': 'SundarPichai1'})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'jack.smith@hotmail.com',
                                     'password': 'JackSmith1'})
        assert result.status_code == InputError.code


@pytest.mark.usefixtures("clear")
class TestLogout:
    """
    Test case for user logout
    """
    def test_logout(self, dict_list):
        """
        Test cases for user logout

        Args:
            dict_list: Some pre-register users, obtain their return value as a list

        Returns:
            N/A

        """
        for ret_dict in dict_list:
            result = requests.post(config.url + 'auth/logout/v1',
                                   json={'token': ret_dict['token']}).json()
            assert result == {'is_success': True}
        for ret_dict in dict_list:
            result = requests.post(config.url + 'auth/logout/v1',
                                   json={'token': ret_dict['token']}).json()
            assert result == {'is_success': False}
