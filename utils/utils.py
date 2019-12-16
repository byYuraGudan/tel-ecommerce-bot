from functools import wraps

from telegram import ChatAction

from eccomerceBot.settings import ALLOWED_HOSTS


def inheritors(class_):
    subclasses = set()
    parents = [class_]
    while parents:
        parent = parents.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                parents.append(child)
    return subclasses


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(context, bot, update, *args, **kwargs):
            bot.send_chat_action(chat_id=update._effective_message.chat_id, action=action)
            return func(context, bot, update, *args, **kwargs)

        return command_func

    return decorator


def set_callback_data(key, data):
    return ";".join([key, data])


def get_callback_data(data):
    split_data = data.split(';')
    key = split_data[0]
    data_info = split_data[1:]
    return data_info

def generate_book_link(id):
    host = ALLOWED_HOSTS[0]
    return '{}/bot/book/detail/{}'.format(host, id)


send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)
