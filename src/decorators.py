from functools import wraps


def mentioned(bot_command):
    """Only execute the decorated bot command if the bot was mentioned."""
    @wraps(bot_command)
    def _func(bot, message, *args, **kwargs):
        if bot.mentioned(message):
            return bot_command(bot, message, *args, **kwargs)
    return _func


def admin_only(bot_command):
    """Only execute the decorated bot command if the user is an admin."""
    @wraps(bot_command)
    def _func(bot, message, *args, **kwargs):
        if bot.from_admin(message):
            return bot_command(bot, message, *args, **kwargs)
    return _func
