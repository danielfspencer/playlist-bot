from . import logging
logging.init()
from . import config
config.init()

from . import bot
from . import spotify

def init():
    spotify.init()
    bot.start()
