import pytest

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.dm import dm_create_v1, dm_list_v1, dm_invite_v1, dm_details_v1, dm_remove_v1, dm_messages_v1, dm_leave_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.message import message_senddm_v1


@pytest.fixture()
def clear():
    clear_v1()

@pytest.fixture(name="users")
def create_users():
    """Create different users and store their id in a list."""
    users = list()
    users.append(auth_register_v2("pony.ma@qq.com", "PonyMa", "Pony", "Ma"))
    users.append(auth_register_v2("pony.ma@qqqw.com", "PonyMa", "Pony", "Ma"))
    users.append(auth_register_v2("jack.smith@hotmail.com", "JackSmith", "Jack", "Smith"))
    users.append(auth_register_v2("joyceliu@qq.com", "JoyceLiu", "Joyce", "Liu"))
    
    return users
   
@pytest.fixture(name="dm1")
def users_setup():
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
class TestDMInvite:
    def test_invalid_dm_id(self, users):
        """Test dm_invite_v1 when the channel_id does not refer to a valid channel."""
        with pytest.raises(InputError):
            dm_invite_v1(users[0]["token"], -1, users[1]["auth_user_id"])

    def test_invalid_u_id(self, users, dm1):
        """Test dm_invite_v1 when the u_id does not refer to a valid user."""
        with pytest.raises(InputError):
            dm_invite_v1(users[0]["token"], dm1["dm_id"], -1)

    def test_author_not_member_fail(self, users, dm1):
        """Test dm_invite_v1 when the authorised user is not already a member of the channel."""
        with pytest.raises(AccessError):
            dm_invite_v1(users[2]["token"], dm1["dm_id"], users[1]["auth_user_id"])
    
    def test_successful_dm_id(self, users, dm1):
        """Test channel_invite_v2 can succeffully invite user or not."""
        dm_invite_v1(users[0]["token"], dm1["dm_id"], users[2]["auth_user_id"])
        assert len(dm_details_v1(users[0]["token"], dm1["dm_id"])['members']) == 3


@pytest.mark.usefixtures("clear")
class TestDMDetail:
    def test_invalid_dm_id(self, users):
        """
        Test dm_details_v1, it will raise AccessError 
        if give an authorised user is not a member of the channel.
        """
        with pytest.raises(InputError):
            dm_details_v1(users[0]["token"], -1)

    def test_not_member(self, users, dm1):
        """
        Test dm_details_v1, it will raise AccessError 
        if give an authorised user is not a member of the channel.
        """
        with pytest.raises(AccessError):
            dm_details_v1(users[1]["token"], dm1["dm_id"])

    def test_successful(self, users, dm1):
        """
        User1 creates a dm and it directes to user4
        there is no one joins public one, then show the detail of the channel.
        """
        assert len(dm_details_v1(users[0]["token"], dm1["dm_id"])['members']) == 2


@pytest.mark.usefixtures("clear")
class TestDMRemove:
    def test_invalid_dm_id(self, users):
        """
        Test dm_remove_v1, it will raise Inputerror if give a invalid DM ID.
        """
        with pytest.raises(InputError):
            dm_remove_v1(users[0]["token"], -1)
    
    def test_author_not_creator(self, users, dm1):
        """
        Test dm/remove/v1 when the user is not the original DM creator 
        then raise AccessError.
        """
        with pytest.raises(AccessError):
            dm_remove_v1(users[3]["token"], dm1["dm_id"])

    def test_remove_success(self, users, dm1):
        """
        User1 creates a dm and it directes to user4
        User1 remove dm1 successfully.
        """ 
        dm_remove_v1(users[0]["token"], dm1["dm_id"])
        assert dm_list_v1(users[0]["token"]) == {"dms": []}


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
class Test_dm_create:
    def test_dm_create_success(self, info):
        """
            Test dm/create/v1 when the dm_id does refer to a valid dm.
        """
        assert type(info['dm_id']).__name__ == 'int'
        assert info['dm_name'] == 'jacksmith, ponyma, ponyma0, sunderpichai'

    def test_dm_create_invalid(self, info):
        """
            Test dm/create/v1 when the dm_id does not refer to a valid dm.
        """
        with pytest.raises(InputError):
            assert dm_create_v1(info['token'], [415646512, 45645])


@pytest.mark.usefixtures("clear")
class Test_dm_messages:
    def test_dm_messages_success(self, info):
        """
            Test dm/messages/v1 when the channel_id does refer to a valid dm.
        """
        """User01 sends a message to the dm"""
        m_id1 = message_senddm_v1(info['token'], info['dm_id'], 'Success message01')['message_id']
        m_id2 = message_senddm_v1(info['token'], info['dm_id'], 'Success message02')['message_id']
        test = dm_messages_v1(info['token'], info['dm_id'], 0)
        assert test['messages'][0]['message_id'] == m_id2
        assert test['messages'][1]['message_id'] == m_id1
        assert test['start'] == 0
        assert test['end'] == -1

    def test_dm_messages_failed(self, info):
        """
            Test dm/messages/v1 when the channel_id does not refer to a valid dm or the user is not in the dm
        """
        with pytest.raises(InputError):
            dm_messages_v1(info['token'], 1234456, 0)

        with pytest.raises(InputError):
            dm_messages_v1(info['token'], info['dm_id'], 9999999)

        with pytest.raises(AccessError):
            """A new user registers"""
            token = auth_register_v2("FakeHayden@qq.com", "Hayden", "Hayden", "Hayden")['token']
            dm_messages_v1(token, info['dm_id'], 0)


@pytest.mark.usefixtures("clear")
class Test_dm_list:
    def test_dm_list_success(self, info):
        """
            Test dm/list/v1 when the dm_id does refer to a valid dm.
        """
        new_dm = dm_create_v1(info['token'], [2])
        test = dm_list_v1(info['token'])
        assert test['dms'][0]['dm_id'] == 1
        assert test['dms'][0]['name'] == info['dm_name']
        assert test['dms'][1]['dm_id'] == new_dm['dm_id']
        assert test['dms'][1]['name'] == new_dm['dm_name']

    def test_dm_list_fail(self, info):
        """
            Test dm/list/v1 when the user is not in the dm.
        """
        token = auth_register_v2("FakeHayden@qq.com", "Hayden", "Hayden", "Hayden")['token']
        test = dm_list_v1(token)
        assert test['dms'] == []


@pytest.mark.usefixtures("clear")
class Test_dm_leave:
    def test_dm_leave_success(self, info):
        """
            Test dm/leave/v1 when the input is valid.
        """
        new_dm = dm_create_v1(info['token'], [2])
        dm_leave_v1(info['token'], info['dm_id'])
        assert dm_list_v1(info['token'])['dms'][0] == {
            'dm_id': new_dm['dm_id'],
            'name': new_dm['dm_name']
        }

    def test_dm_leave_fail(self, info):
        """
            Test dm/leave/v1 when the dm_id is not valid or the user is not in the dm
        """
        token = auth_register_v2("FakeHayden@qq.com", "Hayden", "Hayden", "Hayden")['token']
        with pytest.raises(InputError):
            dm_leave_v1(info['token'], 123456)
        with pytest.raises(AccessError):
            dm_leave_v1(token, info['dm_id'])
