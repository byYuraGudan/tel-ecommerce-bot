from telegram.ext import *


class BaseConversationHandler(ConversationHandler):
    STATE = None

    def __init__(self, *args, **kwargs):
        super(BaseConversationHandler, self).__init__(self.entry_points(), self.states(), self.fallbacks(), *args,
                                                      persistent=True, name=self.__class__.__name__, **kwargs)

    @property
    def states(self):
        raise NotImplementedError

    @property
    def entry_points(self):
        raise NotImplementedError

    @property
    def fallbacks(self):
        raise NotImplementedError
