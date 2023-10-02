import pytest
import requests
import random
import string
import json
from src import config
from src.error import InputError, AccessError


@pytest.fixture()
def clear():
    requests.delete(config.url + 'clear/v1', json={})


def create_dict_list():
    """
    Fixture function, is to pre-register four users for further tests

    Returns:
        dict_list: Dict, contain the pre-register users' information

    """
    dict_list = list()
    '''Register the first user'''
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'pony.ma@qq.com',
        'password': 'PonyMa',
        'name_first': 'Pony',
        'name_last': 'Ma'
    })
    payload = r.json()
    dict_list.append(payload)
    '''the first user logs out'''
    requests.post(config.url + 'auth/logout/v1', json={
        'token': payload['token']
    })

    '''Register the second user'''
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'pony.ma2@qq.com',
        'password': 'PonyMa',
        'name_first': 'Pony',
        'name_last': 'Ma'
    })
    payload = r.json()
    dict_list.append(payload)
    '''the second user logs out'''
    requests.post(config.url + 'auth/logout/v1', json={
        'token': payload['token'],
    })

    '''Register the third user'''
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'sundar.pichai@gmail.com',
        'password': 'SundarPichai',
        'name_first': 'Sunder',
        'name_last': 'Pichai'
    })
    payload = r.json()
    dict_list.append(payload)
    '''the third user logs out'''
    requests.post(config.url + 'auth/logout/v1', json={
        'token': payload['token'],
    })

    '''Register the fourth user'''
    r = requests.post(config.url + 'auth/register/v2', json={
        'email': 'jack.smith@hotmail.com',
        'password': 'JackSmith',
        'name_first': 'Jack',
        'name_last': 'Smith'
    })
    payload = r.json()
    dict_list.append(payload)
    '''the fourth user logs out'''
    requests.post(config.url + 'auth/logout/v1', json={
        'token': payload['token'],
    })
    return dict_list


@pytest.fixture(name='info')
def one_user_create_dm():
    dict_list = create_dict_list()
    """User01 logs in"""
    r = requests.post(config.url + 'auth/login/v2', json={
        'email': 'pony.ma@qq.com',
        'password': 'PonyMa',
    })
    payload = r.json()
    token = payload['token']
    auth_user_id = payload['auth_user_id']
    """User01 create a dm"""
    u_id = list()
    u_id.append(dict_list[1]['auth_user_id'])
    u_id.append(dict_list[2]['auth_user_id'])
    u_id.append(dict_list[3]['auth_user_id'])
    r = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': u_id,
    })
    payload = r.json()
    dm_id = payload['dm_id']
    dm_name = payload['dm_name']
    return {
        'token': token,
        'u_id': auth_user_id,
        'dm_id': dm_id,
        'dm_name': dm_name,
    }


@pytest.mark.usefixtures("clear")
class Test_dm_create:
    def test_dm_create_success(self, info):
        """
            Test successful case

            Args:
                N/A

            Returns:
                N/A

            Raises:
                N/A

        """
        assert type(info['dm_id']).__name__ == 'int'
        assert info['dm_name'] == 'jacksmith, ponyma, ponyma0, sunderpichai'

    def test_dm_create_invalid(self, info):
        """
            Test fail case

            Args:
                N/A

            Returns:
                N/A

            Raises:
                InputError

        """

        res = requests.post(config.url + 'dm/create/v1', json={
            'token': info['token'],
            'u_ids': [1546156, 1452164],
        })
        assert res.status_code == InputError.code


@pytest.mark.usefixtures("clear")
class Test_message_send_dm:
    def test_message_send_dm_success(self, info):
        """
            Test successful case

            Args:
                N/A

            Returns:
                N/A

            Raises:
                N/A

        """

        message = 'Test for successful case'
        """User01 sends a message to the dm"""
        r = requests.post(config.url + 'message/senddm/v1', json={
            'token': info['token'],
            'dm_id': info['dm_id'],
            'message': message
        })
        payload = r.json()
        assert type(payload['message_id']).__name__ == 'int'

    def test_message_send_dm_invalid(self, info):
        """
                Test fail case

                Args:
                    N/A

                Returns:
                    N/A

                Raises:
                    InputError:dm_id is not valid
                    AccessorError:user is not the member of the dm

            """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(1001)]
        too_long_str = ''.join(str_list)
        r = requests.post(config.url + 'auth/register/v2', json={
            'email': 'FakeHayden@qq.com',
            'password': 'Hayden',
            'name_first': 'Hayden',
            'name_last': 'Hayden'
        })
        payload = r.json()
        token = payload['token']
        '''The new user tries to send a message to exiting dm'''
        r = requests.post(config.url + 'message/senddm/v1', json={
            'token': token,
            'dm_id': info['dm_id'],
            'message': 'Expect an error'
        })
        assert r.status_code == AccessError.code
        '''The dm create tries to send An extremely long message'''
        r = requests.post(config.url + 'message/senddm/v1', json={
            'token': info['token'],
            'dm_id': info['dm_id'],
            'message': too_long_str
        })
        assert r.status_code == InputError.code

@pytest.mark.usefixtures("clear")
class Test_dm_messages:
    def test_dm_messages_success(self, info):
        """
                Test successful case

                Args:
                    N/A

                Returns:
                    N/A

                Raises:

        """
        """User01 sends two messages to the dm"""
        r = requests.post(config.url + 'message/senddm/v1', json={
            'token': info['token'],
            'dm_id': info['dm_id'],
            'message': 'Success message01'
        })
        payload = r.json()
        m_id1 = payload['message_id']

        r = requests.post(config.url + 'message/senddm/v1', json={
            'token': info['token'],
            'dm_id': info['dm_id'],
            'message': 'Success message02'
        })
        payload = r.json()
        m_id2 = payload['message_id']

        r = requests.get(config.url + 'dm/messages/v1', params={
            'token': info['token'],
            'dm_id': info['dm_id'],
            'start': 0
        })
        payload = r.json()
        assert payload['messages'][0]['message_id'] == m_id2
        assert payload['messages'][1]['message_id'] == m_id1
        assert payload['start'] == 0
        assert payload['end'] == -1

    def test_dm_messages_failed(self, info):
        r = requests.get(config.url + 'dm/messages/v1', params={
                'token': info['token'],
                'dm_id': 99999,
                'start': 0
        })
        assert r.status_code == InputError.code

        r = requests.get(config.url + 'dm/messages/v1', params={
            'token': info['token'],
            'dm_id': info['dm_id'],
            'start': 9999999
        })
        assert r.status_code == InputError.code
        """A new user registers"""
        r = requests.post(config.url + 'auth/register/v2', json={
            'email': 'FakeHayden@qq.com',
            'password': 'Hayden',
            'name_first': 'Hayden',
            'name_last': 'Hayden'
        })
        payload = r.json()
        token = payload['token']
        r = requests.get(config.url + 'dm/messages/v1', params={
            'token': token,
            'dm_id': info['dm_id'],
            'start': 0
        })
        assert r.status_code == AccessError.code

@pytest.mark.usefixtures("clear")
class Test_dm_list:
    def test_dm_list_success(self, info):
        r = requests.get(config.url + 'dm/list/v1', params={
            'token': info['token'],
        })
        test = r.json()
        assert test['dms'][0]['dm_id'] == 1
        assert test['dms'][0]['name'] == info['dm_name']

    def test_dm_list_fail(self, info):
        token = requests.post(config.url + 'auth/register/v2', json={
            'email': 'FakeHayden@qq.com',
            'password': 'Hayden',
            'name_first': 'Hayden',
            'name_last': 'Hayden'
        }).json()['token']
        test = requests.get(config.url + 'dm/list/v1', params={
            'token': token,
        }).json()
        assert test['dms'] == []

@pytest.mark.usefixtures("clear")
class Test_dm_leave:
    def test_dm_leave_success(self, info):
        """
            Test successful case

            Args:
                N/A

            Returns:
                N/A

            Raises:
                N/A

        """
        new_dm = requests.post(config.url + 'dm/create/v1', json={
            'token': info['token'],
            'u_ids': [2],
        }).json()
        requests.post(config.url + 'dm/leave/v1', json={
            'token': info['token'],
            'dm_id': info['dm_id']
        })
        test = requests.get(config.url + 'dm/list/v1', params={
            'token': info['token'],
        }).json()
        assert test['dms'][0] == {
            'dm_id': new_dm['dm_id'],
            'name': new_dm['dm_name']
        }

    def test_dm_leave_fail(self, info):
        token = requests.post(config.url + 'auth/register/v2', json={
            'email': 'FakeHayden@qq.com',
            'password': 'Hayden',
            'name_first': 'Hayden',
            'name_last': 'Hayden'
        }).json()['token']

        r = requests.post(config.url + 'dm/leave/v1', json={
            'token': info['token'],
            'dm_id': 546544456564
        })
        assert r.status_code == InputError.code
        r = requests.post(config.url + 'dm/leave/v1', json={
            'token': token,
            'dm_id': info['dm_id']
        })
        assert r.status_code == AccessError.code


@pytest.fixture(name="users")
def create_users():
    """Create different users and store their id and token in a list."""
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
    
    users.append(requests.post(config.url + 'auth/register/v2', json={
        "email": "joyceliu@qq.com", 
        "password": "JoyceLiu", 
        "name_first": "Joyce", 
        "name_last": "Liu"
    }).json())
    
    return users
    

@pytest.fixture(name="dm1")
def users_setup():
    """User1 creates a dm and it directes to user4 and store the dm_id and name"""
    resp = requests.post(config.url + 'auth/login/v2', json={
        'email': 'pony.ma@qq.com', 
        'password': 'PonyMa'
    })
    user1 = resp.json()
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "joyceliu@qq.com",
        "password": "JoyceLiu",
    })
    user4 = resp.json()
    

    u_ids = list()
    u_ids.append(user4["auth_user_id"])
    resp = requests.post(config.url + 'dm/create/v1', json={
        "token": user1["token"],
        'u_ids': u_ids,
    })
    requests.post(config.url + 'auth/logout/v1', json={'token': user1['token']})
    requests.post(config.url + 'auth/logout/v1', json={'token': user4['token']})
    dm1 = resp.json()
    return dm1


@pytest.mark.usefixtures("clear")
class TestDMInvite:
    def test_invalid_dm_id(self, users):
        """Test dm/invite/v1 when the dm_id does not refer to a valid dm."""
        resp = requests.post(config.url + 'dm/invite/v1', json={
            "token": users[0]["token"],
            "dm_id": -1,
            "u_id": users[1]["auth_user_id"]
        })
        assert resp.status_code == InputError.code
        

    def test_invalid_u_id(self, users, dm1):
        """Test dm/invite/v1 when the u_id does not refer to a valid user."""
        resp = requests.post(config.url + 'dm/invite/v1', json={
            "token": users[0]["token"],
            "dm_id": dm1["dm_id"],
            "u_id": -1
        })
        assert resp.status_code == InputError.code
            

    def test_author_not_member_fail(self, users, dm1):
        """Test dm/invite/v1 when the authorised user is not already a member of the dm."""
        resp = requests.post(config.url + 'dm/invite/v1', json={
            "token": users[2]["token"],
            "dm_id": dm1["dm_id"],
            "u_id": users[1]["auth_user_id"],
        })
        assert resp.status_code == AccessError.code
             
    def test_user_alreadyindm(self, users, dm1):
        """Test dm/invite/v1 when the user who will be invited is already a member of the dm."""
        resp = requests.post(config.url + 'dm/invite/v1', json={
            "token": users[0]["token"],
            "dm_id": dm1["dm_id"],
            "u_id": users[3]["auth_user_id"],
        }) 
        resp = requests.get(config.url + 'dm/details/v1', params={
            "token": users[0]["token"], 
            "dm_id": dm1["dm_id"], 
        })
        details = json.loads(resp.text)
        assert len(details['members']) == 2


    def test_successful_dm_id(self, users, dm1):
        """Test dm/invite/v1 can succeffully invite user or not."""
        resp = requests.post(config.url + 'dm/invite/v1', json={
            "token": users[0]["token"],
            "dm_id": dm1["dm_id"],
            "u_id": users[2]["auth_user_id"],
        }) 
        resp = requests.get(config.url + 'dm/details/v1', params={
            "token": users[0]["token"], 
            "dm_id": dm1["dm_id"], 
        })
        details = json.loads(resp.text)
        assert len(details['members']) == 3


@pytest.mark.usefixtures("clear")
class TestDMDetail:
    def test_invalid_dm_id(self, users):
        """
        Test dm_details_v1, it will raise AccessError 
        if give an authorised user is not a member of the dm.
        """
        resp = requests.get(config.url + 'dm/details/v1', params={
            "token": users[0]["token"], 
            "dm_id": -1
        })
        assert resp.status_code == InputError.code
            
            
    def test_not_member(self, users, dm1):
        """
        Test dm_details_v1, it will raise AccessError 
        if give an authorised user is not a member of the dm.
        """
        resp = requests.get(config.url + 'dm/details/v1', params={
            "token": users[1]["token"], 
            "dm_id": dm1["dm_id"], 
        })
        assert resp.status_code == AccessError.code

    def test_successful(self, users, dm1):
        """
        User1 creates a dm and it directes to user4, then show the detail of the dm.
        """
        resp = requests.get(config.url + 'dm/details/v1', params={
            "token": users[0]["token"], 
            "dm_id": dm1["dm_id"], 
        })
        details = json.loads(resp.text)
        assert len(details['members']) == 2

@pytest.mark.usefixtures("clear")
class TestDMRemove:
    def test_invalid_dm_id(self, users):
        """
        Test dm_remove_v1, it will raise Inputerror if give a invalid DM ID.
        """
        resp = requests.delete(config.url + 'dm/remove/v1', json={
            "token": users[0]["token"], 
            "dm_id": -1
        })
        assert resp.status_code == InputError.code
            
    
    def test_author_not_creator(self, users, dm1):
        """
        Test dm/remove/v1 when the user is not the original DM creator 
        then raise AccessError.
        """
        resp = requests.delete(config.url + 'dm/remove/v1', json={
            "token": users[3]["token"], 
            "dm_id": dm1["dm_id"]
        })
        assert resp.status_code == AccessError.code
    
    def test_remove_success(self, users, dm1):
        """
        User1 creates a dm and it directes to user4
        User1 remove dm1 successfully.
        """ 
        requests.delete(config.url + 'dm/remove/v1', json={
            "token": users[0]["token"], 
            "dm_id": dm1["dm_id"]
        })
        resp = requests.get(config.url + 'dm/list/v1', params={"token": users[0]["token"]}) 
        assert json.loads(resp.text) == {"dms": []}
