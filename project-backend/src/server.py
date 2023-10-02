import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src import admin
from src import auth
from src import channel
from src import channels
from src import dm
from src import message
from src import other
from src import user


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    input_info = request.get_json()
    output_info = auth.auth_login_v2(
        input_info['email'],
        input_info['password'],
    )
    return dumps(output_info)


@APP.route("/auth/register/v2", methods=['POST'])
def register():
    input_info = request.get_json()
    output_info = auth.auth_register_v2(
        input_info['email'],
        input_info['password'],
        input_info['name_first'],
        input_info['name_last'],
    )
    return dumps(output_info)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    input_info = request.get_json()
    output_info = auth.auth_logout_v1(
        input_info['token'],
    )
    return dumps(output_info)


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    input_info = request.get_json()
    output_info = channel.channel_invite_v2(
        input_info['token'],
        input_info['channel_id'],
        input_info['u_id'],
    )
    return dumps(output_info)


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))

    output_info = channel.channel_details_v2(
        token,
        channel_id
    )
    return dumps(output_info)


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
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
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    output_info = channel.channel_messages_v2(
        token,
        channel_id,
        start
    )
    return dumps(output_info)


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    input_info = request.get_json()
    output_info = channel.channel_join_v2(
        input_info['token'],
        input_info['channel_id'],
    )
    return dumps(output_info)


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    input_info = request.get_json()
    output_info = channel.channel_addowner_v1(
        input_info['token'],
        input_info['channel_id'],
        input_info['u_id'],
    )
    return dumps(output_info)


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner_v1():
    input_info = request.get_json()
    output_info = channel.channel_removeowner_v1(
        input_info['token'],
        input_info['channel_id'],
        input_info['u_id'],
    )
    return dumps(output_info)


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave_v1():
    input_info = request.get_json()
    output_info = channel.channel_leave_v1(
        input_info['token'],
        input_info['channel_id'],
    )
    return dumps(output_info)


@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    # input_info = request.get_json()
    # output_info = channels.channels_list_v2(
    #     input_info['token'],
    # )
    token = str(request.args.get('token'))
    output_info = channels.channels_list_v2(token)
    return dumps(output_info)


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    # input_info = request.get_json()
    # output_info = channels.channels_listall_v2(
    #     input_info['token'],
    # )
    token = str(request.args.get('token'))
    output_info = channels.channels_listall_v2(token)
    return dumps(output_info)


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    input_info = request.get_json()
    output_info = channels.channels_create_v2(
        input_info['token'],
        input_info['name'],
        input_info['is_public'],
    )
    return dumps(output_info)


@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    input_info = request.get_json()
    output_info = message.message_send_v2(
        input_info['token'],
        input_info['channel_id'],
        input_info['message'],
    )
    return dumps(output_info)


@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
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

    input_info = request.get_json()
    output_info = message.message_edit_v2(
        input_info['token'],
        input_info['message_id'],
        input_info['message'],
    )
    return dumps(output_info)


@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
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

    input_info = request.get_json()
    output_info = message.message_remove_v1(
        input_info['token'],
        input_info['message_id'],
    )
    return dumps(output_info)


@APP.route("/message/share/v1", methods=['POST'])
def message_share():
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

    input_info = request.get_json()
    output_info = message.message_share_v1(
        input_info['token'],
        input_info['og_message_id'],
        input_info['message'],
        input_info['channel_id'],
        input_info['dm_id'],
    )
    return dumps(output_info)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    output_info = dm.dm_details_v1(
        token,
        dm_id
    )
    return dumps(output_info)


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    """
        list all the message in the dm

        Args:
            token:string

        Returns:
            a dictionary and the value of 'dms' is List of dictionaries, where each dictionary
            contains types { dm_id, name }
            {
                'dms':[{}]
            }

        Raises:
            N/A
    """
    token = str(request.args.get('token'))
    output_info = dm.dm_list_v1(
        token
    )
    return dumps(output_info)


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
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
    token = request.json.get('token')
    u_ids = [int(u_id) for u_id in request.json.get('u_ids')]
    output_info = dm.dm_create_v1(
        token,
        u_ids,
    )
    return dumps(output_info)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
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
    input_info = request.get_json()
    output_info = dm.dm_remove_v1(
        input_info['token'],
        input_info['dm_id'],
    )
    return dumps(output_info)


@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    input_info = request.get_json()
    output_info = dm.dm_invite_v1(
        input_info['token'],
        input_info['dm_id'],
        input_info['u_id'],
    )
    return dumps(output_info)


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    """
        the user is removed from a dm

        Args:
            token:string
            dm_id:int

        Returns:
            N/A

        Raises:
            InputError:
                dm_id is not valid
            AccessError:
                the user is not a part of members in the dm
    """
    input_info = request.get_json()
    output_info = dm.dm_leave_v1(
        input_info['token'],
        input_info['dm_id'],
    )
    return dumps(output_info)


@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
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
    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    output_info = dm.dm_messages_v1(
        token,
        dm_id,
        start
    )
    return dumps(output_info)


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    """
        send a message to dm

        Args:
            token:string
            dm_id:int
            message:string

            Returns:
                the message id
                {
                    'message_id': new_message.id
                }

            Raises:
                InputError:Message is more than 1000 characters
                AccessError:the authorised user is not a member of the DM they are trying to  post to
    """
    input_info = request.get_json()
    output_info = message.message_senddm_v1(
        input_info['token'],
        input_info['dm_id'],
        input_info['message'],
    )
    return dumps(output_info)


@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    token = str(request.args.get('token'))
    u_id = int(request.args.get('u_id'))
    output_info = user.user_profile_v2(
        token,
        u_id
    )
    return dumps(output_info)


@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_setname():
    input_info = request.get_json()
    output_info = user.user_profile_setname_v2(
        input_info['token'],
        input_info['name_first'],
        input_info['name_last'],
    )
    return dumps(output_info)


@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def user_profile_setemail():
    input_info = request.get_json()
    output_info = user.user_profile_setemail_v2(
        input_info['token'],
        input_info['email'],
    )
    return dumps(output_info)


@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    input_info = request.get_json()
    output_info = user.user_profile_sethandle_v1(
        input_info['token'],
        input_info['handle_str'],
    )
    return dumps(output_info)


@APP.route("/users/all/v1", methods=['GET'])
def user_all():
    token = str(request.args.get('token'))
    output_info = user.users_all_v1(
        token
    )
    return dumps(output_info)


@APP.route("/search/v2", methods=['GET'])
def search():
    token = str(request.args.get('token'))
    query_str = str(request.args.get('query_str'))
    output_info = other.search_v2(
        token,
        query_str
    )
    return dumps(output_info)


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    input_info = request.get_json()
    output_info = admin.admin_user_remove_v1(
        input_info['token'],
        input_info['u_id'],
    )
    return dumps(output_info)


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    input_info = request.get_json()
    output_info = admin.admin_userpermission_change_v1(
        input_info['token'],
        input_info['u_id'],
        input_info['permission_id'],
    )
    return dumps(output_info)


@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    token = str(request.args.get('token'))
    output_info = other.notifications_get_v1(
        token
    )
    return dumps(output_info)


@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    output_info = other.clear_v1()
    return dumps(output_info)

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
