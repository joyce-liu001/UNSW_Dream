from src.data import load_db, save_db
from src.data import User
from src.error import InputError, AccessError

def user_profile_v2(token, u_id):
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
    User.check_u_id_match(token_uid)
    # check if the target has been removed
    match_user = User.check_u_id_match_in_removed(u_id)
    # if not, check if the target is in "user"
    if match_user is None:
        # if the user not exist, raise InputError
        match_user = User.check_u_id_match(u_id)
    # token_uid == u_id
    output = dict()
    # get the corresponding profile
    output['user'] = match_user.transfer_to_user()

    return output

def user_profile_setname_v2(token, name_first, name_last):
    """

    Given a registered user's token, name_first and name_last,
    if the name_first or name_last is invalid, function will raise an InputError.
    Else if the token is invalid,
    an AccessError will be raised.

    Reset id_root in class User

    Args:
        'token': string
        'u_id': integer

    Returns:
        N/A
    
    Raises:
        InputError: When the name_first or name_last is invalid
        AccessError: When the token is invalid

    """
    # load database
    load_db()
    # get the corresponding u_id
    token_uid = User.token_to_id(token)
    match_user = User.check_u_id_match(token_uid)
    # check if the name is valid
    # if not, raise InputError
    User.check_name_length(name_first)
    User.check_name_length(name_last)
    # set name
    match_user.name['name_fir'] = name_first
    match_user.name['name_last'] = name_last
    # update database
    save_db()

    return {
    }

def user_profile_setemail_v2(token, email):
    """

    Given a registered user's token and email,
    if the email is invalid, function will raise an InputError.
    Else if the token is invalid,
    an AccessError will be raised.

    Reset id_root in class User

    Args:
        'token': string
        'email': string

    Returns:
        N/A
    
    Raises:
        InputError: When the email is invalid
        AccessError: When the token is invalid

    """
    # load database
    load_db()
    # get the corresponding u_id
    token_uid = User.token_to_id(token)
    match_user = User.check_u_id_match(token_uid)
    # Check whether the email is valid and whether it has been taken
    User.check_email_valid(email)
    User.check_email_been_used(email)
    # set email
    match_user.email = email
    # update database
    save_db()

    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    """

    Given a registered user's token and handle_str,
    if the handle is invalid, function will raise an InputError.
    Else if the token is invalid,
    an AccessError will be raised.

    Args:
        'token': string
        'handle_str': string

    Returns:
        N/A
    
    Raises:
        InputError: When the handle_str is invalid
        AccessError: When the token is invalid

    """
    # load database
    load_db()
    # get the corresponding u_id
    token_uid = User.token_to_id(token)
    match_user = User.check_u_id_match(token_uid)
    # Check whether the handle is valid and whether it has been taken
    User.check_handle_valid(handle_str)
    # set handle
    match_user.handle = handle_str
    # update database
    save_db()

    return {
    }

def users_all_v1(token):
    """

    Given a registered user's token,
    if the handle is invalid, function will raise an InputError.
    Else if the token is invalid,
    an AccessError will be raised.

    Args:
        'token': string

    Returns:
        N/A
    
    Raises:
        AccessError: When the token is invalid

    """
    # load database
    load_db()
    # get the corresponding u_id
    token_uid = User.token_to_id(token)
    User.check_u_id_match(token_uid)
    # update database
    save_db()
    # retur all users' profile
    return User.profile_append_in_users()

