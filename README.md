# flowbot-barebones
A boilerplate for quickly prototyping [Semaphor](https://spideroak.com/solutions/semaphor) Bots!

## Developing with `flowbot-barebones`
To build a bot with flowbot barebones, you first need to install `flow-python` and `flowbot-barebones` into your local environment. Until both of those repos are listed on pypi, just run these commands:

```
pip install git+git://github.com/SpiderOak/flow-python.git@master
pip install git+ssh://git@github.com/SpiderOak/flowbot-barebones.git@master
```

You can now import the boilerpate bot:

```python
from flobot import FlowBot
```

### Example Usage
Create a new bot class that inherits the `FlowBot` class. If you want your bot to respond to messages, you must implement the `commands` method which should return a dict that maps a trigger word to a method that accepts the triggering-message as a parameter. 

```python
# mybot.py
from flowbot import FlowBot


class MyBot(FlowBot):
    """MyBot just responds to 'hello' with 'Hello!'."""

    def commands(self):
        return {
            'hello': self.hello
        }

    def hello(self, message):
        """Respond to to the message with 'Hello!'."""
        self.reply(message, "Hello!")
```

Then create a run file that creates an instance of your bot with bot settings as a passed dictionary

```python
# runbot.py
from mybot import MyBot

if __name__ == "__main__":

    bot = MyBot({
        'username': 'mybotusername',
        'password': 'mybotpassword',
        'org_id': 'THEORGIDOFTHETEAMIWANTTHISBOTTOBELONGTO'
    })
    bot.run()
```

Now just run your bot!

```
python runbot.py
```

### Bot Settings
When you initiate a FlowBot, you can provide some or all of the following settings

- `username` (required): the username of your bot, if it doesn't exist yet, it will be created
- `password` (required): the password of your bot
- `org_id`(required): the id of the team you want your bot to be a member of
- `display_name`: the display name of your bot
- `biography`: the bot's bio,
- `photo`: a path to the photo to be used as the bot's avatar (e.g. `bot.png`)
- `db_keys`: if you wish to take advantage of the channel-as-a-db service, this is a list of keys that should be pre-fetched from that channel on bot startup
- `db_channel`: the name of the db-channel, if you leave this blank the bot will create a random channel name
- `message_age_limit`: ignore channel messages older than this number of seconds (integer). Default is 120.


### Public Methods

#### `reply(original_message, msg, highlight=None`
Reply to a flow message with the given response test. Optionally highlight a list of account_idss (will trigger a notification for those users in Semaphor).

#### `message_channel(channel_id, msg, highlight=None)`
Send a message to the given channel. Optionally highlithy a list of account_ids.


#### `message_all_channels(msg, highlight=None)`
Send a message to all channels this bot is a member of. Optionally highlithy a list of account_ids.

#### `mentioned(messsage, account_id)`
Determine if the account_id was mentioned in the given flow message. If no `account_id` was given, determine if this bot was mentioned.

#### `from_admin(message)`
Determine if the message was sent from an admin of the channel.

#### `channels()`
Returns a list of all channels this bot is a member of.

### Incoming Message Decorators
FlowBots can respond to any message in a channel, although you may only want the bot to focus on specific messages (i.e. Messages in which the bot's username was mentioned, or messages from an admin, etc.). FlowBot provides a couple useful decorators for handling these cases:

#### `@mentioned`
Only respond to a message if the bot was mentioned. For example:

```python
from flowbot import FlowBot
from flowbot.decorators import mentioned

class MyBot(FlowBot):
    def commands(self):
        return {
            'hello': self.hello
        }

    @mentioned
    def hello(self, message):
        """Respond to to the message with 'Hello!'."""
        self.reply(message, "Hello!")
```

In this example (above) `MyBot` responds to the trigger word `hello`, but only if the bot's username is mentioned in the message.

#### `@admin_only`
Only respond to a message if the message was sent by an admin of the channel. See the `mentioned` example above for usage, this decorator works in the same way.



## Example Bots
1. https://github.com/SpiderOak/flowbot-respondbot
2. https://github.com/SpiderOak/flowbot-github
3. https://github.com/SpiderOak/flowbot-twitter