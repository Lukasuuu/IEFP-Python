from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for,session,flash
import json
import requests
import datetime

def ligar_db():
       return mysql.connector.connect(
                host="62.28.39.135",
                user="efa0125",
                password="123.Abc",
                database="efa0125_08_vet_clinic")
        
################ CRIAÇÃO DA APLICAÇÃO FLASK #################
app = Flask(__name__)
# Chave secreta usada para sessões (login)
app.secret_key = "123"

#injetar variáveis ou funções automaticamente em TODOS os templates do Flask
@app.context_processor
def datetime_ano():
        return {"ano":datetime.datetime.now().year}

#Direcionar a routa como principal sendo Index
@app.route("/")
def index():
    
    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Conecta ao banco
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)  # Retorna resultados como dicionário

    # Busca todos os utilizadores ordenados do mais recente para o mais antigo
    cursor.execute("SELECT id, username, created_at FROM users ORDER BY id DESC")
    utilizadores = cursor.fetchall() # traz todas as linhas parao Python

    cursor.close() #encerra a execucao da tabela 
    conexao.close() #encerra a conexao com a base de dados

    # Verifica se o utilizador logado é admin
    is_admin = session.get("role") == "admin"

    # Envia dados para o template index.html
    return render_template("index.html", utilizadores=utilizadores, is_admin=is_admin)

# ============================================================
# ROTA DE LOGIN
# ============================================================
@app.route("/login", methods=["GET","POST"])
def login():
    ############### Requerer Login ##########################
    if request.method == "POST":
         username = request.form["username"]
         password = request.form["password"]
         
         conexao = ligar_db()
         cursor = conexao.cursor(dictionary=True)

         #Buscar os utilizadores da base de dados
         cursor.execute("SELECT id,username,password,role FROM users WHERE username = %s", (username, ))
         utilizador = cursor.fetchone()

         cursor.close()
         conexao.close()

         #verifica senha do utilizador
         if utilizador and utilizador.get("password") == password:
              
                #Guarda dados da sessão
                session["user_id"] = utilizador["id"]
                session["username"] = utilizador["username"]
                session["role"] = utilizador["role"]
                return redirect(url_for("index"))
         else:
                flash("Password ou login incorreto.")
                return redirect(url_for("login"))  
    return render_template("login.html")

@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar():
        # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admins podem editar
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))
    
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    #Buscar os utilizadores da base de dados
    cursor.execute("UPDATE clientes SET id=%s, cliente_id=%s, nome=%s, especie=%s, raca=%s, data_nascimento=%s", (cliente_id, nome, especie, raca, data_nascimento))


    conexao.commit()
    cursor.close()
    conexao.close()
    
    return render_template("dashboard.html")

@app.route("/animais_listar")
def animais_listar():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("animais_listar.html")

@app.route("/dashboard")
def dashboard():
    # Proteção: só entra se estiver logado
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")    

@app.route("/clientes_listar")
def clientes_listar():
     if not session.get("user_id"):
        return redirect(url_for("login"))
     return render_template("clientes_listar.html")

@app.route("/consultas_listar")
def consultas_listar():
     if not session.get("user_id"):
        return redirect(url_for("login"))
     return render_template("consultas_listar.html")

@app.route("/users_listar")
def users_listar():
     if not session.get("user_id"):
        return redirect(url_for("login"))
     return render_template("users_listar.html")


# ============================================================
# ROTA DE LOGOUT
# ============================================================
@app.route("/logout")
def logout():
    session.clear()  # Remove tudo da sessão
    return redirect(url_for("login"))

if __name__ == "__main__": 
      app.run(debug=True)