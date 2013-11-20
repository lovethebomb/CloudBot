import re
from util import hook
from random import choice


hello_re = (r'(^(hello|hi|bonjour|salut|hey|plop|pouet|yo).?.?$)', re.I)
back_re = (r'(^(back|re|me revoila|bk).?$)', re.I)
shake_re = (r'(^(\\o/|\\o\\|/o/|\|\\o/\|).?$)', re.I)

@hook.regex(*hello_re)
def greet(match, nick=None, say=None):
    greets = ["Hello", "Pouet", "plop", "Salut", "Yo", "Wassup", "Bonjour", "Hallo", "Hola", "Bonjourno", "Moin moin"]
    say("%s %s!" % (choice(greets), nick))


@hook.regex(*back_re)
def welcomeback(match, nick=None, say=None):
    greets = ["Welcome back", "re", "re-bienvenu", "wb"]
    say("%s %s!" % (choice(greets), nick))


@hook.regex(*shake_re)
def shake(match, say=None):
    greets = ["\o/", "/o/", "\o\\", "|\o/|"]
    say("%s" % choice(greets))
