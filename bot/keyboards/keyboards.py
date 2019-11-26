from telegram import *


def main_keyboard():
    keyboards = [
        ['Новинки 🆘🆕', 'Топ книжок ‼️🔥'],
        ['Жанри книг 📚'],
        ['Корзина 🛒']
    ]
    return ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
