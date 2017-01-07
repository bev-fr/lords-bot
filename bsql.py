
import sqlite3 as lite
import sys

con = lite.connect('test.db')


def player_table():
    with con:
        cur = con.cursor()    
        #cur.execute("CREATE TABLE Player(Id INT, TelegramId INT, Name TEXT, UserName TEXT, Welcome TEXT)")
        cur.execute("INSERT INTO Player VALUES(0, 0, 'Test', 'Test', 'Test')")


def version(bot, update):
    with con:
        cur = con.cursor()    
        cur.execute('SELECT SQLITE_VERSION()')
        
        data = cur.fetchone()
        
        update.message.reply_text("SQLite version: %s" % data, quote=False)


def uwelc(uid):
    with con:
        cur.execute("SELECT Welcome From Player Where TelegramId=?", (uid))




def querry(bot, update): 
    return 'Test'
