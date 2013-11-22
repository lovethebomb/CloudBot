"""
ackbar.py written by lovethebomb fur the funz"
initial credit hubot script
https://github.com/github/hubot-scripts/blob/master/src/scripts/ackbar.coffee
"""

from re     import match
from util   import hook
from random import choice


@hook.singlethread
@hook.event('PRIVMSG')
def nein(paraml, input=None, nick=None):
    nein = [
        "http://www.youtube.com/watch?feature=player_detailpage&v=1MLry6Cn_D4",
        "http://www.youtube.com/watch?v=kQeKskCvJwc",
        "http://www.youtube.com/watch?feature=player_detailpage&v=h4se9_vexUM",
        "http://www.youtube.com/watch?v=8n4_BxQlCFg",
        "http://www.youtube.com/watch?v=bj2KSiEeCcM",
        "http://www.youtube.com/watch?v=ILtxKWHrGyQ",
        "http://www.youtube.com/watch?v=sLs19nIikwQ",
    ]

    if match(".* nein", input.msg.lower()):
        return 'Ach, {nick!s}! {url!s}'.format(nick = nick, url = choice(nein))
