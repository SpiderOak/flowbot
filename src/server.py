from flow import Flow
import logging

from . import settings

LOG = logging.getLogger("flowbot.server")


class Server(object):
    """A connection to Flow."""

    def __init__(self):
        """Initialize a flow server instance."""
        self.flow = Flow()

        self._start_server()
        self._setup_account()
        self._setup_device()

    def _start_server(self):
        """Attempt to start the flow server."""
        try:
            self.flow.start_up(username=settings.USERNAME)
            LOG.info("local account '%s' started", settings.USERNAME)
        except Flow.FlowError as start_up_err:
            LOG.debug("start_up failed: '%s'", str(start_up_err))

    def _setup_account(self):
        """Create an account, if it doesn't already exist."""
        self.flow.create_account(
            username=settings.USERNAME,
            password=settings.PASSWORD
        )

    def _setup_device(self):
        """Create a device if it doesn't already exist."""
        try:
            self.flow.create_device(
                username=settings.USERNAME,
                password=settings.PASSWORD
            )
            LOG.info("local Device for '%s' created", settings.USERNAME)
        except Flow.FlowError as create_device_err:
            LOG.debug("create_device failed: '%s'", str(create_device_err))
