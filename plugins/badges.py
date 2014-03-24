
from util        import ( hook, timesince )
from prettytable import PrettyTable

import time
import re
import types
import karma

class RoleEveryone(dict):

    def __contains__(self, item):
        return True

db_ready    = False
roles       = {
    'admin': ['lovethebomb', 'dysosmus'],
    'everyone': RoleEveryone()
}

permissions = {
    'badge' : {
        'give' :      roles['everyone'],
        'buy' :       roles['everyone'],
        'create' :    roles['admin'],
        'remove':     roles['admin'],
        'remove-all': roles['admin']
    } 
}

@hook.command('badge')
@hook.command('b')
def badge(input, nick = None, chan = None, db = None, notice = None, message = None,
                 bot = None ):
    handler = BadgeHandler(nick, chan, db, notice, message, bot)

    handler.dispatch(input)

    return 

class BadgeHandler(object):

    taxe_percentage = 0.10

    usage = u'''Badge usage:
This help:
    badge help
Create a new badge:
    badge create <name> [<price>]
Delete a badge:
    badge remove <name>
List all available badges
    badge list 
Buy a badge for yourself:
    badge buy <name> 
Give a badge you own to an another nick
    badge user <nick> give   <name>
Remove a badge for a nick
    badge user <nick> remove <name>
Remove all the badges of a nick 
    badge user <nick> remove-all 
List all the badges for a nick
    badge user <nick> list'''

    def __init__(self, nick = None, chan = None, db = None, notice = None, 
                       message = None, bot = None):
        self.current_nick = nick.lower()
        self.current_chan = chan
        self.bot          = bot
        self.db           = db
        self._notice      = notice 
        self._message     = message

        if not db_ready:
            _db_init(self.db)

        if not karma.db_ready:
            karma.db_init(self.db)

        self.badge        = Badge(self.db)

    def multiline(self, message, target, method): # todo move outside
        lines = None

        try :
            lines = message.split('\n')
        except AttributeError:
            lines = message

        for line in lines:
            method(message = line, target = target)

    def notice(self, message, target = None): # todo move outside
        if not target:
            target = self.current_nick

        self.multiline(message, target, self._notice)        

    def message(self, message, target = None): # todo move outside
        if not target:
            target = self.current_chan

        self.multiline(message, target, self._message)

    def _parse_args(self, input):
        args = re.findall(r'\w+|"(?:\\"|[^"])+"', input) 
        args = [ arg.strip('"\'') for arg in args ]

        return args

    def dispatch(self, input):
        self.args   = self._parse_args(input) 
        try:
            command = self.args[0]

            # badge create <name> [<price>]
            if   command == u'create':
                print self.current_nick
                print permissions['badge']['create']
                if self.current_nick in permissions['badge']['create']:
                    try:
                        name  = self.args[1]
                        price = 0
                        try:
                            price = int(self.args[2])
                        except IndexError:
                            pass
                        except ValueError:
                            self.notice('Bad price format')

                        self.create(name, price)
                    except IndexError:
                        self.notice('Missing badge name')
                else:
                    self.notice('You don\'t have the right permission.')

            # badge remove <name>
            elif command == u'remove':
                if self.current_nick in permissions['badge']['remove']:
                    try:
                        name  = self.args[1]
                        self.remove(name)
                    except IndexError:
                        self.notice('Missing badge name')
                else:
                    self.notice('You don\'t have the right permission.')
            # badge remove-all
            elif command == u'remove-all':
                if self.current_nick in permissions['badge']['remove-all']:
                    pass
                else:
                    self.notice('You don\'t have the right permission.')
            # badge list
            elif command == u'list':
                self.list()
            # badge user <nick> give   <name>
            # badge user <nick> remove <name>
            # badge user <nick> remove-all 
            # badge user <nick> list 
            elif command == u'user':
                try:
                    nick = self.args[1]
                    try :
                        subcommand = self.args[2]
                        try:
                            name = self.args[3]
                            if   subcommand == u'give':
                                self.user_give(nick, name)
                            elif subcommand == u'remove':
                                if self.current_nick in permissions['badge']['remove']:
                                    self.user_remove(nick, name)
                                else:
                                    self.notice('You don\'t have the right permission.')
                            else:
                               self.notice('Unknow subcommand (give, remove, remove-all, list)')
                        except IndexError:
                            if   subcommand == u'list':
                                self.user_list(nick)
                            elif subcommand == u'remove-all':
                                if self.current_nick in permissions['badge']['remove']:
                                    self.user_remove_all(nick)
                                else:
                                    self.notice('You don\'t have the right permission.')
                            elif subcommand in ('give', 'remove'):
                                self.notice('Missing badge name')
                            else:
                                self.notice('Uknow subcommand (give, remove, remove-all, list)')  

                    except IndexError:
                        self.notice('Missing subcommand (give, remove, remove-all, list)')

                except IndexError:
                    self.notice('Missing nickname')

            # badge buy <name> 
            elif command == u'buy':
                if self.current_nick in permissions['badge']['buy']:
                    try:
                        name  = self.args[1]
                        self.buy(name)
                    except IndexError:
                        self.notice('Missing badge name')
                else:
                    self.notice('You don\'t have the right permission.')
            elif command == u'help':
                self.notice(BadgeHandler.usage)
            else:
                self.notice(BadgeHandler.usage)
        except IndexError:
            self.notice(BadgeHandler.usage)


    def create(self, name, price):
        if not self.badge.exist(name):
            self.badge.create(name, price)
        else:
            self.notice('The badge {name} already exist'.format(name = name))

    def remove(self, name):
        if self.badge.exist(name):
            self.badge.remove(name)
        else:
            self.notice('The badge {name} doesn\'t exist'.format(name = name))

    def buy(self, name):
        if self.badge.exist(name):
            badge = self.badge.by_name(name)
            id    =  badge[0]
            price = int(badge[2])

            if karma.available(self.db, self.current_nick) >= price: 
                self.badge.user_add(self.current_nick, id)
                karma.down(self.db, price, self.current_nick)
            else:
                self.notice('You need {karma} for the badge {name}'.format(karma = price, name = name))
        else:
            self.notice('The badge {name} doesn\'t exist'.format(name = name))

    def list(self):   
        badges = self.badge.all(order_by = 'b.price DESC')
        table  = PrettyTable(['Name', 'Price'])

        table.align['Name'] = 'l'

        for badge in badges: 
            name    = badge[1]
            price   = badge[2]

            table.add_row([name, price])
        
        self.message(str(table))

    def user_give(self, nick, name):
        if self.badge.exist(name):
            badge = self.badge.by_name(name)

            if self.badge.user_has(nick = self.current_nick, badge_id = badge[0]):
                
                price = int(badge[2])
                taxe  = int(price * BadgeHandler.taxe_percentage)

                if karma.available(self.db, self.current_nick) >= taxe:
                    karma.down(self.db, taxe, self.current_nick)
                    self.badge.user_remove(nick = self.current_nick, badge_id = badge[0])
                    self.badge.user_add(nick, badge_id = badge[0])
                else:
                    self.notice('You need {karma} (taxe) to perform this action'.format(karma = taxe))
            else:
                self.notice('You dont\'t have the badge {name}'.format(name = name))
        else:
            self.notice('The badge {name} doesn\'t exist'.format(name = name))

    def user_remove(self, nick, name):
        if self.badge.exist(name):
            badge = self.badge.by_name(name)
            if self.badge.user_has(nick = nick, badge_id = badge[0]):
                pass
            else:
                self.notice('You dont\'t have the badge {name}'.format(name = name))
        else:
            self.notice('The badge {name} doesn\'t exist'.format(name = name))

    def user_remove_all(self, nick):
        pass

    def user_list(self, nick):
        badges = self.badge.all(order_by = 'b.price DESC', for_nick = nick)
        table  = PrettyTable(['Name', 'Price'])

        table.align['Name'] = 'l'

        for badge in badges: 
            name    = badge[1]
            price   = badge[2]

            table.add_row([name, price])
        
        self.message(str(table))

def _db_init(db):
    db.execute("""CREATE TABLE IF NOT EXISTS badge (
               id    INTEGER PRIMARY KEY AUTOINCREMENT,
               name  TEXT    NOT NULL UNIQUE,
               price INTEGER )""")

    db.execute("""CREATE TABLE IF NOT EXISTS user_badge (
               nick          TEXT    NOT NULL,
               badge_id      INTEGER NOT NULL,
               session_badge BOOLEAN NOT NULL DEFAULT FALSE,
               expirable     BOOLEAN NOT NULL DEFAULT FALSE,
               expire_at     DATETIME DEFAULT NULL,
               PRIMARY KEY(nick, badge_id), 
               FOREIGN KEY(badge_id) REFERENCES badge(id) ON DELETE CASCADE )""")

    db_ready = True

class Badge(object):
    
    def __init__(self, db):
        self.db = db

    def by_name(self, name):
        cursor = self.db.cursor()

        cursor.execute('''SELECT b.id, b.name, b.price
                          FROM badge b
                          WHERE Lower(name) = Lower(:name)''', {
                            'name': name.strip()
                          })

        row         = cursor.fetchone()

        cursor.close();

        return row

    def remove_all(self):
        self.db.execute('DELETE FROM badge')
        self.db.commit()

    def all(self, for_nick = None, order_by = 'b.price DESC'):
        cursor = self.db.cursor()

        if for_nick:
            cursor.execute('''SELECT b.id, b.name, b.price
                              FROM badge b
                               JOIN user_badge ub ON b.id = ub.badge_id
                              WHERE ub.nick = :nick 
                              ORDER BY {order_by} '''.format(order_by = order_by), { 
                                'nick' : for_nick.strip().lower()
                              })
        else:
            cursor.execute('''SELECT b.id, b.name, b.price 
                              FROM badge b
                              ORDER BY {order_by} '''.format(order_by = order_by))       

        badges = cursor.fetchall()

        cursor.close();

        return badges

    def create(self, name, price = 0):
        self.db.execute('''INSERT INTO badge
                        (name, price)
                      VALUES
                        (:name, :price)''', {
                        'name' : name.strip(),
                        'price': price if price > 0 else 0
                    })
        self.db.commit()

    def remove(self, name):
        self.db.execute('''DELETE FROM badge 
                           WHERE Lower(name) = Lower(:name)''', {
                            'name': name.strip()
                        })
        self.db.commit()

    def exist(self, name):
        cursor = self.db.cursor()

        cursor.execute('''SELECT COUNT(id) as count 
                          FROM badge 
                          WHERE Lower(name) = Lower(:name)''', {
                            'name': name.strip()
                          })

        row         = cursor.fetchone()
        badge_exist = row[0] > 0

        cursor.close();

        return badge_exist

    def user_has(self, nick, badge_id):
        cursor = self.db.cursor()

        cursor.execute('''SELECT COUNT(b.id) as count 
                          FROM badge b
                           JOIN user_badge ub ON b.id = ub.badge_id
                          WHERE ub.nick = :nick AND
                                b.id    = :badge_id ''', { 
                            'nick'     : nick.strip().lower(),
                            'badge_id' : badge_id
                          })
       
        row       = cursor.fetchone()
        has_badge = row[0] > 0

        cursor.close();

        return has_badge

    def user_add(self, nick, badge_id, session_badge = False, expirable = False, expire_at = None):
        self.db.execute('''INSERT INTO user_badge
                     (nick, badge_id, session_badge, expirable, expire_at) 
                   VALUES 
                     (:nick, :badge_id, :session_badge, :expirable, :expire_at)''', 
                {
                    'nick'          : nick.strip().lower(),
                    'badge_id'      : badge_id,
                    'session_badge' : session_badge,
                    'expirable'     : expirable,
                    'expire_at'     : expire_at
                })

    def user_remove(self, nick, badge_id):
        self.db.execute('''DELETE FROM user_badge
                      WHERE nick     = :nick AND
                            badge_id = :badge_id''', {
                    'nick'    : nick.strip().lower(),
                    'badge_id': badge_id
                   })
        self.db.commit()
