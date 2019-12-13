from django.core.paginator import Paginator
from telegram import *
from telegram.ext import *

from bot import models as bot_models
from bot.handlers.payments import paypal
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
    def set_callback_data(cls, **kwargs):
        data = [cls.KEY]
        data.extend(list('{}={}'.format(key, value) for key, value in kwargs.items()))
        return ";".join(data)

    @staticmethod
    def get_callback_data(data):
        data = data.split(';')[1:]
        return {key: value for key, value in [item.split('=') for item in data]}


class CatalogsCallback(BaseCallbackQueryHandler):
    KEY = 'catalogs'

    def callback(self, bot, update):
        query = update.callback_query
        data = self.get_callback_data(query.data)
        page = int(data.get('page', 1))
        books_list = list(bot_models.Book.objects.filter(type_id__id=data.get('id')).values('id', 'name'))
        books_paginator = Paginator(books_list, 5)
        books = books_paginator.get_page(page).object_list
        reply_markup = self.get_reply_markup(data, books, books_paginator, page)
        query.edit_message_text(text="Виберіть, які книжки вам цікаві.", reply_markup=reply_markup)
        return True

    def get_reply_markup(self, data, books, paginator, page):
        keyboards_markup = keyboards.build_menu([
            InlineKeyboardButton(
                book['name'], callback_data=BookInfoCallback.set_callback_data(id=book['id'])
            ) for book in books
        ], cols=1)
        paginator_data = {'id': data['id']}
        keyboards_markup.append(keyboards.build_paginator(paginator, page, CatalogsCallback, paginator_data))
        return InlineKeyboardMarkup(keyboards_markup, resize_keyboard=True)


class BookInfoCallback(BaseCallbackQueryHandler):
    KEY = 'book-info'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        book = bot_models.Book.objects.get(id=data.get('id'))
        button = keyboards.get_button_by_user(book, user)
        keyboards_markup = [
            InlineKeyboardButton('Переглянуту інформацію', callback_data='show_data'),
            InlineKeyboardButton('❤️ {}'.format(book.get_likes()),
                                 callback_data=BookLikeCallback.set_callback_data(id=book.id)),
            button,
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n{}".format(book.show_details()),
                                reply_markup=reply_markup)
        return True


class BookLikeCallback(BaseCallbackQueryHandler):
    KEY = 'book-like'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        book = bot_models.Book.objects.get(id=data.get('id'))
        book.set_likes(user)
        button = keyboards.get_button_by_user(book, user)
        keyboards_markup = [
            InlineKeyboardButton('Переглянуту інформацію', callback_data='show_data'),
            InlineKeyboardButton('❤️ {}'.format(book.get_likes()),
                                 callback_data=self.set_callback_data(id=book.id)),
            button,
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n{}".format(book.show_details()),
                                reply_markup=reply_markup)
        return True



class BasketAddItemCallback(BaseCallbackQueryHandler):
    KEY = 'basket-add'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        basket = bot_models.Basket.get_basket_user(user)
        book = bot_models.Book.objects.get(id=data.get('id'))
        basket.add_item_basket(basket, book)
        button = keyboards.get_button_by_user(book, user)
        keyboards_markup = [
            InlineKeyboardButton('Переглянуту інформацію', callback_data='show_data'),
            button,
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        query.edit_message_text(text="Інформація про книжку: \n{}".format(book.show_details()),
                                reply_markup=reply_markup)
        return True


class BasketRemoveItemCallback(BaseCallbackQueryHandler):
    KEY = 'basket-remove'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        basket = bot_models.Basket.get_basket_user(user)
        book = bot_models.Book.objects.get(id=data.get('id'))
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


class BasketClearCallback(BaseCallbackQueryHandler):
    KEY = 'basket-clear'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        basket = bot_models.Basket.get_basket_user(user)
        basket.clear_basket()
        query.edit_message_text(text="Корзина очищена.", reply_markup=keyboards.clear_inline)
        return True


class BuyCallback(BaseCallbackQueryHandler):
    KEY = 'buy'

    def callback(self, bot, update):
        query = update.callback_query
        user = bot_models.TelegramUser.get_user(query.from_user)
        data = self.get_callback_data(query.data)
        basket = bot_models.Basket.get_basket_by_id(data.get('basket_id', 0))

        title = "Оплата за книги"
        description = "Оплата за книги на суму {}, для отримання доступу до книг.".format(basket.total_price)

        provider_data = {'user_id': user.id, 'basket_id': basket.id}
        price = int(basket.total_price * 100)
        prices = [LabeledPrice("Ціна оплати", price if price else 100)]
        query.edit_message_text("Очікується оплата на суму {} грн.".format(basket.total_price),
                                reply_markup=keyboards.clear_inline)
        bot.send_invoice(query.message.chat_id, title, description, paypal.payload, paypal.provider_token,
                         paypal.start_parameter, paypal.currency, prices, provider_data=provider_data)

        return True
