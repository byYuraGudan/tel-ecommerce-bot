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


class TypeBookConversation(BaseConversationHandler):
    STATE = ['catalog', 'catalog-books', 'book-info']

    def entry_points(self):
        return [MessageHandler(Filters.regex('^Каталог+'), self.catalog)]

    def states(self):
        states = {
            self.STATE[0]: [CallbackQueryHandler(self.catalog_books)],
            self.STATE[1]: [CallbackQueryHandler(self.book_info)]
        }
        return states

    def fallbacks(self):
        return [MessageHandler(Filters.regex("^Назад+"), self.exit)]

    def catalog(self, bot, update):
        catalogs = bot_models.TypeBook.objects.exclude(hidden=True).values('id', 'name')
        if not catalogs:
            update.effective_message.reply_text('Нажаль немає каталогів', reply_markup=keyboards.main_keyboard())

        keyboards_markup = [
            InlineKeyboardButton(catalog['name'], callback_data=str(catalog['id'])) for catalog in catalogs
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text('Виберіть цікавий вам каталог.', reply_markup=reply_markup)
        return self.STATE[0]

    def catalog_books(self, bot, update):
        query = update.callback_query
        data = json.loads(query.data)
        books = bot_models.Book.objects.filter(type_id__id=data).values('id', 'name')

        keyboards_markup = [
            InlineKeyboardButton(book['name'], callback_data=str(book['id'])) for book in books
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Виберіть цікаву вам книжки.", reply_markup=reply_markup)
        return self.STATE[1]

    def book_info(self, bot, update):
        query = update.callback_query
        data = json.loads(query.data)
        book = bot_models.Book.objects.filter(id=data).values()
        keyboards_markup = [
            InlineKeyboardButton('Преглянуту інформацію', callback_data='show_data'),
            InlineKeyboardButton('Додати до корзини', callback_data='add_basket'),
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n {}".format(dict(book)), reply_markup=reply_markup)
        return ConversationHandler.END
