import threading

from src.data import load_db, save_db, User, Channel, Message, DirectMessage, set_dream_stats
from src.helper import check_tagged, share_message, generate_timestamp
from src.error import InputError, AccessError


def message_send_v2(token, channel_id, message):
    """
    Send a message from authorised_user to the channel specified by channel_id. Note: Each message should have it's
    own unique ID.

    Args:
        token: String, the current's token
        channel_id: Integer, the channel's id
        message: String, the content of the message

    Returns:
        Dictionary:
        {
        message_id: Integer, the message's id
        }

    Raises:
        AccessError: When the token is invalid
                    or the authorised user has not joined the channel they are trying to post to

        InputError: Message is more than 1000 characters

    """
    load_db()
    if len(message) > 1000:
        raise InputError
    au_id = User.token_to_id(token)
    au_user = User.check_u_id_match(au_id)
    match_channel = Channel.check_channel_id_match(channel_id)
    if au_id not in match_channel.member:
        raise AccessError
    # Create new message object and add it to the database
    new_message = Message(au_id, message)
    match_channel.messages.append(new_message)
    # checking for tagged message. If so, create notification and save to database
    handle_list = check_tagged(message)
    # The list contain all tagged users
    tagged_users = list()
    User.build_tagged_list(tagged_users, handle_list)
    for tagged_user in tagged_users:
        if tagged_user in match_channel.member:
            User.channel_tag_notification(tagged_user, au_user.handle, match_channel, message[:20])
    au_user.set_user_stats('send_message')
    set_dream_stats(num=1, action='add_message')
    save_db()
    return {
        'message_id': new_message.id
    }


def message_senddm_v1(token, dm_id, message):
    load_db()
    dm_id = int(dm_id)
    if len(message) > 1000:
        raise InputError
    u_id = User.token_to_id(token)
    new_message = Message(u_id, message)
    new_user = User.check_u_id_match(u_id)
    exist_dm = DirectMessage.check_dm_id_match(dm_id)
    if new_user not in exist_dm.users:
        raise AccessError
    exist_dm.messages.append(new_message)
    # checking for tagged message. If so, create notification and save to database
    handle_list = check_tagged(message)
    # The list contain all tagged users
    tagged_users_id = list()
    User.build_tagged_list(tagged_users_id, handle_list)
    for tagged_user_id in tagged_users_id:
        for user in exist_dm.users:
            if tagged_user_id == user.id:
                User.dm_tag_notification(tagged_user_id, new_user.handle, exist_dm, message[:20])
    new_user.set_user_stats('send_message')
    set_dream_stats(num=1, action='add_message')
    save_db()
    return {
        'message_id': new_message.id
    }


def message_edit_v2(token, message_id, message):
    '''
    Author (with token) 
    edit a message (witn message_id) to a new message (with message)
    If the new message is an empty string, the message is deleted.    

    Args:
        token: string, authorisation hash
        message_id: integer, message's id
        message: string

    Returns:
        {}

    Raise:
        InputError:
            Length of message is over 1000 characters
            message_id refers to a deleted message
        AccessError:
            when none of the following are true:
                Message with message_id was sent by the authorised user making this request
                The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**
    '''

    load_db()
    message_id = int(message_id)
    if len(message) > 1000:
        raise InputError
    if len(message) == 0:
        message_remove_v1(token, message_id)
        save_db()
        return
    au_id = User.token_to_id(token)
    sender = User.check_u_id_match(au_id)
    match_message = Message.id_to_message(message_id)
    # match_message.check_id_match(au_id)
    Message.check_user_permission(au_id, message_id)
    match_message.edit(message, sender)
    save_db()
    return {}


def message_remove_v1(token, message_id):
    '''
    Author (with token) 
    remove a message (witn message_id) 

    Args:
        token: string, authorisation hash
        message_id: integer, message's id
    Returns:
        {}

    Raise:
        InputError:
            Message (based on ID) no longer exists
        AccessError:
            when none of the following are true:
                Message with message_id was sent by the authorised user making this request
                The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**
    '''

    load_db()
    message_id = int(message_id)
    au_id = User.token_to_id(token)
    match_message = Message.id_to_message(message_id)
    # match_message.check_id_match(au_id)
    Message.check_user_permission(au_id, message_id)
    Message.remove(match_message)
    au_user = User.check_u_id_match(au_id)
    au_user.set_user_stats()
    set_dream_stats(num=1, action='remove_message')
    save_db()
    return {}


def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    Author (with token) 
    share a message (with og_message_id) with optional message(with message) 
    to a channel(with channel_id) or a DM(with dm_id) 

    Args:
        token: string, authorisation hash
        og_message_id: integer, message's id
        message: string
        channel_id: integer, channel's id, if not share to a channel channel_id becomes -1
        dm_id: integer, DM's id, if not share to a DM dm_id becomes -1
    Returns:
        {shared_message_id: integer}

    Raise:
        AccessError:
            the authorised user has not joined the channel or DM they are trying to share the message to
    '''

    load_db()
    auth_id = User.token_to_id(token)
    auth_user = User.check_u_id_match(auth_id)
    match_message = Message.id_to_message(og_message_id)
    new_message = share_message(match_message.content, message)
    if channel_id != -1:
        ret_dict = message_send_v2(token, channel_id, new_message)
    elif dm_id != -1:
        ret_dict = message_senddm_v1(token, dm_id, new_message)
    else:
        raise InputError
    auth_user.set_user_stats('send_message')
    set_dream_stats(num=1, action='add_message')
    save_db()
    return {
        'shared_message_id': ret_dict['message_id']
    }
