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
    """
    Fixture function, is to pre-create channel for further tests

    Returns:
        channel_list: Dict, contain the pre-create channels' information

    """
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
    return channel_list


@pytest.fixture(name='login_list')
def create_user_list():
    """
    Fixture function, is to pre-login for further tests

    Returns:
        login_list: Dict, contain the pre-login users' information

    """
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
class TestSend:
    """
    Test cases for message send
    """
    def test_message_send(self, channel_list, login_list):
        """
        Test cases for general cases for message send

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A

        """
        ret_list = list()
        ret_list.append(requests.post(config.url + 'message/send/v2',
                                      json={'token': login_list[0]['token'],
                                            'channel_id': channel_list[0]['channel_id'],
                                            'message': "pony's message in pony's channel"}).json())
        ret_list.append(requests.post(config.url + 'message/send/v2',
                                      json={'token': login_list[1]['token'],
                                            'channel_id': channel_list[0]['channel_id'],
                                            'message': "pony2's message in pony's channel"}).json())
        ret_list.append(requests.post(config.url + 'message/send/v2',
                                      json={'token': login_list[2]['token'],
                                            'channel_id': channel_list[0]['channel_id'],
                                            'message': "sunder's message in pony's channel"}).json())
        ret_list.append(requests.post(config.url + 'message/send/v2',
                                      json={'token': login_list[3]['token'],
                                            'channel_id': channel_list[0]['channel_id'],
                                            'message': "jack's message in pony's channel"}).json())
        ret_list.append(requests.post(config.url + 'message/send/v2',
                                      json={'token': login_list[1]['token'],
                                            'channel_id': channel_list[1]['channel_id'],
                                            'message': "pony2's message in jack's channel"}).json())
        for ret_dict in ret_list:
            assert type(ret_dict).__name__ == 'dict'
            assert type(ret_dict['message_id']).__name__ == 'int'

    def test_too_long_message(self, channel_list, login_list):
        """
         Test cases for message is too long

         Args:
             channel_list: list contain pre-create channels
             login_list: list contain pre-login users

         Returns:
             N/A

         """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(1001)]
        too_long_str = ''.join(str_list)
        result = requests.post(config.url + 'message/send/v2',
                               json={'token': login_list[0]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'message': too_long_str})
        assert result.status_code == InputError.code
        result = requests.post(config.url + 'message/send/v2',
                               json={'token': login_list[1]['token'],
                                     'channel_id': channel_list[0]['channel_id'],
                                     'message': too_long_str})
        assert result.status_code == InputError.code

    def test_user_not_join(self, channel_list, login_list):
        """
         Test cases for authorised user haven't join the channel

         Args:
             channel_list: list contain pre-create channels
             login_list: list contain pre-login users

         Returns:
             N/A

         """
        result = requests.post(config.url + 'message/send/v2',
                               json={'token': login_list[0]['token'],
                                     'channel_id': channel_list[1]['channel_id'],
                                     'message': "message from Pony"})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'message/send/v2',
                               json={'token': login_list[1]['token'],
                                     'channel_id': channel_list[2]['channel_id'],
                                     'message': "message from Pony"})
        assert result.status_code == AccessError.code
        result = requests.post(config.url + 'message/send/v2',
                               json={'token': login_list[3]['token'],
                                     'channel_id': channel_list[2]['channel_id'],
                                     'message': "message from Pony"})
        assert result.status_code == AccessError.code


@pytest.mark.usefixtures("clear")
class TestMessageEdit:
    """

    This class contains a series of tests
    for the "message_edit" function.

    """

    def test_message_edit(self, channel_list, login_list):
        """

        Test message_edit.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()

        requests.put(config.url + 'message/edit/v2',
                     json={"token": login_list[0]["token"],
                           "message_id": message['message_id'],
                           "message": "message4"})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "message4"

    def test_message_edit_empty(self, channel_list, login_list):
        """

        Test message_edit with empty new message

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()

        requests.put(config.url + 'message/edit/v2',
                     json={"token": login_list[0]["token"],
                           "message_id": message['message_id'],
                           "message": ""})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "message1"

    def test_message_edit_invalid_user(self, channel_list, login_list):
        """

        Test message_edit with invalid user.

        Args:
            N/A

        Returns:
            N/A

        """
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message1"}).json()
        requests.put(config.url + 'message/edit/v2',
                              json={"token": login_list[2]["token"],
                                    "message_id": message['message_id'],
                                    "message": "message"})

    def test_message_edit_invalid_message(self, channel_list, login_list):
        """

        Test message_edit with too long message.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()

        result = requests.put(config.url + 'message/edit/v2',
                              json={"token": login_list[0]["token"],
                                    "message_id": message['message_id'],
                                    "message": "a" * 1500})
        assert result.status_code == InputError.code

    def test_message_edit_invalid_message_id(self, channel_list, login_list):
        """

        Test message_edit with invalid message_id.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message2"})

        result = requests.put(config.url + 'message/edit/v2',
                              json={"token": login_list[0]["token"],
                                    "message_id": -1,
                                    "message": "message3"})
        assert result.status_code == InputError.code


@pytest.mark.usefixtures("clear")
class TestMessageRemove:
    """

    This class contains a series of tests
    for the "message_remove" function.

    """

    def test_message_remove(self, channel_list, login_list):
        """

        Test message_remove.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()

        requests.delete(config.url + 'message/remove/v1',
                        json={"token": login_list[0]["token"],
                              "message_id": message['message_id']})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "message1"

    def test_message_remove_invalid_message_id(self, channel_list, login_list):
        """

        Test message_remove with invalid message_id.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message2"})
        result = requests.delete(config.url + 'message/remove/v1',
                                 json={"token": login_list[0]["token"],
                                       "message_id": -1})
        assert result.status_code == InputError.code

    def test_message_remove_invalid_user(self, channel_list, login_list):
        """

        Test message_remove with invalid user.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()
        requests.delete(config.url + 'message/remove/v1',
                                 json={"token": login_list[2]["token"],
                                       "message_id": message['message_id']})


@pytest.mark.usefixtures("clear")
class TestMessageShare:
    """

    This class contains a series of tests
    for the "messages_share" function.

    """

    def test_message_share(self, channel_list, login_list):
        """

        Test message_share.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()
        requests.post(config.url + 'message/share/v1',
                      json={'token': login_list[0]['token'],
                            'og_message_id': message['message_id'],
                            'message': "message",
                            'channel_id': channel_list[0]['channel_id'],
                            'dm_id': -1})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "message\n\"\"\"\nmessage2\n\"\"\""

    def test_message_share_empty(self, channel_list, login_list):
        """

        Test message_share with empty message.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()
        requests.post(config.url + 'message/share/v1',
                      json={'token': login_list[0]['token'],
                            'og_message_id': message['message_id'],
                            'message': "",
                            'channel_id': channel_list[0]['channel_id'],
                            'dm_id': -1})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "\n\"\"\"\nmessage2\n\"\"\""

    def test_message_share_twice(self, channel_list, login_list):
        """

        Test message_share with share a message which has been shared before.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()
        message2 = requests.post(config.url + 'message/share/v1',
                                 json={'token': login_list[0]['token'],
                                       'og_message_id': message['message_id'],
                                       'message': "",
                                       'channel_id': channel_list[0]['channel_id'],
                                       'dm_id': -1}).json()
        requests.post(config.url + 'message/share/v1',
                      json={'token': login_list[0]['token'],
                            'og_message_id': message2['shared_message_id'],
                            'message': "",
                            'channel_id': channel_list[0]['channel_id'],
                            'dm_id': -1})
        result = json.loads(requests.get(config.url + 'channel/messages/v2',
                                         params={'token': login_list[0]['token'],
                                                 'channel_id': channel_list[0]['channel_id'],
                                                 'start': 0}).text)
        assert result['messages'][0]['message'] == "\n\"\"\"\n\n\t\"\"\"\n\tmessage2\n\t\"\"\"\n\"\"\""

    def test_message_share_invalid_user(self, channel_list, login_list):
        """

        Test message_share with invalid user.

        Args:
            N/A

        Returns:
            N/A

        """
        requests.post(config.url + 'message/send/v2',
                      json={'token': login_list[0]['token'],
                            'channel_id': channel_list[0]['channel_id'],
                            'message': "message1"})
        message = requests.post(config.url + 'message/send/v2',
                                json={'token': login_list[0]['token'],
                                      'channel_id': channel_list[0]['channel_id'],
                                      'message': "message2"}).json()
        result = requests.post(config.url + 'message/share/v1',
                               json={'token': login_list[0]['token'],
                                     'og_message_id': message['message_id'],
                                     'message': "",
                                     'channel_id': channel_list[1]['channel_id'],
                                     'dm_id': -1})
        assert result.status_code == AccessError.code
