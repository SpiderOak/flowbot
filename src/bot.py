"""bot.py - implements the FlowBot class, a boilerplate for other bots."""
from .channel_db import ChannelDb
from .server import Server
from .config import Config
import logging

LOG = logging.getLogger(__name__)


class FlowBot(object):
    """A boilerplate for bot development."""

    def __init__(self, settings):
        """Initialize the bot with an active flow instance."""
        self.config = Config(settings)
        self.server = Server(self.config)
        self.account_id = self.server.flow.account_id()
        self._commands = self._register_commands()
        self.channel_db = ChannelDb(self.server, self.config)

        @self.server.flow.message
        def _handle_message(notification_type, message):
            self.handle_message(notification_type, message)

    def run(self):
        """Run the bot."""
        try:
            LOG.info('FlowBot is starting up...')
            self.server.flow.process_notifications()
        except(KeyboardInterrupt, SystemExit):
            LOG.info('FlowBot is shutting down...')
        self.server.flow.terminate()

    def reply(self, original_message, response_msg):
        """Reply to the original message in the same channel."""
        self.server.flow.send_message(
            cid=original_message.get('channelId'),
            oid=self.config.org_id,
            msg=response_msg
        )

    def handle_message(self, notification_type, message):
        """Handle an incoming flow message."""
        for m in message.get('regularMessages', []):
            self._process_commands(m)

    def mentioned(self, message):
        """Determine if this bot was mentioned in the message."""
        username_mention = '@' + self.config.username.lower()
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
                    command(message)
