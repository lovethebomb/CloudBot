# -*- coding: utf-8 -*-
import re
import datetime
from calendar import monthrange
from util     import hook
from random   import choice


hello_re = (r'(^(hello|morgen|goedemorgen|hi|bonjour|salut|hey|plop|pouet|yo).?.?$)', re.I)
back_re  = (r'(^(back|re|me revoila|bk).?$)',                      re.I)
shake_re = (r'(^(\\o/|\\o\\|/o/|\|\\o/\|).?$)',                    re.I)
hehe_re  = (r'(^((h+e+)+).?$)',                                    re.I)
krkr_re  = (r'(^((k+r+)+).?$)',                                    re.I)

@hook.regex(*hello_re)
def greet(match, nick = None):
    today               = datetime.date.today()
    first_day, last_day = monthrange(today.year, today.month)

    greets  = ["Hello", "Pouet", "plop", "Salut", "Yo", "Wassup", "Bonjour", "Hallo", "Hola", "Bonjourno", "Moin moin"]
    
    message = u'{greet!s} {nick!s}!'.format(nick = nick, greet = choice(greets))

    if (last_day - today.day) < 2:
        message += u" Aujourd'hui c'est actualisation Pôle emploi \o/"
    
    if today.day < 3:
		message += u" Il encore temps de s'actualiser àPôle emploi :3"
     
    return message


@hook.regex(*back_re)
def welcomeback(match, nick = None):
    greets = ["Welcome back", "re",  "re-bienvenu", "wb"]
    
    return '{greet!s} {nick!s}!'.format(nick = nick, greet = choice(greets))


@hook.regex(*shake_re)
def shake(match):
    greets = ["\o/", "/o/", "\o\\", "|\o/|"]
    
    return '{greet!s}'.format(greet = choice(greets))
	

@hook.regex(*hehe_re)
def hehe(match, nick = None):
    url = 'http://i.imgur.com/1gOMM.jpg'
    
    return 'hhhehehe {nick!s} {url!s}'.format(url = url, nick = nick)
	

@hook.regex(*krkr_re)
def krkr(match, nick = None):
    url = 'http://i.imgur.com/ph9k7os.gif'
    
    return 'krkrkr {nick!s} {url!s}'.format(url = url, nick = nick)
	
