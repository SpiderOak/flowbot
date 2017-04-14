"""settings.py - Configuration model for FlowBot."""
from flow import definitions
import base64


class ImproperlyConfigured(object):
    """Raise when the settings dictionary passed is improper."""

    pass


class Config(object):
    """The configuration settings for a bot."""

    def __init__(self, settings):
        """Create Config object from a settings dictionary."""
        self.username = self.get_or_raise(settings, 'username')
        self.password = self.get_or_raise(settings, 'password')
        self.email_confirm_code = settings.get('email_confirm_code', None)
        self.org_id = self.get_or_raise(settings, 'org_id')

        self.display_name = settings.get('display_name', None)
        self.biography = settings.get('biography', None)
        self.photo = self.get_photo(settings)

        self.message_age_limit = self.get_message_age(settings)
        self.db_channel = settings.get('db_channel', 'FLOWBOT_DB_CHANNEL')
        self.db_keys = settings.get('db_keys', [])
        self.flowappglue = settings.get('flowappglue', "")
        self.uri = settings.get('uri', definitions.DEFAULT_URI)
        self.host = settings.get('host', definitions.DEFAULT_SERVER)
        self.port = settings.get('port', definitions.DEFAULT_PORT)
        self.db_dir = settings.get('db_dir', definitions.get_default_db_path())  # NOQA
        self.schema_dir = settings.get('schema_dir', "")
        self.attachment_dir = settings.get('attachment_dir', definitions.get_default_attachment_path())  # NOQA
        self.use_tls = settings.get('use_tls', definitions.DEFAULT_USE_TLS)
        self.decrement_file = settings.get('decrement_file', None)

        self.extra_config = settings.get("extra_config", {})

    def get_or_raise(self, settings, key):
        """Return the settings value or raise 'ImproperlyConfigured'."""
        if key not in settings:
            raise ImproperlyConfigured('Missing setting: %s' % key)
        return settings.get(key)

    def get_message_age(self, settings):
        """The message age limit is an integer number of seconds."""
        message_age_limit = settings.get('message_age_limit', 2 * 60)
        if type(message_age_limit) != int:
            raise ImproperlyConfigured(
                'Message age limit should be integer number of seconds.')
        return message_age_limit

    def get_photo(self, settings):
        """Return a base64 image URI based on image path in settings."""
        path = settings.get('photo', None)

        if path:
            with open(path, "rb") as image_file:
                image_raw_data = image_file.read()
            return "data:image/png;base64,%s" % (
                base64.b64encode(image_raw_data),
            )
        return None
