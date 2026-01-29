from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for,session,flash
import json
import requests
import datetime

# Função que cria a ligação com o banco de dados MySQL
def ligar_db():
       return mysql.connector.connect(
                host="62.28.39.135",
                user="efa0125",
                password="123.Abc",
                database="efa0125_08_vet_clinic"
       )
        
################ CRIAÇÃO DA APLICAÇÃO FLASK #################
app = Flask(__name__)

# Chave secreta usada para sessões (login)
app.secret_key = "123"

# Injeta automaticamente a variável "ano" em TODOS os templates
@app.context_processor
def datetime_ano():
        return {"ano": datetime.datetime.now().year}

# Funções simples para verificar permissões
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

    # Se o utilizador não estiver logado, volta para o login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Liga ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os utilizadores ordenados do mais recente para o mais antigo
    cursor.execute("SELECT id, username, created_at FROM users ORDER BY id DESC")
    utilizadores = cursor.fetchall()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia os dados para o template index.html
    return render_template(
        "index.html",
        utilizadores=utilizadores,
        role=session.get("role")
    )


# ============================================================
# ROTA DE LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    # Se o formulário foi enviado (POST)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Liga ao banco
        conexao = ligar_db()
        cursor = conexao.cursor(dictionary=True)

        # Procura o utilizador pelo username
        cursor.execute(
            "SELECT id, username, password, role FROM users WHERE username = %s",
            (username,)
        )
        utilizador = cursor.fetchone()

        cursor.close()
        conexao.close()

        # Verifica se encontrou o utilizador e se a password está correta
        if utilizador and utilizador.get("password") == password:

            # Guarda informações na sessão
            session["user_id"] = utilizador["id"]
            session["username"] = utilizador["username"]
            session["role"] = utilizador["role"]

            # Redireciona para o dashboard
            return redirect(url_for("dashboard"))

        else:
            # Caso falhe, mostra mensagem e volta ao login
            flash("Login ou password incorreto.")
            return redirect(url_for("login"))

    # Se for GET, apenas mostra o formulário de login
    return render_template("login.html")


# ============================================================
# CRIAR UTILIZADOR (APENAS ADMIN)
# ============================================================
@app.route("/criar_utilizador", methods=["GET", "POST"])
def criar_utilizador():

    # Apenas administradores podem aceder a esta rota
    if "user_id" not in session or session.get("role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    # Se o formulário foi enviado
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        # Liga ao banco
        conexao = ligar_db()
        cursor = conexao.cursor()

        # Insere o novo utilizador
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Utilizador criado com sucesso!")
        return redirect(url_for("dashboard"))

    # Se for GET, mostra o formulário
    return render_template("criar_utilizador.html")


# ============================================================
# CRIAR CLIENTE (ADMIN E STAFF)
# ============================================================
@app.route("/criar_cliente", methods=["GET", "POST"])
def criar_cliente():

    # Apenas admin e staff podem criar clientes
    if "user_id" not in session or session.get("role") not in ["admin", "staff"]:
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    # Se o formulário foi enviado
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]

        # Liga ao banco
        conexao = ligar_db()
        cursor = conexao.cursor()

        # Insere o novo cliente
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)",
            (nome, email, telefone)
        )

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Cliente criado com sucesso!")
        return redirect(url_for("dashboard"))

    #mostra o formulário
    return render_template("criar_cliente.html")
# ============================================================
# ROTA PARA EDITAR CLIENTE (ADMIN E STAFF)
# ============================================================
@app.route("/cliente_editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admin e staff podem editar clientes
    if not (is_admin() or is_staff()):
        flash("Apenas administradores ou staff podem editar clientes.")
        return redirect(url_for("dashboard"))

    # Conecta ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Se o formulário foi enviado (POST)
    if request.method == "POST":
        # Recebe os dados enviados pelo formulário
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        morada = request.form["morada"]

        # Atualiza os dados do cliente no banco
        cursor.execute("""
            UPDATE clientes 
            SET nome=%s, telefone=%s, email=%s, morada=%s
            WHERE id=%s
        """, (nome, telefone, email, morada, id))

        # Salva as alterações
        conexao.commit()

        # Fecha cursor e conexão
        cursor.close()
        conexao.close()

        # Mensagem de sucesso
        flash("Cliente atualizado com sucesso!")

        # Volta para a lista de clientes
        return redirect(url_for("clientes_listar"))

    # Se for GET, busca os dados do cliente para preencher o formulário
    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia os dados do cliente para o template
    return render_template("editar_cliente.html", cliente=cliente)



# ============================================================
# ROTA PARA APAGAR CLIENTE (APENAS ADMIN)
# ============================================================
@app.route("/apagar/<int:id>")
def apagar_cliente(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem apagar clientes
    if not is_admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Conecta ao banco
    conexao = ligar_db()
    cursor = conexao.cursor()

    # Apaga o cliente pelo ID
    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conexao.commit()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Mensagem de sucesso
    flash("Cliente apagado com sucesso!")

    # Volta para a lista de clientes
    return redirect(url_for("clientes_listar"))



# ============================================================
# ROTA MINHA CONTA (APENAS CLIENTE)
# ============================================================
@app.route("/minha_conta")
def minha_conta():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem ver esta página
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Conecta ao banco
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca os dados do cliente associado ao utilizador logado
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (session.get("cliente_id"),))
    cliente = cursor.fetchone()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia os dados para o template
    return render_template("minha_conta.html", cliente=cliente)



# ============================================================
# ROTA PARA LISTAR TODOS OS ANIMAIS (ADMIN E STAFF)
# ============================================================
@app.route("/animais_listar")
def animais_listar():

    # Verifica se o utilizador está logado
    if not session.get("user_id"):
        return redirect(url_for("login"))
    
    # Conecta ao banco
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os animais cadastrados
    cursor.execute("SELECT * from animais")
    animais = cursor.fetchall()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()
    
    # Envia a lista de animais para o template
    return render_template("animais_listar.html", animais=animais)

# ============================
# ROTA DE DASHBOARD
# ============================
@app.route("/dashboard")
def dashboard():

    # Verifica se o utilizador está logado.
    # Se não estiver, é redirecionado para o login.
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Obtém da sessão o papel (role) e o nome do utilizador logado
    role = session.get("role")
    username = session.get("username")

    # Define se o utilizador pode apagar registos.
    # Apenas administradores têm essa permissão.
    pode_apagar = (role == "admin")

    # Envia para o template o username e o role
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        role=session.get("role")
    )



# ============================
# LISTAR CLIENTES
# ============================
@app.route("/clientes_listar")
def clientes_listar():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Liga ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    
    # Busca todos os clientes da tabela
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    
    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia a lista de clientes para o template
    return render_template("clientes_listar.html", clientes=clientes)



# ============================
# LISTAR CONSULTAS
# ============================
@app.route("/consultas_listar")
def consultas_listar():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Liga ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)
    
    # Busca todas as consultas da tabela
    cursor.execute("SELECT * FROM consultas")
    consultas = cursor.fetchall()
    
    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia a lista de consultas para o template
    return render_template("consultas_listar.html", consultas=consultas)



# ============================
# LISTAR UTILIZADORES
# ============================
@app.route("/users_listar")
def users_listar():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Liga ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os utilizadores com os campos principais
    cursor.execute("SELECT id, username, role, cliente_id, created_at FROM users")
    users = cursor.fetchall()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia a lista de utilizadores para o template
    return render_template("users_listar.html", users=users)

# Rota onde o cliente vê apenas os animais dele
@app.route("/meus_animais")
def meus_animais():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem aceder a esta página
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Conectar ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar todos os animais que pertencem ao cliente logado
    # O cliente_id está guardado na sessão quando ele faz login
    cursor.execute("SELECT * FROM animais WHERE cliente_id = %s", (session.get("cliente_id"),))
    animais = cursor.fetchall()

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

    # Enviar os animais encontrados para o template meus_animais.html
    return render_template("meus_animais.html", animais=animais)



# Rota onde o cliente vê apenas as consultas dos seus animais
@app.route("/minhas_consultas")
def minhas_consultas():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem aceder a esta página
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Conectar ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # ⚠️ Aqui ainda falta a query para buscar as consultas
    # Você ainda vai completar esta parte depois
    cursor.execute("")

    # Buscar resultados da consulta
    consultas = cursor.fetchall()

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

    # Enviar as consultas encontradas para o template minhas_consultas.html
    return render_template("minhas_consultas.html", consultas=consultas)



# ============================================================
# ROTA DE LOGOUT
# ============================================================
@app.route("/logout")
def logout():

    # Limpa todos os dados da sessão (desloga o utilizador)
    session.clear()

    # Redireciona para a página de login
    return redirect(url_for("login"))



# Iniciar a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)