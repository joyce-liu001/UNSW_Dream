from src.data import load_db, save_db, User, Channel, Message, DirectMessage, Notification
from src import data
from src.error import InputError
from src.helper import generate_timestamp
import os


def clear_v1():
    """
    Resets the internal data of the application to it's initial state

    Returns:
        Dictionary, empty dictionary

    """
    data.db['users'].clear()
    data.db['channels'].clear()
    data.db['direct_messages'].clear()
    data.db['login_token'].clear()
    data.db['removed_users'].clear()
    data.db['dreams_stats'] = {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': generate_timestamp()}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': generate_timestamp()}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': generate_timestamp()}],
        'utilization_rate': float(),
    }
    # Reset root in class User
    User.reset_root()
    # Reset root in class Channel
    Channel.reset_root()
    # Reset root in class Message
    Message.reset_root()
    # Reset root in class DirectMessage
    DirectMessage.reset_root()
    # clear_db()
    save_db()
    return {}


def search_v2(token, query_str):
    """
    Given a query string, return a collection of messages in all of the channels/DMs that the user has joined that
    match the query

    Args:
        token: String, the current user's token
        query_str: String, the content that the user want to search

    Returns:
        Dictionary
        {
        messages: list contain data type message
        }

    Raises:
        AccessError: The token is invalid
                    or query_str is above 1000 characters

    """
    load_db()
    if len(query_str) > 1000:
        raise InputError
    au_id = User.token_to_id(token)
    ret_list = list()
    ret_list = Message.search(au_id, query_str, ret_list)
    save_db()
    return {
        'messages': ret_list
    }


def notifications_get_v1(token):
    """
    Return the user's most recent 20 notifications

    Args:
        token: String, the current user's token

    Returns:
        Dictionary
        {
        notifications: A list contain datatype notification
        }

    """
    load_db()
    au_id = User.token_to_id(token)
    ret_list = list()
    Notification.get_notifications(au_id, ret_list)
    save_db()
    return {
        'notifications': ret_list
    }
