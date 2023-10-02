"""
File of data structure and database
"""
from src.error import InputError, AccessError
from src.helper import generate_timestamp, check_tagged
import re
import os
import jwt
import hashlib
from pickle import dump, load

SECRET = 'aero'

program_root = 0

# database: dictionary store the objects of users and channels
db = {
    'uid_root': 0,
    'cid_root': 0,
    'dmid_root': 0,
    'mid_root': 0,
    'users': list(),
    'channels': list(),
    'direct_messages': list(),
    'login_token': list(),
    'removed_users': list(),
    'dreams_stats': {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': generate_timestamp()}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': generate_timestamp()}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': generate_timestamp()}],
        'utilization_rate': float(),
    }
}


def load_db():
    """

    A function to load database from pickle file

    """
    global db
    if os.access('database.p', os.R_OK) and os.path.getsize('database.p') > 0:
        try:
            with open('database.p', 'rb') as f:
                db = load(f)
        except EOFError:
            return


def save_db():
    """

    A function to save databse to a pickle file

    """
    global db
    # if os.path.exists('database.p'):
    #     os.remove('database.p')
    with open('database.p', 'wb') as f:
        dump(db, f)
    return


def get_dream_stats():
    return db['dreams_stats']

def set_dream_stats(num=0, action=''):
    User.update_all_user_stats()
    time = generate_timestamp()

    if action == 'add_channel':
        prev_num = db['dreams_stats']['channels_exist'][-1]['num_channels_exist']
        db['dreams_stats']['channels_exist'].append(
            {'num_channels_exist': prev_num + num, 'time_stamp': time})
    elif action == 'remove_channel':
        prev_num = db['dreams_stats']['channels_exist'][-1]['num_channels_exist']
        db['dreams_stats']['channels_exist'].append(
            {'num_channels_exist': prev_num - num, 'time_stamp': time})
    elif action == 'add_dm':
        prev_num = db['dreams_stats']['dms_exist'][-1]['num_dms_exist']
        db['dreams_stats']['dms_exist'].append(
            {'num_dms_exist': prev_num + num, 'time_stamp': time})
    elif action == 'remove_dm':
        prev_num = db['dreams_stats']['dms_exist'][-1]['num_dms_exist']
        db['dreams_stats']['dms_exist'].append(
            {'num_dms_exist': prev_num - num, 'time_stamp': time})
    elif action == 'add_message':
        prev_num = db['dreams_stats']['messages_exist'][-1]['num_messages_exist']
        db['dreams_stats']['messages_exist'].append(
            {'num_messages_exist': prev_num + num, 'time_stamp': time})
    elif action == 'remove_message':
        prev_num = db['dreams_stats']['messages_exist'][-1]['num_messages_exist']
        db['dreams_stats']['messages_exist'].append(
            {'num_messages_exist': prev_num - num, 'time_stamp': time})

    num_join = 0
    num_user = len(db['users'])
    for user in db['users']:
        if user.user_stats['channels_joined'][-1]['num_channels_joined'] > 0 or user.user_stats['dms_joined'][-1]['num_dms_joined'] > 0:
            num_join += 1
    if num_user == 0:
        utilization_rate = 0.0
    else:
        utilization_rate = num_join / num_user
    db['dreams_stats']['utilization_rate'] = utilization_rate

    return


class User:
    """

    The user's class, each user will be an object and store in db['users']

    Attributes:
        id: Integer, user's id
        email: String, user's email
        password: String, user's password
        name: Dictionary, contain user's first name and last name
        handle: String, user's handle

    """

    def __init__(self, email, password, name_fir, name_last, handle):
        global db
        # id: integer
        self.id = db['uid_root'] + 1
        # auth_id: integer to verify login user
        # self.auth_id = self.id
        db['uid_root'] += 1
        # email: string
        self.email = email
        # password: string
        self.password = User.encrypt_password(password)
        # name: dictionary contain first name and last name
        self.name = dict()
        self.name["name_fir"] = name_fir
        self.name["name_last"] = name_last
        # handle: string
        self.handle = handle
        # permission id 1: 1 dream owner, 2 dream member
        self.permission_id = 2
        # this user's notifications, which saved with notification object
        self.notifications = list()
        self.img_info = {'img_url': str(), 'x_start': int(), 'x_end': int(), 'y_start': int(), 'y_end': int()}
        self.pin_code = str()
        self.user_stats = {
            'channels_joined': [{'num_channels_joined': 0, 'time_stamp': generate_timestamp()}],
            'dms_joined': [{'num_dms_joined': 0, 'time_stamp': generate_timestamp()}],
            'messages_sent': [{'num_messages_sent': 0, 'time_stamp': generate_timestamp()}],
            'involvement_rate': float()
        }

    def check_first_user(self):
        """

        Check all the user's permission, if no Dream user exist, set the current user to Dream owner

        """
        has_owner = False
        for user in db['users']:
            if user.permission_id == 1:
                has_owner = True

        if not has_owner:
            self.permission_id = 1

    def generate_token(self):
        """

        Generate token base on user's id and program root

        Returns: String, Token

        """
        global program_root
        payload = {
            "u_id": self.id,
            "program_root": program_root
        }
        program_root += 1
        token = jwt.encode(payload, SECRET, algorithm='HS256')
        if token not in db['login_token']:
            db['login_token'].append(token)
        return token

    @staticmethod
    def check_owner(u_id):
        """
        check whether the user with u_id is the Dream owner

        Args:
            u_id: Integer, user's id

        Returns:
            True if the user is the Dream owner
            False if the user is the member

        """
        match_user = User.check_u_id_match(u_id)
        if match_user.permission_id == 1:
            return True
        return False

    @staticmethod
    def logout(token):
        """
        Logout base on the current token

        Args:
            token: String, user's token

        Returns:
            True if success
            False if unsuccess

        """
        if token in db['login_token']:
            db['login_token'].remove(token)
            return True
        return False

    @staticmethod
    def encrypt_password(password):
        """
        Encrypt the password

        Args:
            password: String, the user's original password

        Returns:
            String that the encoded password

        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def reset_root():
        """

        Reset id_root in class User

        Args:
            N/A

        Returns:
            N/A

        """
        global db
        db['uid_root'] = 0

    @staticmethod
    def check_email_valid(email):
        """

        Check whether the email address is valid

        Args:
            email: String, the email address of the user

        Returns:
            N/A

        Raises:
            InputError: When the email is invalid

        """
        regx = r'^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regx, email):
            raise InputError

    @staticmethod
    def check_email_been_used(email):
        """
        Check whether the user's email is been used

        Args:
            email: String, the email of the user

        Returns:
            N/A

        Raises:
            InputError: If the email is been used by other user

        """
        for exist_user in db['users']:
            if exist_user.email == email:
                raise InputError

    @staticmethod
    def check_password_length(password):
        """

        Check whether the password is satisfy the length request

        Args:
            password: String, the user's password

        Returns:
            N/A

        Raises:
            InputError: When the password is not satisfy the length request

        """
        if len(password) < 6:
            raise InputError

    @staticmethod
    def check_name_length(name):
        """
        Check whether the length of user is satisfy length request

        Args:
            name: String, the name of the user

        Returns:
            N/A

        Raises:
            InputError: When the length of the user name is not satisfy the request

        """
        if len(name) < 1 or len(name) > 50:
            raise InputError

    @staticmethod
    def generate_handle(name_first, name_last):
        """
        Generate a handle base on user's firstname and last name

        Args:
            name_first: String, the user's first name
            name_last: String, the user's last name

        Returns:
            new_handle: String, the string been generated

        """
        regx = r'[@\s]'
        handle = name_first.lower() + name_last.lower()
        handle = re.sub(regx, '', handle)
        handle = handle[:20]
        new_handle = handle
        i = 0
        while 1:
            is_repeat = False
            for exist_user in db["users"]:
                if exist_user.handle == new_handle:
                    is_repeat = True
                    new_handle = handle + str(i)
                    i += 1
                    break
            if not is_repeat:
                break
        return new_handle

    @staticmethod
    def check_email_password_match(email, password):
        """
        Check whether the input email and password are match

        Args:
            email: String, the user's email
            password: String, the user's password

        Returns:
            N/A

        Raises:
            InputError: When the email and password are not match

        """
        for exist_user in db["users"]:
            if exist_user.email == email and exist_user.password == User.encrypt_password(password):
                return exist_user
        raise InputError

    @staticmethod
    def token_to_id(token):
        """

        Args:
            token: Integer, auth_user_id

        Returns:
            id: Integer, user's id

        """
        # for exist_user in db["users"]:
        #     if exist_user.auth_id == token:
        #         return exist_user.id
        if token in db['login_token']:
            preload = jwt.decode(token, SECRET, algorithms=['HS256'])
            User.check_u_id_match(preload['u_id'])
            return preload['u_id']
        else:
            raise AccessError

    @staticmethod
    def build_tagged_list(tagged_users, handle_list):
        for handle in handle_list:
            for user in db['users']:
                if user.handle == handle:
                    tagged_users.append(user.id)
        return

    def add_to_db(self):
        """
        Add the current user to the database, if the user is the first user, let him become a
        Dream owner

        Returns:
            N/A

        """
        # global db
        db['users'].append(self)

    @staticmethod
    def check_u_id_match(u_id):
        """
        Check whether u_id does refer to a valid user or not.
        Args:
            u_id: integer, user's user id

        Returns:
            exist_user: class

        Raise:
            InputError: u_id does not refer to a valid user.
        """
        for exist_user in db['users']:
            if exist_user.id == u_id:
                return exist_user
        raise InputError

    def transfer_to_user(self):
        """
        transfer the detail of the user into a dict

        Args:
            N/A

        Returns:
            user: dict
        """
        user = dict()
        user['u_id'] = self.id
        user['name_first'] = self.name["name_fir"]
        user['name_last'] = self.name['name_last']
        user['email'] = self.email
        user['handle_str'] = self.handle
        user['profile_img_url'] = self.img_info['img_url']
        return user

    @staticmethod
    def check_handle_valid(handle_str):
        """
        check if the handle_str is valid

        Args:
            handle_str: str

        Returns:
            N/A

        Raise:
            InputError: if the handle_str is invalid or has been taken
        """
        if len(handle_str) < 3 or len(handle_str) > 20:
            raise InputError
        for exist_user in db['users']:
            if exist_user.handle == handle_str:
                raise InputError

    @staticmethod
    def channel_tag_notification(user_id, au_handle, channel, message):
        """
        Add notification base on tagged message in channel

        Args:
            user_id: Integer, user's id
            au_handle: string, user's handle
            channel: Object, channel
            message: Object, message

        Returns:
            N/A

        """
        note_message = f"{au_handle} tagged you in {channel.name}: {message}"
        for _, user in enumerate(db['users']):
            if user.id == user_id:
                notification = Notification(channel.id, -1, note_message)
                user.notifications.append(notification)
                break
        return

    @staticmethod
    def channel_add_notification(user_id, au_handle, channel):
        """
        Add notification base on added to channel

        Args:
            user_id: Integer, user's id
            au_handle: string, user's handle
            channel: Object, channel

        Returns:
            N/A

        """
        note_message = f"{au_handle} added you to {channel.name}"
        for _, user in enumerate(db['users']):
            if user.id == user_id:
                notification = Notification(channel.id, -1, note_message)
                user.notifications.append(notification)
                break
        return

    @staticmethod
    def dm_tag_notification(user_id, au_handle, dm, message):
        """
        Add notification base on tagged message in dm

        Args:
            user_id: Integer, user's id
            au_handle: string, user's handle
            dm: Object, direct message
            message: Object, message

        Returns:
            N/A

        """
        note_message = f"{au_handle} tagged you in {dm.name}: {message}"
        for _, user in enumerate(db['users']):
            if user.id == user_id:
                notification = Notification(-1, dm.id, note_message)
                user.notifications.append(notification)
                break
        return

    @staticmethod
    def dm_add_notification(user_id, au_handle, dm):
        """
        Add notification base on added to channel

        Args:
            user_id: Integer, user's id
            au_handle: string, user's handle
            dm: Object, directly message

        Returns:
            N/A

        """
        note_message = f"{au_handle} added you to {dm.name}"
        for _, user in enumerate(db['users']):
            if user.id == user_id:
                notification = Notification(-1, dm.id, note_message)
                user.notifications.append(notification)
                break
        return

    @staticmethod
    def check_owner_not_one():
        """
        check if number of dream owner is only one

        Args:
            N/A

        Returns:
            N/A

        Raise:
            InputError: if there is only one dream owner
        """
        owner_num = 0
        for user in db['users']:
            if user.permission_id == 1:
                owner_num += 1
        if owner_num == 1:
            raise InputError

    @staticmethod
    def set_message_removeduser(u_id):
        """
        set message content of removed user to "Removed user"

        Args:
            u_id: integer, user's user id

        Returns:
            N/A
        """
        target_user = User.check_u_id_match(u_id)

        for channel_i in range(len(db['channels'])):
            for message_i in range(len(db['channels'][channel_i].messages)):
                if db['channels'][channel_i].messages[message_i].owner_id == u_id:
                    db['channels'][channel_i].messages[message_i].content = "Removed user"

        for dm_i in range(len(db['direct_messages'])):
            for dm_message_i in db['direct_messages'][dm_i].messages:
                if db['direct_messages'][dm_i].messages[dm_message_i].owner_id == u_id:
                    db['direct_messages'][dm_i].messages[dm_message_i].content = "Removed user"

        db['removed_users'].append(target_user)

        for channel in db['channels']:
            for member_uid in channel.member:
                if member_uid == u_id:
                    channel.member.remove(member_uid)
                    break

        for dm in db['direct_messages']:
            for member_uid in dm.users:
                if member_uid == u_id:
                    dm.users.remove(member_uid)
                    break

        for token_id in db['login_token']:
            if User.token_to_id(token_id) == u_id:
                db['login_token'].remove(token_id)

        for index in range(len(db['users'])):
            if db['users'][index].id == u_id:
                db['users'].pop(index)
                break
        return

    @staticmethod
    def profile_append_in_users():
        result_all = {
            'users': []
        }
        for user in db['users']:
            user_profile = user.transfer_to_user()
            # print(user_profile)
            result_all['users'].append(user_profile)

        return result_all

    @staticmethod
    def check_u_id_match_in_removed(u_id):
        for removed_user in db['removed_users']:
            if removed_user.id == u_id:
                return removed_user
        return None

    def set_user_stats(self, action=''):
        time = generate_timestamp()
        if action == 'join_channel':
            prev_num = self.user_stats['channels_joined'][-1]['num_channels_joined']
            self.user_stats['channels_joined'].append(
                {'num_channels_joined': prev_num + 1, 'time_stamp': time})
        elif action == 'leave_channel':
            prev_num = self.user_stats['channels_joined'][-1]['num_channels_joined']
            self.user_stats['channels_joined'].append(
                {'num_channels_joined': prev_num - 1, 'time_stamp': time})
        elif action == 'join_dm':
            prev_num = self.user_stats['dms_joined'][-1]['num_dms_joined']
            self.user_stats['dms_joined'].append(
                {'num_dms_joined': prev_num + 1, 'time_stamp': time})
        elif action == 'leave_dm':
            prev_num = self.user_stats['dms_joined'][-1]['num_dms_joined']
            self.user_stats['dms_joined'].append(
                {'num_dms_joined': prev_num - 1, 'time_stamp': time})
        elif action == 'send_message':
            prev_num = self.user_stats['messages_sent'][-1]['num_messages_sent']
            self.user_stats['messages_sent'].append(
                {'num_messages_sent': prev_num + 1, 'time_stamp': time})

        messages_exist = 0
        for channel in db['channels']:
            messages_exist += len(channel.messages)
        for dm in db['direct_messages']:
            messages_exist += len(dm.messages)
        denominator = len(db['channels']) + len(db['direct_messages']) + messages_exist

        if denominator == 0:
            involvement_rate = 0.0
            print(f'deno: {denominator}')
        else:
            numerator = self.user_stats['channels_joined'][-1]['num_channels_joined'] + \
                        self.user_stats['dms_joined'][-1]['num_dms_joined'] + \
                        self.user_stats['messages_sent'][-1]['num_messages_sent']
            involvement_rate = numerator / denominator
            print(f'num:{numerator}')
            print(f'deno: {denominator}')

        self.user_stats['involvement_rate'] = involvement_rate
        return

    @staticmethod
    def update_all_user_stats():
        for user in db['users']:
            channels_exist = len(db['channels'])
            dms_exist = len(db['direct_messages'])
            messages_exist = 0
            for channel in db['channels']:
                messages_exist += len(channel.messages)
            for dm in db['direct_messages']:
                messages_exist += len(dm.messages)

            numerator = (user.user_stats['channels_joined'][-1]['num_channels_joined'] +
                         user.user_stats['dms_joined'][-1]['num_dms_joined'] +
                         user.user_stats['messages_sent'][-1]['num_messages_sent'])
            denominator = channels_exist + dms_exist + messages_exist

            if denominator != 0:
                new_involvement_rate = numerator / denominator
                user.user_stats['involvement_rate'] = new_involvement_rate
            else:
                user.user_stats['involvement_rate'] = 0

        return


class Channel:
    """
    The channel's class, each channel will be an object and store in db['channels']
        id: Integer:
        owner: list of integer
        member: list of integer
        name: string
        is_public: boolean
        messages: list of objects
    """

    def __init__(self, u_id, name, is_public):
        global db
        # id: integer
        self.id = db['cid_root'] + 1
        db['cid_root'] += 1
        # owner: list contain the channel owner's u_id
        self.owner = []
        self.owner.append(u_id)
        # member: list contain the channel member's u_id
        self.member = []
        self.member.append(u_id)
        # name: string
        self.name = name
        # is_public: boolean to make channel private/public
        self.is_public = is_public
        # message: list contain message object (not id)
        self.messages = []
        self.standup_info = {'is_standup': False, 'message': str(), 'time_finish': int()}

    @staticmethod
    def reset_root():
        """

        Reset id_root in class Channel

        Args:
            N/A

        Returns:
            N/A

        """
        global db
        db['cid_root'] = 0

    @staticmethod
    def check_name_length(name):
        """

        Check whether the length of the hannel's name is valid

        Args:
            name: String, the user's name

        Returns:
            N/A

        Raises:
            InputError: When the length of name is not valid

        """
        if len(name) > 20:
            raise InputError

    def add_to_db(self):
        """
        Add the channel object to database

        Returns:
            N/A

        """
        db['channels'].append(self)

    @staticmethod
    def check_channel_id_match(channel_id):
        """
        Check whether channel_id refers to a valid channel or not.
        Args:
            channel_id: integer, channel's id

        Returns:
            exist_channel: class

        Raise:
            InputError: channel_id does not refer to a valid channel.
        """
        for exist_channel in db['channels']:
            if exist_channel.id == channel_id:
                return exist_channel
        raise InputError(description='Channel ID is not a valid channel')

    def check_user_access(self, u_id):
        """

        Given an user_id, check whether this user
        have permission to join the channel.
        Raise an AccessError if the user does not have permission.

        Args:
            'auth_user_id': integer

        Returns:
            N/A

        Raises:
            AccessError: When the user does not have permission

        """
        global db
        if self.is_public:
            return
        for user in db['users']:
            if user.id == u_id and user.permission_id == 1:
                return
        raise AccessError

    def check_member_existence(self, u_id):
        """

        Given an user_id, check whether this user
        already exists in the channel.
        if so, return True, else return False

        Reset id_root in class User

        Args:
            'auth_user_id': integer

        Returns:
            True or False

        """
        for exist_member in self.member:
            if exist_member == u_id:
                return True
        return False

    def add_member(self, u_id):
        """Adds user (with u_id) to that channel"""
        self.member.append(u_id)

    @staticmethod
    def list_v2(u_id):
        """
        set details of all channels into a dict

        Args:
            N/A

        Returns:
            channels_list: dict
        """
        channels_list = dict()
        channels_list['channels'] = list()
        for channel in db['channels']:
            for member in channel.member:
                information = dict()
                if member == u_id:
                    information['channel_id'] = channel.id
                    information['name'] = channel.name
                    channels_list['channels'].append(information)
        return channels_list

    @staticmethod
    def listall_v2():
        """
        set details of all channels into a dict

        Args:
            N/A

        Returns:
            channels_list: dict
        """
        channels_list = dict()
        channels_list['channels'] = list()
        # Traverse the channel in the database
        for exist_channel in db['channels']:
            # package the information of channels into "detail" dictionary
            detail = dict()
            detail['channel_id'] = exist_channel.id
            detail['name'] = exist_channel.name
            # append the "detail" into channels_list
            channels_list['channels'].append(detail)

        return channels_list

    def check_standup_state(self):
        return self.standup_info['is_standup']

    def start_standup(self, length):
        self.standup_info['is_standup'] = True
        self.standup_info['time_finish'] = generate_timestamp() + length

    @staticmethod
    def end_standup(channel_id, u_id):
        load_db()
        match_channel = Channel.check_channel_id_match(channel_id)
        new_message = Message(u_id, match_channel.standup_info['message'])
        match_channel.messages.append(new_message)
        match_channel.standup_info['is_standup'] = False
        match_channel.standup_info['message'] = str()
        match_channel.standup_info['time_finish'] = int()
        user = User.check_u_id_match(u_id)
        user.set_user_stats('send_message')
        set_dream_stats(num=1, action='add_message')
        save_db()

    def modify_standup_message(self, user, message):
        self.standup_info['message'] += f'{user.handle}: {message}\n'

    @staticmethod
    def send_late_message(channel_id, late_message):
        load_db()
        for channel in db['channels']:
            if channel.id == channel_id:
                channel.messages.append(late_message)
        user = User.check_u_id_match(late_message.owner_id)
        user.set_user_stats('send_message')
        set_dream_stats(num=1, action='add_message')
        save_db()


class Message:
    """
    The message's class, each message will be an object and store in one of the attribute in channel
    Attributes:
        id: integer
        owner_id: integer
        content: string
        time: integer
    """

    def __init__(self, u_id, content):
        global db
        # id: integer
        self.id = db['mid_root'] + 1
        db['mid_root'] += 1
        # owner_id: integer the owner's u_id
        self.owner_id = u_id
        # content: string the content of the message
        self.content = content
        # time: integer (unix timestamp) time of the message
        self.time = generate_timestamp()
        self.react_infos = [{'react_id': 1, 'u_ids': list()}]
        self.is_pin = False

    @staticmethod
    def reset_root():
        """

        Reset id_root in class Message

        Args:
            N/A

        Returns:
            N/A

        """
        global db
        db['mid_root'] = 0

    def transfer_to_react(self, react_id, auth_id):
        target = None
        for react_info in self.react_infos:
            if react_info['react_id'] == react_id:
                target = react_info
        if target is None:
            raise InputError(description='React ID is not exist!')
        react = dict()
        react['react_id'] = target['react_id']
        react['u_ids'] = target['u_ids']
        if auth_id in target['u_ids']:
            react['is_this_user_reacted'] = True
        else:
            react['is_this_user_reacted'] = False
        return react

    def transfer_to_message(self, reacts):
        """

        Create a dictionary of message

        Return:
            A dictionary of message

        """
        message = dict()
        message['message_id'] = self.id
        message['u_id'] = self.owner_id
        message['message'] = self.content
        message['time_created'] = self.time
        message['reacts'] = reacts
        message['is_pinned'] = self.is_pin
        return message

    @staticmethod
    def search(user_id, query_str, ret_list):
        for channel in db['channels']:
            for message in channel.messages:
                if user_id in channel.member:
                    if re.search(query_str.encode('unicode_escape').decode(), message.content):
                        reacts = list()
                        for react_info in message.react_infos:
                            reacts.append(message.transfer_to_react(react_info['react_id'], user_id))
                        ret_list.append(message.transfer_to_message(reacts))
        for dm in db['direct_messages']:
            for message in dm.messages:
                for user in dm.users:
                    if user.id == user_id:
                        if re.search(query_str.encode('unicode_escape').decode(), message.content):
                            reacts = list()
                            for react_info in message.react_infos:
                                reacts.append(message.transfer_to_react(react_info['react_id'], user_id))
                            ret_list.append(message.transfer_to_message(reacts))
        return ret_list

    @staticmethod
    def id_to_message(message_id):
        """
        Get a message object base on the id

        Args:
            message_id: Integer, the message's id

        Returns:
            Object, the message

        """
        for channel in db['channels']:
            for message in channel.messages:
                if message.id == message_id:
                    return message
        for dm in db['direct_messages']:
            for message in dm.messages:
                if message.id == message_id:
                    return message
        raise InputError

    def edit(self, new_message, sender):
        """
        Edit message

        Args:
            new_message: String, the new message the user want to edit to
            sender: Object, the user who want to edit the message

        Returns:
            N/A

        """
        for channel in db['channels']:
            for message in channel.messages:
                if message.id == self.id:
                    handle_list = check_tagged(new_message)
                    for handle in handle_list:
                        for user_id in channel.member:
                            user = User.check_u_id_match(user_id)
                            if user.handle == handle:
                                add_message = f"{sender.handle} tagged you in {channel.name}: {new_message[:20]}"
                                new_note = Notification(channel.id, -1, add_message)
                                user.notifications.append(new_note)
        for dm in db['direct_messages']:
            for message in dm.messages:
                if message.id == self.id:
                    handle_list = check_tagged(new_message)
                    for handle in handle_list:
                        for user in dm.users:
                            if user.handle == handle:
                                add_message = f"{sender.handle} tagged you in {dm.name}: {new_message[:20]}"
                                new_note = Notification(-1, dm.id, add_message)
                                user.notifications.append(new_note)
        self.content = new_message

    # def check_id_match(self, user_id):
    #     if self.owner_id == user_id:
    #         return
    #     raise AccessError

    @staticmethod
    def check_user_permission(user_id, message_id):
        """
        Check whether the user has permission to edit/remove message

        Args:
            user_id: Integer, the user's id
            message_id: Integer, the message's id

        Returns:
            N/A

        Raises:
            AccessError: When the user don't have permission

        """
        for channel in db['channels']:
            for message in channel.messages:
                if message.id == message_id and message.owner_id == user_id:
                    return
        for dm in db['direct_messages']:
            for message in dm.messages:
                if message.id == message_id and message.owner_id == user_id:
                    return
        for channel in db['channels']:
            if user_id in channel.owner:
                return
        for user in db['users']:
            if user_id == user.id and user.permission_id == 1:
                return
        raise AccessError

    @staticmethod
    def remove(message):
        """
        Remove message base on the object

        Args:
            message:Object, message

        Returns:
            N/A

        """
        for channel in db['channels']:
            for i in range(0, len(channel.messages)):
                if channel.messages[i].id == message.id:
                    del channel.messages[i]
                    return
        for dm in db['direct_messages']:
            for i in range(0, len(dm.messages)):
                if dm.messages[i].id == message.id:
                    del dm.messages[i]
                    return


class DirectMessage:

    def __init__(self, name, users, owner_id):
        global db
        self.name = name
        self.id = db['dmid_root'] + 1
        db['dmid_root'] += 1
        self.users = users
        self.owner_id = owner_id
        self.messages = []

    @staticmethod
    def reset_root():
        global db
        db['dmid_root'] = 0

    @staticmethod
    def check_dm_id_match(dm_id):
        """
        Check whether d_id does refer to a valid dm or not.
        Args:
            dm_id: integer

        Returns:
            exist_user: class

        Raise:
            InputError: dm_id does not refer to a valid user.
        """
        for exist_dm in db['direct_messages']:
            if exist_dm.id == dm_id:
                return exist_dm
        raise InputError

    def add_to_db(self):
        """
        Add the current user to the database, if the user is the first user, let him become a
        Dream owner

        Returns:
            N/A

        """
        # global db
        db['direct_messages'].append(self)

    def remove_to_db(self):
        """
        Remove the current dm from the database.
        """
        global db
        db['direct_messages'].remove(self)

    @staticmethod
    def dm_list(u_id):
        """
        Check whether u_id is in the dm
        Args:
            u_id: integer

        Returns:
            exist_dm: class
        """
        dms = list()
        for exist_dm in db['direct_messages']:
            for user in exist_dm.users:
                if user.id == u_id:
                    dm = dict()
                    dm['dm_id'] = exist_dm.id
                    dm['name'] = exist_dm.name
                    dms.append(dm)

        return dms

    @staticmethod
    def dm_leave(u_id, dm_id):
        """
        Leave dm base on user id and dm id

        Args:
            u_id: Integer, user's id
            dm_id: Integer, dm's id

        Returns:
            N/A

        Raises:
            InputError: When dm is not found

            AccessError: When user is not found

        """
        for exist_dm in db['direct_messages']:
            if exist_dm.id == dm_id:
                for i in range(0, len(exist_dm.users)):
                    if exist_dm.users[i].id == u_id:
                        del (exist_dm.users[i])

    @staticmethod
    def send_late_message(dm_id, late_message):
        load_db()
        for direct_message in db['direct_messages']:
            if direct_message.id == dm_id:
                direct_message.messages.append(late_message)
        user = User.check_u_id_match(late_message.owner_id)
        user.set_user_stats('send_message')
        set_dream_stats(num=1, action='add_message')
        save_db()


class Notification:

    def __init__(self, channel_id, dm_id, message):
        global db
        self.channel_id = channel_id
        self.dm_id = dm_id
        self.message = message

    def transfer_to_notification(self):
        temp = {'channel_id': self.channel_id, 'dm_id': self.dm_id,
                'notification_message': self.message}
        return temp

    @staticmethod
    def get_notifications(user_id, ret_list):
        """
        Get the current 20 notifications

        Args:
            user_id:
            ret_list:

        Returns:

        """
        for user in db['users']:
            if user.id == user_id:
                for i in range(1, 21):
                    if i > len(user.notifications):
                        break
                    ret_list.append(user.notifications[-i].transfer_to_notification())
        return ret_list
