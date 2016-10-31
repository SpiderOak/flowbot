from flow import Flow
import logging

LOG = logging.getLogger(__name__)


class Server(object):
    """A connection to Flow."""

    def __init__(self, config):
        """Initialize a flow server instance."""
        self.config = config

        self.flow = Flow(
            server_uri=config.uri,
            flowappglue=config.flowappglue,
            host=config.host,
            port=config.port,
            schema_dir=config.schema_dir,
            db_dir=config.db_dir,
            attachment_dir=config.attachment_dir,
            use_tls=config.use_tls,
            glue_out_filename=config.glue_out_filename,
            decrement_file=config.decrement_file
        )

        if not self._start_server():
            if not self._setup_device():
                self._setup_account()

        self._setup_org()
        self._set_profile()

    def _start_server(self):
        """Attempt to start the flow server."""
        try:
            self.flow.start_up(username=self.config.username)
            LOG.info("local account '%s' started", self.config.username)
            return True
        except Flow.FlowError as start_up_err:
            LOG.debug("start_up failed: '%s'", str(start_up_err))

    def _setup_device(self):
        """Create a device for an existing account."""
        try:
            self.flow.create_device(
                username=self.config.username,
                password=self.config.password
            )
            return True
        except Flow.FlowError as create_device_err:
            LOG.debug("Create device failed: '%s'", str(create_device_err))

    def _setup_account(self):
        """Create an account, if it doesn't already exist."""
        try:
            self.flow.create_account(
                username=self.config.username,
                password=self.config.password,
                email_confirm_code=self.config.email_confirm_code,
            )
        except Flow.FlowError as create_account_err:
            LOG.debug("Create account failed: '%s'", str(create_account_err))

    def _setup_org(self):
        """"Join the org if not already a member."""
        try:
            self.flow.new_org_join_request(oid=self.config.org_id)
        except Flow.FlowError as org_join_err:
            LOG.debug("org join failed: '%s'", str(org_join_err))

    def _set_profile(self):
        """Set the user profile based on the items passed in the config."""
        profile = self.flow.get_profile_item_json(
            display_name=getattr(self.config, 'display_name', None),
            biography=getattr(self.config, 'biography', None),
            photo=getattr(self.config, 'photo', None),

        )
        self.flow.set_profile('profile', profile)
