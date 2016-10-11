from flowbot import FlowBot
from flowbot.decorators import mentioned, admin_only


class RespondBot(FlowBot):

    def commands(self):
        return {
            '/hello': self.hello_response,
            '/coolio': self.coolio_msg
        }

    @mentioned
    def hello_response(self, message):
        """Respond to to the message with 'Hello!'."""
        self.reply(message, "Hello!")

    @admin_only
    def coolio_msg(self, message):
        """Respond to the message with a Coolio lyric."""
        self.reply(message, "Come on y'all let's take a ride...")
