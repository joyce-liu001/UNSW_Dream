import pytest
import random
import string
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
    return channel_list


@pytest.mark.usefixtures("clear")
class TestCreate:
    """
    Tests for the function channels_create_v2
    """

    def test_channel_create(self, channel_list):
        """
        Test case for create normal channel

        Args:
            token: integer, the login user's auth_user_id

        Returns:
            N/A

        """
        for ret_dict in channel_list:
            # Check whether the return type is correct
            assert type(ret_dict).__name__ == "dict", "return type ==  dict"
            assert type(ret_dict["channel_id"]).__name__ == "int", "value type in dict == int"

    def test_channel_too_long_name(self, reg_list):
        """
        Test create channel with too long channel name

        Args:
            token: integer, the login user's auth_user_id

        Returns:
            N/A

        Raises:
            InputError: When the channel's name is too long

        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(1001)]
        too_long_name = ''.join(str_list)
        result = requests.post(config.url + 'channels/create/v2',
                               json={'token': reg_list[0]['token'],
                                     'name': too_long_name,
                                     'is_public': True})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'channels/create/v2',
                               json={'token': reg_list[1]['token'],
                                     'name': too_long_name,
                                     'is_public': True})
        assert result.status_code == InputError.code
