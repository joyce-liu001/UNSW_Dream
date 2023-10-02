from src.data import load_db, save_db, set_dream_stats
from src.data import User
from src.user import user_profile_v2
from src.error import InputError, AccessError

def admin_user_remove_v1(token, u_id):
    """

    Given a registered user's token and the target u_id,
    if the target u_id is invalid, function will raise an InputError.
    Else if the user does not have permission to join the channel or the token is invalid,
    an AccessError will be raised.

    Reset id_root in class User

    Args:
        'token': string
        'u_id': integer

    Returns:
        N/A

    Raises:
        InputError: When the u_id is invalid
        AccessError: When the user does not have permission or the token is invalid

    """
    # load database
    load_db()
    # make sure the type of u_id is "int"
    u_id = int(u_id)
    # get the corresponding u_id
    token_uid = User.token_to_id(token)
    # if the user is not dream owner, raise AccesError
    if not User.check_owner(token_uid):
        raise AccessError
    # check if the target u_id exists
    target_user = User.check_u_id_match(u_id)
    # if target is also owner, check if there is only one owner in the dream
    if target_user.permission_id == 1:
        User.check_owner_not_one()
    # reset target's name
    target_user.name['name_fir'] = "Removed"
    target_user.name['name_last'] = "user"
    # re set target's message
    User.set_message_removeduser(u_id)
    # update database
    set_dream_stats()
    save_db()
    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    """

    Given a registered user's token and the target u_id,
    if the target u_id is invalid, function will raise an InputError.
    Else if the user does not have permission to join the channel or the token is invalid,
    an AccessError will be raised.

    Reset id_root in class User

    Args:
        'token': string
        'u_id': integer
        'permission_id': integer

    Returns:
        N/A

    Raises:
        InputError: When the u_id or permission_id is invalid
        AccessError: When the user does not have permission or the token is invalid

    """
    # load database
    load_db()
    # make sure the type of u_id and permission_id is "int"
    u_id = int(u_id)
    permission_id = int(permission_id)
    # if permission_id is invalid, raise InputError
    if permission_id != 1 and permission_id != 2:
        raise InputError
    # get corresponding user u_id
    token_uid = User.token_to_id(token)
    # if the user is not owner, raise AccessError
    if not User.check_owner(token_uid):
        raise AccessError
    # check if target user exists
    target_user = User.check_u_id_match(u_id)
    # set target's permission_id
    target_user.permission_id = permission_id
    # update database
    save_db()
    return {}
