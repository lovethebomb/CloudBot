import re
from util   import hook
from random import choice


hello_re = (r'(^(hello|hi|bonjour|salut|hey|plop|pouet|yo).?.?$)', re.I)
back_re  = (r'(^(back|re|me revoila|bk).?$)',                      re.I)
shake_re = (r'(^(\\o/|\\o\\|/o/|\|\\o/\|).?$)',                    re.I)

@hook.regex(*hello_re)
def greet(match, nick = None):
    greets = ["Hello", "Pouet", "plop", "Salut", "Yo", "Wassup", "Bonjour", "Hallo", "Hola", "Bonjourno", "Moin moin"]
    
    return '{greet!s} {nick!s}!'.format(nick = nick, greet = choice(greets))


@hook.regex(*back_re)
def welcomeback(match, nick = None):
    greets = ["Welcome back", "re",  "re-bienvenu", "wb"]
    
    return '{greet!s} {nick!s}!'.format(nick = nick, greet = choice(greets))


@hook.regex(*shake_re)
def shake(match):
    greets = ["\o/", "/o/", "\o\\", "|\o/|"]
    
    return '{greet!s}'.format(greet = choice(greets))
	
