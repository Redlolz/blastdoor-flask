import sqlite3
from argon2 import PasswordHasher
import rsa

class database:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)
        self.cursor = self.db.cursor()
        self.ph = PasswordHasher()

    def make_db(self):
        self.cursor.execute('''CREATE TABLE users (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                username varchar(255) NOT NULL UNIQUE,
                                password varchar(255) NOT NULL,
                                publickey text(850) NOT NULL,
                                admin BOOL 
                            )''')
        self.db.commit()

    def add_user(self, username, password, publickey):
        cmd = "INSERT INTO users (username, password, publickey) VALUES (?, ?, ?)"
        self.cursor.execute(cmd, (username, self.ph.hash(password), publickey))
        self.db.commit()

    def get_user(self, username):
        cmd = "SELECT * FROM users WHERE username=?"
        self.cursor.execute(cmd, (username,))
        return self.cursor.fetchall()

    def del_user(self, userid):
        cmd = "DELETE FROM users WHERE ID=?"
        self.cursor.execute(cmd, (userid,))
        self.db.commit()

    def verify_password(self, username, password):
        cmd = "SELECT * FROM users WHERE username=?"
        self.cursor.execute(cmd, (username,))
        user = self.cursor.fetchall()
        try:
            self.ph.verify(user[0][2], password)
            return True
        except:
            return False
        
    def isadmin(self, username):
        cmd = "SELECT * FROM users WHERE username=?"
        self.cursor.execute(cmd, (username,))
        user = self.cursor.fetchall()
        if user[0][4] == 1:
            return True
        else:
            return False

    def setadmin(self, username):
        cmd = "UPDATE users SET admin=1 WHERE username=?"
        self.cursor.execute(cmd, (username,))
        self.db.commit()

    def unsetadmin(self, username):
        cmd = "UPDATE users SET admin=0 WHERE username=?"
        self.cursor.execute(cmd, (username,))
        self.db.commit()

    def verify_signature(self, username, message, signature):
        cmd = "SELECT * FROM users WHERE username=?"
        self.cursor.execute(cmd, (username,))
        user = self.cursor.fetchall()
        return rsa.verify(message, signature, user[0][3])

    def close_conn(self):
        self.db.commit()
        self.db.close()
        
