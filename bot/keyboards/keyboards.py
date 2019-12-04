from telegram import *

from bot.handlers.callbacks import BasketAddItem, BasketRemoveItem

clear = ReplyKeyboardRemove()


def main_keyboard():
    keyboards = ['Каталог 📚', 'Корзина 🛒']  # ['Новинки 🆘🆕', 'Топ книжок ‼️🔥', 'Каталог 📚', 'Корзина 🛒']
    return ReplyKeyboardMarkup(build_menu(keyboards), resize_keyboard=True)


def build_menu(buttons, n_cols=2, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def build_keyboard_markup(buttons, **kwargs):
    return ReplyKeyboardMarkup(build_menu(buttons, **kwargs), resize_keyboard=True)


def get_button_by_user(book, user):
    book_state = book.check_book_in_basket(user)
    if book_state is None:
        return InlineKeyboardButton('Додати до корзини',
                                   callback_data=BasketAddItem.set_callback_data(book.id))
    if not book_state:
        return InlineKeyboardButton('Видалити з корзини',
                                    callback_data=BasketRemoveItem.set_callback_data(book.id))
    return InlineKeyboardButton('Завантажити книгу', callback_data='download_book')