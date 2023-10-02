import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError


@pytest.fixture()
def clear():
    requests.delete(config.url + 'clear/v1', json={})


@pytest.fixture(name='reg_list')
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


@pytest.fixture(name='user_list')
def create_user_list():
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


@pytest.fixture(name='channel_list')
def create_channel_list():
    """
    Fixture function, is to pre-create some channels for further testing

    Returns:
        dict_list: Dict, contain the pre-register channel's information

    """
    channel_list = list()
    token = requests.post(config.url + 'auth/login/v2',
                          json={'email': 'pony.ma@qq.com',
                                'password': 'PonyMa'}).json()['token']
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': token,
                                            'name': "Pony's channel",
                                            'is_public': True}).json())
    token = requests.post(config.url + 'auth/login/v2',
                          json={'email': 'pony.ma2@qq.com',
                                'password': 'PonyMa'}).json()['token']
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': token,
                                            'name': "Pony2's channel",
                                            'is_public': True}).json())
    token = requests.post(config.url + 'auth/login/v2',
                          json={'email': 'sundar.pichai@gmail.com',
                                'password': 'SundarPichai'}).json()['token']
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': token,
                                            'name': "Sundar's channel",
                                            'is_public': False}).json())
    token = requests.post(config.url + 'auth/login/v2',
                          json={'email': 'jack.smith@hotmail.com',
                                'password': 'JackSmith'}).json()['token']
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': token,
                                            'name': "Jack's channel",
                                            'is_public': False}).json())
    return channel_list


@pytest.fixture(name='channel2_list')
def create_channel2_list(reg_list):
    channel_list = list()
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': reg_list[0]['token'],
                                            'name': "pony's channel",
                                            'is_public': True}).json())
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': reg_list[3]['token'],
                                            'name': "jack's channel",
                                            'is_public': False}).json())
    channel_list.append(requests.post(config.url + 'channels/create/v2',
                                      json={'token': reg_list[2]['token'],
                                            'name': "sunder's channel",
                                            'is_public': True}).json())
    requests.post(config.url + 'channel/invite/v2',
                  json={'token': reg_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'u_id': reg_list[1]['auth_user_id']})
    requests.post(config.url + 'channel/invite/v2',
                  json={'token': reg_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'u_id': reg_list[2]['auth_user_id']})
    requests.post(config.url + 'channel/invite/v2',
                  json={'token': reg_list[3]['token'],
                        'channel_id': channel_list[1]['channel_id'],
                        'u_id': reg_list[1]['auth_user_id']})
    requests.post(config.url + 'channel/invite/v2',
                  json={'token': reg_list[3]['token'],
                        'channel_id': channel_list[1]['channel_id'],
                        'u_id': reg_list[2]['auth_user_id']})

    requests.post(config.url + 'message/send/v2',
                  json={'token': reg_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'message': "pony's message in pony's channel"})
    requests.post(config.url + 'message/send/v2',
                  json={'token': reg_list[1]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'message': "pony2's message in pony's channel"})
    requests.post(config.url + 'message/send/v2',
                  json={'token': reg_list[2]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'message': "sunder's message in pony's channel"})
    requests.post(config.url + 'message/send/v2',
                  json={'token': reg_list[1]['token'],
                        'channel_id': channel_list[1]['channel_id'],
                        'message': "pony2's message in jack's channel"})
    for user in reg_list:
        requests.post(config.url + 'auth/logout/v1',
                      json={'token': user['token']})
    return channel_list


@pytest.fixture(name='login_list')
def create_login_list():
    login_list = list()
    login_list.append(requests.post(config.url + 'auth/login/v2',
                                    json={'email': 'pony.ma@qq.com',
                                          'password': 'PonyMa'}).json())
    login_list.append(requests.post(config.url + 'auth/login/v2',
                                    json={'email': 'pony.ma2@qq.com',
                                          'password': 'PonyMa'}).json())
    login_list.append(requests.post(config.url + 'auth/login/v2',
                                    json={'email': 'sundar.pichai@gmail.com',
                                          'password': 'SundarPichai'}).json())
    login_list.append(requests.post(config.url + 'auth/login/v2',
                                    json={'email': 'jack.smith@hotmail.com',
                                          'password': 'JackSmith'}).json())
    return login_list


@pytest.mark.usefixtures("clear")
class TestAddOwner:
    """
    Test cases for add user as owner to the channel
    """
    def test_addowner(self, user_list, channel_list):
        """
        General case for adding owner to the channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        requests.post(config.url + 'auth/login/v2',
                      json={'email': 'pony.ma@qq.com',
                            'password': 'PonyMa'})
        # Test whether Dream owner can add others to become other channel's owner
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[1]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[1]['channel_id'],
                                     'u_id': user_list[0]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': channel_list[1]['channel_id'],
                                     'u_id': user_list[2]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[2]['token'],
                                     'channel_id': channel_list[2]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']}).json()
        assert result == {}
        result = json.loads(requests.get(config.url + 'channel/details/v2',
                                         params={'token': user_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id']}).text)
        assert len(result['owner_members']) == 1
        result = json.loads(requests.get(config.url + 'channel/details/v2',
                                         params={'token': user_list[1]['token'],
                                                 'channel_id': channel_list[1]['channel_id']}).text)
        assert len(result['owner_members']) == 4
        result = json.loads(requests.get(config.url + 'channel/details/v2',
                                         params={'token': user_list[2]['token'],
                                                 'channel_id': channel_list[2]['channel_id']}).text)
        assert len(result['owner_members']) == 2

    def test_invalid_channel_id(self, user_list, channel_list):
        """
        Test cases for adding owner with an invalid channel_id

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        invalid_id = -1
        # Generate an invalid id, find an invalid id for testing
        for i in range(0, 5):
            invalid = True
            for channel in channel_list:
                if i == channel['channel_id']:
                    invalid = False
            if invalid:
                invalid_id = i
                break
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': invalid_id,
                                     'u_id': user_list[0]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': invalid_id,
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': invalid_id,
                                     'u_id': user_list[2]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': invalid_id,
                                     'u_id': user_list[3]['auth_user_id']})
        assert result.status_code == InputError.code

    def test_already_owner(self, user_list, channel_list):
        """
        Test cases with the user is already the owner of the channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': channel_list[1]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[0]['auth_user_id']})
        assert result.status_code == InputError.code

    def test_not_owner(self, user_list, channel_list):
        """
        Test case for the authorised user is not an owner of channel/Dream

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': channel_list[2]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']})
        assert result.status_code == AccessError.code


@pytest.mark.usefixtures("clear")
class TestRemoveOwner:
    """
    Test cases for remove owner from in the channel
    """
    def test_removeowner(self, user_list, channel_list):
        """
        Test cases for general case for remove owner

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[2]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']}).json()
        assert result == {}
        result = json.loads(requests.get(config.url + 'channel/details/v2',
                                         params={'token': user_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id']}).text)
        assert len(result['owner_members']) == 4
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[2]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']}).json()
        assert result == {}
        result = json.loads(requests.get(config.url + 'channel/details/v2',
                                         params={'token': user_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id']}).text)
        assert len(result['owner_members']) == 1

    def test_invalid_channel_id(self, user_list, channel_list):
        """
        Test cases for channel_id is invalid

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        invalid_id = -1
        # Generate an invalid id, find an invalid id for testing
        for i in range(0, 5):
            invalid = True
            for channel in channel_list:
                if i == channel['channel_id']:
                    invalid = False
            if invalid:
                invalid_id = i
                break
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[1]['channel_id'],
                                     'u_id': user_list[0]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[2]['channel_id'],
                                     'u_id': user_list[0]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': invalid_id,
                                     'u_id': user_list[0]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[2]['token'],
                                     'channel_id': invalid_id,
                                     'u_id': user_list[0]['auth_user_id']})
        assert result.status_code == InputError.code

    def test_user_not_owner(self, user_list, channel_list):
        """
         Test case for the user is not an owner of channel

         Args:
             user_list: pre-register users
             channel_list: pre-create channel

         Returns:
             N/A

         """
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[2]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']})
        assert result.status_code == InputError.code

    def test_user_user_only_owner(self, user_list, channel_list):
        """
        Test case for the user is the only owner of this channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[0]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[2]['auth_user_id']})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[3]['auth_user_id']})
        assert result.status_code == InputError.code

    def test_not_owner(self, user_list, channel_list):
        """
          Test case for the authorised user is not an owner of channel/Dream

          Args:
              user_list: pre-register users
              channel_list: pre-create channel

          Returns:
              N/A

          """
        result = requests.post(config.url + 'channel/addowner/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[2]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'channel/removeowner/v1',
                               json={'token': user_list[3]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'u_id': user_list[1]['auth_user_id']})
        assert result.status_code == AccessError.code


@pytest.mark.usefixtures("clear")
class TestLeave:
    """
    Test case for channel leave
    """
    def test_channel_leave(self, user_list, channel_list):
        """
        Test case for general case for channel leave

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        requests.post(config.url + 'channel/invite/v2',
                      json={'token': user_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'u_id': user_list[1]['auth_user_id']})
        requests.post(config.url + 'channel/invite/v2',
                      json={'token': user_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'u_id': user_list[2]['auth_user_id']})
        requests.post(config.url + 'channel/invite/v2',
                      json={'token': user_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'u_id': user_list[3]['auth_user_id']})
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': channel_list[0]['channel_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[2]['token'],
                                     'channel_id': channel_list[0]['channel_id']}).json()
        assert result == {}
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[3]['token'],
                                     'channel_id': channel_list[0]['channel_id']}).json()
        assert result == {}

    def test_invalid_id(self, user_list, channel_list):
        """
        Test case for the channel id is invalid

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        invalid_id = -1
        # Generate an invalid id, find an invalid id for testing
        for i in range(0, 5):
            invalid = True
            for channel in channel_list:
                if i == channel['channel_id']:
                    invalid = False
            if invalid:
                invalid_id = i
                break
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': invalid_id})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': invalid_id})
        assert result.status_code == InputError.code

    def test_not_member(self, user_list, channel_list):
        """
        Test case for the user is not the member of this channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[0]['token'],
                                     'channel_id': channel_list[3]['channel_id']})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[1]['token'],
                                     'channel_id': channel_list[0]['channel_id']})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[2]['token'],
                                     'channel_id': channel_list[1]['channel_id']})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'channel/leave/v1',
                               json={'token': user_list[3]['token'],
                                     'channel_id': channel_list[2]['channel_id']})
        assert result.status_code == AccessError.code


@pytest.fixture(name="users")
def create_users():
    """Create different users and store their id and token in a list."""
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


@pytest.fixture(name="channel_id")
def users_setup():
    """User1 creates one public channel and return the channel id"""
    resp = requests.post(config.url + 'auth/login/v2', json={
        'email': 'pony.ma@qq.com',
        'password': 'PonyMa'
    })
    user1 = resp.json()
    resp = requests.post(config.url + 'channels/create/v2', json={
        "token": user1["token"],
        "name": "Channel1",
        "is_public": True
    })
    channel1 = resp.json()
    resp = requests.post(config.url + 'auth/logout/v1', json={"token": user1["token"]})
    return channel1['channel_id']


@pytest.mark.usefixtures("clear")
class TestInvite:
    def test_invalid_channel_id(self, users):
        """Test channel/invite/v2 when the channel_id does not refer to a valid channel."""
        resp = requests.post(config.url + 'channel/invite/v2', json={
            "token": users[0]["token"],
            "channel_id": -1,
            "u_id": users[1]["auth_user_id"]
        })
        assert resp.status_code == InputError.code

    def test_invalid_u_id(self, users, channel_id):
        """Test channel/invite/v2 when the u_id does not refer to a valid user."""
        resp = requests.post(config.url + 'channel/invite/v2', json={
            "token": users[0]["token"],
            "channel_id": channel_id,
            "u_id": -1
        })
        assert resp.status_code == InputError.code

    def test_author_not_member_fail(self, users):
        """Test channel/invite/v2 when the authorised user is not already a member of the channel."""
        resp = requests.post(config.url + 'channels/create/v2', json={
            "token": users[1]["token"],
            "name": "Channel2",
            "is_public": True
        })
        channel2 = resp.json()
        resp = requests.post(config.url + 'channel/invite/v2', json={
            "token": users[0]["token"],
            "channel_id": channel2["channel_id"],
            "u_id": users[1]["auth_user_id"]
        })
        assert resp.status_code == AccessError.code

    def test_successful_channel_id(self, users, channel_id):
        """Test channel/invite/v2 can succeffully invite user or not."""
        resp = requests.post(config.url + 'channel/invite/v2', json={
            "token": users[0]["token"],
            "channel_id": channel_id,
            "u_id": users[2]["auth_user_id"]
        })
        resp = requests.get(config.url + 'channel/details/v2', params={
            "token": users[0]["token"],
            "channel_id": channel_id
        })
        detail = json.loads(resp.text)
        assert len(detail['all_members']) == 2


@pytest.mark.usefixtures("clear")
class TestChannelDetail:

    def test_invalid_channel_id(self, users):
        '''
        scenario 1 : user1 creates one public channel
        there is no one joins public one
        raise Inputerror if give a invalid channel ID
        '''
        resp = requests.get(config.url + 'channel/details/v2', params={
            "token": users[0]["token"],
            "channel_id": -1
        })
        assert resp.status_code == InputError.code

    def test_not_member(self, users, channel_id):
        '''
        scenario 2 : user1 creates one public channel
        there is no one joins public one
        raise AccessError if give an authorised user is not a member of the channel
        '''
        resp = requests.get(config.url + 'channel/details/v2', params={
            "token": users[1]["token"],
            "channel_id": channel_id
        })
        assert resp.status_code == AccessError.code

    def test_scenario3(self, users, channel_id):
        '''
        scenario 3 : user1 creates one public channel
        there is no one joins public one then show the detail of the channel
        '''

        resp = requests.get(config.url + 'channel/details/v2', params={
            "token": users[0]["token"],
            "channel_id": channel_id
        })
        detail = json.loads(resp.text)
        assert len(detail['all_members']) == 1

    def test_scenario4(self, users, channel_id):
        '''
        scenario 4 : user1 creates one public channel
        user3 joins the public channel, show the detail of the channel
        '''
        resp = requests.post(config.url + 'channel/invite/v2', json={
            "token": users[0]["token"],
            "channel_id": channel_id,
            "u_id": users[2]["auth_user_id"]
        })
        resp = requests.get(config.url + 'channel/details/v2', params={
            "token": users[0]["token"],
            "channel_id": channel_id
        })
        detail = json.loads(resp.text)
        assert len(detail['all_members']) == 2


@pytest.mark.usefixtures("clear")
class TestJoin:
    """

    This class contains a series of tests
    for the "channel_join" function.

    Args:
            N/A

        Returns:
            N/A

    """

    def test_channel_invalid_id(self, users, channel_id):
        """

        Test whether channel_join can raise an error.
        Given an invalid id of the channel,
        channel_join function should raise an InputError.

        Args:
            N/A

        Returns:
            N/A

        """
        resp = requests.post(config.url + 'channel/join/v2', json={
            "token": users[0]["token"],
            "channel_id": -1,
        })
        # if InputError raised, test pass.
        assert resp.status_code == InputError.code

    def test_invalid_u_id(self, users, channel_id):
        """

        Test channel/join/v2 when the u_id does not refer to a valid user.

        """

        resp = requests.post(config.url + 'channel/join/v2', json={
            "token": -10,
            "channel_id": channel_id,
        })
        # should raise an AccessError
        assert resp.status_code == AccessError.code

    def test_join_private_fail(self, users, channel_id):
        """

        Test whether channel_join can raise an error.
        Given an valid id of a private channel,
        When the user is not global owner,
        channel_join function should raise an AccessError.

        Args:
            N/A

        Returns:
            N/A

        """
        # create a private channel
        resp = requests.post(config.url + 'channels/create/v2', json={
            "token": users[0]["token"],
            "name": "Channel1",
            "is_public": False,
        })
        channel1 = resp.json()

        resp = requests.post(config.url + 'channel/join/v2', json={
            "token": users[1]["token"],
            "channel_id": channel1["channel_id"],
        })
        # AccessError should be raised, because Sundar does not have permission.
        assert resp.status_code == AccessError.code

    def test_join_private_success(self, users, channel_id):
        """

        Test whether channel_join can succeed.
        Given an valid id of a private channel,
        When the user is the global owner,
        channel_join function should succeed.

        Args:
            N/A

        Returns:
            N/A

        """

        resp = requests.post(config.url + 'channels/create/v2', json={
            "token": users[1]["token"],
            "name": "Channel1",
            "is_public": False,
        })
        channel1 = resp.json()

        requests.post(config.url + 'channel/join/v2', json={
            "token": users[0]["token"],
            "channel_id": channel1["channel_id"],
        })
        # using "channels_list_v2" to obtain all the channels' detail
        resp = requests.get(config.url + 'channels/list/v2', params={
            "token": users[0]["token"],
        })

        user1_channle_list = json.loads(resp.text)['channels']

        join_success = False
        # if the target channel_id is valid, join_success will be True
        for channel in user1_channle_list:
            if channel['channel_id'] == channel1['channel_id']:
                # once the channel_id is valid, break
                join_success = True
                break
        assert join_success == True

    def test_valid_channel_id(self, users, channel_id):
        """

        Test whether channel_join can succeed
        if the channel_id is valid.

        Args:
            N/A

        Returns:
            N/A

        """

        requests.post(config.url + 'channel/join/v2', json={
            "token": users[1]["token"],
            "channel_id": channel_id,
        })
        # using "channels_list_v2" to obtain all the channels' detail
        resp = requests.get(config.url + 'channels/list/v2', params={
            "token": users[1]["token"],
        })

        user2_channle_list = json.loads(resp.text)['channels']

        join_success = False
        # if the target channel_id is valid, join_success will be True
        for channel in user2_channle_list:
            if channel['channel_id'] == channel_id:
                # once the channel_id is valid, break
                join_success = True
                break
        assert join_success == True

    def test_join_exist_user(self, users, channel_id):
        """

        Test whether the same user will appear more than once in 'owner_members'
        if we join the same user twice.

        Args:
            N/A

        Returns:
            N/A

        """

        requests.post(config.url + 'channel/join/v2', json={
            "token": users[1]["token"],
            "channel_id": channel_id,
        })
        # join same user twice
        requests.post(config.url + 'channel/join/v2', json={
            "token": users[1]["token"],
            "channel_id": channel_id,
        })

        resp = requests.get(config.url + 'channel/details/v2', params={
            "token": users[1]["token"],
            "channel_id": channel_id,
        })

        channels_dict = json.loads(resp.text)
        # record the number of times the same user appears
        same_member = 0
        for member in channels_dict['all_members']:
            if member['u_id'] == users[1]['auth_user_id']:
                same_member += 1
        # if user appears more than once, test fails
        assert same_member == 1


@pytest.mark.usefixtures("clear")
class TestListall:
    """

    This class contains a series of tests
    for the "channel_listall" function.

    """

    def test_list_mix_channel(self, users):
        """

        Test whether channel_listall can list channels correctly.
        Given a few public channels, channel_listall function should list channels correctly.

        Args:
            N/A

        Returns:
            N/A

        """
        # create public channels
        resp = requests.post(config.url + 'channels/create/v2', json={
            "token": users[0]["token"],
            "name": "Channel1",
            "is_public": True,
        })
        channel1 = resp.json()
        # create public channels
        resp = requests.post(config.url + 'channels/create/v2', json={
            "token": users[1]["token"],
            "name": "Channel2",
            "is_public": True,
        })
        channel2 = resp.json()
        # create private channel
        resp = requests.post(config.url + 'channels/create/v2', json={
            "token": users[0]["token"],
            "name": "Channel3",
            "is_public": False,
        })
        pri_channel = resp.json()

        resp = requests.get(config.url + 'channels/listall/v2', params={
            "token": users[0]["token"],
        })
        # channels' detail should match
        assert json.loads(resp.text) == {
            'channels': [
                {
                    'channel_id': channel1["channel_id"],
                    'name': 'Channel1'
                },
                {
                    'channel_id': channel2["channel_id"],
                    'name': 'Channel2'
                },
                {
                    'channel_id': pri_channel["channel_id"],
                    'name': 'Channel3'
                },
            ]
        }


@pytest.mark.usefixtures("clear")
class TestChannelMessage:
    """

    This class contains a series of tests
    for the "channel_messages" function.

    """

    def test_channel_message(self, channel2_list, login_list):
        """

        Test channel_message.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message1"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message2"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message3"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message4"})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel2_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "message4"
        assert result['messages'][1]['message'] == "message3"
        assert result['messages'][2]['message'] == "message2"
        assert result['messages'][3]['message'] == "message1"

    def test_channel_message_invalid_start(self, channel2_list, login_list):
        """

        Test channel_message with invalid start

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message1"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message2"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message3"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message4"})
        result = requests.get(config.url + 'channel/messages/v2',
                              params={'token': login_list[0]['token'],
                                      'channel_id': channel2_list[0]['channel_id'],
                                      'start': 20})
        assert result.status_code == InputError.code

    def test_channel_message_invalid_channel_id(self, channel2_list, login_list):
        """

        Test channel_message with invalid channel_id

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message1"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message2"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message3"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message4"})
        result = requests.get(config.url + 'channel/messages/v2',
                              params={'token': login_list[0]['token'],
                                      'channel_id': -1,
                                      'start': 0})
        assert result.status_code == InputError.code

    def test_channel_message_invalid_user(self, channel2_list, login_list):
        """

        Test channel_message with invalid user

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message1"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message2"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message3"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel2_list[0]['channel_id'],
                            'message': "message4"})
        result = requests.get(config.url + 'channel/messages/v2',
                              params={'token': login_list[3]['token'],
                                      'channel_id': channel2_list[0]['channel_id'],
                                      'start': 0})
        assert result.status_code == AccessError.code
