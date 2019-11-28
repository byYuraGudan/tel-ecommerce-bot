from telegram import *


def main_keyboard():
    keyboards = ['Каталог 📚'] #['Новинки 🆘🆕', 'Топ книжок ‼️🔥', 'Каталог 📚', 'Корзина 🛒']
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
