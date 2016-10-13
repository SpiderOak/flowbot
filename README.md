# flowbot-barebones
A boilerplate for quickly prototyping Flow (Semaphor) Bots!

## Install
Make sure both `flow-python` and `flowbot-barebones` are installed in your environment: 
```
pip install git+git://github.com/SpiderOak/flow-python.git@master
pip install git+git://github.com/SpiderOak/flowbot-barebones.git@master
```

> NOTE: While this is a private repo you will need to use `git+ssh`
```
pip install git+ssh://git@github.com/SpiderOak/flowbot-barebones.git@master
```

## Usage
Create a new bot class that inherits the FlowBot class. If you want your bot to respond to messages, you must implement the `commands` method which should return a dict that maps a trigger word to a method that accepts the triggering-message as a parameter. 

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

## Bot Settings
When you initiate a FlowBot, you can provide some or all of the following settings
- `username` (required): the username of your bot, if it doesn't exist yet, it will be created
- `password` (required): the password of your bot
- `org_id`(required): the id of the team you want your bot to be a member of
- `db_keys`: if you wish to take advantage of the channel-as-a-db service, this is a list of keys that should be pre-fetched from that channel on bot startup
- `db_channel`: the name of the db-channel, if you leave this blank the bot will create a random channel name


## Example Bots
1. https://github.com/SpiderOak/flowbot-respondbot