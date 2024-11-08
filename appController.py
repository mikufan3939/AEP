from flask import Flask, redirect, render_template, request, session, url_for
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

        newUser=User(username,key,False)
        session["key"]=newUser.chave
        try:
            cur.execute("INSERT INTO usuario(chave, nome_usuario, chave_controle) VALUES(?,?,?)", (newUser.chave, newUser.nome_usuario, newUser.chave_controle))
            cur.close()
            return redirect(url_for("", user=newUser.nome_usuario))
        except:
            cur.close()
            return redirect("/"+newUser.nome_usuario)
    

@app.route("/<user>", methods=["GET", "POST"])
def usuario(user=None):
    if request.method=="GET":
            key=None
            cur = appservice.get_db(database).cursor()
            cur.execute("SELECT chave_controle FROM usuario WHERE nome_usuario=?", (user,))
            key_control=cur.fetchone()
            if(not key_control):
                key_control=(1,)
            if(not key_control[0]):
                key=session.get("key", None).decode("utf-8")
            cur.execute("UPDATE usuario SET chave_controle=? WHERE nome_usuario=?", (True, user,))
            cur.close()
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
            return render_template("index.html", user=user, passwordName=newPassword.nome_senha)
        except:
            return render_template("index.html", user=user, error="Senha Já Existe!")
        
@app.route("/<user>/senhas", methods=["GET", "POST"])
def senhas(user=None):
    if request.method=="GET":
        error=request.args.get("error", None)
        cur = appservice.get_db(database).cursor()
        cur.execute("SELECT senhas.nome_senha FROM senhas JOIN usuario ON usuario.id=senhas.id_usuario WHERE nome_usuario=?", (user,))
        names=cur.fetchall()
        cur.close()
        return render_template("senhas.html", user=user, passwords=names, decrypt=False, error=error)
    else:
        try:
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
        except:
            return redirect(url_for("senhas", user=user, error="Chave Inválida!"))
        
