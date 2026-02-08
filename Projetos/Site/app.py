# Importa a classe Flask e outras funções necessárias
from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for, session, flash
import json
import requests
import datetime

# Função que cria a ligação com o banco de dados MySQL
def ligar_db():
       return mysql.connector.connect(
                host="62.28.39.135",      # Endereço do servidor MySQL
                user="efa0125",           # Nome do utilizador da base de dados
                password="123.Abc",       # Palavra-passe da base de dados
                database="efa0125_08_vet_clinic"  # Nome da base de dados
       )
        
################ CRIAÇÃO DA APLICAÇÃO FLASK #################
# Cria a aplicação Flask
app = Flask(__name__)

# Chave secreta usada para sessões (necessária para login)
app.secret_key = "123"

# ============================
# Funções de permissões
# ============================

def admin():
    # Retorna True se o utilizador tiver o papel "admin"
    return session.get("role") == "admin"

def staff():
    # Retorna True se o utilizador tiver o papel "staff"
    return session.get("role") == "staff"

def is_cliente():
    # Retorna True se o utilizador tiver o papel "cliente"
    return session.get("role") == "cliente"

# ============================
# Disponibilizar funções no Jinja
# ============================

# Esta função diz ao Flask para disponibilizar variáveis e funções
# automaticamente em TODOS os templates HTML
@app.context_processor
def inject_roles():
    # Torna as funções admin(), staff() e cliente() acessíveis no HTML
    return dict(
        admin=admin,
        staff=staff,
        is_cliente=is_cliente
    )
    
def datetime_ano():
    # Retorna o ano atual para usar no footer
    return {"ano": datetime.datetime.now().year}

# ============================
# ROTA PRINCIPAL (INDEX)
# ============================
@app.route("/")
def index():

    # Se o utilizador já estiver autenticado,
    # redireciona para o dashboard.
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    # Se NÃO estiver autenticado,
    # mostra a página inicial pública.
    return render_template("index.html")

# ============================
# LOGIN
# ============================
@app.route("/login", methods=["GET", "POST"])
def login():
    # Se já existe sessão ativa, evita novo login e redireciona para o dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    # GET → apenas mostra o formulário de login
    if request.method == "GET":
        return render_template("login.html")

    # POST → recolhe os dados enviados pelo formulário
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # Verifica se os campos obrigatórios foram preenchidos
    if not username or not password:
        flash("Preencha todos os campos.")
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Procura o utilizador com username e password correspondentes
        cursor.execute("""
            SELECT id, username, password, role, cliente_id
            FROM users
            WHERE username = %s AND password = %s
        """, (username, password))

        user = cursor.fetchone()

        # Se não encontrou utilizador, as credenciais são inválidas
        if not user:
            flash("Credenciais inválidas.")
            return redirect(url_for("login"))

        # LOGIN OK → limpa sessão antiga e cria nova
        session.clear()
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        session["username"] = user["username"]

        # Se o utilizador for cliente, deve ter cliente_id associado
        if user["role"] == "cliente":
            if not user["cliente_id"]:
                flash("Erro: este utilizador cliente não está associado a um cliente.")
                return redirect(url_for("login"))

            # Guarda o cliente_id na sessão para filtrar dados do cliente
            session["cliente_id"] = user["cliente_id"]

        flash("Login efetuado com sucesso!")
        return redirect(url_for("dashboard"))

    except Exception as erro:
        # Regista o erro e mostra mensagem genérica
        app.logger.exception("ERRO AO EFETUAR LOGIN")
        flash("Erro ao efetuar login. Tente novamente.")
        return redirect(url_for("login"))

    finally:
        # Fecha a ligação ao banco
        cursor.close()
        conexao.close()
        
# ============================
# DASHBOARD (área principal após login)
# ============================
@app.route("/dashboard")
def dashboard():
    # Verifica se existe sessão ativa; caso contrário, redireciona para login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Obtém informações essenciais do utilizador para exibir no dashboard
    username = session.get("username")
    role = session.get("role")

    # Renderiza o dashboard com os dados do utilizador autenticado
    return render_template("dashboard.html",
                           username=username,
                           role=role)
    
# ============================
# CRIAR UTILIZADOR (apenas admin)
# ============================
@app.route("/criar_user", methods=["GET", "POST"])
def criar_user():
    # Apenas administradores podem criar utilizadores
    if not admin():
        flash("Apenas administradores podem criar utilizadores.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Carrega lista de clientes para o dropdown
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        # POST real (clicou no botão Criar)
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados enviados pelo formulário
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            role_form = request.form.get("role", "").strip()

            # Trata o cliente_id (pode vir vazio)
            cliente_id_raw = request.form.get("cliente_id", "").strip()
            cliente_id = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Validação simples
            if not username or not password:
                flash("Username e password são obrigatórios.")
                return render_template("criar_user.html", clientes=clientes)


            # Insere o novo utilizador
            cursor.execute("""
                INSERT INTO users (username, password, role, cliente_id)
                VALUES (%s, %s, %s, %s)
            """, (username, password, role_form, cliente_id))

            conexao.commit()
            flash("Utilizador criado com sucesso!")
            return redirect(url_for("users_listar"))

        # GET normal → mostra o formulário
        return render_template("criar_user.html", clientes=clientes)

    finally:
        cursor.close()
        conexao.close()


# ============================
# CRIAR CLIENTE (admin e staff)
# ============================
@app.route("/criar_cliente", methods=["GET", "POST"])
def criar_cliente():
    # Apenas admin e staff podem criar clientes
    if not (admin() or staff()):
        flash("Não tem permissão para criar clientes.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # POST real (clicou no botão Criar)
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados enviados pelo formulário
            nome = request.form.get("nome", "").strip()
            telefone = request.form.get("telefone", "").strip()
            email = request.form.get("email", "").strip()
            morada = request.form.get("morada", "").strip()

            # Validação simples
            if not nome:
                flash("O nome é obrigatório.")
                return render_template("criar_cliente.html")

            # Insere o cliente na base de dados
            cursor.execute("""
                INSERT INTO clientes (nome, telefone, email, morada)
                VALUES (%s, %s, %s, %s)
            """, (nome, telefone, email, morada))

            conexao.commit()
            flash("Cliente criado com sucesso!")
            return redirect(url_for("clientes_listar"))

        # GET normal → mostra o formulário
        return render_template("criar_cliente.html")

    except Exception:
        app.logger.exception("ERRO AO CRIAR CLIENTE")
        conexao.rollback()
        flash("Erro ao criar cliente.")
        return redirect(url_for("clientes_listar"))

    finally:
        cursor.close()
        conexao.close()


# ============================
# CRIAR ANIMAL (admin, staff e cliente)
# ============================
@app.route("/criar_animal", methods=["GET", "POST"])
def criar_animal():
    # Apenas admin e staff podem criar animais
    if not (admin() or staff()):
        flash("Não tem permissão para criar animais.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Carrega lista de clientes para o dropdown
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        # POST real (clicou no botão Criar)
        if request.method == "POST" and request.form.get("acao") == "salvar":

            nome = request.form.get("nome", "").strip()
            especie = request.form.get("especie", "").strip()
            raca = request.form.get("raca", "").strip()
            data_nascimento = request.form.get("data_nascimento", "").strip()

            cliente_id_raw = request.form.get("cliente_id", "").strip()
            cliente_id = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Validação simples
            if not nome or not especie or not cliente_id:
                flash("Nome, espécie e cliente são obrigatórios.")
                return render_template("criar_animal.html", clientes=clientes)

            # Insere o animal
            cursor.execute("""
                INSERT INTO animais (cliente_id, nome, especie, raca, data_nascimento)
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, nome, especie, raca, data_nascimento or None))

            conexao.commit()
            flash("Animal criado com sucesso!")
            return redirect(url_for("animais_listar"))

        # GET normal
        return render_template("criar_animal.html", clientes=clientes)

    finally:
        cursor.close()
        conexao.close()


# ============================
# CRIAR CONSULTA (admin, staff e cliente)
# ============================
@app.route("/criar_consulta", methods=["GET", "POST"])
def criar_consulta():
    # Apenas admin e staff podem criar consultas
    if not (admin() or staff()):
        flash("Não tem permissão para criar consultas.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Carrega lista de animais (com nome do cliente)
    cursor.execute("""
        SELECT animais.id, animais.nome, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome
    """)
    animais = cursor.fetchall()

    try:
        if request.method == "POST" and request.form.get("acao") == "salvar":

            animal_id_raw = request.form.get("animal_id", "").strip()
            animal_id = int(animal_id_raw) if animal_id_raw.isdigit() else None

            data_hora = request.form.get("data_hora", "").strip()
            motivo = request.form.get("motivo", "").strip()
            notas = request.form.get("notas", "").strip()

            # Validação simples
            if not animal_id or not data_hora:
                flash("Animal e data/hora são obrigatórios.")
                return render_template("criar_consulta.html", animais=animais)

            # Insere a consulta
            cursor.execute("""
                INSERT INTO consultas (animal_id, data_hora, motivo, notas)
                VALUES (%s, %s, %s, %s)
            """, (animal_id, data_hora, motivo, notas))

            conexao.commit()
            flash("Consulta criada com sucesso!")
            return redirect(url_for("consultas_listar"))

        return render_template("criar_consulta.html", animais=animais)

    finally:
        cursor.close()
        conexao.close()

    # ============================
    # GET ou POST AUTOMÁTICO
    # ============================
    return render_template("criar_consulta.html", clientes=clientes, animais=animais)

# ============================
# EDITAR CLIENTE (admin e staff)
# ============================
@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    # Apenas admin e staff podem editar clientes
    if not (admin() or staff()):
        flash("Não tem permissão para editar clientes.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca o cliente pelo ID
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()

    if not cliente:
        flash("Cliente não encontrado.")
        return redirect(url_for("clientes_listar"))

    try:
        # POST real (clicou em Guardar)
        if request.method == "POST" and request.form.get("acao") == "salvar":

            nome = request.form.get("nome", "").strip()
            telefone = request.form.get("telefone", "").strip()
            email = request.form.get("email", "").strip()
            morada = request.form.get("morada", "").strip()

            # Validação simples
            if not nome:
                flash("O nome é obrigatório.")
                return render_template("editar_cliente.html", cliente=request.form)

            # Atualiza o cliente
            cursor.execute("""
                UPDATE clientes
                SET nome=%s, telefone=%s, email=%s, morada=%s
                WHERE id=%s
            """, (nome, telefone, email, morada, id))

            conexao.commit()
            flash("Cliente atualizado com sucesso!")
            return redirect(url_for("clientes_listar"))

        # GET normal
        return render_template("editar_cliente.html", cliente=cliente)

    except Exception:
        app.logger.exception("ERRO AO EDITAR CLIENTE")
        conexao.rollback()
        flash("Erro ao atualizar cliente.")
        return redirect(url_for("clientes_listar"))

    finally:
        cursor.close()
        conexao.close()

# ============================
# EDITAR CONSULTA (apenas admin e staff)
# ============================
@app.route("/editar_consulta/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):
    # Apenas admin e staff podem editar consultas
    if not (admin() or staff()):
        flash("Não tem permissão para editar consultas.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca a consulta pelo ID
    cursor.execute("SELECT * FROM consultas WHERE id = %s", (id,))
    consulta = cursor.fetchone()

    if not consulta:
        flash("Consulta não encontrada.")
        return redirect(url_for("consultas_listar"))

    # Carrega lista de animais
    cursor.execute("""
        SELECT animais.id, animais.nome, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome
    """)
    animais = cursor.fetchall()

    try:
        if request.method == "POST" and request.form.get("acao") == "salvar":

            animal_id_raw = request.form.get("animal_id", "").strip()
            animal_id = int(animal_id_raw) if animal_id_raw.isdigit() else None

            data_hora = request.form.get("data_hora", "").strip()
            motivo = request.form.get("motivo", "").strip()
            notas = request.form.get("notas", "").strip()

            if not animal_id or not data_hora:
                flash("Animal e data/hora são obrigatórios.")
                return render_template("editar_consulta.html",
                                       consulta=request.form,
                                       animais=animais)

            cursor.execute("""
                UPDATE consultas
                SET animal_id=%s, data_hora=%s, motivo=%s, notas=%s
                WHERE id=%s
            """, (animal_id, data_hora, motivo, notas, id))

            conexao.commit()
            flash("Consulta atualizada com sucesso!")
            return redirect(url_for("consultas_listar"))

        return render_template("editar_consulta.html",
                               consulta=consulta,
                               animais=animais)

    finally:
        cursor.close()
        conexao.close()

# ============================
# EDITAR ANIMAL (admin, staff e cliente)
# ============================
@app.route("/editar_animal/<int:id>", methods=["GET", "POST"])
def editar_animal(id):
    # Apenas admin e staff podem editar animais
    if not (admin() or staff()):
        flash("Não tem permissão para editar animais.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca o animal pelo ID
    cursor.execute("SELECT * FROM animais WHERE id = %s", (id,))
    animal = cursor.fetchone()

    if not animal:
        flash("Animal não encontrado.")
        return redirect(url_for("animais_listar"))

    # Carrega lista de clientes
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        if request.method == "POST" and request.form.get("acao") == "salvar":

            nome = request.form.get("nome", "").strip()
            especie = request.form.get("especie", "").strip()
            raca = request.form.get("raca", "").strip()
            data_nascimento = request.form.get("data_nascimento", "").strip()

            cliente_id_raw = request.form.get("cliente_id", "").strip()
            cliente_id = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            if not nome or not especie or not cliente_id:
                flash("Nome, espécie e cliente são obrigatórios.")
                return render_template("editar_animal.html",
                                       animal=request.form,
                                       clientes=clientes)

            cursor.execute("""
                UPDATE animais
                SET cliente_id=%s, nome=%s, especie=%s, raca=%s, data_nascimento=%s
                WHERE id=%s
            """, (cliente_id, nome, especie, raca, data_nascimento or None, id))

            conexao.commit()
            flash("Animal atualizado com sucesso!")
            return redirect(url_for("animais_listar"))

        return render_template("editar_animal.html",
                               animal=animal,
                               clientes=clientes)

    finally:
        cursor.close()
        conexao.close()

# ============================
# EDITAR UTILIZADOR (apenas admin)
# ============================
@app.route("/editar_user/<int:id>", methods=["GET", "POST"])
def editar_user(id):
    # Apenas admin e staff podem editar utilizadores
    if not (admin() or staff()):
        flash("Não tem permissão para editar utilizadores.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca o utilizador pelo ID
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()

    if not user:
        flash("Utilizador não encontrado.")
        return redirect(url_for("users_listar"))

    # Carrega lista de clientes
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        if request.method == "POST" and request.form.get("acao") == "salvar":

            username = request.form.get("username", "").strip()
            role_form = request.form.get("role", "").strip()

            cliente_id_raw = request.form.get("cliente_id", "").strip()
            cliente_id = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Apenas admin pode alterar password
            nova_password = None
            if admin():
                nova_password_raw = request.form.get("password", "").strip()
                if nova_password_raw:
                    nova_password = generate_password_hash(nova_password_raw)

            if not username:
                flash("Username é obrigatório.")
                return render_template("editar_user.html",
                                       user=request.form,
                                       clientes=clientes)

            # Atualiza o utilizador
            if nova_password:
                cursor.execute("""
                    UPDATE users
                    SET username=%s, role=%s, cliente_id=%s, password=%s
                    WHERE id=%s
                """, (username, role_form, cliente_id, nova_password, id))
            else:
                cursor.execute("""
                    UPDATE users
                    SET username=%s, role=%s, cliente_id=%s
                    WHERE id=%s
                """, (username, role_form, cliente_id, id))

            conexao.commit()
            flash("Utilizador atualizado com sucesso!")
            return redirect(url_for("users_listar"))

        return render_template("editar_user.html",
                               user=user,
                               clientes=clientes)

    finally:
        cursor.close()
        conexao.close()

        
# ============================
# APAGAR CLIENTE (apenas admin)
# ============================
@app.route("/apagar_cliente/<int:id>", methods=["POST"])
def apagar_cliente(id):
    # Apenas administradores podem apagar clientes
    if not admin():
        flash("Apenas administradores podem apagar clientes.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor()

    # Apaga o cliente pelo ID
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Cliente apagado com sucesso!")
    return redirect(url_for("clientes_listar"))

# ============================
# APAGAR ANIMAL (apenas admin)
# ============================
@app.route("/apagar_animal/<int:id>", methods=["POST"])
def apagar_animal(id):
    # Apenas administradores podem apagar animais
    if not admin():
        flash("Apenas administradores podem apagar animais.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM animais WHERE id = %s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Animal apagado com sucesso!")
    return redirect(url_for("animais_listar"))

# ============================
# APAGAR CONSULTA (apenas admin)
# ============================
@app.route("/apagar_consulta/<int:id>", methods=["POST"])
def apagar_consulta(id):
    # Verifica se existe sessão ativa; caso contrário, redireciona para login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem apagar consultas
    if not admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Tenta apagar a consulta pelo ID
        cursor.execute("DELETE FROM consultas WHERE id = %s", (id,))
        conexao.commit()
        flash("Consulta apagada com sucesso!")

    except Exception as erro:
        # Regista o erro e desfaz a operação
        app.logger.exception("ERRO AO APAGAR CONSULTA")
        conexao.rollback()
        flash("Erro ao apagar consulta. Verifique dependências ou tente novamente.")

    finally:
        # Fecha a ligação ao banco
        cursor.close()
        conexao.close()

    # Redireciona após tentativa de apagar
    return redirect(url_for("consultas_listar"))

# ============================
# APAGAR UTILIZADOR (apenas admin)
# ============================
@app.route("/apagar_user/<int:id>", methods=["POST"])
def apagar_user(id):
    if not admin():
        flash("Apenas administradores podem apagar utilizadores.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Utilizador apagado com sucesso!")
    return redirect(url_for("users_listar"))

# ============================
# LISTAR CLIENTES (admin e staff)
# ============================
@app.route("/clientes")
def clientes_listar():
    # Apenas admin e staff podem ver a lista completa de clientes
    if not (admin() or staff()):
        flash("Não tem permissão para ver clientes.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os clientes ordenados por nome
    cursor.execute("SELECT * FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    # Fecha a ligação
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de clientes
    return render_template("clientes_listar.html", clientes=clientes)

# ============================
# LISTAR USERS (apenas admin)
# ============================
@app.route("/users")
def users_listar():
    # Apenas administradores e staff podem ver a lista completa de utilizadores
    if not (admin() or staff()):
        flash("Não tem permissão para ver utilizadores.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os utilizadores e junta o nome do cliente associado (se existir)
    cursor.execute("""
        SELECT users.*, clientes.nome AS cliente_nome
        FROM users
        LEFT JOIN clientes ON clientes.id = users.cliente_id
        ORDER BY users.username
    """)
    users = cursor.fetchall()

    # Fecha a ligação
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de utilizadores
    return render_template("users_listar.html", users=users)

# ============================
# LISTAR ANIMAIS
# ============================
@app.route("/animais")
def animais_listar():
    # Apenas admin e staff podem ver todos os animais
    if not (admin() or staff()):
        flash("Não tem permissão para ver animais.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os animais e junta o nome do cliente dono
    cursor.execute("""
        SELECT animais.*, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome
    """)
    animais = cursor.fetchall()

    # Fecha a ligação
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de animais
    return render_template("animais_listar.html", animais=animais)

# ============================
# LISTAR CONSULTAS
# ============================
@app.route("/consultas")
def consultas_listar():
    # Apenas admin e staff podem ver todas as consultas
    if not (admin() or staff()):
        flash("Não tem permissão para ver consultas.")
        return redirect(url_for("dashboard"))

    # Liga à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todas as consultas, juntando o nome do animal e do cliente
    cursor.execute("""
        SELECT consultas.*, 
               animais.nome AS animal_nome,
               clientes.nome AS cliente_nome
        FROM consultas
        INNER JOIN animais ON animais.id = consultas.animal_id
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY consultas.data_hora DESC
    """)
    consultas = cursor.fetchall()

    # Fecha ligação
    cursor.close()
    conexao.close()

    # Renderiza o template
    return render_template("consultas_listar.html", consultas=consultas)

# ============================
# MINHA CONTA (apenas cliente)
# ============================
@app.route("/minha_conta")
def minha_conta():
    # Verifica se existe sessão ativa; caso contrário, redireciona para login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem aceder a esta página
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Busca os dados do cliente associado ao utilizador autenticado
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (session.get("cliente_id"),))
        cliente = cursor.fetchone()

        # Renderiza a página com os dados do cliente
        return render_template("minha_conta.html", cliente=cliente)

    finally:
        # Fecha a ligação ao banco
        cursor.close()
        conexao.close()
        
# ============================
# MEUS ANIMAIS (apenas cliente)
# ============================
@app.route("/meus_animais")
def meus_animais():
    # Verifica se existe sessão ativa; caso contrário, redireciona para login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem aceder a esta página
    if session.get("role") != "cliente":
        flash("Apenas clientes podem ver os seus próprios animais.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Busca todos os animais pertencentes ao cliente autenticado
        cursor.execute("""
            SELECT id, nome, especie, raca, data_nascimento
            FROM animais
            WHERE cliente_id = %s
            ORDER BY nome
        """, (session.get("cliente_id"),))

        animais = cursor.fetchall()

        # Renderiza a página com a lista de animais
        return render_template("meus_animais.html", animais=animais)

    finally:
        # Fecha a ligação ao banco
        cursor.close()
        conexao.close()
        
# ============================
# MINHAS CONSULTAS (apenas cliente)
# ============================
@app.route("/minhas_consultas")
def minhas_consultas():
    # Verifica se existe sessão ativa; caso contrário, redireciona para login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas clientes podem aceder a esta página
    if session.get("role") != "cliente":
        flash("Apenas clientes podem ver as suas consultas.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Busca todas as consultas dos animais pertencentes ao cliente autenticado
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

        consultas = cursor.fetchall()

        # Renderiza a página com a lista de consultas
        return render_template("minhas_consultas.html", consultas=consultas)

    finally:
        # Fecha a ligação ao banco
        cursor.close()
        conexao.close()

# ============================
# LOGOUT
# ============================
@app.route("/logout")
def logout():
    # Limpa todos os dados da sessão, terminando a autenticação do utilizador
    session.clear()

    # Redireciona o utilizador para a página de login após sair
    return redirect(url_for("login"))

# Iniciar a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)