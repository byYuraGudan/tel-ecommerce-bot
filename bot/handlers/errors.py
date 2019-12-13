import logging

logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    ignore_error = ('Message is not modified')
    if str(error).startswith(ignore_error):
        return True
    logger.warning('Update "%s" caused error "%s"' % (update, error))
