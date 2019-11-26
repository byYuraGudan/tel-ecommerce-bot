import logging

from django_telegrambot.apps import DjangoTelegramBot
from telegram.ext import PicklePersistence

from bot.handlers import all_command_handlers, all_message_handlers, all_conversation_handlers
from bot.handlers import errors as error_handlers
from bot.handlers.messages import unknown_message

logger = logging.getLogger(__name__)


def init_handler(dispatcher, *handlers):
    for handler in handlers:
        for item in handler:
            dispatcher.add_handler(item())


def main():
    logger.info("Loading handlers for telegram bot")
    # persistence = PicklePersistence('persistence.pickle')
    dp = DjangoTelegramBot.dispatcher
    # dp.persistence = persistence
    init_handler(dp, all_command_handlers, all_conversation_handlers, all_message_handlers)
    dp.add_handler(unknown_message)
    dp.add_error_handler(error_handlers.error)
