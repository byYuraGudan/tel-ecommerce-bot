from django.core.paginator import Paginator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters

from bot import models as bot_models
from bot.handlers.callbacks import CatalogsCallback, BookInfoCallback, UserBooksCallback
from bot.keyboards import keyboards


class BaseMessageHandler(MessageHandler):
    COMMAND = None
    STATE = None

    def __init__(self, *args, **kwargs):
        super(BaseMessageHandler, self).__init__(self.COMMAND, self.callback, *args, **kwargs)

    def callback(self, bot, update):
        raise NotImplementedError


class CatalogsMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Каталог+')
    STATE = 'catalogs'

    def callback(self, bot, update):
        catalogs = bot_models.TypeBook.objects.exclude(hidden=True)
        if not catalogs.exists():
            update.effective_message.reply_text('Нажаль немає каталогів', reply_markup=keyboards.main_keyboard())
            return False
        keyboards_markup = [
            InlineKeyboardButton(
                catalog['name'], callback_data=CatalogsCallback.set_callback_data(id=catalog['id'])
            ) for catalog in catalogs.values('id', 'name')
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text('Виберіть цікавий вам каталог.', reply_markup=reply_markup)
        return True


class TopBooksMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Топ-10 книг+')
    STATE = 'top-10-books'

    def callback(self, bot, update):
        top_books = bot_models.Book.get_top_books(limit=10)
        if not top_books.exists():
            update.effective_message.reply_text('Нажаль немає популярних книг',
                                                reply_markup=keyboards.main_keyboard())
            return False
        keyboards_markup = [
            InlineKeyboardButton(
                book['name'], callback_data=BookInfoCallback.set_callback_data(id=book['id'])
            ) for book in top_books.values('id', 'name')
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text('Виберіть цікаву вам книжку.', reply_markup=reply_markup)
        return True


class TopPurchaseBooksMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Топ-10 продажів+')
    STATE = 'top-10-purchase-books'

    def callback(self, bot, update):
        top_books = bot_models.Book.get_top_purchase_books(limit=10)
        if not top_books.exists():
            update.effective_message.reply_text('Нажаль немає популярних проданих книг',
                                                reply_markup=keyboards.main_keyboard())
            return False
        keyboards_markup = [
            InlineKeyboardButton(
                book['name'], callback_data=BookInfoCallback.set_callback_data(id=book['id'])
            ) for book in top_books.values('id', 'name')
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text('Виберіть цікаву вам книжку.', reply_markup=reply_markup)
        return True


class NewBooksMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Новинки+')
    STATE = 'new-books'

    def callback(self, bot, update):
        top_books = bot_models.Book.get_new_books(limit=6)
        if not top_books.exists():
            update.effective_message.reply_text('Нажаль немає нових книг.',
                                                reply_markup=keyboards.main_keyboard())
            return False
        keyboards_markup = [
            InlineKeyboardButton(
                book['name'], callback_data=BookInfoCallback.set_callback_data(id=book['id'])
            ) for book in top_books.values('id', 'name')
        ]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text('Виберіть цікаву вам книжку.', reply_markup=reply_markup)
        return True


class UserBooksMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Мої книги+')
    STATE = 'user-books'

    def callback(self, bot, update):
        user = bot_models.TelegramUser.get_user(update.effective_message.from_user)
        books_list = bot_models.Book.get_user_books(user)
        if not books_list.exists():
            update.effective_message.reply_text('Нажаль у вас немає куплених книг.',
                                                reply_markup=keyboards.main_keyboard())
            return False
        books_paginator = Paginator(books_list, 5)
        books = books_paginator.get_page(1).object_list
        reply_markup = UserBooksCallback.get_reply_markup(books, books_paginator, page=1)
        update.effective_message.reply_text('Виберіть книгу, яка вам цікава.', reply_markup=reply_markup)
        return True


class BasketMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Корзина+')
    STATE = 'baskets'

    def callback(self, bot, update):
        user = bot_models.TelegramUser.get_user(update.effective_message.from_user)
        basket = bot_models.Basket.get_basket_user(user)
        list_basket = basket.get_list_basket()
        if not list_basket.exists():
            update.effective_message.reply_text('Корзина пуста, додайте книжку в корзинку',
                                                reply_markup=keyboards.main_keyboard())
            return False
        keyboards_markup = []
        text = 'Ваша корзина (сума - {} грн.): \n'.format(list_basket[0].basket_id.total_price)
        for index, item in enumerate(list_basket):
            text += '{}. {} - {} грн.\n'.format(index + 1, item.book_id.name, item.price)
            keyboards_markup.append(
                InlineKeyboardButton(
                    item.book_id.name, callback_data=BookInfoCallback.set_callback_data(id=item.book_id.id)
                )
            )
        keyboards_markup = keyboards.build_menu(keyboards_markup, cols=1)
        keyboards_markup.append(keyboards.basket_button(user, basket))
        reply_markup = InlineKeyboardMarkup(keyboards_markup)
        update.effective_message.reply_text(text, reply_markup=reply_markup)
        return True


class SuccesfulPaymentMessage(BaseMessageHandler):
    COMMAND = Filters.successful_payment
    STATE = 'successful_payment'

    def callback(self, bot, update):

        update.message.reply_text("Thank you for your payment!")
        return True


def unknown(bot, update):
    text = 'Незрозуміла команда. Спробуйте ще раз. ️😊'
    update.message.reply_text(text)
    return 'unknown'


unknown_message = MessageHandler(Filters.all, unknown)
