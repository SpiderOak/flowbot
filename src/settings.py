"""Configure your bot here.

By default, all settings should be set as environment parameters which are read
into the key below.
"""
import os


USERNAME = os.environ.get('FLOWBOT_USERNAME', '')
PASSWORD = os.environ.get('FLOWBOT_PASSWORD', '')
ORG_ID = os.environ.get('FLOWBOT_ORG_ID', '')
DB_CHANNEL_NAME = os.environ.get('FLOWBOT_DB_CHANNEL_NAME', '')

# Prefetch keys trigger loading of db records into memory at startup. This way
# we don't have to do a message search of the db channel every request.
# Example evn:
#     export FLOWBOT_PREFETCH_KEYS=hello,world

_prefetch_keys = os.environ.get('FLOWBOT_PREFETCH_KEYS', '')
_prefetch_keys = _prefetch_keys.replace(' ', '')
PREFETCH_KEYS = _prefetch_keys.split(',') if _prefetch_keys else None
