from .channel_db import ChannelDb
from .server import Server
from . import settings


class FlowBot(object):

    def __init__(self):
        """Initialize the bot with an active flow instance."""
        self.server = Server()
        self.account_id = self.server.flow.account_id()
        self._commands = self._register_commands()
        self.channel_db = ChannelDb(self.server)

    def reply(self, response_msg, original_message):
        """Reply to the original message in the same channel."""
        self.server.flow.send_message(
            cid=original_message.get('channelId'),
            oid=settings.ORG_ID,
            msg=response_msg
        )

    def mentioned(self, message):
        """Determine if this bot was mentioned in the message."""
        username_mention = '@' + settings.FLOWBOT_USERNAME.lower()
        return username_mention in message.get('text', '').lower()

    def from_admin(self, message):
        """Determine if this message was sent from an admin of the org."""
        if message['senderAccountId'] == self.account_id:
            return False

        for member in self.server.flow.enumerate_channel_members(message['channelId']):  # NOQA
            if member['accountId'] == message['senderAccountId']:
                if member['state'] in ['o', 'a']:
                    return True
        return False

    def _is_author(self, message):
        """Determine if the bot is the author of this message."""
        return message['senderAccountId'] == self.account_id

    def commands(self):
        """Override this method to provide customer commands.

        Returns a dict where the key is the command trigger and the value is
        a function which accepts the message as a parameter.
        """
        return {}

    def _register_commands(self):
        """Register the given commands to this bot.

        Expects a dictionary where the key is the command trigger and the value
        is the function which processes the message.
        """
        commands = []
        for commandKey, commandFunc in self.commands().iteritems():
            commands.append((commandKey, commandFunc))
        return commands

    def _process_commands(self, message):
        """Detect and execute commands within the message."""
        if not self._is_author(message):
            message_text = message.get('text', '')
            for match, command in self._commands:
                if match in message_text:
                    return command(message)
