import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError


@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1', json={})


@pytest.fixture(name="users")
def create_users():
    """Create different users and store their id in a list."""
    users = list()
    users.append(requests.post(config.url + 'auth/register/v2', json={
        'email': 'pony.ma@qq.com', 
        'password': 'PonyMa', 
        'name_first': 'Pony', 
        'name_last': 'Ma'
    }).json())
    users.append(requests.post(config.url + 'auth/register/v2', json={
        'email': 'pony.ma@qqqw.com', 
        'password': 'PonyMa', 
        'name_first': 'Pony', 
        'name_last': 'Ma'
    }).json())
    users.append(requests.post(config.url + 'auth/register/v2', json={
        'email': 'jack.smith@hotmail.com', 
        'password': 'JackSmith', 
        'name_first': 'Jack', 
        'name_last': 'Smith'
    }).json())
    return users



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
    def test_valid_id(self, users):
        """

        Test user/profile/v2 when conditions are all valid

        """
        resp = requests.get(config.url + 'user/profile/v2', params={
            'token':  users[0]["token"],
            'u_id':  users[0]["auth_user_id"],
        })
        # get the profile of the user
        result_profile = json.loads(resp.text)
        
        assert result_profile['user']['email'] == 'pony.ma@qq.com'

    def test_invalid_id(self, users):
        """

        Test user/profile/v2 when the u_id does not refer to a valid user

        """
        resp = requests.get(config.url + 'user/profile/v2', params={
            'token': users[0]['token'],
            'u_id': -10,
        })
        # should raise InputError, because u_id is invalid
        assert resp.status_code == InputError.code


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
    def test_valid_name(self, users):
        """

        Test user/profile/setname/v2 when conditions are all valid

        """
        # set new name
        requests.put(config.url + 'user/profile/setname/v2', json={
            'token': users[0]['token'],
            'name_first': 'NewFirst',
            'name_last': 'NewLast',
        })
        # get the profile of the user
        resp = requests.get(config.url + 'user/profile/v2', params={
            'token': users[0]['token'],
            'u_id': users[0]['auth_user_id'],
        })
        # the name of the user should match new name
        assert json.loads(resp.text)['user']['name_first'] == 'NewFirst'
        assert json.loads(resp.text)['user']['name_last'] == 'NewLast'

    def test_invalid_name(self, users):
        """

        Test user/profile/setname/v2 when the new name is invalid

        """
        resp = requests.put(config.url + 'user/profile/setname/v2', json={
            'token': users[0]['token'],
            'name_first': '',
            'name_last': 'NewLast',
        })
        # should raise InputError, because the new name are invalid
        assert resp.status_code == InputError.code

        resp = requests.put(config.url + 'user/profile/setname/v2', json={
            'token': users[0]['token'],
            'name_first': 'NewFirst',
            'name_last': '',
        })
        # should raise InputError, because the new name are invalid
        assert resp.status_code == InputError.code

        resp = requests.put(config.url + 'user/profile/setname/v2', json={
            'token': users[0]['token'],
            'name_first': 'NewFirst',
            'name_last': 'NewLastddddddddddddddddddddddddddddddddddddddddddddddddddd',
        })
        # should raise InputError, because the new name are invalid
        assert resp.status_code == InputError.code

        resp = requests.put(config.url + 'user/profile/setname/v2', json={
            'token': users[0]['token'],
            'name_first': 'NewFirstddddddddddddddddddddddddddddddddddddddddddddddddddd',
            'name_last': 'NewLast',
        })
        # should raise InputError, because the new name are invalid
        assert resp.status_code == InputError.code
        
    def test_invalid_token(self, users):
        resp = requests.put(config.url + 'user/profile/setname/v2', json={
            'token': -10,
            'name_first': 'NewFirst',
            'name_last': 'NewLast',
        })
        # should raise InputError, because the token is invalid
        assert resp.status_code == AccessError.code

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
    def test_valid_email(self, users):
        """

        Test user/profile/setemail/v2 when conditions are all valid

        """
        # set new email
        requests.put(config.url + 'user/profile/setemail/v2', json={
            'token': users[0]['token'],
            'email': 'ankitrai326@gmail.com',
        })
        # get the new profile of the user
        resp = requests.get(config.url + 'user/profile/v2', params={
            'token': users[0]['token'],
            'u_id': users[0]['auth_user_id'],
        })
        # the email now should match the new email
        assert json.loads(resp.text)['user']['email'] == 'ankitrai326@gmail.com'
    
    def test_invalid_email(self, users):
        """

        Test user/profile/setemail/v2 when the new email is invalid

        """
        resp = requests.put(config.url + 'user/profile/setemail/v2', json={
            'token': users[0]['token'],
            'email': 'ankitrai326.com',
        })
        # should raise InputError, because the new email is invalid
        assert resp.status_code == InputError.code

    def test_duplicate_email(self, users):
        """

        Test user/profile/setemail/v2 when the new email has been taken
        
        """
        resp = requests.put(config.url + 'user/profile/setemail/v2', json={
            'token': users[0]['token'],
            'email': 'pony.ma@qqqw.com',
        })
        # should raise InputError, because the new email has been taken
        assert resp.status_code == InputError.code
    
    def test_invalid_token(self, users):
        """

        Test user/profile/setemail/v2 when the token is invalid
        
        """    
        resp = requests.put(config.url + 'user/profile/setemail/v2', json={
            'token': -10,
            'email': 'ankitrai326@gmail.com',
        })
        # should raise InputError, because the token is invalid
        assert resp.status_code == AccessError.code

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
    def test_valid_handle(self, users):
        """

        Test user/profile/sethandle/v1 when conditions are all valid

        """
        # set new handle
        requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': users[0]['token'],
            'handle_str': 'ponymanew',
        })
        # get the new profile of the user
        resp = requests.get(config.url + 'user/profile/v2', params={
            'token': users[0]['token'],
            'u_id': users[0]['auth_user_id'],
        })
        # the handle now should match the new handle
        assert json.loads(resp.text)['user']['handle_str'] == 'ponymanew'
    
    def test_invalid_handle(self, users):
        """

        Test user/profile/sethandle/v1 when the handle is invalid

        """
        resp = requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': users[0]['token'],
            'handle_str': 'a',
        })
        # should raise InputError, because the handle is invalid
        assert resp.status_code == InputError.code
        
        resp = requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': users[0]['token'],
            'handle_str': 'aa',
        })
        # should raise InputError, because the handle is invalid
        assert resp.status_code == InputError.code

        resp = requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': users[0]['token'],
            'handle_str': 'aaaaaaaaaaaaaaaaaaaaaaaaa',
        })
        # should raise InputError, because the handle is invalid
        assert resp.status_code == InputError.code
    
    def test_duplicate_handle(self, users):
        """

        Test user/profile/sethandle/v1 when the handle has been taken

        """
        # set new handle
        requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': users[0]['token'],
            'handle_str': 'ponymanew',
        })
        
        resp = requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': users[1]['token'],
            'handle_str': 'ponymanew',
        })
        # should raise InputError, because the new handle has been taken
        assert resp.status_code == InputError.code
    
    def test_invalid_token(self, users):
        """

        Test user/profile/sethandle/v1 when the handle has been taken

        """
        resp = requests.put(config.url + 'user/profile/sethandle/v1', json={
            'token': -10,
            'handle_str': 'ponymanew',
        })
        # should raise InputError, because the token is invalid
        assert resp.status_code == AccessError.code
    
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
    def test_valid_token(self, users):
        """

        Test users/all/v1 when conditions are all valid

        """
        # get profile of all users
        resp = requests.get(config.url + 'users/all/v1', params={
            'token': users[0]['token']
        })

        result_all = json.loads(resp.text)
        # the output should match below
        assert len(result_all['users']) == 3

    def test_invalid_token(self, users):
        """

        Test users/all/v1 when the token is invalid

        """
        resp = requests.get(config.url + 'users/all/v1', params={
            'token': -10,
        })
        # should raise InputError, because the token is invalid
        assert resp.status_code == AccessError.code
