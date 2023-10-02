import pytest
import random
import string

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.channel import channel_invite_v2, channel_messages_v2, channel_addowner_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.message import message_send_v2, message_share_v1, message_edit_v2, message_remove_v1, message_senddm_v1
from src.other import clear_v1
from src.dm import dm_create_v1, dm_messages_v1


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
    """
    Fixture function, is to pre-create channel for further tests

    Returns:
        channel_list: Dict, contain the pre-create channels' information

    """
    channel_list = list()
    channel_list.append(channels_create_v2(reg_list[0]['token'], "pony's channel", is_public=True))
    channel_list.append(channels_create_v2(reg_list[3]['token'], "jack's channel", is_public=False))
    channel_list.append(channels_create_v2(reg_list[2]['token'], "sunder's channel", is_public=True))
    channel_invite_v2(reg_list[0]['token'], channel_list[0]['channel_id'], reg_list[1]['auth_user_id'])
    channel_invite_v2(reg_list[0]['token'], channel_list[0]['channel_id'], reg_list[2]['auth_user_id'])
    channel_invite_v2(reg_list[0]['token'], channel_list[0]['channel_id'], reg_list[3]['auth_user_id'])
    channel_invite_v2(reg_list[3]['token'], channel_list[1]['channel_id'], reg_list[1]['auth_user_id'])
    channel_invite_v2(reg_list[3]['token'], channel_list[1]['channel_id'], reg_list[2]['auth_user_id'])
    for user in reg_list:
        auth_logout_v1(user['token'])
    return channel_list


@pytest.fixture(name='login_list')
def create_user_list():
    """
    Fixture function, is to pre-login for further tests

    Returns:
        login_list: Dict, contain the pre-login users' information

    """
    login_list = list()
    login_list.append(auth_login_v2("pony.ma@qq.com", "PonyMa"))
    login_list.append(auth_login_v2("pony.ma2@qq.com", "PonyMa"))
    login_list.append(auth_login_v2("sundar.pichai@gmail.com", "SundarPichai"))
    login_list.append(auth_login_v2("jack.smith@hotmail.com", "JackSmith"))
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
        ret_list.append(message_send_v2(login_list[0]['token'], channel_list[0]['channel_id'], 'message from Pony'))
        ret_list.append(message_send_v2(login_list[1]['token'], channel_list[0]['channel_id'], 'message from Pony'))
        ret_list.append(message_send_v2(login_list[2]['token'], channel_list[0]['channel_id'], 'message from Sundar'))
        ret_list.append(message_send_v2(login_list[3]['token'], channel_list[0]['channel_id'], 'message from Jack'))
        ret_list.append(message_send_v2(login_list[2]['token'], channel_list[1]['channel_id'], 'message from Jack'))
        ret_list.append(message_send_v2(login_list[3]['token'], channel_list[1]['channel_id'], 'message from Jack'))
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
        with pytest.raises(InputError):
            assert message_send_v2(login_list[0]['token'], channel_list[0]['channel_id'], too_long_str)
        with pytest.raises(InputError):
            assert message_send_v2(login_list[1]['token'], channel_list[0]['channel_id'], too_long_str)

    def test_user_not_join(self, channel_list, login_list):
        """
        Test cases for authorised user haven't join the channel

        Args:
            channel_list: list contain pre-create channels
            login_list: list contain pre-login users

        Returns:
            N/A

        """
        with pytest.raises(AccessError):
            assert message_send_v2(login_list[0]['token'], channel_list[1]['channel_id'], 'message from Pony')
        with pytest.raises(AccessError):
            assert message_send_v2(login_list[1]['token'], channel_list[2]['channel_id'], 'message from Pony')
        with pytest.raises(AccessError):
            assert message_send_v2(login_list[3]['token'], channel_list[2]['channel_id'], 'message from Pony')


@pytest.fixture(name="users")
def create_users():
    """Create different users and store their id in a list."""
    users = list()
    users.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    users.append(auth_register_v2("pony.ma@qqqw.com", "PonyMa", "Pony", "Ma"))
    users.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    users.append(auth_register_v2("joyceliu@qq.com", "JoyceLiu", "Joyce", "Liu"))

    '''
    auth_logout_v1(user1['token'])
    auth_logout_v1(user2['token']) 
    auth_logout_v1(user3['token'])
    auth_logout_v1(user4['token']) 
    '''

    return users


@pytest.fixture(name="channel_id")
def users_setup(users):
    """User01 creates one public channel"""
    user1 = auth_login_v2("pony.ma@qq.com", "PonyMa")
    channel1 = channels_create_v2(user1["token"], "Channel1", True)
    auth_logout_v1(user1['token'])
    return channel1['channel_id']


@pytest.fixture(name="dm1")
def dm_setup():
    """User1 creates a dm and it directes to user4"""
    user1 = auth_login_v2("pony.ma@qq.com","PonyMa")
    user4 = auth_login_v2("joyceliu@qq.com","JoyceLiu")
    u_id = list()
    u_id.append(user4["auth_user_id"])
    dm1 = dm_create_v1(user1["token"], u_id)
    auth_logout_v1(user1['token'])
    auth_logout_v1(user4['token'])
    return dm1


@pytest.mark.usefixtures("clear")
class TestMessageEdit:
    """

    This class contains a series of tests
    for the "message_edit" function.

    """
    def test_message_edit_channel(self, users, channel_id):
        """

        Test message_edit in channel.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        msg = message_send_v2(users[2]["token"], channel_id, "message2")
        with pytest.raises(AccessError):
            message_edit_v2(users[1]['token'], msg['message_id'], "message0")
        channel_addowner_v1(users[0]['token'], channel_id, users[1]['auth_user_id'])
        message_edit_v2(users[1]['token'], msg['message_id'], "message1")
        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "message1"
        message_edit_v2(users[2]['token'], msg['message_id'], "message2")
        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "message2"
        message_edit_v2(users[0]["token"], msg['message_id'], "message0")

        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "message0"

    def test_message_edit_dm(self, users, dm1):
        msg = message_senddm_v1(users[0]["token"], dm1["dm_id"], "message1")
        message_edit_v2(users[0]["token"], msg['message_id'], "message2")

        message = dm_messages_v1(users[0]["token"], dm1["dm_id"], 0)
        assert message['messages'][0]['message'] == "message2"

    def test_message_edit_empty(self, users, channel_id):
        """

        Test message_edit with empty new message

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        msg = message_send_v2(users[0]["token"], channel_id, "message2")
        message_edit_v2(users[0]["token"], msg['message_id'], "")

        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "message1"

    def test_message_edit_length(self, users, channel_id):
        """

        Test message_edit with too long message.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        msg = message_send_v2(users[0]["token"], channel_id, "message1")
        with pytest.raises(InputError):
            message_edit_v2(users[0]["token"], msg['message_id'], 'a' * 10000)

    def test_message_edit_invalid_message_id(self, users, channel_id):
        """

        Test message_edit with invalid message_id.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        with pytest.raises(InputError):
            message_edit_v2(users[0]["token"], -1, "message2")

    def test_message_edit_invalid_user(self, users, channel_id):
        """

        Test message_edit with invalid user.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        msg = message_send_v2(users[0]["token"], channel_id, "message1")

        with pytest.raises(AccessError):
            message_edit_v2(users[2]["token"], msg['message_id'], "message2")


@pytest.mark.usefixtures("clear")
class TestRemove:
    """

    This class contains a series of tests
    for the "message_remove" function.

    """
    def test_message_remove_channel(self, users, channel_id):
        """

        Test message_remove.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")

        msg = message_send_v2(users[2]["token"], channel_id, "message2")

        message_remove_v1(users[2]["token"], msg['message_id'])
        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "message1"

    def test_message_remove_dm(self, users, dm1):
        message_senddm_v1(users[0]["token"], dm1["dm_id"], "message1")
        msg = message_senddm_v1(users[3]["token"], dm1["dm_id"], "message2")
        message_remove_v1(users[3]["token"], msg['message_id'])
        message = dm_messages_v1(users[0]["token"], dm1["dm_id"], 0)
        assert message['messages'][0]['message'] == "message1"


    def test_message_remove_invalid_message_id(self, users, channel_id):
        """

        Test message_remove with invalid message_id.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        with pytest.raises(InputError):
            message_remove_v1(users[0]["token"], -1)

    def test_message_remove_invalid_user(self, users, channel_id):
        """

        Test message_remove with invalid user.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        msg = message_send_v2(users[0]["token"], channel_id, "message1")
        with pytest.raises(AccessError):
            message_remove_v1(users[2]["token"], msg['message_id'])


@pytest.mark.usefixtures("clear")
class TestShare:
    """

    This class contains a series of tests
    for the "messages_share" function.

    """
    def test_message_share_channel_to_channel(self, users, channel_id):
        """

        Test message_share.

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        msg = message_send_v2(users[0]["token"], channel_id, "message1")

        message_share_v1(users[0]["token"], msg["message_id"], '', channel_id, -1)
        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "\n\"\"\"\nmessage1\n\"\"\""
        assert message['messages'][1]['message'] == "message1"

    def test_message_share_dm(self, users, dm1):
        msg = message_senddm_v1(users[0]["token"], dm1["dm_id"], "message1")

        message_share_v1(users[0]["token"], msg["message_id"], '', -1, dm1["dm_id"])
        message = dm_messages_v1(users[0]["token"], dm1["dm_id"], 0)
        assert message['messages'][0]['message'] == "\n\"\"\"\nmessage1\n\"\"\""
        assert message['messages'][1]['message'] == "message1"


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


@pytest.fixture(name='info')
def one_user_create_dm():
    dict_list = create_dict_list()
    """User01 logs in"""
    User01 = auth_login_v2("pony.ma@qq.com", "PonyMa")
    """User01 create a dm"""
    u_id = list()
    u_id.append(dict_list[1]['auth_user_id'])
    u_id.append(dict_list[2]['auth_user_id'])
    u_id.append(dict_list[3]['auth_user_id'])
    dm_info = dm_create_v1(User01['token'], u_id)
    return {
        'token': User01['token'],
        'u_id': User01['auth_user_id'],
        'dm_id': dm_info['dm_id'],
        'dm_name': dm_info['dm_name']
    }


@pytest.mark.usefixtures("clear")
class Test_message_send_dm:
    def test_message_send_dm_success(self, info):
        """User01 sends a message to the dm"""
        m_id = message_senddm_v1(info['token'], info['dm_id'], 'Success message')['message_id']
        assert type(m_id).__name__ == 'int'

    def test_message_send_dm_invalid(self, info):
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(1001)]
        too_long_str = ''.join(str_list)
        """A new user registers"""
        token = auth_register_v2("FakeHayden@qq.com", "Hayden", "Hayden", "Hayden")['token']
        '''The new user tries to send a message to exiting dm'''
        with pytest.raises(AccessError):
            message_senddm_v1(token, info['dm_id'], 'Failed message')
        '''The dm create tries to send An extremely long message'''
        with pytest.raises(InputError):
            message_senddm_v1(info['token'], info['dm_id'], too_long_str)
