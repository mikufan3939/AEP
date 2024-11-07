from flask import Flask, redirect, render_template, request, session
from utils import generate_password
import services.appService as appservice
from model.userModel import User
from model.senhaModel import Senha
# Configure application
app = Flask(__name__)
database='teste.db'
app.secret_key="teste"
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="GET":
        appservice.init_db(app,database)
        return render_template("set_user.html")
    else:
        cur = appservice.get_db(database).cursor()
        
        username=request.form.get('username')
        key=appservice.generateKey()

        newUser=User(username,key)
        session["key"]=newUser.chave
        try:
            cur.execute("INSERT INTO usuario(chave, nome_usuario) VALUES(?,?)", (newUser.chave, newUser.nome_usuario,))
            cur.close()
            return redirect("/"+newUser.nome_usuario)
        except:
            cur.close()
            return redirect("/"+newUser.nome_usuario)
    

@app.route("/<user>", methods=["GET", "POST"])
def usuario(user=None):
    if request.method=="GET":
            key=None
            if(session.get("key")):
                key=session.get("key", None)
            appservice.init_db(app,database)
            return render_template("index.html", user=user, key=key)
    else:
        try:
            cur = appservice.get_db(database).cursor()
            name=request.form.get("name")
            
            cur.execute("SELECT * FROM usuario")
            print(cur.fetchall())
            
            cur.execute("SELECT id FROM usuario WHERE nome_usuario=?", (user,))
            id_usuario=cur.fetchone()
            
            cur.execute("SELECT chave FROM usuario WHERE nome_usuario=?", (user,))
            key=cur.fetchone()
            print("+++++++++++++++++++++++++++++")
            print(key)
            
            encryptedPassword=appservice.encryptPassword(key, generate_password())
            
            newPassword=Senha(encryptedPassword, name, id_usuario[0])
            
            cur.execute("INSERT INTO senhas(nome_senha, senha, id_usuario) VALUES (?,?,?)", (newPassword.nome_senha, newPassword.senha, newPassword.id_usuario,))
            cur.close()
            return redirect("/"+user)
        except:
            return render_template("index.html", user=user, error="ERRO!")
        
@app.route("/<user>/senhas", methods=["GET", "POST"])
def senhas(user=None):
    if request.method=="GET":
        cur = appservice.get_db(database).cursor()
        cur.execute("SELECT senhas.nome_senha FROM senhas JOIN usuario ON usuario.id=senhas.id_usuario WHERE nome_usuario=?", (user,))
        names=cur.fetchall()
        cur.close()
        return render_template("senhas.html", passwords=names, decrypt=False)
    else:
        key=request.form.get("decryption_key")
        cur = appservice.get_db(database).cursor()
        
        cur.execute("SELECT senhas.senha, senhas.nome_senha FROM senhas JOIN usuario ON usuario.id=senhas.id_usuario WHERE nome_usuario=?", (user,))
        passwords=list(cur.fetchall())
        cur.close()
        aux=0
        for password in passwords:
            password=list(password)
            password[0]=appservice.decryptPassword(key, password[0]).decode('utf-8')
            print(password)
            print(password[0])
            passwords[aux]=password
            aux=aux+1
            
    
        return render_template("senhas.html", user=user, passwords=passwords, decrypt=True)
        
