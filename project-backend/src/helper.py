from time import time


def check_tagged(string):
    ret_list = list()
    for i in range(0, len(string)):
        if string[i] == '@':
            handle = ''
            for j in range(i + 1, len(string)):
                if string[j] == ' ' or string[j] == '\n':
                    break
                handle += string[j]
            ret_list.append(handle)
    return ret_list


def generate_timestamp():
    # today = date.today()
    # dt = datetime(today.year, today.month, today.day)
    # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    timestamp = int(time())
    return timestamp


def share_message(message, share):
    old_message = message.replace('\n', '\n\t')
    old_message = f"\n\"\"\"\n{old_message}\n\"\"\""
    ret_message = share + old_message
    return ret_message


