from telegram import *
from telegram.ext import *

from bot import models as bot_models
from bot.keyboards import keyboards


class BaseCallbackQueryHandler(CallbackQueryHandler):
    KEY = None

    def __init__(self, *args, **kwargs):
        if self.KEY is None:
            raise AttributeError('Key must by not None.')
        pattern = '^{};+'.format(self.KEY)
        super(BaseCallbackQueryHandler, self).__init__(self.callback, *args, pattern=pattern, **kwargs)

    def callback(self, bot, update):
        raise NotImplementedError

    @classmethod
    def set_callback_data(cls, data):
        callback_data = [cls.KEY, str(data)]
        return ";".join(callback_data)

    @staticmethod
    def get_callback_data(data):
        return data.split(';')[1:]


class CatalogsCallback(BaseCallbackQueryHandler):
    KEY = 'catalogs'

    def callback(self, bot, update):
        query = update.callback_query
        data = self.get_callback_data(query.data)
        books = bot_models.Book.objects.filter(type_id__id=data[0]).values('id', 'name')
        keyboards_markup = [
            InlineKeyboardButton(
                book['name'], callback_data=BookInfoCallback.set_callback_data(book['id'])
            ) for book in books
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Виберіть цікаву вам книжки.", reply_markup=reply_markup)
        return True


class BookInfoCallback(BaseCallbackQueryHandler):
    KEY = 'book-info'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        book = bot_models.Book.objects.get(id=data[0])
        button = keyboards.get_button_by_user(book, user)
        keyboards_markup = [
            InlineKeyboardButton('Оплатити', callback_data='show_data', pay=True),
            InlineKeyboardButton('Преглянуту інформацію', callback_data='show_data'),
            button,
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n{}".format(book.show_details()),
                                reply_markup=reply_markup)
        return True


class BasketAddItem(BaseCallbackQueryHandler):
    KEY = 'basket-add'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        basket = bot_models.Basket.get_basket_user(user)
        book = bot_models.Book.objects.get(id=data[0])
        basket.add_item_basket(basket, book)
        button = keyboards.get_button_by_user(book, user)
        keyboards_markup = [
            InlineKeyboardButton('Оплатити', callback_data='show_data', pay=True),
            InlineKeyboardButton('Преглянуту інформацію', callback_data='show_data'),
            button,
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n{}".format(book.show_details()),
                                reply_markup=reply_markup)
        return True


class BasketRemoveItem(BaseCallbackQueryHandler):
    KEY = 'basket-remove'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        basket = bot_models.Basket.get_basket_user(user)
        book = bot_models.Book.objects.get(id=data[0])
        basket.delete_item_basket(basket, book)
        button = keyboards.get_button_by_user(book, user)
        keyboards_markup = [
            InlineKeyboardButton('Оплатити', callback_data='show_data', pay=True),
            InlineKeyboardButton('Преглянуту інформацію', callback_data='show_data'),
            button,
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n{}".format(book.show_details()),
                                reply_markup=reply_markup)
        return True
