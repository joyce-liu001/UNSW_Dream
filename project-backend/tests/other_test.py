import pytest
import random
import string

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.channel import channel_invite_v2
from src.channels import channels_create_v2
from src.error import InputError
from src.message import message_send_v2, message_senddm_v1, message_edit_v2
from src.other import clear_v1, search_v2, notifications_get_v1
from src.dm import dm_create_v1



@pytest.fixture()
def clear():
    clear_v1()


@pytest.fixture(name='reg_list')
def create_reg_list():
    """
    Fixture function, is to pre-register four users for further tests

    Returns:
        reg_list: Dict, contain the pre-register users' information

    """
    reg_list = list()
    reg_list.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    reg_list.append(auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma"))
    reg_list.append(auth_register_v2("sundar.pichai@gmail.com", "SundarPichai",
                                     "Sunder", "Pichai"))
    reg_list.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    return reg_list


@pytest.fixture(name='channel_list')
def create_channel_list(reg_list):
    channel_list = list()
    channel_list.append(channels_create_v2(reg_list[0]['token'], "pony's channel", is_public=True))
    channel_list.append(channels_create_v2(reg_list[3]['token'], "jack's channel", is_public=False))
    channel_list.append(channels_create_v2(reg_list[2]['token'], "sunder's channel", is_public=True))
    channel_invite_v2(reg_list[0]['token'], channel_list[0]['channel_id'], reg_list[1]['auth_user_id'])
    channel_invite_v2(reg_list[0]['token'], channel_list[0]['channel_id'], reg_list[2]['auth_user_id'])
    channel_invite_v2(reg_list[0]['token'], channel_list[0]['channel_id'], reg_list[3]['auth_user_id'])
    channel_invite_v2(reg_list[3]['token'], channel_list[1]['channel_id'], reg_list[1]['auth_user_id'])
    channel_invite_v2(reg_list[3]['token'], channel_list[1]['channel_id'], reg_list[2]['auth_user_id'])
    message_send_v2(reg_list[0]['token'], channel_list[0]['channel_id'], "pony's message in pony's channel")
    message_send_v2(reg_list[1]['token'], channel_list[0]['channel_id'], "pony2's message in pony's channel")
    message_send_v2(reg_list[2]['token'], channel_list[0]['channel_id'], "sunder's message in pony's channel")
    message_send_v2(reg_list[3]['token'], channel_list[0]['channel_id'], "jack's message in pony's channel")
    message_send_v2(reg_list[1]['token'], channel_list[1]['channel_id'], "pony2's message in jack's channel")
    for user in reg_list:
        auth_logout_v1(user['token'])
    return channel_list


@pytest.fixture(name='login_list')
def create_user_list():
    login_list = list()
    login_list.append(auth_login_v2("pony.ma@qq.com", "PonyMa"))
    login_list.append(auth_login_v2("pony.ma2@qq.com", "PonyMa"))
    login_list.append(auth_login_v2("sundar.pichai@gmail.com", "SundarPichai"))
    login_list.append(auth_login_v2("jack.smith@hotmail.com", "JackSmith"))
    return login_list


@pytest.fixture(name='dm_dict')
def create_dm_list(reg_list):
    """ponyma create a dm"""
    u_id = list()
    u_id.append(reg_list[1]['auth_user_id'])
    u_id.append(reg_list[2]['auth_user_id'])
    u_id.append(reg_list[3]['auth_user_id'])
    dm_dict = dm_create_v1(reg_list[0]['token'], u_id)
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
        assert type(reg_list).__name__ == 'list'
        auth_login_v2("pony.ma@qq.com", "PonyMa")
        auth_login_v2("pony.ma2@qq.com", "PonyMa")
        auth_login_v2("sundar.pichai@gmail.com", "SundarPichai")
        auth_login_v2("jack.smith@hotmail.com", "JackSmith")
        clear_v1()
        with pytest.raises(InputError):
            auth_login_v2("pony.ma@qq.com", "PonyMa")
        with pytest.raises(InputError):
            auth_login_v2("pony.ma2@qq.com", "PonyMa")
        with pytest.raises(InputError):
            auth_login_v2("sundar.pichai@gmail.com", "SundarPichai")
        with pytest.raises(InputError):
            auth_login_v2("jack.smith@hotmail.com", "JackSmith")


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
        assert type(channel_list).__name__ == 'list'
        ret_list = search_v2(login_list[1]['token'], "pony2")['messages']
        assert len(ret_list) == 2
        for ret_dict in ret_list:
            assert type(ret_dict).__name__ == 'dict'
        message_senddm_v1(login_list[0]['token'], dm_dict['dm_id'], "dm message from ponyma0")
        message_senddm_v1(login_list[2]['token'], dm_dict['dm_id'], "dm message from sunder")
        ret_list = search_v2(login_list[1]['token'], "dm message")['messages']
        assert len(ret_list) == 2
        for ret_dict in ret_list:
            assert type(ret_dict).__name__ == 'dict'

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
        with pytest.raises(InputError):
            assert search_v2(login_list[0]['token'], too_long_str)
        with pytest.raises(InputError):
            assert search_v2(login_list[1]['token'], too_long_str)


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
        message_send_v2(login_list[0]['token'], channel_list[0]['channel_id'], "@ponyma0 @sunderpichai")
        message_send_v2(login_list[2]['token'], channel_list[0]['channel_id'], "@ponyma0 @jacksmith")
        assert len(notifications_get_v1(login_list[1]['token'])['notifications']) == 4
        assert len(notifications_get_v1(login_list[2]['token'])['notifications']) == 3
        assert len(notifications_get_v1(login_list[3]['token'])['notifications']) == 2

    def test_dm_notification(self, dm_dict, login_list):
        """
        Test cases for notification in dm

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A


        """
        message_senddm_v1(login_list[0]['token'], dm_dict['dm_id'], "@ponyma0 @sunderpichai")
        message_senddm_v1(login_list[2]['token'], dm_dict['dm_id'], "@ponyma0 @jacksmith")
        assert len(notifications_get_v1(login_list[1]['token'])['notifications']) == 3
        assert len(notifications_get_v1(login_list[2]['token'])['notifications']) == 2
        assert len(notifications_get_v1(login_list[3]['token'])['notifications']) == 2

    def test_edit_channel(self, channel_list, login_list):
        """
        Test cases for edit message and notification in channel

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A


        """
        id1 = message_send_v2(login_list[0]['token'], channel_list[0]['channel_id'], "original message")['message_id']
        id2 = message_send_v2(login_list[2]['token'], channel_list[0]['channel_id'], "original message")['message_id']
        assert len(notifications_get_v1(login_list[1]['token'])['notifications']) == 2
        assert len(notifications_get_v1(login_list[2]['token'])['notifications']) == 2
        assert len(notifications_get_v1(login_list[3]['token'])['notifications']) == 1
        message_edit_v2(login_list[0]['token'], id1, "@ponyma0 @sunderpichai")
        message_edit_v2(login_list[2]['token'], id2, "@ponyma0 @jacksmith")
        assert len(notifications_get_v1(login_list[1]['token'])['notifications']) == 4
        assert len(notifications_get_v1(login_list[2]['token'])['notifications']) == 3
        assert len(notifications_get_v1(login_list[3]['token'])['notifications']) == 2

    def test_edit_dm(self, dm_dict, login_list):
        """
        Test cases for edit message and notification in dm

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A


        """
        id1 = message_senddm_v1(login_list[0]['token'], dm_dict['dm_id'], "origin dm message")['message_id']
        id2 = message_senddm_v1(login_list[2]['token'], dm_dict['dm_id'], "origin dm message")['message_id']
        assert len(notifications_get_v1(login_list[1]['token'])['notifications']) == 1
        assert len(notifications_get_v1(login_list[2]['token'])['notifications']) == 1
        assert len(notifications_get_v1(login_list[3]['token'])['notifications']) == 1
        message_edit_v2(login_list[0]['token'], id1, "@ponyma0 @sunderpichai")
        message_edit_v2(login_list[2]['token'], id2, "@ponyma0 @jacksmith")
        assert len(notifications_get_v1(login_list[1]['token'])['notifications']) == 3
        assert len(notifications_get_v1(login_list[2]['token'])['notifications']) == 2
        assert len(notifications_get_v1(login_list[3]['token'])['notifications']) == 2
