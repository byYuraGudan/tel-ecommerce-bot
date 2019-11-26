from telegram.ext import CommandHandler

from bot.keyboards import keyboards


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
        text = 'Я телеграм бот, який надає тобі список книг, які ти зможеш придбати для того аби їх прочитати.'
        update.effective_message.reply_text(text)
        return self.STATE


class StartCommand(BaseCommandHandler):
    COMMAND = 'start'
    STATE = 'help'

    def callback(self, bot, update):
        text = 'Привіт я бот, який надасть тобі можливість переглянуту та ' \
               'придбати книжки для того щоб ти став розуміншим. 😉. У мене ти зможеш знайти найпопулярніші книжки !!!'
        reply_markup = keyboards.main_keyboard()
        update.effective_message.reply_text(text, reply_markup=reply_markup)
        return self.STATE
