#!/usr/bin/env python3
import db
import sys
import os
import os.path
import tempfile
import subprocess
from getpass import getpass
from riposte import Riposte
from riposte.printer import Palette

class Application:
    def __init__(self):
        self.databasefile = None
        self.db = None

class CustomRiposte(Riposte):
    @property
    def prompt(self):
        if app.databasefile:
            return f"[blastdoor@{app.databasefile}]$ "
        else:
            return self._prompt  # reference to `prompt` parameter.

app = Application()
peekr = CustomRiposte(prompt="[blastdoor]$ ")

@peekr.command('exit')
def exit():
    peekr.status("Goobye!")
    sys.exit()

@peekr.command('create')
def create(databasefile: str):
    try:
        open(databasefile, 'a').close()
        database = db.database(databasefile)
        database.make_db()
        database.close_conn()
        peekr.success("Succesfully created database")
    except Exception as e:
        peekr.error("Something went wrong")
        peekr.error(e)

@peekr.command('use')
def use(database: str):
    if os.path.isfile(database):
        app.databasefile = database
        app.db = db.database(database)
    else:
        peekr.error("File doesn't exist")

@peekr.command('adduser')
def adduser():
    username = input("Username: ")
    password = getpass()
    passwordverify = getpass(prompt='Password verify: ')
    if password == passwordverify:
        EDITOR = os.environ.get('EDITOR','vim') #that easy!

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            tf.flush()
            subprocess.call([EDITOR, tf.name])
            tf.seek(0)
            publickey = tf.read().decode('utf-8')        

        app.db.add_user(username, password, publickey)
    else:
        peekr.error("Passwords don't match")

@peekr.command('getuser')
def getuser(username: str):
    user = app.db.get_user(username)
    if user != []:
        peekr.status("ID: " + Palette.YELLOW.format(user[0][0]))
        peekr.status("USERNAME: " + Palette.YELLOW.format(user[0][1]))
        peekr.status("PASSHASH: " + Palette.YELLOW.format(user[0][2]))
        peekr.status("PUBLICKEY: ")
        peekr.print(Palette.YELLOW.format(user[0][3]))
        peekr.status("ADMIN: " + Palette.YELLOW.format(user[0][4]))
    else:
        peekr.error("User doesn't exist")

@peekr.command('setadmin')
def setadmin(username: str):
    try:
        app.db.setadmin(username)
        peekr.success("Successfully changed admin state")
    except Exception as e:
        peekr.error(e)
        peekr.error("User doesn't exist")

@peekr.command('unsetadmin')
def unsetadmin(username: str):
    try:
        app.db.unsetadmin(username)
        peekr.success("Successfully changed admin state")
    except Exception as e:
        peekr.error(e)
        peekr.error("User doesn't exist")

@peekr.command('deluser')
def deluser(userid: int):
    try:
        app.db.del_user(userid)
        peekr.success("Successfully deleted user with ID " + userid)
    except:
        peekr.error("User doesn't exist")

peekr.run()