from bot.handlers import commands, messages, conversations
from utils.utils import inheritors

all_command_handlers = [command for command in inheritors(commands.BaseCommandHandler)]
all_message_handlers = [message for message in inheritors(messages.BaseMessageHandler)]
all_conversation_handlers = [conversation for conversation in inheritors(conversations.BaseConversationHandler)]
