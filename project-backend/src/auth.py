from src.data import User, load_db, save_db, set_dream_stats


def auth_login_v2(email, password):
    """
    Given a registered users' email and password and returns their `auth_user_id` value

    Args:
        email: String, the email of the user
        password: String, the password of the user

    Returns:
        Dictionary
        {
        token: String, the user's string,
        auth_user_id: Integer, the user's id
        }

    Raises:
        InputError: Email entered is not a valid email
                    or Email entered does not belong to a user
                    or Password is not correct

    """
    load_db()
    # Check whether the user's email address is valid
    User.check_email_valid(email)
    # Check whether the email and password is match, return the match user object
    match_user = User.check_email_password_match(email, password)
    token = match_user.generate_token()
    save_db()
    return {
        'token': token,
        'auth_user_id': match_user.id
    }


def auth_register_v2(email, password, name_first, name_last):
    """
    Given a user's first and last name, email address, and password, create a new account for
    them and return a new `auth_user_id`.

    Args:
        email: String, the user's email address
        password: String, the user's password
        name_first: String, the user's first name
        name_last: String, the user's last name

    Returns:
        Dictionary
        {
        token: String, the user's token,
        auth_user_id: Integer, the user's id
        }

    Raises:
        InputError: Email entered is not a valid email
                    or Email address is already being used by another user
                    or Password entered is less than 6 characters long
                    or name_first is not between 1 and 50 characters inclusively in length
                    or name_last is not between 1 and 50 characters inclusively in length
    """
    load_db()
    # Check whether the email is valid
    User.check_email_valid(email)
    # Check whether the email is been used
    User.check_email_been_used(email)
    # Check whether the password is been used
    User.check_password_length(password)
    # Check whether the first name is valid
    User.check_name_length(name_first)
    # Check whether the last name is valid
    User.check_name_length(name_last)
    # Create a new User object
    handle = User.generate_handle(name_first, name_last)
    new_user = User(email, password, name_first, name_last, handle)
    new_user.check_first_user()
    token = new_user.generate_token()
    new_user.add_to_db()
    set_dream_stats()
    save_db()
    return {
        'token': token,
        'auth_user_id': new_user.id
    }


def auth_logout_v1(token):
    """
    Given an active token, invalidates the token to log the user out. If a valid token is given, and the user is
    successfully logged out, it returns true, otherwise false.

    Args:
        token: String, the user's token

    Returns:
        Dictionary:
        {
        is_success: Boolean, whether the user logout success or not
        }

    Raises:
        N/A

    """
    load_db()
    if User.logout(token):
        save_db()
        return {'is_success': True}
    else:
        save_db()
        return {'is_success': False}
