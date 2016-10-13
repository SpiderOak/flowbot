"""settings.py - Configuration model for FlowBot."""
import uuid
from flow import definitions


class ImproperlyConfigured(object):
    """Raise when the settings dictionary passed is improper."""

    pass


class Config(object):
    """The configuration settings for a bot."""

    def __init__(self, settings):
        """Create Config object from a settings dictionary."""
        self.username = self.get_or_raise(settings, 'username')
        self.password = self.get_or_raise(settings, 'password')
        self.org_id = self.get_or_raise(settings, 'org_id')
        self.db_channel = settings.get('db_channel', self.random_db_channel())
        self.db_keys = settings.get('db_keys', [])
        self.flowappglue = settings.get('flowappglue', definitions.get_default_flowappglue_path())  # NOQA
        self.uri = settings.get('uri', definitions.DEFAULT_URI)
        self.host = settings.get('host', definitions.DEFAULT_SERVER)
        self.port = settings.get('port', definitions.DEFAULT_PORT)

    def get_or_raise(self, settings, key):
        """Return the settings value or raise 'ImproperlyConfigured'."""
        if key not in settings:
            raise ImproperlyConfigured('Missing setting: %s' % key)
        return settings.get(key)

    def random_db_channel(self):
        """Return a random db channel name."""
        return 'BOT_DB_CHANNEL::%s' % (uuid.uuid4().hex)
