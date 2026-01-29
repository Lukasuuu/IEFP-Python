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

def is_admin():
    return session.get("role") == "admin"

def is_staff():
    return session.get("role") == "staff"

def is_cliente():
    return session.get("role") == "cliente"

# ============================
# ROTA PRINCIPAL (INDEX)
# ============================
@app.route("/")
def index():
    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Conecta ao banco
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os utilizadores
    cursor.execute("SELECT id, username, created_at FROM users ORDER BY id DESC")
    utilizadores = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Envia dados para o template index.html
    return render_template("index.html", utilizadores=utilizadores, role=session.get("role"))


# ============================================================
# ROTA DE LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conexao = ligar_db()
        cursor = conexao.cursor(dictionary=True)

        # Busca utilizador pelo username
        cursor.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
        utilizador = cursor.fetchone()

        cursor.close()
        conexao.close()

        # Verifica senha
        if utilizador and utilizador.get("password") == password:
            # Guarda dados na sessão
            session["user_id"] = utilizador["id"]
            session["username"] = utilizador["username"]
            session["role"] = utilizador["role"]
            return redirect(url_for("dashboard"))
        else:
            flash("Login ou password incorreto.")
            return redirect(url_for("login"))

    return render_template("login.html")

# Criar Utilizador (apenas admin)
@app.route("/criar_utilizador", methods=["GET", "POST"])
def criar_utilizador():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conexao = ligar_db()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, password, role))
        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Utilizador criado com sucesso!")
        return redirect(url_for("dashboard"))

    return render_template("criar_utilizador.html")


# Criar Cliente (admin e staff podem)
@app.route("/criar_cliente", methods=["GET", "POST"])
def criar_cliente():
    if "user_id" not in session or session.get("role") not in ["admin", "staff"]:
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone =  request.form["telefone"]

        conexao = ligar_db()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)",
                       (nome, email, telefone))
        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Cliente criado com sucesso!")
        return redirect(url_for("dashboard"))

    return render_template("criar_cliente.html")


@app.route("/cliente_editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Admin e staff podem editar (igual ao dashboard)
    if not (is_admin() or is_staff()):
        flash("Apenas administradores ou staff podem editar clientes.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        morada = request.form["morada"]

        cursor.execute("""
            UPDATE clientes 
            SET nome=%s, telefone=%s, email=%s, morada=%s
            WHERE id=%s
        """, (nome, telefone, email, morada, id))

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Cliente atualizado com sucesso!")
        return redirect(url_for("clientes_listar"))

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/apagar/<int:id>")
def apagar_cliente(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admin pode apagar (igual ao dashboard)
    if not is_admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Cliente apagado com sucesso!")
    return redirect(url_for("clientes_listar"))

@app.route("/minha_conta")
def minha_conta():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Só clientes devem aceder
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Buscar dados do cliente associado ao utilizador
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (session.get("cliente_id"),))
    cliente = cursor.fetchone()
    cursor.close()
    conexao.close()

    return render_template("minha_conta.html", cliente=cliente)

@app.route("/animais_listar")
def animais_listar():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * from animais")
    
    animais = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return render_template("animais_listar.html", animais=animais)

# ============================
# ROTA DE DASHBOARD
# ============================
@app.route("/dashboard")
def dashboard():
    # Proteção: só entra se estiver logado
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    role = session.get("role")
    username = session.get("username")

    # Apenas admin pode apagar
    pode_apagar = (role == "admin")

    # Passa username e role para o template
    return render_template("dashboard.html",
                           username=session.get("username"),
                           role=session.get("role"))
 

@app.route("/clientes_listar")
def clientes_listar():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    
    cursor.close()
    conexao.close()

    return render_template("clientes_listar.html", clientes=clientes)

@app.route("/consultas_listar")
def consultas_listar():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM consultas")
    consultas = cursor.fetchall()
    
    cursor.close()
    conexao.close()

    return render_template("consultas_listar.html", consultas=consultas)

@app.route("/users_listar")
def users_listar():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os utilizadores
    cursor.execute("SELECT id, username, role, cliente_id, created_at FROM users")
    users = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("users_listar.html", users=users)

@app.route("/meus_animais")
def meus_animais():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Só clientes devem aceder
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Buscar animais do cliente logado
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM animais WHERE cliente_id = %s", (session.get("cliente_id"),))
    animais = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template("meus_animais.html", animais=animais)

@app.route("/minhas_consultas")
def minhas_consultas():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Só clientes devem aceder
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))
    
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("")
    
    consultas = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template("minhas_consultas.html", consultas=consultas)

# ============================================================
# ROTA DE LOGOUT
# ============================================================
@app.route("/logout")
def logout():
    session.clear()  # Remove tudo da sessão
    return redirect(url_for("login"))

if __name__ == "__main__": 
      app.run(debug=True)