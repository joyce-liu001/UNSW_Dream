from src.data import load_db, save_db, User, Channel, Message, set_dream_stats
from src.error import InputError, AccessError


def channel_addowner_v1(token, channel_id, u_id):
    """
    This function make user with user id u_id an owner of this channel

    Args:
        token: string, the token of current user
        channel_id: integer, the channel's id
        u_id: integer, the user's id

    Returns:
        Dictionary, empty dictionary


    Raises:
        AccessError: When the authorised user is not an owner of the Dreams, or an owner of this channel
                    or The token is invalid

        InputError: Channel ID is not a valid channel
                    or When user with user id u_id is already an owner of the channel

    """
    load_db()
    # Get the user's id
    au_id = User.token_to_id(token)
    match_channel = Channel.check_channel_id_match(channel_id)
    # Check whether the user is not the owner of Dream and the owner of this channel
    if au_id not in match_channel.owner and not User.check_owner(au_id):
        raise AccessError
    # Check whether the user is already this channel's owner
    if u_id in match_channel.owner:
        raise InputError
    # Append the user to become match channel's owner
    match_channel.owner.append(u_id)
    if u_id not in match_channel.member:
        match_channel.member.append(u_id)
        user = User.check_u_id_match(u_id)
        user.set_user_stats('add_channel')
        set_dream_stats()
    save_db()
    return {}


def channel_removeowner_v1(token, channel_id, u_id):
    """
    This function remove user with user id u_id an owner of this channel

    Args:
        token: String, the current user's token
        channel_id: Integer, The channel's id
        u_id: Integer, the user's id

    Returns:
        Dictionary: an empty dictionary

    Raises:
        AccessError: When the authorised user is not an owner of the Dreams, or an owner of this channel
                    or The token is invalid

        InputError: Channel ID is not a valid channel
                    or When user with user id u_id is already an owner of the channel
    """
    load_db()
    au_id = User.token_to_id(token)
    match_channel = Channel.check_channel_id_match(channel_id)
    if au_id not in match_channel.owner and not User.check_owner(au_id):
        raise AccessError
    if u_id not in match_channel.owner:
        raise InputError
    if len(match_channel.owner) == 1:
        raise InputError
    match_channel.owner.remove(u_id)
    save_db()
    return {}


def channel_leave_v1(token, channel_id):
    """
    Given a channel ID, the user removed as a member of this channel. Their messages should remain in the channel

    Args:
        token: String, the current's user's token
        channel_id: Integer, the channel's id

    Returns:
        Dictionary: Empty dictionary

    Raises:
        AccessError: When the token is invalid
                    or Authorised user is not a member of channel with channel_id

        InputError: Channel ID is not a valid channel

    """
    load_db()
    au_id = User.token_to_id(token)
    match_channel = Channel.check_channel_id_match(channel_id)
    if match_channel.standup_info['is_standup']:
        raise AccessError(description='The user cannot leave channel in standup period')
    if au_id not in match_channel.member:
        raise AccessError
    match_channel.member.remove(au_id)
    if au_id in match_channel.owner:
        match_channel.owner.remove(au_id)
    user = User.check_u_id_match(au_id)
    user.set_user_stats('leave_channel')
    set_dream_stats()
    save_db()
    return{}


def channel_invite_v2(token, channel_id, u_id):
    """
    Author (with token) invites a user (with user id u_id)
    to join a channel with ID channel_id. Once invited the user is
    added to the channel immediately

    Args:
        token: string, authorisation hash
        channel_id: integer, channel's id
        u_id: integer, user's user id

    Returns:
        {}

    Raise:
        InputError:
            channel_id does not refer to a valid channel.
            u_id does not refer to a valid user.
        AccessError:
            the authorised user is not already a member of the channel.
    """
    load_db()
    channel_id = int(channel_id)
    u_id = int(u_id)
    # Check channe_id is valid.
    match_channel = Channel.check_channel_id_match(channel_id)
    # Check u_id is valid.
    user = User.check_u_id_match(u_id)
    # Check token refers valid user.
    auth_user_id = User.token_to_id(token)
    author = User.check_u_id_match(auth_user_id)
    # Check the authorised user is a member of the channel or not.
    if auth_user_id in match_channel.member:
        # Don't need to invite user is already in the channel.
        if u_id in match_channel.member:
            return {}
        match_channel.add_member(u_id)
    else:
        # The authorised user is not already a member of the channel.
        raise AccessError
    # Add a notification to user who is invited.
    User.channel_add_notification(u_id, author.handle, match_channel)
    user.set_user_stats('join_channel')
    set_dream_stats()
    save_db()
    return {}


def channel_details_v2(token, channel_id):
    """
    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel

    Args:
        token: string, authorisation hash
        channel_id: integer, channel's id

    Returns:
        {
            'name': string,
            'is_public': True/False
            'owner_members': [
                {
                    'u_id': integer,
                    'name_first': string,
                    'name_last': string',
                    'email': string,
                    'handle_str': string,
                }
            ],
            'all_members': [
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
            Channel ID is not a valid channel.
        AccessError:
            Authorised user is not a member of channel with channel_id.
    """
    load_db()
    channel_id = int(channel_id)
    # Check channel_id is valid.
    match_channel = Channel.check_channel_id_match(channel_id)
    # Check token refers valid user.
    auth_user_id = User.token_to_id(token)
    if auth_user_id not in match_channel.member:
        # Check the authorised user is a member of the channel or not.
        raise AccessError
    # Create a dictionary contains details of channel.
    channels_dict = dict()
    channels_dict['name'] = match_channel.name
    channels_dict['is_public'] = match_channel.is_public
    channels_dict['owner_members'] = list()
    channels_dict['all_members'] = list()

    for owner_id in match_channel.owner:
        # Owner list contain the channel owners' u_id.
        user = User.check_u_id_match(owner_id)
        information = User.transfer_to_user(user)
        channels_dict['owner_members'].append(information)
        
    for member_id in match_channel.member:
        # Member list contain the channel members' u_id.
        user = User.check_u_id_match(member_id)
        information = User.transfer_to_user(user)
        channels_dict['all_members'].append(information)

    save_db()
    return channels_dict


def channel_join_v2(token, channel_id):
    """

    Given a registered users' token and the target channel_id,
    if the target channel_id is invalid, function will raise an InputError.
    Else if the user does not have permission to join the channel,
    an AccessError will be raised.

    Args:
        'token': string
        'channel_id': integer

    Returns:
        N/A
    
    Raises:
        InputError: When the channel_id is invalid or the token is invalid
        AccessError: When the user does not have permission

    """
    # load database
    load_db()
    # make sure the type of channel_id is "int"
    channel_id = int(channel_id)
    # To obtain auth_user_id
    u_id = User.token_to_id(token)
    # Check if the channel_id is valid
    # if not, an InputError will be raised
    match_channel = Channel.check_channel_id_match(channel_id)
    # Check if the user has permission
    match_channel.check_user_access(u_id)
    # if member is already exist in channel, do nothing
    if match_channel.check_member_existence(u_id) == True:
        return {}
    # add the user into target channel
    else:
        match_channel.add_member(u_id)
    # update database
    user = User.check_u_id_match(u_id)
    user.set_user_stats('join_channel')
    set_dream_stats()
    save_db()
    return {
    }


def channel_messages_v2(token, channel_id, start):
    """

    Return up to 50 messages between index "start" and "start + 50"


    Args:
        auth_user_id: integer
        channel_id: integer
        start: integer

    Return:
        A dictionary
        {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
        }

    """


    load_db()
    match_channel = Channel.check_channel_id_match(channel_id)
    message_num = len(match_channel.messages)
    if start > message_num:
        raise InputError
    au_id = User.token_to_id(token)
    if au_id not in match_channel.member:
        raise AccessError
    messages_list = []
    end = start
    for i in range(1, 51):
        if i + start > message_num:
            end = -1
            break
        end += 1
        reacts = list()
        for react_info in match_channel.messages[- i - start].react_infos:
            reacts.append(match_channel.messages[- i - start].transfer_to_react(react_info['react_id'], au_id))
        messages = match_channel.messages[-i - start].transfer_to_message(reacts)
        messages_list.append(messages)
    save_db()
    return {
        'messages': messages_list,
        'start': start,
        'end': end
    }
