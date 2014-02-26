# -*- utf-8 -*-
from util import ( hook, timesince )

import time
import re

db_ready = False


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
               FOREIGN KEY(badge_id) REFERENCES badge(id) )""")

    db_ready = True

class Badge(object):
    
    def __init__(self, db):
        self.db = db

    def all(self, for_nick):
        cursor = self.db.cursor()

        if for_nick:
            cursor.execute('''SELECT b.name, b.price, 
                              FROM badge b
                               JOIN user_badge ub ON b.id = ub.badge_id
                              WHERE ub.nick = :nick ''', { 
                                'nick' : for_nick.strip().lowercase()
                              })
        else:
            cursor.execute('''SELECT id, name, price 
                              FROM badge ''')       

        badges = cursor.fetchall()

        cursor.close();

        return badges

    def add(self, name, price = 0):
        self.db.execute('''INSERT INTO badge
                        (name, price)
                      VALUES
                        (:name, :price)''', {
                        'name':  name.strip().lowercase(),
                        'price': price if price > 0 else 0
                    })

    def remove(self, name):
        self.db.execute('''DELETE badge 
                           WHERE name = :name 
                           LIMIT 0, 1 ''', {
                            'name': name.strip().lowercase()
                        })

    def exist(self, name):
        cursor = self.db.cursor()

        cursor.execute('''SELECT COUNT(id) as count 
                          FROM badge 
                          WHERE Upper(name) = Upper(Trim(:name))''', {
                            'name': name
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
                            'nick'     : for_nick.strip().lowercase(),
                            'badge_id' : badge_id
                          })
       
        row       = cursor.fetchone()
        has_badge = row[0] > 0

        cursor.close();

        return has_badge

    def user_add(self, nick, badge_id, session_badge = False, expirable = False, 
                 expire_at = None):

        self.db('''INSERT INTO 
                     (nick, badge_id, session_badge, expirable, expire_at) 
                   VALUES 
                     (:nick, :badge_id, :session_badge, :expirable, :expire_at)''', 
                {
                    'nick'          : nick.strip().lowercase(),
                    'badge_id'      : badge_id,
                    'session_badge' : session_badge,
                    'expirable'     : expirable,
                    'expire_at'     : expire_at
                })
        pass

    def user_remove(self, nick, badge_id):
        db.execute('''DELETE badge 
                      WHERE nick     = :nick AND
                            badge_id = :badge_id
                      LIMIT 0, 1 ''', {
                    'nick'    : nick.strip().lowercase(),
                    'badge_id': badge_id
                   })
