from cryptography.fernet import Fernet
from flask import Flask, flash, redirect, render_template, request, session,g
import sqlite3
from utils import generate_password
# Configure application
app = Flask(__name__)
database='teste.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database,isolation_level=None)
    return db

def init_db():
    with app.app_context():
        db = get_db()
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
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="GET":
        init_db()
        return render_template("set_user.html")
    else:
        cur = get_db().cursor()
        username=request.form.get('username')
        key=generateKey()
        try:
            cur.execute("INSERT INTO usuario(chave, nome_usuario) VALUES(?,?)", (key,username,))
            cur.close()
            return redirect("/"+username)
        except:
            return redirect("/"+username)
    

@app.route("/<user>", methods=["GET", "POST"])
def usuario(user=None):
    if request.method=="GET":
            init_db()
            return render_template("index.html", user=user)
    else:
        try:
            cur = get_db().cursor()
            name=request.form.get("name")
            
            cur.execute("SELECT * FROM usuario")
            print(cur.fetchall())
            
            cur.execute("SELECT id FROM usuario WHERE nome_usuario=?", (user,))
            id_usuario=cur.fetchone()
            
            cur.execute("SELECT chave FROM usuario WHERE nome_usuario=?", (user,))
            key=cur.fetchone()
            print("+++++++++++++++++++++++++++++")
            print(key)
            
            encryptedPassword=encryptPassword(key, generate_password())
            cur.execute("INSERT INTO senhas(nome_senha, senha, id_usuario) VALUES (?,?,?)", (name, encryptedPassword, id_usuario[0],))
            cur.close()
            return redirect("/"+user)
        except:
            return render_template("index.html", user=user, error="ERRO!")
        
@app.route("/<user>/senhas", methods=["GET", "POST"])
def senhas(user=None):
    if request.method=="GET":
        cur = get_db().cursor()
        cur.execute("SELECT senhas.nome_senha FROM senhas JOIN usuario ON usuario.id=senhas.id_usuario WHERE nome_usuario=?", (user,))
        names=cur.fetchall()
        cur.close()
        return render_template("senhas.html", passwords=names, decrypt=False)
    else:
        key=request.form.get("decryption_key")
        cur = get_db().cursor()
        
        cur.execute("SELECT senhas.senha, senhas.nome_senha FROM senhas JOIN usuario ON usuario.id=senhas.id_usuario WHERE nome_usuario=?", (user,))
        passwords=list(cur.fetchall())
        cur.close()
        aux=0
        for password in passwords:
            password=list(password)
            password[0]=decryptPassword(key, password[0]).decode('utf-8')
            print(password)
            print(password[0])
            passwords[aux]=password
            aux=aux+1
            
    
        return render_template("senhas.html", user=user, passwords=passwords, decrypt=True)
        
