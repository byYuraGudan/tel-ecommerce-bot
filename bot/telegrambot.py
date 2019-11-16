import logging
from telegram.ext import PicklePersistence
from django_telegrambot.apps import DjangoTelegramBot

logger = logging.getLogger(__name__)


def main():
    logger.info("Loading handlers for telegram bot")
    persistence = PicklePersistence('persistence.pickle')
    dp = DjangoTelegramBot.dispatcher
    dp.persistence = persistence