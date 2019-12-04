import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import *

from bot import models as bot_models
from bot.keyboards import keyboards


class BaseConversationHandler(ConversationHandler):
    STATE = None

    def __init__(self, *args, **kwargs):
        super(BaseConversationHandler, self).__init__(
            self.entry_points(), self.states(), self.fallbacks(), *args, **kwargs
        )

    @property
    def states(self):
        raise NotImplementedError

    @property
    def entry_points(self):
        raise NotImplementedError

    @property
    def fallbacks(self):
        raise NotImplementedError

    def exit(self, bot, update):
        update.effective_message.reply_text('Виберіть що вас цікавить.', reply_markup=keyboards.main_keyboard())
        return ConversationHandler.END
