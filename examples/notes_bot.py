from flowbot import FlowBot
from flowbot.decorators import mentioned


class NotesBot(FlowBot):

    def commands(self):
        return {
            '/new': self.save_note,
            '/last': self.show_last_note
        }

    @mentioned
    def save_note(self, message):
        """Save the note in the channel db."""
        self.channel_db.new('note', message['data']['text'])
        self.reply(message, "Your note has been saved!")

    @mentioned
    def show_last_note(self, message):
        """Show the last known note from the channel db."""
        last_note = self.channel_db.get('note')[-1]
        self.reply(message, last_note)
