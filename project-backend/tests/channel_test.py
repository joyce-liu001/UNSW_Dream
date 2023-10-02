from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.channel import channel_addowner_v1, channel_removeowner_v1, channel_invite_v2, channel_details_v2, channel_leave_v1, channel_join_v2, channel_messages_v2
from src.channels import channels_create_v2, channels_list_v2
from src.message import message_send_v2
from src.other import clear_v1
from src.error import InputError, AccessError
import pytest


@pytest.fixture()
def clear():
    clear_v1()


@pytest.fixture(name='user_list')
def create_user_list():
    """
    Fixture function, is to pre-register four users for further tests

    Returns:
        user_list: Dict, contain the pre-register users' information

    """
    user_list = list()
    user_list.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    user_list.append(auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma"))
    user_list.append(auth_register_v2("sundar.pichai@gmail.com", "SundarPichai",
                                      "Sunder", "Pichai"))
    user_list.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    return user_list


@pytest.fixture(name='channel_list')
def create_channel_list():
    """
    Fixture function, is to pre-create some channels for further testing

    Returns:
        dict_list: Dict, contain the pre-register channel's information

    """
    channel_list = list()
    token = auth_login_v2("pony.ma@qq.com", "PonyMa")['token']
    channel_list.append(channels_create_v2(token, "Pony's channel", is_public=True))
    auth_logout_v1(token)
    token = auth_login_v2("pony.ma2@qq.com", "PonyMa")['token']
    channel_list.append(channels_create_v2(token, "Pony2's channel", is_public=True))
    auth_logout_v1(token)
    token = auth_login_v2("sundar.pichai@gmail.com", "SundarPichai")['token']
    channel_list.append(channels_create_v2(token, "Sundar's channel", is_public=False))
    auth_logout_v1(token)
    token = auth_login_v2("jack.smith@hotmail.com", "JackSmith")['token']
    channel_list.append(channels_create_v2(token, "Jack's channel", is_public=False))
    auth_logout_v1(token)
    return channel_list


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
        # Test whether Dream owner can add others to become other channel's owner
        assert channel_addowner_v1(user_list[0]['token'], channel_list[1]['channel_id'],
                                   user_list[3]['auth_user_id']) == {}
        # Test whether Dream owner can add himself to become other channel's owner
        assert channel_addowner_v1(user_list[0]['token'], channel_list[1]['channel_id'],
                                   user_list[0]['auth_user_id']) == {}
        # Test whether channel owner can add others to become this channel's owner
        assert channel_addowner_v1(user_list[1]['token'], channel_list[1]['channel_id'],
                                   user_list[2]['auth_user_id']) == {}
        assert channel_addowner_v1(user_list[2]['token'], channel_list[2]['channel_id'],
                                   user_list[3]['auth_user_id']) == {}
        assert len(channel_details_v2(user_list[0]['token'], channel_list[0]['channel_id'])['owner_members']) == 1
        assert len(channel_details_v2(user_list[1]['token'], channel_list[1]['channel_id'])['owner_members']) == 4
        assert len(channel_details_v2(user_list[2]['token'], channel_list[2]['channel_id'])['owner_members']) == 2

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
        with pytest.raises(InputError):
            assert channel_addowner_v1(user_list[0]['token'], invalid_id,
                                       user_list[0]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_addowner_v1(user_list[0]['token'], invalid_id,
                                       user_list[1]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_addowner_v1(user_list[0]['token'], invalid_id,
                                       user_list[2]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_addowner_v1(user_list[0]['token'], invalid_id,
                                       user_list[3]['auth_user_id'])

    def test_already_owner(self, user_list, channel_list):
        """
        Test cases with the user is already the owner of the channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        assert channel_addowner_v1(user_list[0]['token'], channel_list[1]['channel_id'],
                                   user_list[3]['auth_user_id']) == {}
        with pytest.raises(InputError):
            assert channel_addowner_v1(user_list[0]['token'], channel_list[1]['channel_id'],
                                       user_list[3]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_addowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                       user_list[0]['auth_user_id'])

    def test_not_owner(self, user_list, channel_list):
        """
        Test case for the authorised user is not an owner of channel/Dream

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        with pytest.raises(AccessError):
            assert channel_addowner_v1(user_list[1]['token'], channel_list[0]['channel_id'],
                                       user_list[1]['auth_user_id'])
        with pytest.raises(AccessError):
            assert channel_addowner_v1(user_list[1]['token'], channel_list[2]['channel_id'],
                                       user_list[3]['auth_user_id'])
        with pytest.raises(AccessError):
            assert channel_addowner_v1(user_list[1]['token'], channel_list[3]['channel_id'],
                                       user_list[2]['auth_user_id'])


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
        # Add all other user to become the first channel's owners
        assert channel_addowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                   user_list[1]['auth_user_id']) == {}
        assert channel_addowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                   user_list[2]['auth_user_id']) == {}
        assert channel_addowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                   user_list[3]['auth_user_id']) == {}
        assert len(channel_details_v2(user_list[0]['token'], channel_list[0]['channel_id'])['owner_members']) == 4
        assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                      user_list[1]['auth_user_id']) == {}
        assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                      user_list[2]['auth_user_id']) == {}
        assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                      user_list[3]['auth_user_id']) == {}
        assert len(channel_details_v2(user_list[0]['token'], channel_list[0]['channel_id'])['owner_members']) == 1

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
        assert channel_addowner_v1(user_list[0]['token'], channel_list[1]['channel_id'],
                                   user_list[0]['auth_user_id']) == {}
        assert channel_addowner_v1(user_list[0]['token'], channel_list[2]['channel_id'],
                                   user_list[0]['auth_user_id']) == {}
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], invalid_id,
                                          user_list[0]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], invalid_id,
                                          user_list[0]['auth_user_id'])

    def test_user_not_owner(self, user_list, channel_list):
        """
         Test case for the user is not an owner of channel

         Args:
             user_list: pre-register users
             channel_list: pre-create channel

         Returns:
             N/A

         """
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                          user_list[1]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                          user_list[2]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                          user_list[3]['auth_user_id'])

    def test_user_user_only_owner(self, user_list, channel_list):
        """
        Test case for the user is the only owner of this channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                          user_list[0]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[1]['channel_id'],
                                          user_list[1]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[2]['channel_id'],
                                          user_list[2]['auth_user_id'])
        with pytest.raises(InputError):
            assert channel_removeowner_v1(user_list[0]['token'], channel_list[3]['channel_id'],
                                          user_list[3]['auth_user_id'])

    def test_not_owner(self, user_list, channel_list):
        """
          Test case for the authorised user is not an owner of channel/Dream

          Args:
              user_list: pre-register users
              channel_list: pre-create channel

          Returns:
              N/A

          """
        assert channel_addowner_v1(user_list[0]['token'], channel_list[0]['channel_id'],
                                   user_list[1]['auth_user_id']) == {}
        with pytest.raises(AccessError):
            assert channel_removeowner_v1(user_list[2]['token'], channel_list[0]['channel_id'],
                                          user_list[1]['auth_user_id'])
        with pytest.raises(AccessError):
            assert channel_removeowner_v1(user_list[3]['token'], channel_list[0]['channel_id'],
                                          user_list[1]['auth_user_id'])


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
        channel_invite_v2(user_list[0]['token'], channel_list[0]['channel_id'], user_list[1]['auth_user_id'])
        channel_invite_v2(user_list[0]['token'], channel_list[0]['channel_id'], user_list[2]['auth_user_id'])
        channel_invite_v2(user_list[0]['token'], channel_list[0]['channel_id'], user_list[3]['auth_user_id'])
        pre_end = channel_messages_v2(user_list[0]['token'], channel_list[0]['channel_id'], 0)['end']
        assert channel_leave_v1(user_list[1]['token'], channel_list[0]['channel_id']) == {}
        assert channel_leave_v1(user_list[2]['token'], channel_list[0]['channel_id']) == {}
        assert channel_leave_v1(user_list[3]['token'], channel_list[0]['channel_id']) == {}
        # Check whether the number of message is the same after they leave
        assert channel_messages_v2(user_list[0]['token'], channel_list[0]['channel_id'], 0)['end'] == pre_end

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
        with pytest.raises(InputError):
            assert channel_leave_v1(user_list[0]['token'], invalid_id)
        with pytest.raises(InputError):
            assert channel_leave_v1(user_list[1]['token'], invalid_id)

    def test_not_member(self, user_list, channel_list):
        """
        Test case for the user is not the member of this channel

        Args:
            user_list: pre-register users
            channel_list: pre-create channel

        Returns:
            N/A

        """
        with pytest.raises(AccessError):
            assert channel_leave_v1(user_list[0]['token'], channel_list[3]['channel_id'])
        with pytest.raises(AccessError):
            assert channel_leave_v1(user_list[1]['token'], channel_list[0]['channel_id'])
        with pytest.raises(AccessError):
            assert channel_leave_v1(user_list[2]['token'], channel_list[1]['channel_id'])
        with pytest.raises(AccessError):
            assert channel_leave_v1(user_list[3]['token'], channel_list[2]['channel_id'])


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
    def test_channel_invalid_id(self, user_list):
        """

        Test whether channel_join can raise an error.
        Given an invalid id of the channel,
        channel_join function should raise an InputError.

        Args:
            N/A

        Returns:
            N/A

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_channel = channels_create_v2(result_user["token"], 'valid_channel_name', True)
        # obtain an unused channel_id, which is invalid id.
        for unuse_cid in range(0, 1000):
            if unuse_cid != result_channel['channel_id']:
                break
        # if InputError raised, test pass.
        with pytest.raises(InputError):
            assert channel_join_v2(result_user["token"], unuse_cid)

    def test_invalid_u_id(self, user_list):
        """

        Test channel/join/v2 when the u_id does not refer to a valid user.

        """
        result_user = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # create a channel
        result_channel = channels_create_v2(result_user["token"], 'valid_channel_name', True)
        # get a unused u_id
        for unuse_uid in range(0, 10000):
            if unuse_uid != result_user["token"]:
                break
        # should raise an AccessError
        with pytest.raises(AccessError):
            assert channel_join_v2(unuse_uid, result_channel['channel_id'])

    def test_valid_channel_id(self, user_list):
        """

        Test whether channel_join can succeed
        if the channel_id is valid.

        Args:
            N/A

        Returns:
            N/A

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('sundar.pichai@gmail.com', 'SundarPichai')
        # create a channel
        result_channel = channels_create_v2(result_user1['token'], 'valid_channel_name', True)
        channel_join_v2(result_user2["token"], result_channel['channel_id'])
        # using "channels_list_v2" to obtain all the channels' detail
        user2_channels_list = channels_list_v2(result_user2["token"])['channels']
        join_success = False
        for channel in user2_channels_list:
            # if the target channel_id is valid, join_success will be True
            if channel['channel_id'] == result_channel['channel_id']:
                # once the channel_id is valid, break
                join_success = True
                break
        assert join_success == True


    def test_join_private_fail(self, user_list):
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
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('sundar.pichai@gmail.com', 'SundarPichai')
        # create a private channel
        result_channel = channels_create_v2(result_user1["token"], 'valid_channel_name', False)
        # AccessError should be raised, because Sundar does not have permission.
        with pytest.raises(AccessError):
            assert channel_join_v2(result_user2['token'], result_channel['channel_id'])

    def test_join_private_success(self, user_list):
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
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('sundar.pichai@gmail.com', 'SundarPichai')
        result_channel = channels_create_v2(result_user2['token'], 'valid_channel_name', False)
        channel_join_v2(result_user1["token"], result_channel['channel_id'])
        # using "channels_list_v2" to obtain all the channels' detail
        user1_channels_list = channels_list_v2(result_user1["token"])['channels']

        join_success = False
        # if the target channel_id is valid, join_success will be True
        for channel in user1_channels_list:
            if channel['channel_id'] == result_channel['channel_id']:
                # once the channel_id is valid, break
                join_success = True
                break
        assert join_success == True

    def test_join_exist_user(self, user_list):
        """

        Test whether the same user will appear more than once in 'owner_members'
        if we join the same user twice.

        Args:
            N/A

        Returns:
            N/A

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        result_channel = channels_create_v2(result_user1["token"], 'valid_channel_name', True)
        # join same user twice
        channel_join_v2(result_user2["token"], result_channel["channel_id"])
        channel_join_v2(result_user2["token"], result_channel["channel_id"])
        # obtain channel's dict
        channels_dict = channel_details_v2(result_user2["token"], result_channel["channel_id"])
        # record the number of times the same user appears
        same_member = 0
        for member_id in channels_dict['all_members']:
            if member_id['u_id'] == result_user2["auth_user_id"]:
                same_member += 1

        # if user appears more than once, test fails
        assert same_member == 1


@pytest.fixture(name="users")
def create_users():
    """Create different users and store their id in a list."""
    users = list()
    users.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    users.append(auth_register_v2("pony.ma@qqqw.com", "PonyMa", "Pony", "Ma"))
    users.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))

    return users
   
@pytest.fixture(name="channel_id")
def users_setup():
    """User1 creates one public channel"""
    user1 = auth_login_v2("pony.ma@qq.com","PonyMa")
    channel1 = channels_create_v2(user1["token"], "Channel1", True)
    auth_logout_v1(user1['token'])
    return channel1['channel_id']


@pytest.mark.usefixtures("clear")
class TestChannelInvite:
    def test_invalid_channel_id(self, users):
        """Test channel_invite_v2 when the channel_id does not refer to a valid channel."""
        with pytest.raises(InputError):
            channel_invite_v2(users[0]["token"], -1, users[1]["auth_user_id"])

    def test_invalid_u_id(self, users, channel_id):
        """Test channel_invite_v2 when the u_id does not refer to a valid user."""
        with pytest.raises(InputError):
            channel_invite_v2(users[0]["token"], channel_id, -1)

    def test_author_not_member_fail(self, users):
        """Test channel_invite_v2 when the authorised user is not already a member of the channel."""
        channel2 = channels_create_v2(users[2]["token"], "Channel2", True)
        with pytest.raises(AccessError):
            channel_invite_v2(users[0]["token"], channel2["channel_id"], users[1]["auth_user_id"])
    
    def test_successful_channel_id(self, users, channel_id):
        """Test channel/invite/v2 can succeffully invite user or not."""
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])
        assert len(channel_details_v2(users[0]["token"], channel_id)['all_members']) == 2



@pytest.mark.usefixtures("clear")
class TestChannelDetail:

    def test_scenario1(self, users):
        """
        scenario 1 : user1 creates one public channel
        there is no one joins public one
        raise Inputerror if give a invalid channel ID.
        """
        with pytest.raises(InputError):
            channel_details_v2(users[0]["token"], -1)

    def test_scenario2(self, users, channel_id):
        """
        scenario 2 : user1 creates one public channel
        there is no one joins public one
        raise AccessError if give an authorised user is not a member of the channel.
        """
        with pytest.raises(AccessError):
            channel_details_v2(users[1]["token"], channel_id)

    def test_scenario3(self, users, channel_id):
        """
        scenario 3 : user1 creates one public channel
        there is no one joins public one then show the detail of the channel.
        """
        assert len(channel_details_v2(users[0]["token"], channel_id)['all_members']) == 1

    def test_scenario4(self, users, channel_id):
        """
        scenario 4 : user1 creates one public channel.
        user2 joins the public channel, show the detail of the channel.
        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])
        assert len(channel_details_v2(users[0]["token"], channel_id)['all_members']) == 2


@pytest.mark.usefixtures("clear")
class TestChannelMessage:
    """

    This class contains a series of tests
    for the "channel_messages" function.

    """
    def test_channel_message(self, users, channel_id):
        """

        Test channel_message.

        Args:
            N/A

        Returns:
            N/A

        """

        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        message_send_v2(users[0]["token"], channel_id, "message2")
        message_send_v2(users[0]["token"], channel_id, "message3")
        message_send_v2(users[0]["token"], channel_id, "message4")
        message_send_v2(users[0]["token"], channel_id, "message5")


        message = channel_messages_v2(users[0]["token"], channel_id, 0)
        assert message['messages'][0]['message'] == "message5"
        assert message['messages'][1]['message'] == "message4"
        assert message['messages'][2]['message'] == "message3"
        assert message['messages'][3]['message'] == "message2"
        assert message['messages'][4]['message'] == "message1"

    def test_channel_message_invalid_start(self, users, channel_id):
        """

        Test channel_message with invalid start

        Args:
            N/A

        Returns:
            N/A

        """

        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        message_send_v2(users[0]["token"], channel_id, "message2")
        message_send_v2(users[0]["token"], channel_id, "message3")
        message_send_v2(users[0]["token"], channel_id, "message4")
        message_send_v2(users[0]["token"], channel_id, "message5")

        with pytest.raises(InputError):
            channel_messages_v2(users[0]["token"], channel_id, 100)

    def test_channel_message_invalid_channel_id(self, users, channel_id):
        """

        Test channel_message with invalid channel_id

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        message_send_v2(users[0]["token"], channel_id, "message2")
        message_send_v2(users[0]["token"], channel_id, "message3")
        message_send_v2(users[0]["token"], channel_id, "message4")
        message_send_v2(users[0]["token"], channel_id, "message5")

        with pytest.raises(InputError):
            channel_messages_v2(users[0]["token"], -1, 0)

    def test_channel_message_invalid_users(self, users, channel_id):
        """

        Test channel_message with invalid user

        Args:
            N/A

        Returns:
            N/A

        """
        channel_invite_v2(users[0]["token"], channel_id, users[2]["auth_user_id"])

        message_send_v2(users[0]["token"], channel_id, "message1")
        message_send_v2(users[0]["token"], channel_id, "message2")
        message_send_v2(users[0]["token"], channel_id, "message3")
        message_send_v2(users[0]["token"], channel_id, "message4")
        message_send_v2(users[0]["token"], channel_id, "message5")

        with pytest.raises(AccessError):
            channel_messages_v2(users[1]["token"], channel_id, 0)
