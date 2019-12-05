from telegram import *

from bot.handlers.callbacks import BasketAddItem, BasketRemoveItem

clear = ReplyKeyboardRemove()


def main_keyboard():
    keyboards = ['Каталог 📚', 'Корзина 🛒']  # ['Новинки 🆘🆕', 'Топ книжок ‼️🔥', 'Каталог 📚', 'Корзина 🛒']
    return ReplyKeyboardMarkup(build_menu(keyboards), resize_keyboard=True)


def build_menu(buttons, cols=2, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + cols] for i in range(0, len(buttons), cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def build_keyboard_markup(buttons, **kwargs):
    return ReplyKeyboardMarkup(build_menu(buttons, **kwargs), resize_keyboard=True)


def build_paginator(paginator, current_page, callback, data, max_page=5):
    keyboards = list()
    previous_page = current_page - 1 if current_page > 2 else 1
    next_page = current_page + 1 if current_page < paginator.num_pages else current_page
    keyboards.append(
        InlineKeyboardButton('⬅️', callback_data=callback.set_callback_data(**data, page=previous_page))
    )
    keyboards.extend([
        InlineKeyboardButton('{}*'.format(page) if page == current_page else page,
                             callback_data=callback.set_callback_data(**data, page=page))
        for page in paginator.page_range
    ])
    keyboards.append(
        InlineKeyboardButton('➡️', callback_data=callback.set_callback_data(**data, page=next_page))
    )
    return keyboards


def get_button_by_user(book, user):
    book_state = book.check_book_in_basket(user)
    if book_state is None:
        return InlineKeyboardButton('Додати до корзини',
                                    callback_data=BasketAddItem.set_callback_data(id=book.id))
    if not book_state:
        return InlineKeyboardButton('Видалити з корзини',
                                    callback_data=BasketRemoveItem.set_callback_data(id=book.id))
    return InlineKeyboardButton('Завантажити книгу', callback_data='download_book')
