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
            port=config.port
        )

        if not self._start_server():
            self._setup_account_and_start_server()

        self._setup_org()

    def _start_server(self):
        """Attempt to start the flow server."""
        try:
            self.flow.start_up(username=self.config.username)
            LOG.info("local account '%s' started", self.config.username)
            return True
        except Flow.FlowError as start_up_err:
            LOG.debug("start_up failed: '%s'", str(start_up_err))

    def _setup_account_and_start_server(self):
        """Create an account, if it doesn't already exist."""
        try:
            self.flow.create_account(
                username=self.config.username,
                password=self.config.username
            )
        except Flow.FlowError as create_account_err:
            LOG.debug("Create account failed: '%s'", str(create_account_err))

    def _setup_org(self):
        """"Join the org if not already a member."""
        try:
            self.flow.new_org_join_request(oid=self.config.org_id)
        except Flow.FlowError as org_join_err:
            LOG.debug("org join failed: '%s'", str(org_join_err))
