from src.error import AccessError, InputError
from src.data import DirectMessage, User, load_db, save_db, set_dream_stats
import json


def dm_invite_v1(token, dm_id, u_id):
    """
    Author (with token) invites a user (with user id u_id)
    to to an existing dm. Once invited the user is
    added to the dm immediately
  
    Args:
        token: string, authorisation hash
        dm_id: integer, dm's id
        u_id: integer, user's user id

    Returns:
        {}

    Raise:
        InputError:
            dm_id does not refer to an existing dm.
            u_id does not refer to a valid user.
        AccessError:
            the authorised user is not already a member of the DM.
    """
    load_db()
    # Find the dm that dm_id matched.
    match_dm = DirectMessage.check_dm_id_match(dm_id)
    # Find user that u_id matched.
    user_invite = User.check_u_id_match(u_id)
    # Check token refers valid user.
    auth_user_id = User.token_to_id(token)
    author = User.check_u_id_match(auth_user_id)
    # Check the authorised user is a member of the dm or not.
    if author in match_dm.users:
        # Don't need to invite user is already in the dm.
        if user_invite in match_dm.users:
            return {}
        match_dm.users.append(user_invite)
    else:
        # The authorised user is not already a member of the dm.
        raise AccessError
    # Add a notification to user who is invited.
    User.dm_add_notification(u_id, author.handle, match_dm)
    user_invite.set_user_stats('join_dm')
    set_dream_stats()
    save_db()
    return {}


def dm_details_v1(token, dm_id):
    """
    Users that are part of this direct message can view basic information about the DM

    Args:
        token: string, authorisation hash
        dm_id: integer, channel's id

    Returns:
        {
            'name': string,
            'members': [
                {
                    'u_id': integer,
                    'name_first': string,
                    'name_last': string,
                    'email': string,
                    'handle_str': string,
                }
            ],
        }

    Raise:
        InputError:
            DM ID is not a valid DM.
        AccessError:
            Authorised user is not a member of this DM with dm_id
    """
    load_db()
    dm_id = int(dm_id)
    # Find the dm that dm_id matched.
    match_dm = DirectMessage.check_dm_id_match(dm_id)
    # Check token refers valid user.
    auth_user_id = User.token_to_id(token)
    author = User.check_u_id_match(auth_user_id)
    if author not in match_dm.users:
        # Check the authorised user is a member of the dm or not.
        raise AccessError
    # Create a dictionary contains details of dm.
    channels_dict = dict()
    channels_dict['name'] = match_dm.name
    channels_dict['members'] = list()

    for member in match_dm.users:
        information = User.transfer_to_user(member)
        channels_dict['members'].append(information)

    save_db()
    return channels_dict

def dm_remove_v1(token, dm_id):
    """
    Remove an existing DM. This can only be done by the original creator of the DM.

    Args:
        token: string, authorisation hash
        dm_id: integer, channel's id

    Returns:
        {}

    Raise:
        InputError:
            DM ID is not a valid DM.
        AccessError:
            the user is not the original DM creator.
    """
    load_db()
    dm_id = int(dm_id)
    # Check dm_id is valid or not.
    match_dm = DirectMessage.check_dm_id_match(dm_id)
    # Check token refers valid user.
    auth_user_id = User.token_to_id(token)
    if auth_user_id is not match_dm.owner_id:
        # Check the authorised user is the original DM creator or not.
        raise AccessError
    users_list = list()
    messages_num = len(match_dm.messages)
    for user in match_dm.users:
        users_list.append(user)
    DirectMessage.remove_to_db(match_dm)
    for user in users_list:
        user.set_user_stats('leave_dm')
    set_dream_stats(num=messages_num, action='remove_message')
    set_dream_stats(num=1, action='remove_dm')
    save_db()
    return {}

def dm_create_v1(token, u_ids):
    """
        Create a direct message

        Args:
            token:string
            u_id:int

        Returns:
            a list of dictionaries than contain information about dm
            {
                'dm_id': new_dm.id,
                'dm_name': new_dm.name
            }

        Raises:
            InputError when any of: u_id does not refer to a valid user
        """
    load_db()
    dm_name = list()
    members = list()
    # if type(u_id).__name__ == 'list':
    for uid in u_ids:
        member = User.check_u_id_match(uid)
        members.append(member)
        dm_name.append(member.handle)

    owner_id = User.token_to_id(token)
    owner = User.check_u_id_match(owner_id)
    dm_name.append(owner.handle)
    members.append(owner)
    dm_name.sort()
    dm_name = ', '.join(dm_name)
    new_dm = DirectMessage(dm_name, members, owner_id)
    new_dm.add_to_db()
    if type(u_ids).__name__ == 'list':
        for uid in u_ids:
            User.dm_add_notification(uid, owner.handle, new_dm)
    for member in members:
        member.set_user_stats('join_dm')
    set_dream_stats(num=1, action='add_dm')
    save_db()
    return {
        'dm_id': new_dm.id,
        'dm_name': new_dm.name
    }


def dm_messages_v1(token, dm_id, start):
    """
        Create a direct message

        Args:
            token:string
            dm_id:int
            start:int

        Returns:
            a list of dictionaries than contain information about messages
            {
                'messages': messages,
                'start': int(start),
                'end': index
            }

        Raises:
            AccessError:
                DM ID is not a valid DM
                start is greater than the total number of messages in the channel
            InputError:
                Authorised user is not a member of DM with dm_id
    """
    load_db()
    match_dm = DirectMessage.check_dm_id_match(dm_id)
    message_num = len(match_dm.messages)
    if start > message_num:
        raise InputError(description='Start out of bound')
    au_id = User.token_to_id(token)
    auth_user = User.check_u_id_match(au_id)
    if auth_user not in match_dm.users:
        raise AccessError
    messages_list = []
    end = start
    for i in range(1, 51):
        if i + start > message_num:
            end = -1
            break
        end += 1
        reacts = list()
        for react_info in match_dm.messages[- i - start].react_infos:
            reacts.append(match_dm.messages[- i - start].transfer_to_react(react_info['react_id'], au_id))
        messages = match_dm.messages[-i - start].transfer_to_message(reacts)
        messages_list.append(messages)
    save_db()
    return {
        'messages': messages_list,
        'start': int(start),
        'end': end
    }


def dm_list_v1(token):
    load_db()
    cur_user_id = User.token_to_id(token)
    save_db()
    return {'dms': DirectMessage.dm_list(cur_user_id)}


def dm_leave_v1(token, dm_id):
    load_db()
    cur_dm = DirectMessage.check_dm_id_match(dm_id)
    cur_user_id = User.token_to_id(token)
    cur_user = User.check_u_id_match(cur_user_id)
    if cur_user not in cur_dm.users:
        raise AccessError(description='The auth_user is not in this DM!')
    DirectMessage.dm_leave(cur_user_id, dm_id)
    cur_user.set_user_stats('leave_dm')
    if len(cur_dm.users) == 1:
        set_dream_stats(1, 'remove_dm')
    else:
        set_dream_stats()
    save_db()
    return {}

