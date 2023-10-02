import pytest
from src.user import user_profile_v2, user_profile_setname_v2, user_profile_setemail_v2, user_profile_sethandle_v1, users_all_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.other import clear_v1

@pytest.fixture()
def clear():
    clear_v1()

@pytest.fixture(name='user_list')
def create_user_list():
    user_list = list()
    user_list.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    user_list.append(auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma"))
    user_list.append(auth_register_v2("sundar.pichai@gmail.com", "SundarPichai", \
        "Sunder", "Pichai"))
    user_list.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    return user_list


@pytest.mark.usefixtures("clear")
class TestProfile:
    """

    This class contains a series of tests
    for the "user_profile" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_valid_id(self, user_list):
        """

        Test user/profile/v2 when conditions are all valid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get the profile of the user
        result_profile = user_profile_v2(result_user['token'], result_user['auth_user_id'])

        assert result_profile['user']['email'] == 'pony.ma@qq.com'

    def test_invalid_id(self, user_list):
        """

        Test user/profile/v2 when the u_id does not refer to a valid user

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get an unused u_id
        for unuse_uid in range(0, 100000):
            if unuse_uid != result_user['auth_user_id']:
                break
        # should raise InputError, because u_id is invalid
        with pytest.raises(InputError):
            assert user_profile_v2(result_user['token'], unuse_uid)


@pytest.mark.usefixtures("clear")
class TestProfileSetName:
    """

    This class contains a series of tests
    for the "user_profile_setname" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_valid_name(self, user_list):
        """

        Test user/profile/setname/v2 when conditions are all valid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # set new name
        user_profile_setname_v2(result_user['token'], 'NewFirst', 'NewLast')
        # get the profile of the user
        result_profile = user_profile_v2(result_user['token'], result_user['auth_user_id'])
        # the name of the user should match new name
        assert result_profile['user']['name_first'] == 'NewFirst'
        assert result_profile['user']['name_last'] == 'NewLast'

    def test_invalid_name(self, user_list):
        """

        Test user/profile/setname/v2 when the new name is invalid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # should raise InputError, because the new name are invalid
        with pytest.raises(InputError):
            assert user_profile_setname_v2(result_user['token'], '', 'NewLast')
            assert user_profile_setname_v2(result_user['token'], 'NewFirst', '')
            assert user_profile_setname_v2(result_user['token'], 'NewFirst', 'NewLastddddddddddddddddddddddddddddddddddddddddddddddddddd')
            assert user_profile_setname_v2(result_user['token'], 'NewFirstddddddddddddddddddddddddddddddddddddddddddddddddddd', 'NewLast')
            assert user_profile_setname_v2(result_user['token'], 1, 'NewLast')
            assert user_profile_setname_v2(result_user['token'], 'NewFirst', 1)
        
    def test_invalid_token(self, user_list):
        """

        Test user/profile/setname/v2 when the new name is invalid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get an unused token
        for unuse_token in range(0, 100000):
            if unuse_token != result_user['token']:
                break
        # should raise InputError, because the token is invalid
        with pytest.raises(AccessError):
            assert user_profile_setname_v2(unuse_token, 'NewFirst', 'NewLast')


@pytest.mark.usefixtures("clear")
class TestProfileSetEmail:
    """

    This class contains a series of tests
    for the "user_profile_setemail" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_valid_email(self, user_list):
        """

        Test user/profile/setemail/v2 when conditions are all valid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # set new email
        user_profile_setemail_v2(result_user['token'], 'ankitrai326@gmail.com')
        # get the new profile of the user
        result_profile = user_profile_v2(result_user['token'], result_user['auth_user_id'])
        # the email now should match the new email
        assert result_profile['user']['email'] == 'ankitrai326@gmail.com'
    
    def test_invalid_email(self, user_list):
        """

        Test user/profile/setemail/v2 when the new email is invalid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # should raise InputError, because the new email is invalid
        with pytest.raises(InputError):
            assert user_profile_setemail_v2(result_user['token'], 'ankitrai326.com')

    def test_duplicate_email(self, user_list):
        """

        Test user/profile/setemail/v2 when the new email has been taken
        
        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # should raise InputError, because the new email has been taken
        with pytest.raises(InputError):
            assert user_profile_setemail_v2(result_user1['token'], 'pony.ma2@qq.com')
    
    def test_invalid_token(self, user_list):
        """

        Test user/profile/setemail/v2 when the token is invalid
        
        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get an unused token
        for unuse_token in range(0, 100000):
            if unuse_token != result_user['token']:
                break
        # should raise InputError, because the token is invalid
        with pytest.raises(AccessError):
            assert user_profile_setemail_v2(unuse_token, 'ankitrai326@gmail.com')


@pytest.mark.usefixtures("clear")
class TestProfileSetHandle:
    """

    This class contains a series of tests
    for the "user_profile_sethandle" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_valid_handle(self, user_list):
        """

        Test user/profile/sethandle/v1 when conditions are all valid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # set new handle
        user_profile_sethandle_v1(result_user['token'], 'ponymanew')
        # get the new profile of the user
        result_profile = user_profile_v2(result_user['token'], result_user['auth_user_id'])
        # the handle now should match the new handle
        assert result_profile['user']['handle_str'] == 'ponymanew'
    
    def test_invalid_handle(self, user_list):
        """

        Test user/profile/sethandle/v1 when the handle is invalid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # should raise InputError, because the handle is invalid
        with pytest.raises(InputError):
            assert user_profile_sethandle_v1(result_user['token'], 'a')
            assert user_profile_sethandle_v1(result_user['token'], 'aa')
            assert user_profile_sethandle_v1(result_user['token'], 'aaaaaaaaaaaaaaaaaaaaaaaaa')
    
    def test_duplicate_handle(self, user_list):
        """

        Test user/profile/sethandle/v1 when the handle has been taken

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # set new handle
        user_profile_sethandle_v1(result_user1['token'], 'ponymanew')
        # should raise InputError, because the new handle has been taken
        with pytest.raises(InputError):
            assert user_profile_sethandle_v1(result_user2['token'], 'ponymanew')
    
    def test_invalid_token(self, user_list):
        """

        Test user/profile/sethandle/v1 when the handle has been taken

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get an unused token
        for unuse_token in range(0, 100000):
            if unuse_token != result_user['token']:
                break
        # should raise InputError, because the token is invalid
        with pytest.raises(AccessError):
            assert user_profile_sethandle_v1(unuse_token, 'ponymanew')


@pytest.mark.usefixtures("clear")
class TestUsersAll:
    """

    This class contains a series of tests
    for the "users_all" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_valid_token(self, user_list):
        """

        Test users/all/v1 when conditions are all valid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get profile of all users
        result_all = users_all_v1(result_user['token'])
        # the output should match below
        assert len(result_all['users']) == 4

    def test_invalid_token(self, user_list):
        """

        Test users/all/v1 when the token is invalid

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # get the unused token
        for unuse_token in range(0, 100000):
            if unuse_token != result_user['token']:
                break
        # should raise InputError, because the token is invalid
        with pytest.raises(AccessError):
            assert users_all_v1(unuse_token)
