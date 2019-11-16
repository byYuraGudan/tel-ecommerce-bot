from telegram.ext import MessageHandler, Filters


class BaseMessageHandler(MessageHandler):
    COMMAND = None
    STATE = None

    def __init__(self, *args, **kwargs):
        super(BaseMessageHandler, self).__init__(self.COMMAND, self.callback, *args, **kwargs)

    def callback(self, update, context):
        raise NotImplementedError


def unknown(bot, update):
    text = 'Незрозуміла команда. Спробуйте ще раз. ️😊'
    update.message.reply_text(text)
    return 'unknown'


unknown_message = MessageHandler(Filters.all, unknown)
