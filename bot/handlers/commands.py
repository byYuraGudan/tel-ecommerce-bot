from telegram.ext import CommandHandler


class BaseCommandHandler(CommandHandler):
    COMMAND = None
    STATE = None

    def __init__(self, *args, **kwargs):
        super(BaseCommandHandler, self).__init__(self.COMMAND, self.callback, *args, **kwargs)

    def callback(self, bot, update):
        raise NotImplementedError


class HelpCommand(BaseCommandHandler):
    COMMAND = 'help'
    STATE = 'help'

    def callback(self, bot, update):
        text = 'Привіт я бот продажнік ))'
        update.message.reply_text(text)
        return self.STATE


class StartCommand(BaseCommandHandler):
    COMMAND = 'start'
    STATE = 'help'

    def callback(self, bot, update):
        text = 'Привіт я бот продажнік))))))'
        update.message.reply_text(text)
        return self.STATE
