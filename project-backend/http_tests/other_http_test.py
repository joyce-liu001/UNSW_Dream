import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError
import string
import random


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


@pytest.fixture(name='channel_list')
def create_channel_list(reg_list):
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
                  json={'token': reg_list[0]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'u_id': reg_list[3]['auth_user_id']})
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
                  json={'token': reg_list[3]['token'],
                        'channel_id': channel_list[0]['channel_id'],
                        'message': "jack's message in pony's channel"})
    requests.post(config.url + 'message/send/v2',
                  json={'token': reg_list[1]['token'],
                        'channel_id': channel_list[1]['channel_id'],
                        'message': "pony2's message in jack's channel"})
    for user in reg_list:
        requests.post(config.url + 'auth/logout/v1',
                      json={'token': user['token']})
    return channel_list


@pytest.fixture(name='login_list')
def create_user_list():
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


@pytest.fixture(name='dm_dict')
def create_dm_list(reg_list):
    """ponyma create a dm"""
    u_ids = list()
    u_ids.append(reg_list[1]['auth_user_id'])
    u_ids.append(reg_list[2]['auth_user_id'])
    u_ids.append(reg_list[3]['auth_user_id'])
    dm_dict = requests.post(config.url + 'dm/create/v1',
                            json={'token': reg_list[0]['token'],
                                  'u_ids': u_ids}).json()
    return dm_dict


@pytest.mark.usefixtures("clear")
class TestClear:
    """
    Test for clear all the data

    Returns:
        N/A

    Raises:
        InputError: When a user can login after clear

    """

    def test_clear(self, reg_list):
        requests.post(config.url + 'auth/login/v2',
                      json={'email': 'pony.ma@qq.com',
                            'password': 'PonyMa'})
        requests.post(config.url + 'auth/login/v2',
                      json={'email': 'pony.ma2@qq.com',
                            'password': 'PonyMa'})
        requests.post(config.url + 'auth/login/v2',
                      json={'email': 'sundar.pichai@gmail.com',
                            'password': 'SundarPichai'})
        requests.post(config.url + 'auth/login/v2',
                      json={'email': 'jack.smith@hotmail.com',
                            'password': 'JackSmith'})
        requests.delete(config.url + 'clear/v1', json={})
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'pony.ma@qq.com',
                                     'password': 'PonyMa'})
        result.status_code = InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'pony.ma2@qq.com',
                                     'password': 'PonyMa'})
        result.status_code = InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'sundar.pichai@gmail.com',
                                     'password': 'SundarPichai'})
        result.status_code = InputError.code
        result = requests.post(config.url + 'auth/login/v2',
                               json={'email': 'jack.smith@hotmail.com',
                                     'password': 'JackSmith'})
        result.status_code = InputError.code


@pytest.mark.usefixtures("clear")
class TestSearch:
    """
    Test cases for search
    """
    def test_search(self, dm_dict, channel_list, login_list):
        """
        General test cases for search

        Args:
            dm_dict: dict contain pre-create direct message
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A

        """
        ret_list = json.loads(requests.get(config.url + 'search/v2',
                                           params={'token': login_list[1]['token'],
                                                   'query_str': "pony2"}).text)
        assert len(ret_list['messages']) == 2
        requests.post(config.url + 'message/senddm/v1',
                      json={'token': login_list[0]['token'],
                            'dm_id': dm_dict['dm_id'],
                            'message': "dm message from ponyma0"})
        requests.post(config.url + 'message/senddm/v1',
                      json={'token': login_list[2]['token'],
                            'dm_id': dm_dict['dm_id'],
                            'message': "dm message from sunder"})
        ret_list = json.loads(requests.get(config.url + 'search/v2',
                                           params={'token': login_list[1]['token'],
                                                   'query_str': "dm message"}).text)
        assert len(ret_list['messages']) == 2

    def test_too_long_query(self, channel_list, login_list):
        """
        Test case that the query string is too long

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A

        """
        assert type(channel_list).__name__ == 'list'
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(1001)]
        too_long_str = ''.join(str_list)
        result = requests.get(config.url + 'search/v2',
                              params={'token': login_list[0]['token'],
                                      'query_str': too_long_str})
        assert result.status_code == InputError.code
        result = requests.get(config.url + 'search/v2',
                              params={'token': login_list[1]['token'],
                                      'query_str': too_long_str})
        assert result.status_code == InputError.code


@pytest.mark.usefixtures("clear")
class TestNotification:
    """
    Test cases for notification get
    """
    def test_notification(self, channel_list, login_list):
        """
        Test cases for notification in channel

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A


        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "@ponyma0 @sunderpichai"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[2]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "@ponyma0 @jacksmith"})
        result = json.loads(requests.get(config.url + 'notifications/get/v1',
                                         params={'token': login_list[1]['token']}).text)
        assert len(result['notifications']) == 4
        result = json.loads(requests.get(config.url + 'notifications/get/v1',
                                         params={'token': login_list[2]['token']}).text)
        assert len(result['notifications']) == 3
        result = json.loads(requests.get(config.url + 'notifications/get/v1',
                                         params={'token': login_list[3]['token']}).text)
        assert len(result['notifications']) == 2

    def test_dm_notification(self, dm_dict, login_list):
        """
        Test cases for notification in dm

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A


        """
        requests.post(config.url + 'message/senddm/v1',
                      json={'token': login_list[0]['token'],
                            'dm_id': dm_dict['dm_id'],
                            'message': "@ponyma0 @sunderpichai"})
        requests.post(config.url + 'message/senddm/v1',
                      json={'token': login_list[2]['token'],
                            'dm_id': dm_dict['dm_id'],
                            'message': "@ponyma0 @jacksmith"})
        result = json.loads(requests.get(config.url + 'notifications/get/v1',
                                         params={'token': login_list[1]['token']}).text)
        assert len(result['notifications']) == 3
        result = json.loads(requests.get(config.url + 'notifications/get/v1',
                                         params={'token': login_list[2]['token']}).text)
        assert len(result['notifications']) == 2
        result = json.loads(requests.get(config.url + 'notifications/get/v1',
                                         params={'token': login_list[3]['token']}).text)
        assert len(result['notifications']) == 2
