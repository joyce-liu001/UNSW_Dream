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
class TestUserRemove:
    """

    This class contains a series of tests
    for the "admin_user_remove" function.

    Args:
            N/A

        Returns:
            N/A

    """
    def test_invalid_user_id(self, users):
        """

        Test admin/user/remove/v1 when the u_id does not refer to a valid user.

        """
        resp = requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[0]['token'],
            'u_id': -10,
        })
        # the target u_id is invalid
        # should raise InputError
        assert resp.status_code == InputError.code

    def test_only_one_owner(self, users):
        """

        Test admin/user/remove/v1 when the target is the only one owner.

        """
        resp = requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[0]['token'],
            'u_id': users[0]['auth_user_id'],
        })
        # the test should raise InputError, because the target is the only one owner
        assert resp.status_code == InputError.code
    
    def test_access_error(self, users):
        """

        Test admin/user/remove/v1 when the target is the only one owner.

        """
        resp = requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[1]['token'],
            'u_id': users[0]['auth_user_id'],
        })
        # the test should raise AccessError, because the user does not hanve permission
        assert resp.status_code == AccessError.code

        resp = requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[1]['token'],
            'u_id': users[2]['auth_user_id'],
        })
        # the test should raise AccessError, because the user does not hanve permission
        assert resp.status_code == AccessError.code

    def test_remove_success(self, users):
        """

        Test whether admin_user_remove can succeed
        if all conditions are valid.

        """
        # remove user2
        requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[0]['token'],
            'u_id': users[1]['auth_user_id'],
        })
        # get the profile of all users
        resp = requests.get(config.url + 'users/all/v1', params={
            'token': users[0]['token'],
        })

        users_all = json.loads(resp.text)['users']

        found = False
        for user in users_all:
            # if the users' profile contain user2, found is True
            if user['u_id'] == users[1]['auth_user_id']:
                found = True
                break
        # users' profile shouldn't contain user2
        assert found == False
    
    def test_remove_owner_success(self, users):
        """

        Test whether admin_user_remove can succeed
        if the target is dream owner.

        """
        # set user2 to dream owner
        requests.post(config.url + 'admin/userpermission/change/v1', json={
            'token': users[0]['token'],
            'u_id': users[1]['auth_user_id'],
            'permission_id': 1,
        })
        # remove another dream owner
        requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[1]['token'],
            'u_id': users[0]['auth_user_id'],
        })
        # get the profile of all users
        resp = requests.get(config.url + 'users/all/v1', params={
            'token': users[1]['token'],
        })

        users_all = json.loads(resp.text)['users']

        found = False
        for user in users_all:
            # if the users' profile contain user1, found is True
            if user['u_id'] == users[0]['auth_user_id']:
                found = True
                break
        # users' profile shouldn't contain user1
        assert found == False

    def test_removed_message(self, users):
        """

        Test when admin_user_remove succeed,
        whether the old message is is reset to "Removed user".

        """
        # create channel
        resp = requests.post(config.url + 'channels/create/v2', json={
            'token': users[1]['token'],
            'name': 'channel1',
            'is_public': True,
        })
        channel1 = resp.json()
        # user1 join the channel
        requests.post(config.url + 'channel/join/v2', json={
            'token': users[0]['token'],
            'channel_id': channel1['channel_id'],
        })
        # user2 send a message
        requests.post(config.url + 'message/send/v2', json={
            'token': users[1]['token'],
            'channel_id': channel1['channel_id'],
            'message': 'TEST_MESSAGE',
        })
        # user1 remove user2
        requests.delete(config.url + 'admin/user/remove/v1', json={
            'token': users[0]['token'],
            'u_id': users[1]['auth_user_id'],
        })
        # get the message detail in channel1
        resp = requests.get(config.url + 'channel/messages/v2', params={
            'token': users[0]['token'],
            'channel_id': channel1['channel_id'],
            'start': 0,
        })
        channel1_message = json.loads(resp.text)
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
    def test_invalid_permission_id(self, users):
        """

        Test whether admin_userpermission_change can raise InputError
        if the permission_id is invalid.

        """
        resp = requests.post(config.url + 'admin/userpermission/change/v1', json={
            'token': users[0]['token'],
            'u_id': users[1]['auth_user_id'],
            'permission_id': -1,
        })
        # the test should raise InputError, because the permission id is invalid
        assert resp.status_code == InputError.code

    def test_invalid_user_id(self, users):
        """

        Test whether admin_userpermission_change can raise InputError
        if the target u_id is invalid.

        """
        resp = requests.post(config.url + 'admin/userpermission/change/v1', json={
            'token': users[0]['token'],
            'u_id': -10,
            'permission_id': 1,
        })
        # the test should raise InputError, because the target u_id is invalid
        assert resp.status_code == InputError.code
    
    def test_access_error(self, users):
        """

        Test whether admin_userpermission_change can raise AccessError

        """
        resp = requests.post(config.url + 'admin/userpermission/change/v1', json={
            'token': users[1]['token'],
            'u_id': users[2]['auth_user_id'],
            'permission_id': 1,
        })
        # the test should raisse AccessError, because the user doesn't have permission
        assert resp.status_code == AccessError.code

    def test_change_success(self, users):
        """

        Test whether admin_userpermission_change can succeed

        """
        # create a private channel
        resp = requests.post(config.url + 'channels/create/v2', json={
            'token': users[0]['token'],
            'name': 'private_channel',
            'is_public': False,
        })
        private_channel = resp.json()
        # set user2 to owner
        requests.post(config.url + 'admin/userpermission/change/v1', json={
            'token': users[0]['token'],
            'u_id': users[1]['auth_user_id'],
            'permission_id': 1,
        })
        # user2 join the private channel
        requests.post(config.url + 'channel/join/v2', json={
            'token': users[1]['token'],
            'channel_id': private_channel['channel_id'],
        })
        # get the channel list
        resp = requests.get(config.url + 'channels/list/v2', params={
            'token': users[1]['token'],
        })
        user2_channel_list = json.loads(resp.text)

        join_success = False
        # if the target channel_id is valid, join_success will be True
        for channel in user2_channel_list['channels']:
            if channel['channel_id'] == private_channel['channel_id']:
                # once the channel_id is valid, break
                join_success = True
                break
        # user2 should join the private channel successfully
        assert join_success == True
