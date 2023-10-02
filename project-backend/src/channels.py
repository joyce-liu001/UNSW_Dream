from src.data import User, Channel, load_db, save_db, set_dream_stats
from src.error import AccessError


def channels_create_v2(token, name, is_public):
    """
    Creates a new channel with that name that is either a public or private channel

    Args:
        token: String, the auth_user_id for the user
        name: String, the name of the channel
        is_public: Boolean, whether or not the channel is public

    Returns:
        Dictionary { channel_id: Integer, the channel's id }

    Raises:
        InputError: Name is more than 20 characters long

    """
    load_db()
    if token is None:
        raise AccessError
    # Check whether the length of the channel name is valid
    Channel.check_name_length(name)
    # Transfer token
    u_id = User.token_to_id(token)
    # Create new object
    new_channel = Channel(u_id, name, is_public)
    new_channel.add_to_db()
    user = User.check_u_id_match(u_id)
    user.set_user_stats('join_channel')
    set_dream_stats(1, 'add_channel')
    save_db()
    return {
        'channel_id': new_channel.id,
    }


def channels_listall_v2(token):
    """
    Given a registered user's token,
    and list all the channels and their associated details
    output format:

    Args:
        'token': string,

    Returns:
        {
            'channels': [
                {
                    'channel_id': integer,
                    'name': string,
                }
            ]
        }
    
    Raises:
        InputError: When the channel_id is invalid or the token is invalid
        AccessError: when the token is invalid

    """
    # load database
    load_db()
    # check if the token is valid
    User.token_to_id(token)
    # get output list
    channels_list = Channel.listall_v2()
    # update database
    save_db()
    return channels_list


def channels_list_v2(token):
    """
    Provide a list of all channels (and their associated details) that the authorised user is
    part of

    Args:
        token:integer

    Returns:
        a list of dictionaries than contain information about each channels
        {
            'channels': [
                {
                    'channel_id': id,
                    'name': 'Channel1'
                },
        }

    Raises:
        N/A

    """
    load_db()
    cur_id = User.token_to_id(token)
    save_db()
    return Channel.list_v2(cur_id)

