import pytest
import random
import string

from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_create_v2, channels_listall_v2, channels_list_v2
from src.channel import channel_join_v2
from src.error import InputError
from src.other import clear_v1


@pytest.fixture()
def clear():
    clear_v1()


@pytest.fixture(name='user_list')
def create_user_list():
    user_list = list()
    user_list.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    user_list.append(auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma"))
    user_list.append(auth_register_v2("sundar.pichai@gmail.com", "SundarPichai",
                                      "Sunder", "Pichai"))
    user_list.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    return user_list


@pytest.fixture(name="token")
def user_initial():
    """
    Fixture function, is to pre-register and login user for further tests

    Returns:
        token: integer, the login user's auth_user_id

    """
    auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma")
    token_dict = auth_login_v2("pony.ma@qq.com", "PonyMa")
    return token_dict["token"]


@pytest.mark.usefixtures("clear")
class TestCreate:
    """
    Tests for the function channels_create_v2
    """
    def test_channel_create(self, token):
        """
        Test case for create normal channel

        Args:
            token: integer, the login user's auth_user_id

        Returns:
            N/A

        """
        dict_list = list()
        # Test deliberately with some same name channels
        dict_list.append(channels_create_v2(token, "Tencent", is_public=True))
        dict_list.append(channels_create_v2(token, "Tencent", is_public=True))
        dict_list.append(channels_create_v2(token, "Tencent", is_public=False))
        dict_list.append(channels_create_v2(token, "WeChat", is_public=False))
        id_list = list()
        for id_dict in dict_list:
            # Check whether the return type is correct
            assert type(id_dict).__name__ == "dict", "return type ==  dict"
            assert type(id_dict["channel_id"]).__name__ == "int", "value type in dict == int"
            id_list.append(id_dict["channel_id"])
        # Check whether each return id is unique
        assert len(id_list) == len(set(id_list))

    def test_channel_too_long_name(self, token):
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
        with pytest.raises(InputError):
            assert channels_create_v2(token, too_long_name, is_public=True)
        with pytest.raises(InputError):
            assert channels_create_v2(token, too_long_name, is_public=False)


@pytest.mark.usefixtures("clear")
class TestListall:
    """

    This class contains a series of tests
    for the "channel_listall" function.

    """
    def test_list_public_channel(self, user_list):
        """

        Test whether channel_listall can list channels correctly.
        Given a few public channels, channel_listall function should list channels correctly.

        Args:
            N/A

        Returns:
            N/A

        """
        channels_list = list()
        # login
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # create public channels
        pub_channel1 = channels_create_v2(result_user1['token'], 'valid_channel_name1', True)
        pub_channel2 = channels_create_v2(result_user2['token'], 'valid_channel_name2', True)
        # append channels into channels list
        channels_list.append(pub_channel1)
        channels_list.append(pub_channel2)
        # channels' detail should match
        assert channels_listall_v2(result_user1['token']) == {
            'channels': [
                {
                    'channel_id': channels_list[0]["channel_id"],
                    'name': 'valid_channel_name1'
                },
                {
                    'channel_id': channels_list[1]["channel_id"],
                    'name': 'valid_channel_name2'
                }
            ]
        }

    def test_list_mix_channel(self, user_list):
        """

        Test whether channel_listall can list channels correctly.
        Given a few public and private channels, channel_listall function
        should list all the channels correctly.
        
        Args:
            N/A

        Returns:
            N/A

        """
        channels_list = list()
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # create public and private channels
        pub_channel1 = channels_create_v2(result_user1['token'], 'valid_channel_name1', True)
        pub_channel2 = channels_create_v2(result_user2['token'], 'valid_channel_name2', True)
        pri_channel = channels_create_v2(result_user1['token'], 'valid_channel_name3', False)
        # append channels into channels list
        channels_list.append(pub_channel1)
        channels_list.append(pub_channel2)
        channels_list.append(pri_channel)
        # channels' detail should match
        assert channels_listall_v2(result_user1['token']) == {
            'channels': [
                {
                    'channel_id': channels_list[0]["channel_id"],
                    'name': 'valid_channel_name1'
                },
                {
                    'channel_id': channels_list[1]["channel_id"],
                    'name': 'valid_channel_name2'
                },
                {
                    'channel_id': channels_list[2]["channel_id"],
                    'name': 'valid_channel_name3'
                }
            ]
        }


@pytest.fixture(name="users")
def create_users(clear):
    """ register different users

        Args:
              clear all data in database

        Returns:
              N/A
    """
    auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma")
    auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma")
    auth_register_v2("sundar.pichai@gmail.com", "SundarPichai", "Sunder", "Pichai")
    auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith")


@pytest.fixture(name="user01_info")
def users_setup(clear):
    """ user01 creates one public channel and one private channel

        Args:
              clear all data in database

        Returns:
              a tuple that contains information about user01
    """
    user_info = list()
    user_info.append(auth_login_v2("pony.ma@qq.com", "PonyMa")["token"])
    user_info.append(channels_create_v2(user_info[0], "Channel1", True)['channel_id'])
    user_info.append(channels_create_v2(user_info[0], "Channel2", False)['channel_id'])

    return tuple(user_info)


@pytest.mark.usefixtures("clear")
@pytest.mark.usefixtures("users")
class TestChannelList:

    def test_scenario1(self, user01_info):
        """
        scenario1 : user01 creates one public channel and one private channel
        there is no one who joins public one
        check if the list contains 2 channels

        Args:
              user01_info:a tuple that contains auth_id, public_channel_id, private_channel_id

        Returns:
              N/A

        """
        token = auth_login_v2("pony.ma@qq.com", "PonyMa")["token"]
        _, pub_channel_id, pri_channel_id = user01_info
        assert channels_list_v2(token) == {
            'channels': [
                {
                    'channel_id': pub_channel_id,
                    'name': 'Channel1'
                },
                {
                    'channel_id': pri_channel_id,
                    'name': 'Channel2'
                }
            ]
        }

    def test_scenario2(self, user01_info):
        """
        scenario2 : user01 creates one public channel and one private channel
        user02 joins the public one
        check if list(user02 joins) only contains 'Channel1

        Args:
              user01_info:a tuple that contains auth_id, public_channel_id, private_channel_id

        Returns:
              N/A

        """
        token = auth_login_v2("pony.ma2@qq.com", "PonyMa")["token"]
        _, pub_channel_id, _ = user01_info
        channel_join_v2(token, pub_channel_id)
        assert channels_list_v2(token) == {
            'channels': [
                {
                    'channel_id': pub_channel_id,
                    'name': 'Channel1'
                }
            ]
        }

    def test_scenario3(self, user01_info):
        """
        scenario3: user01 creates one public channel and one private channel
        user03 did not join any channels
        check if list(user03) contains no channel

        Args:
              user01_info:a tuple that contains auth_id, public_channel_id, private_channel_id

        Returns:
              N/A

        """
        token = auth_login_v2("sundar.pichai@gmail.com", "SundarPichai")['token']
        assert channels_list_v2(token) == {
            'channels': []
        }

