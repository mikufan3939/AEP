import sqlite3
from cryptography.fernet import Fernet
from flask import g

def get_db(database):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database,isolation_level=None)
    return db

def init_db(app,database):
    with app.app_context():
        db = get_db(database)
        with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                db.cursor().close()
        db.commit()

def generateKey():
    key=Fernet.generate_key()
    return key

def encryptPassword(key, password):
    f=Fernet(key[0])
    passToken=f.encrypt(bytes(password, 'utf-8'))
    return passToken

def decryptPassword(key, password):
    f=Fernet(key)
    return f.decrypt(password)