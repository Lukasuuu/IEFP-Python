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


## ============================================================
# ROTA DE LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conexao = ligar_db()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, username, password, role
            FROM users
            WHERE username = %s
        """, (username,))
        user = cursor.fetchone()

        cursor.close()
        conexao.close()

        # Verifica user e password
        if user and user["password"] == password:

            # Guarda dados básicos
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            # Se for cliente, buscar o cliente_id correspondente
            if user["role"] == "cliente":
                conexao = ligar_db()
                cursor = conexao.cursor(dictionary=True)

                cursor.execute("SELECT id FROM clientes WHERE user_id = %s", (user["id"],))
                cliente = cursor.fetchone()

                cursor.close()
                conexao.close()

                if cliente:
                    session["cliente_id"] = cliente["id"]

            return redirect(url_for("dashboard"))

        flash("Login ou password incorreto.")
        return redirect(url_for("login"))

    return render_template("login.html")



# ============================================================
# ROTA PARA CRIAR USER (apenas admin)
# ============================================================
@app.route("/criar_user", methods=["GET", "POST"])
def criar_user():

    # Apenas administradores podem aceder a esta rota
    if "user_id" not in session or session.get("role") != "admin":
        flash("Acesso restrito.")
        return redirect(url_for("dashboard"))

    # Se o formulário foi enviado
    if request.method == "POST":

        # Dados enviados pelo formulário
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        nome = request.form["nome"]
        email = request.form["email"]

        # Liga ao banco
        conexao = ligar_db()
        cursor = conexao.cursor(dictionary=True)

        # Cria o user na tabela correta
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
        """, (username, password, role))

        user_id = cursor.lastrowid  # ID do novo user

        # Se o user for cliente, cria também o cliente vinculado
        if role == "cliente":
            cursor.execute("""
                INSERT INTO clientes (nome, email, user_id)
                VALUES (%s, %s, %s)
            """, (nome, email, user_id))

        # Salva e fecha conexão
        conexao.commit()
        cursor.close()
        conexao.close()

        flash("User criado com sucesso!")
        return redirect(url_for("users_listar"))

    # Se for GET, mostra o formulário
    return render_template("criar_user.html")

# ============================================================
# ROTA PARA CRIAR CLIENTE (admin e staff)
# ============================================================
@app.route("/criar_cliente", methods=["GET", "POST"])
def criar_cliente():

    # Apenas admin e staff podem aceder
    if "user_id" not in session or session.get("role") not in ["admin", "staff"]:
        flash("Acesso restrito.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        # Dados básicos do cliente
        nome = request.form["nome"]
        email = request.form["email"]

        # Campos opcionais
        telefone = request.form.get("telefone")   # pode ser None
        morada = request.form.get("morada")       # pode ser None

        # Checkbox para criar login
        criar_login = request.form.get("criar_login")

        conexao = ligar_db()
        cursor = conexao.cursor(dictionary=True)

        # Se o admin/staff marcou "criar login", cria também o user
        if criar_login:
            username = request.form["username"]
            password = request.form["password"]

            cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, 'cliente')
            """, (username, password))

            user_id = cursor.lastrowid  # ID do user criado
        else:
            user_id = None  # cliente sem login

        # Cria o cliente com todos os campos (incluindo opcionais)
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, email, morada, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, telefone, email, morada, user_id))

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Cliente criado com sucesso!")
        return redirect(url_for("clientes_listar"))

    # Se for GET, mostra o formulário
    return render_template("criar_cliente.html")

# ============================================================
# CRIAR ANIMAL (admin, staff, cliente)
# ============================================================
@app.route("/criar_animal", methods=["GET", "POST"])
def criar_animal():

    # Precisa estar logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Admin e staff podem escolher o cliente
    if role in ["admin", "staff"]:
        cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
    else:
        clientes = None  # cliente não escolhe cliente_id

    if request.method == "POST":
        nome = request.form["nome"]
        especie = request.form["especie"]
        raca = request.form["raca"]
        data_nascimento = request.form["data_nascimento"]

        # Determinar o cliente_id
        if role in ["admin", "staff"]:
            cliente_id = request.form["cliente_id"]
        else:
            cliente_id = session.get("cliente_id")  # agora funciona!

        # Inserir animal
        cursor.execute("""
            INSERT INTO animais (nome, especie, raca, data_nascimento, cliente_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, especie, raca, data_nascimento, cliente_id))

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Animal criado com sucesso!")
        return redirect(url_for("dashboard"))

    cursor.close()
    conexao.close()

    return render_template("criar_animal.html", clientes=clientes)

# ============================================================
# CRIAR CONSULTA (admin, staff, cliente)
# ============================================================
@app.route("/criar_consulta", methods=["GET", "POST"])
def criar_consulta():

    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Valores padrão
    cliente_selecionado = None
    animais = []

    # ADMIN / STAFF → podem escolher cliente
    if role in ["admin", "staff"]:
        cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
    else:
        clientes = None

    # CLIENTE → só vê os seus animais
    if role == "cliente":
        cursor.execute("SELECT id, nome FROM animais WHERE cliente_id = %s", (session.get("cliente_id"),))
        animais = cursor.fetchall()

    # ============================
    # PROCESSAR POST
    # ============================
    if request.method == "POST":

        # BOTÃO 1 → Selecionar cliente (POST parcial)
        if "selecionar_cliente" in request.form:

            cliente_selecionado = request.form.get("cliente_id")

            # Carregar animais desse cliente
            cursor.execute("SELECT id, nome FROM animais WHERE cliente_id = %s ORDER BY nome", (cliente_selecionado,))
            animais = cursor.fetchall()

            cursor.close()
            conexao.close()

            # Recarregar página com cliente selecionado e animais filtrados
            return render_template(
                "criar_consulta.html",
                clientes=clientes,
                animais=animais,
                cliente_selecionado=cliente_selecionado
            )

        # BOTÃO 2 → Criar consulta (POST final)
        elif "criar_consulta" in request.form:

            animal_id = request.form["animal_id"]
            data_hora = request.form["data_hora"]
            motivo = request.form["motivo"]
            notas = request.form["notas"]

            # Determinar cliente_id
            if role in ["admin", "staff"]:
                cliente_id = request.form["cliente_id"]
            else:
                cliente_id = session.get("cliente_id")

            cursor.execute("""
                INSERT INTO consultas (animal_id, cliente_id, data_hora, motivo, notas)
                VALUES (%s, %s, %s, %s, %s)
            """, (animal_id, cliente_id, data_hora, motivo, notas))

            conexao.commit()
            cursor.close()
            conexao.close()

            flash("Consulta criada com sucesso!")
            return redirect(url_for("dashboard"))

    cursor.close()
    conexao.close()

    return render_template(
        "criar_consulta.html",
        clientes=clientes,
        animais=animais,
        cliente_selecionado=cliente_selecionado
    )

# ============================================================
# ROTA PARA EDITAR CLIENTE (ADMIN E STAFF)
# ============================================================
@app.route("/cliente_editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admin e staff podem editar
    if not (is_admin() or is_staff()):
        flash("Apenas administradores ou staff podem editar clientes.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar cliente (GET)
    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    if not cliente:
        cursor.close()
        conexao.close()
        flash("Cliente não encontrado.")
        return redirect(url_for("clientes_listar"))

    # Se for POST → tentar atualizar
    if request.method == "POST":

        try:
            cursor.execute("""
                UPDATE clientes
                SET nome=%s, telefone=%s, email=%s, morada=%s
                WHERE id=%s
            """, (
                request.form["nome"],
                request.form["telefone"],
                request.form["email"],
                request.form["morada"],
                id
            ))

            conexao.commit()

            cursor.close()
            conexao.close()

            flash("Cliente atualizado com sucesso!")
            return redirect(url_for("clientes_listar"))

        except Exception:
            flash("Erro ao atualizar cliente. Verifique os dados e tente novamente.")

            cursor.close()
            conexao.close()

            # Recarrega formulário com os dados enviados
            return render_template("editar_cliente.html", cliente=request.form)

    # GET → mostrar formulário
    cursor.close()
    conexao.close()
    return render_template("editar_cliente.html", cliente=cliente)

# ============================================================
# ROTA PARA EDITAR CONSULTA (APENAS ADMIN)
# ============================================================
@app.route("/editar_consulta/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem editar consultas
    if not is_admin():
        flash("Apenas administradores podem editar registos.")
        return redirect(url_for("dashboard"))

    # Conecta ao banco
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # ============================
    # POST → Atualizar consulta
    # ============================
    if request.method == "POST":

        data_hora = request.form["data_hora"]
        motivo = request.form["motivo"]
        notas = request.form["notas"]

        cursor.execute("""
            UPDATE consultas
            SET data_hora=%s, motivo=%s, notas=%s
            WHERE id=%s
        """, (data_hora, motivo, notas, id))

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Consulta atualizada com sucesso!")
        return redirect(url_for("editar_consultas"))

    # ============================
    # GET → Carregar dados da consulta
    # ============================
    cursor.execute("SELECT * FROM consultas WHERE id=%s", (id,))
    consulta = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not consulta:
        flash("Consulta não encontrada.")
        return redirect(url_for("editar_consultas"))

    return render_template("editar_consulta.html", consulta=consulta)

# ============================================================
# ROTA PARA APAGAR CLIENTE (APENAS ADMIN)
# ============================================================
@app.route("/apagar_cliente/<int:id>", methods=["GET", "POST"])
def apagar_cliente(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem apagar registos
    if not is_admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Se o método for POST, significa que o admin confirmou o apagamento
    if request.method == "POST":
        try:
            # Liga ao banco de dados
            conexao = ligar_db()
            cursor = conexao.cursor()

            # Tenta apagar o cliente pelo ID
            cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
            conexao.commit()

            # Fecha a ligação ao banco
            cursor.close()
            conexao.close()

            # Mensagem de sucesso
            flash("Cliente apagado com sucesso!")

            # Volta para a lista de clientes
            return redirect(url_for("clientes_listar"))

        except Exception:
            # Se der qualquer erro, mostra mensagem simples
            flash("Erro ao apagar cliente.")

            # Volta para a lista de clientes
            return redirect(url_for("clientes_listar"))

    # Se for GET, mostra a página de confirmação
    return render_template("apagar.html", voltar=url_for("clientes_listar"))

# ============================================================
# ROTA PARA APAGAR ANIMAIS (APENAS ADMIN)
# ============================================================
@app.route("/apagar_animal/<int:id>", methods=["GET", "POST"])
def apagar_animal(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem apagar registos
    if not is_admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Se o método for POST, significa que o admin confirmou o apagamento
    if request.method == "POST":
        try:
            # Liga ao banco de dados
            conexao = ligar_db()
            cursor = conexao.cursor()

            # Tenta apagar o animal pelo ID
            cursor.execute("DELETE FROM animais WHERE id=%s", (id,))
            conexao.commit()

            # Fecha a ligação ao banco
            cursor.close()
            conexao.close()

            # Mensagem de sucesso
            flash("Animal apagado com sucesso!")

            # Volta para a lista de animais
            return redirect(url_for("animais_listar"))

        except Exception:
            # Se der qualquer erro, mostra mensagem simples
            flash("Erro ao apagar animal.")

            # Volta para a lista de animais
            return redirect(url_for("animais_listar"))

    # Se for GET, mostra a página de confirmação
    return render_template("apagar.html", voltar=url_for("animais_listar"))

# ============================================================
# ROTA PARA APAGAR CONSULTAS (APENAS ADMIN)
# ============================================================
@app.route("/apagar_consulta/<int:id>", methods=["GET", "POST"])
def apagar_consulta(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem apagar registos
    if not is_admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Se o método for POST, significa que o admin confirmou o apagamento
    if request.method == "POST":
        try:
            # Liga ao banco de dados
            conexao = ligar_db()
            cursor = conexao.cursor()

            # Tenta apagar a consulta pelo ID
            cursor.execute("DELETE FROM consultas WHERE id=%s", (id,))
            conexao.commit()

            # Fecha a ligação ao banco
            cursor.close()
            conexao.close()

            # Mensagem de sucesso
            flash("Consulta apagada com sucesso!")

            # Volta para a lista de consultas
            return redirect(url_for("consultas_listar"))

        except Exception:
            # Se der qualquer erro, mostra mensagem simples
            flash("Erro ao apagar consulta.")

            # Volta para a lista de consultas
            return redirect(url_for("consultas_listar"))

    # Se for GET, mostra a página de confirmação
    return render_template("apagar.html", voltar=url_for("consultas_listar"))

# ============================================================
# ROTA PARA APAGAR UTILIZADORES (APENAS ADMIN)
# ============================================================
@app.route("/apagar_user/<int:id>", methods=["GET", "POST"])
def apagar_user(id):

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem apagar users
    if not is_admin():
        flash("Apenas administradores podem apagar users.")
        return redirect(url_for("dashboard"))

    # Se o método for POST, significa que o admin confirmou o apagamento
    if request.method == "POST":
        try:
            # Liga ao banco de dados
            conexao = ligar_db()
            cursor = conexao.cursor()

            # Tenta apagar o user pelo ID
            cursor.execute("DELETE FROM users WHERE id=%s", (id,))
            conexao.commit()

            # Fecha a ligação ao banco
            cursor.close()
            conexao.close()

            # Mensagem de sucesso
            flash("User apagado com sucesso!")

            # Volta para a lista de users
            return redirect(url_for("users_listar"))

        except Exception:
            # Se der qualquer erro, mostra mensagem simples
            flash("Erro ao apagar user.")

            # Volta para a lista de users
            return redirect(url_for("users_listar"))

    # Se for GET, mostra a página de confirmação
    return render_template("apagar.html", voltar=url_for("users_listar"))

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
# LISTAR USERS (APENAS ADMIN)
# ============================
@app.route("/users_listar")
def users_listar():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem ver esta página
    if session.get("role") != "admin":
        flash("Apenas administradores podem ver a lista de users.")
        return redirect(url_for("dashboard"))

    # Liga ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os users com os campos principais
    cursor.execute("SELECT id, username, role, created_at FROM users")
    users = cursor.fetchall()

    # Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Envia a lista de users para o template
    return render_template("users_listar.html", users=users)


# ============================
# LISTAR ANIMAIS (por tipo de utilizador)
# ============================
@app.route("/animais_listar")
def animais_listar():
    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Conectar ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # ADMIN: vê todos os animais
    if session.get("role") == "admin":
        cursor.execute("""
            SELECT animais.id, animais.nome, animais.especie, animais.raca, animais.data_nascimento,
                   clientes.nome AS dono
            FROM animais
            LEFT JOIN clientes ON animais.cliente_id = clientes.id
            ORDER BY animais.nome
        """)

    # STAFF: vê todos os animais (sem poder apagar no template)
    elif session.get("role") == "staff":
        cursor.execute("""
            SELECT animais.id, animais.nome, animais.especie, animais.raca, animais.data_nascimento,
                   clientes.nome AS dono
            FROM animais
            LEFT JOIN clientes ON animais.cliente_id = clientes.id
            ORDER BY animais.nome
        """)

    # CLIENTE: vê apenas os seus próprios animais
    elif session.get("role") == "cliente":
        cursor.execute("""
            SELECT id, nome, especie, raca, idade
            FROM animais
            WHERE cliente_id = %s
            ORDER BY nome
        """, (session.get("cliente_id"),))

    else:
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    animais = cursor.fetchall()

    # Fechar conexão
    cursor.close()
    conexao.close()

    # Enviar os dados para o template
    return render_template("animais_listar.html", animais=animais)

# ============================
# LISTAR CONSULTAS (por tipo de utilizador)
# ============================
@app.route("/consultas_listar")
def consultas_listar():
    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Conectar ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # ADMIN e STAFF: veem todas as consultas
    if session.get("role") in ["admin", "staff"]:
        cursor.execute("""
            SELECT 
                consultas.id,
                clientes.nome AS cliente,
                animais.nome AS animal,
                consultas.data_hora,
                consultas.motivo,
                consultas.notas,
                consultas.created_at
            FROM consultas
            INNER JOIN animais ON consultas.animal_id = animais.id
            INNER JOIN clientes ON animais.cliente_id = clientes.id
            ORDER BY consultas.data_hora DESC
        """)

    # CLIENTE: vê apenas as consultas dos seus próprios animais
    elif session.get("role") == "cliente":
        cursor.execute("""
            SELECT
                consultas.id,
                animais.nome AS animal,
                consultas.data_hora,
                consultas.motivo,
                consultas.notas,
                consultas.created_at
            FROM consultas
            INNER JOIN animais ON consultas.animal_id = animais.id
            WHERE animais.cliente_id = %s
            ORDER BY consultas.data_hora DESC
        """, (session.get("cliente_id"),))

    else:
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    consultas = cursor.fetchall()

    # Fechar cursor e conexão
    cursor.close()
    conexao.close()

    # Enviar as consultas para o template
    return render_template("consultas_listar.html", consultas=consultas)

# ============================
# MEUS ANIMAIS (CLIENTE)
# ============================
@app.route("/meus_animais")
def meus_animais():
    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem aceder
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Conectar ao banco de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar apenas os animais do cliente logado
    cursor.execute("""
        SELECT id, nome, especie, raca, data_nascimento
        FROM animais
        WHERE cliente_id = %s
        ORDER BY nome
    """, (session.get("cliente_id"),))

    animais = cursor.fetchall()

    # Fechar conexão
    cursor.close()
    conexao.close()

    # Enviar os dados para o template
    return render_template("meus_animais.html", animais=animais)

# ============================================================
# VINCULAR O CLIENTE AO UTILIZADOR 
# ============================================================
@app.route("/vincular_cliente_utilizador", methods=["GET", "POST"])
def vincular_cliente_utilizador():
    # Apenas admin pode fazer essa operação
    if session.get("role") != "admin":
        flash("Acesso restrito.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        # Recebe os IDs selecionados no formulário
        cliente_id = request.form["cliente_id"]
        utilizador_id = request.form["utilizador_id"]

        # Atualiza o cliente para vincular ao utilizador
        cursor.execute("""
            UPDATE clientes SET utilizador_id = %s WHERE id = %s
        """, (utilizador_id, cliente_id))

        conexao.commit()
        flash("Cliente vinculado ao utilizador com sucesso.")
        return redirect(url_for("dashboard"))

    # Busca utilizadores com role 'cliente' que ainda não têm cliente vinculado
    cursor.execute("""
        SELECT id, username FROM utilizadores
        WHERE role = 'cliente' AND id NOT IN (
            SELECT utilizador_id FROM clientes WHERE utilizador_id IS NOT NULL
        )
    """)
    utilizadores = cursor.fetchall()

    # Busca clientes que ainda não têm utilizador vinculado
    cursor.execute("""
        SELECT id, nome FROM clientes
        WHERE utilizador_id IS NULL
    """)
    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Mostra o formulário com as listas de opções
    return render_template("vincular_cliente_utilizador.html", utilizadores=utilizadores, clientes=clientes)

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