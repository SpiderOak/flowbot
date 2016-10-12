from flow import Flow
import logging

from . import settings

LOG = logging.getLogger(__name__)


class Server(object):
    """A connection to Flow."""

    def __init__(self):
        """Initialize a flow server instance."""
        self.flow = Flow()

        if not self._start_server():
            self._setup_account_and_start_server()

        self._setup_org()

    def _start_server(self):
        """Attempt to start the flow server."""
        try:
            self.flow.start_up(username=settings.USERNAME)
            LOG.info("local account '%s' started", settings.USERNAME)
            return True
        except Flow.FlowError as start_up_err:
            LOG.debug("start_up failed: '%s'", str(start_up_err))

    def _setup_account_and_start_server(self):
        """Create an account, if it doesn't already exist."""
        try:
            self.flow.create_account(
                username=settings.USERNAME,
                password=settings.PASSWORD
            )
        except Flow.FlowError as create_account_err:
            LOG.debug("Create account failed: '%s'", str(create_account_err))

    def _setup_org(self):
        """"Join the org if not already a member."""
        try:
            self.flow.new_org_join_request(oid=settings.ORG_ID)
        except Flow.FlowError as org_join_err:
            LOG.debug("org join failed: '%s'", str(org_join_err))
