"""
nein.py written by lovethebomb fur the funz"
initial credit hubot script
https://github.com/github/hubot-scripts/blob/master/src/scripts/ackbar.coffee
"""

from re import match
from util import hook
from random import choice


@hook.singlethread
@hook.event('PRIVMSG')
def ackbar(paraml, input=None, say=None):
    ackbars = [
        "http://dayofthejedi.com/wp-content/uploads/2011/03/171.jpg",
        "http://farm5.staticflickr.com/4074/4751546688_5c76b0e308_z.jpg",
        "http://farm6.staticflickr.com/5250/5216539895_09f963f448_z.jpg"
    ]

    if match("^it'?s a trap", input.msg.lower()):
        say("%s" % choice(ackbars))
