from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters
from bot.handlers.callbacks import CatalogsCallback, BookInfoCallback
from bot import models as bot_models
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
        keyboards_markup = [
            InlineKeyboardButton(
                catalog['name'], callback_data=CatalogsCallback.set_callback_data(catalog['id'])
            ) for catalog in catalogs.values('id', 'name')]
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text('Виберіть цікавий вам каталог.', reply_markup=reply_markup)
        return True


class BasketMessage(BaseMessageHandler):
    COMMAND = Filters.regex('^Корзина+')
    STATE = 'catalogs'

    def callback(self, bot, update):
        user = bot_models.TelegramUser.get_user(update.effective_message.from_user)
        list_basket = bot_models.ListBasket.objects.filter(basket_id__telegram_user_id=user.id, basket_id__is_active=True)
        if not list_basket.exists():
            update.effective_message.reply_text('Корзина пуста, додайте книжку в корзинку',
                                                reply_markup=keyboards.main_keyboard())
            return False
        keyboards_markup = []
        text = 'Ваша корзина ({} грн.): \n'.format(list_basket[0].basket_id.total_price)
        for index, item in enumerate(list_basket):
            text += '{}. {} - {}\n'.format(index + 1, item.book_id.name, item.price)
            keyboards_markup.append(
                InlineKeyboardButton(
                    item.book_id.name, callback_data=BookInfoCallback.set_callback_data(item.book_id.id)
                )
            )
        reply_markup = InlineKeyboardMarkup(keyboards.build_menu(keyboards_markup))
        update.effective_message.reply_text(text, reply_markup=reply_markup)
        return True


def unknown(bot, update):
    text = 'Незрозуміла команда. Спробуйте ще раз. ️😊'
    update.message.reply_text(text)
    return 'unknown'


unknown_message = MessageHandler(Filters.all, unknown)
