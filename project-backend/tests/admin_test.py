import pytest
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_create_v2, channels_list_v2
from src.channel import channel_join_v2, channel_messages_v2
from src.user import users_all_v1
from src.message import message_send_v2

@pytest.fixture()
def clear():
    clear_v1()

# Create a series of users
@pytest.fixture(name='dict_list')
def create_dict_list():
    dict_list = list()
    dict_list.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    dict_list.append(auth_register_v2("pony.ma2@qq.com", "PonyMa", "Pony", "Ma"))
    dict_list.append(auth_register_v2("sundar.pichai@gmail.com", "SundarPichai", \
        "Sunder", "Pichai"))
    dict_list.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    return dict_list


@pytest.mark.usefixtures("clear")
class TestUserRemove:
    """

    This class contains a series of tests
    for the "admin_user_remove" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_invalid_user_id(self, dict_list):
        """

        Test admin/user/remove/v1 when the u_id does not refer to a valid user.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # the target u_id is invalid
        # should raise InputError
        with pytest.raises(InputError):
            assert admin_user_remove_v1(result_user1['token'], -10)
    
    def test_only_one_owner(self, dict_list):
        """

        Test admin/user/remove/v1 when the target is the only one owner.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # the test should raise InputError, because the target is the only one owner
        with pytest.raises(InputError):
            assert admin_user_remove_v1(result_user1['token'], result_user1['auth_user_id'])
    
    def test_access_error(self, dict_list):
        """

        Test admin/user/remove/v1 when the target is the only one owner.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        result_user3 = auth_login_v2('sundar.pichai@gmail.com', 'SundarPichai')
        # the test should raise AccessError, because the user does not hanve permission
        with pytest.raises(AccessError):
            assert admin_user_remove_v1(result_user2['token'], result_user1['auth_user_id'])
            assert admin_user_remove_v1(result_user2['token'], result_user3['auth_user_id'])

    def test_remove_success(self, dict_list):
        """

        Test whether admin_user_remove can succeed
        if all conditions are valid.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # remove user2
        admin_user_remove_v1(result_user1['token'], result_user2['auth_user_id'])
        # get the profile of all users
        users = users_all_v1(result_user1['token'])['users']

        found = False
        for user in users:
            # if the users' profile contain user2, found is True
            if user['u_id'] == result_user2['auth_user_id']:
                found = True
                break
        # users' profile shouldn't contain user2
        assert found == False
    
    def test_remove_owner_success(self, dict_list):
        """

        Test whether admin_user_remove can succeed
        if the target is dream owner.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # set user2 to dream owner
        admin_userpermission_change_v1(result_user1['token'], result_user2['auth_user_id'], 1)
        # remove another dream owner
        admin_user_remove_v1(result_user2['token'], result_user1['auth_user_id'])
        # get the profile of all users
        users = users_all_v1(result_user2['token'])['users']

        found = False
        for user in users:
            # if the users' profile contain user1, found is True
            if user['u_id'] == result_user1['auth_user_id']:
                found = True
                break
        # users' profile shouldn't contain user1
        assert found == False
    
    def test_removed_message(self, dict_list):
        """

        Test when admin_user_remove succeed,
        whether the old message is is reset to "Removed user".

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # create channel
        channel1 = channels_create_v2(result_user2['token'], 'channel1', True)
        channel_join_v2(result_user1['token'], channel1['channel_id'])
        # user2 send a message
        message_send_v2(result_user2['token'], channel1['channel_id'], 'TEST_MESSAGE')
        # user1 remove user2
        admin_user_remove_v1(result_user1['token'], result_user2['auth_user_id'])
        # get the message detail in channel1
        channel1_message = channel_messages_v2(result_user1['token'], channel1['channel_id'], 0)
        # the old message content should be "Removed user"
        assert channel1_message['messages'][0]['message'] == 'Removed user'


@pytest.mark.usefixtures("clear")
class TestUserPermissionChange:
    """

    This class contains a series of tests
    for the "admin_userpermission_change" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_invalid_permission_id(self, dict_list):
        """

        Test whether admin_userpermission_change can raise InputError
        if the permission_id is invalid.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # the test should raise InputError, because the permission id is invalid
        with pytest.raises(InputError):
            assert admin_userpermission_change_v1(result_user1['token'], result_user2['auth_user_id'], -1)

    def test_invalid_user_id(self, dict_list):
        """

        Test whether admin_userpermission_change can raise InputError
        if the target u_id is invalid.

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        # the test should raise InputError, because the target u_id is invalid
        with pytest.raises(InputError):
            assert admin_userpermission_change_v1(result_user1['token'], -10, 1)
    
    def test_access_error(self, dict_list):
        """

        Test whether admin_userpermission_change can raise AccessError

        """
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        result_user3 = auth_login_v2('sundar.pichai@gmail.com', 'SundarPichai')
        # the test should raisse AccessError, because the user doesn't have permission
        with pytest.raises(AccessError):
            assert admin_userpermission_change_v1(result_user2['token'], result_user3['auth_user_id'], 1)

    def test_change_success(self, dict_list):
        """

        Test whether admin_userpermission_change can succeed

        """
        result_user1 = auth_login_v2('pony.ma@qq.com', 'PonyMa')
        result_user2 = auth_login_v2('pony.ma2@qq.com', 'PonyMa')
        # create a private channel
        private_channel = channels_create_v2(result_user1['token'], 'private_channel', False)
        # set user2 to owner
        admin_userpermission_change_v1(result_user1['token'], result_user2['auth_user_id'], 1)
        # user2 join the private channel
        channel_join_v2(result_user2['token'], private_channel['channel_id'])
        # get the channel list
        user2_channel_list = channels_list_v2(result_user2['token'])

        join_success = False
        # if the target channel_id is valid, join_success will be True
        for channel in user2_channel_list['channels']:
            if channel['channel_id'] == private_channel['channel_id']:
                # once the channel_id is valid, break
                join_success = True
                break
        # user2 should join the private channel successfully
        assert join_success == True
