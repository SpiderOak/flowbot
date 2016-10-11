"""ChannelDb impelements a "Channel as a Database" service for bot use."""
import json

from . import settings


class ChannelDb(object):
    """Flow Channel as a Database."""

    def __init__(self, server):
        """Initialize the channel db using the server connection passed."""
        self.server = server
        self.account_id = self.server.flow.account_id()
        self._data = self._get_all(settings.PREFETCH_KEYS)

    def get(self, key):
        """Get all records for the given key in the channel database.

        If the key has already been loaded into memory (self._data) then just
        fetch it from there. Otherwise, do a search for the key in the
        db-channel.
        """
        if key in self._data:
            return self._data[key]

        messages = self.server.flow.search(
            oid=settings.ORG_ID,
            cid=self._get_db_channel_id(),
            search=key)

        return self._get_data_from_messages(messages, key)

    def new(self, key, value):
        """Save a new record in both memory (self._data) and the db-channel."""
        self._data.setdefault(key, []).append(value)

        self.server.flow.send_message(
            cid=self._get_or_create_db_channel(),
            oid=settings.ORG_ID,
            msg=json.dumps({key: value})
        )

    def _get_all(self, keys):
        """Load records for each of the given keys into a dict."""
        data = {}
        if keys:
            for key in keys:
                data[key] = self.get(key)
        return data

    def _get_data_from_messages(self, messages, key):
        """Retrieve records with the given key saved in the set of messages."""
        data = []
        for message in messages:
            try:
                if self._is_author(message):
                    message_text = json.loads(message['data']['text'])
                    data.append(message_text[key])
            except:
                pass
        return data

    def _get_or_create_db_channel(self):
        """Get or create the db channel."""
        config_channel_id = self._get_db_channel_id()

        if not config_channel_id:
            config_channel_id = self._create_db_channel()

        return config_channel_id

    def _get_db_channel_id(self):
        """Determine if the db channel already exists."""
        for channel in self.server.flow.enumerate_channels(settings.ORG_ID):
            if channel['name'] == settings.DB_CHANNEL_NAME:
                return channel['id']
        return None

    def _create_db_channel(self):
        """Create a db channel for the given org."""
        return self.server.flow.new_channel(
            settings.ORG_ID, settings.DB_CHANNEL_NAME)

    def _is_author(self, message):
        """Determine if the bot is the author of this message."""
        return message['data']['senderAccountId'] == self.account_id
