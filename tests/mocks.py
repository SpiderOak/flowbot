class MockFlow(object):
    """A Mock Flow object."""
    def search(self):
        pass

    def send_message(self):
        pass


class MockServer(object):
    """A Mock Server object."""
    def __init__(self):
        self.flow = MockFlow()
