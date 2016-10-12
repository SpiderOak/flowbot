from unittest import TestCase
from mock import patch

from flowbot.channel_db import ChannelDb
from flowbot.tests.mocks import MockServer


class TestChannelDb(TestCase):
    """Test the ChannelDb object."""

    def init_channel_db(self):
        """Initialize a channel_db with some mocked bits."""
        with patch.object(ChannelDb, '__init__') as init:
            init.return_value = None
            cdb = ChannelDb()
            cdb.account_id = 1
            cdb._data = {}
            cdb.server = MockServer()
        return cdb

    def test_get_from_memory(self):
        """Get should first look at self._data for values."""
        cdb = self.init_channel_db()
        cdb._data = {'hello': 'world'}
        self.assertEqual(cdb.get(key='hello'), 'world')

    def test_get_from_search(self):
        """If a key doesn't exist in self._data, search the db channel."""
        cdb = self.init_channel_db()

        with patch.object(cdb.server.flow, 'search') as search:
            search.return_value = [
                {
                    'data': {
                        'text': '{"hello": "world"}',
                        'senderAccountId': 1
                    }
                }
            ]
            with patch.object(cdb, '_get_db_channel_id') as get_db_channel_id:
                get_db_channel_id.return_value = 1
                result = cdb.get(key='hello')
            self.assertTrue(search.called)
            self.assertEqual(result[0], 'world')

    def test_get_multiple_records(self):
        """Attempt to get multiple records of the same key."""
        cdb = self.init_channel_db()

        with patch.object(cdb.server.flow, 'search') as search:
            search.return_value = [
                {
                    'data': {
                        'text': '{"hello": "world"}',
                        'senderAccountId': 1
                    }
                },
                {
                    'data': {
                        'text': '{"hello": "foo_bar"}',
                        'senderAccountId': 1
                    }
                }
            ]
            with patch.object(cdb, '_get_db_channel_id') as get_db_channel_id:
                get_db_channel_id.return_value = 1
                result = cdb.get(key='hello')
            self.assertTrue(search.called)
            self.assertEqual(result[0], 'world')
            self.assertEqual(result[-1], 'foo_bar')

    def test_is_author_true(self):
        """A message with the same author id as the account."""
        fake_message = {
            'data': {
                'senderAccountId': 1
            }
        }
        cdb = self.init_channel_db()
        self.assertTrue(cdb._is_author(fake_message))

    def test_is_author_false(self):
        """A message with a different author id as the account."""
        fake_message = {
            'data': {
                'senderAccountId': 2
            }
        }
        cdb = self.init_channel_db()
        self.assertFalse(cdb._is_author(fake_message))

    def test_get_all(self):
        """Get all should return a dict with the values for the given keys."""
        cdb = self.init_channel_db()

        # We can bypass flow_search by just seeding the _data object with
        # pre-made data.
        cdb._data = {
            'hello': 'world',
            'foo': 'bar',
            'something': 'else'
        }
        result = cdb._get_all(keys=['hello', 'foo'])
        self.assertDictEqual(result, {
            'hello': 'world',
            'foo': 'bar'
        })

    def test_new_record(self):
        """Create a new record."""
        cdb = self.init_channel_db()
        with patch.object(cdb.server.flow, 'send_message') as send_message:
            with patch.object(cdb, '_get_or_create_db_channel'):
                cdb.new('hello', 'world')
            self.assertTrue(send_message.called)

        self.assertEqual(cdb._data['hello'][0], 'world')
