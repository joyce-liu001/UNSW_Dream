import pytest

from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.other import clear_v1
from src.error import InputError


@pytest.fixture()
def clear():
    clear_v1()


@pytest.fixture(name='dict_list')
def create_dict_list():
    """
    Fixture function, is to pre-register four users for further tests

    Returns:
        dict_list: Dict, contain the pre-register users' information

    """
    dict_list = list()
    dict_list.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    dict_list.append(auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma"))
    dict_list.append(auth_register_v2("sundar.pichai@gmail.com", "SundarPichai",
                                      "Sunder", "Pichai"))
    dict_list.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
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
        with pytest.raises(InputError):
            assert auth_register_v2("", "123456", "Email", "Invalid")
        with pytest.raises(InputError):
            assert auth_register_v2("email", "123456", "Email", "Invalid")
        with pytest.raises(InputError):
            assert auth_register_v2("email@email", "123456", "Email", "Invalid")

    def test_register_email_been_used(self):
        """
        This test is to test for the user register with email that have been used

        Returns:
            N/A

        Raises：
            InputError: When he email address of thr user is been used

        """
        auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma")
        auth_register_v2("sundar.pichai@gmail.com", "SundarPichai", "Sunder", "Pichai")
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "PonyMa2", "Pony2", "Ma2")
        with pytest.raises(InputError):
            auth_register_v2("sundar.pichai@gmail.com", "SundarPichai2", "Sunder2", "Pichai2")

    def test_register_password_too_short(self):
        """
        This test is to test for the user register with too short password

        Returns:
            N/A

        Raises:
            InputError: When the password of the user is too short

        """
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "", "Pony", "Ma")
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "12345", "Pony", "Ma")

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
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "PonyMa", "", "Ma")
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "PonyMa", too_long_name, "Ma")

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
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "")
        with pytest.raises(InputError):
            auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", too_long_name)


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
        comp_list.append(auth_login_v2("pony.ma@qq.com", "PonyMa"))
        comp_list.append(auth_login_v2("pony.ma2@qq.com", "PonyMa"))
        comp_list.append(auth_login_v2("sundar.pichai@gmail.com", "SundarPichai"))
        comp_list.append(auth_login_v2("jack.smith@hotmail.com", "JackSmith"))
        # Make sure the return type is a dict and the value type in it is int
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
        with pytest.raises(InputError):
            assert auth_login_v2("", "123456")
        with pytest.raises(InputError):
            assert auth_login_v2("email", "123456",)
        with pytest.raises(InputError):
            assert auth_login_v2("email@email", "123456")

    @pytest.mark.usefixtures("dict_list")
    def test_login_email_not_belong(self):
        """
        Test for user login with email address that not belong to existing registered user

        Returns:
            N/A

        Raises:
            InputError: When the login email not belong to any registered users

        """
        with pytest.raises(InputError):
            auth_login_v2("pony.ma3@qq.com", "PonyMa")
        with pytest.raises(InputError):
            auth_login_v2("sundar.pichai2@gmail.com", "SundarPichai")
        with pytest.raises(InputError):
            auth_login_v2("jack.smith2@hotmail.com", "JackSmith")

    @pytest.mark.usefixtures("dict_list")
    def test_login_incorrect_password(self):
        """
        Test for user login with correct email but incorrect password

        Returns:
            N/A

        Raises:
            InputError: When the login password is incorrect

        """
        with pytest.raises(InputError):
            auth_login_v2("pony.ma@qq.com", "PonyMa1")
        with pytest.raises(InputError):
            auth_login_v2("pony.ma2@qq.com", "PonyMa1")
        with pytest.raises(InputError):
            auth_login_v2("sundar.pichai@gmail.com", "SundarPichai1")
        with pytest.raises(InputError):
            auth_login_v2("jack.smith@hotmail.com", "JackSmith1")


@pytest.mark.usefixtures("clear")
class TestLogout:
    """
    Test cases for user logout

    Args:
        dict_list: Some pre-register users, obtain their return value as a list

    Returns:
        N/A

    """
    def test_logout(self, dict_list):
        for ret_dict in dict_list:
            assert auth_logout_v1(ret_dict['token']) == {'is_success': True}
        for ret_dict in dict_list:
            assert auth_logout_v1(ret_dict['token']) == {'is_success': False}


# @pytest.mark.usefixtures("clear")
# class TestPasswordResetRequest:
#     test_user = auth_register_v2('andrew.brode233@gmail.com', '123456', 'Andrew', 'Brode')
#
#
#
# @pytest.mark.usefixtures("clear")
# class TestPassword