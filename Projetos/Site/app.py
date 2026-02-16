# =============================================================================
# app.py — Aplicação Flask para Gestão de Clínica Veterinária
# =============================================================================
# Este ficheiro é o núcleo principal da aplicação web.
# Contém todas as rotas (URLs), lógica de negócio e ligação à base de dados.
# =============================================================================

# --- Importações necessárias ---
from flask import Flask                                          # Framework web principal
import mysql.connector                                          # Conector para base de dados MySQL
from flask import render_template, request, redirect, url_for, session, flash
# render_template  → carrega ficheiros HTML (templates)
# request          → acede aos dados enviados pelo utilizador (formulários, etc.)
# redirect         → redireciona o utilizador para outra URL
# url_for          → gera URLs dinamicamente a partir do nome das funções
# session          → guarda dados do utilizador entre pedidos (ex: login)
# flash            → envia mensagens temporárias para mostrar ao utilizador
import json                                                     # Manipulação de dados JSON
import requests                                                 # Pedidos HTTP externos (se necessário)
import datetime                                                 # Manipulação de datas e horas


# =============================================================================
# LIGAÇÃO À BASE DE DADOS
# =============================================================================

def ligar_db():
    """
    Função que cria e devolve uma ligação ao servidor MySQL.
    Deve ser chamada no início de cada rota que precise de aceder à BD.
    Lembre-se sempre de fechar a ligação no bloco 'finally'.
    """
    return mysql.connector.connect(
        host="62.28.39.135",                    # Endereço IP do servidor MySQL
        user="efa0125",                          # Nome de utilizador da base de dados
        password="123.Abc",                      # Palavra-passe da base de dados
        database="efa0125_08_vet_clinic"         # Nome da base de dados a utilizar
    )


# =============================================================================
# CRIAÇÃO DA APLICAÇÃO FLASK
# =============================================================================

# Cria a instância principal da aplicação Flask.
# '__name__' indica ao Flask o nome do módulo atual.
app = Flask(__name__)

# Chave secreta usada para assinar e proteger os dados de sessão (cookies).
# Em produção, deve ser uma string longa, aleatória e guardada de forma segura.
app.secret_key = "123"


# =============================================================================
# FUNÇÕES DE VERIFICAÇÃO DE PERMISSÕES (ROLES)
# =============================================================================
# Estas funções verificam o papel (role) do utilizador guardado na sessão.
# São usadas para controlar o acesso às diferentes rotas da aplicação.

def admin():
    """Devolve True se o utilizador autenticado tiver o papel 'admin'."""
    return session.get("role") == "admin"

def staff():
    """Devolve True se o utilizador autenticado tiver o papel 'staff'."""
    return session.get("role") == "staff"

def is_cliente():
    """Devolve True se o utilizador autenticado tiver o papel 'cliente'."""
    return session.get("role") == "cliente"


# =============================================================================
# CONTEXT PROCESSOR — Disponibiliza funções nos templates HTML (Jinja2)
# =============================================================================

@app.context_processor
def inject_roles():
    """
    Torna as funções admin(), staff() e is_cliente() disponíveis
    automaticamente em TODOS os templates HTML sem necessidade de
    as passar manualmente em cada render_template().
    """
    return dict(
        admin=admin,
        staff=staff,
        is_cliente=is_cliente
    )


def datetime_ano():
    """
    Devolve o ano atual num dicionário.
    Pode ser usada para exibir o ano no rodapé (footer) dos templates.
    """
    return {"ano": datetime.datetime.now().year}


# =============================================================================
# ROTA PRINCIPAL — Página Inicial (/)
# =============================================================================

@app.route("/")
def index():
    """
    Rota principal da aplicação.
    - Se o utilizador já estiver autenticado (sessão ativa), redireciona para o dashboard.
    - Se não estiver autenticado, mostra a página inicial pública.
    """
    # Verifica se existe uma sessão ativa (utilizador já fez login)
    if "user_id" in session:
        return redirect(url_for("dashboard"))   # Redireciona para o dashboard

    # Utilizador não autenticado → mostra a página inicial pública
    return render_template("index.html")


# =============================================================================
# ROTA DE LOGIN — /login
# =============================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Trata o processo de autenticação do utilizador.
    - GET  → mostra o formulário de login.
    - POST → valida as credenciais e cria sessão se corretas.
    """
    # Se o utilizador já tiver sessão ativa, evita login duplo
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    # Pedido GET → apenas mostra o formulário de login
    if request.method == "GET":
        return render_template("login.html")

    # Pedido POST → recolhe os dados do formulário enviado
    username = request.form.get("username", "").strip()   # Remove espaços desnecessários
    password = request.form.get("password", "").strip()

    # Validação: os dois campos são obrigatórios
    if not username or not password:
        flash("Preencha todos os campos.")
        return redirect(url_for("login"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)   # dictionary=True → resultados como dicionários

    try:
        # Consulta SQL: procura utilizador com o username e password fornecidos
        cursor.execute("""
            SELECT id, username, password, role, cliente_id
            FROM users
            WHERE username = %s AND password = %s
        """, (username, password))

        user = cursor.fetchone()   # Obtém o primeiro resultado (ou None se não existir)

        # Se não encontrou utilizador, as credenciais são inválidas
        if not user:
            flash("Credenciais inválidas.")
            return redirect(url_for("login"))

        # Login bem-sucedido → limpa sessão anterior e cria nova sessão
        session.clear()
        session["user_id"]  = user["id"]        # type: ignore   # Guarda o ID do utilizador
        session["role"]     = user["role"]       # type: ignore   # Guarda o papel (admin/staff/cliente)
        session["username"] = user["username"]   # type: ignore   # Guarda o username para exibição

        # Tratamento especial para utilizadores com papel 'cliente'
        if user["role"] == "cliente":            # type: ignore
            # Clientes devem ter um cliente_id associado na tabela users
            if not user["cliente_id"]:           # type: ignore
                flash("Erro: este utilizador cliente não está associado a um cliente.")
                return redirect(url_for("login"))

            # Guarda o cliente_id na sessão para filtrar dados apenas do cliente autenticado
            session["cliente_id"] = user["cliente_id"]   # type: ignore

        flash("Login efetuado com sucesso!")
        return redirect(url_for("dashboard"))   # Redireciona para o dashboard após login

    except Exception as erro:
        # Regista o erro no log da aplicação e mostra mensagem genérica ao utilizador
        app.logger.exception("ERRO AO EFETUAR LOGIN")
        flash("Erro ao efetuar login. Tente novamente.")
        return redirect(url_for("login"))

    finally:
        # Fecha sempre o cursor e a ligação, independentemente de erro ou sucesso
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA DO DASHBOARD — /dashboard
# =============================================================================

@app.route("/dashboard")
def dashboard():
    """
    Página principal após o login.
    Exibe uma visão geral para o utilizador autenticado.
    Redireciona para o login se não existir sessão ativa.
    """
    # Proteção: verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Obtém informações da sessão para exibir no dashboard
    username = session.get("username")   # Nome do utilizador autenticado
    role     = session.get("role")       # Papel do utilizador (admin/staff/cliente)

    # Renderiza o template do dashboard com os dados do utilizador
    return render_template("dashboard.html",
                           username=username,
                           role=role)


# =============================================================================
# ROTA CRIAR UTILIZADOR — /criar_user (apenas admin)
# =============================================================================

@app.route("/criar_user", methods=["GET", "POST"])
def criar_user():
    """
    Permite ao administrador criar novos utilizadores no sistema.
    Apenas utilizadores com papel 'admin' têm acesso a esta rota.
    - GET  → mostra o formulário de criação.
    - POST → valida e insere o novo utilizador na base de dados.
    """
    # Controlo de acesso: apenas administradores podem criar utilizadores
    if not admin():
        flash("Apenas administradores podem criar utilizadores.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Carrega a lista de clientes para preencher o dropdown no formulário
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        # Pedido POST com ação 'salvar' → processar criação do utilizador
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados enviados pelo formulário
            username        = request.form.get("username", "").strip()
            password        = request.form.get("password", "").strip()
            role_form       = request.form.get("role", "").strip()

            # Trata o cliente_id — pode ser vazio (para admin/staff) ou um número inteiro
            cliente_id_raw  = request.form.get("cliente_id", "").strip()
            cliente_id      = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Validação: username e password são obrigatórios
            if not username or not password:
                flash("Username e password são obrigatórios.")
                return render_template("criar_user.html", clientes=clientes)

            # Insere o novo utilizador na tabela 'users'
            cursor.execute("""
                INSERT INTO users (username, password, role, cliente_id)
                VALUES (%s, %s, %s, %s)
            """, (username, password, role_form, cliente_id))

            conexao.commit()   # Confirma a transação na base de dados
            flash("Utilizador criado com sucesso!")
            return redirect(url_for("users_listar"))   # Redireciona para a lista de utilizadores

        # Pedido GET → mostra o formulário de criação
        return render_template("criar_user.html", clientes=clientes)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA CRIAR CLIENTE — /criar_cliente (admin e staff)
# =============================================================================

@app.route("/criar_cliente", methods=["GET", "POST"])
def criar_cliente():
    """
    Permite criar um novo cliente no sistema.
    Acessível por administradores e staff.
    - GET  → mostra o formulário de criação.
    - POST → valida e insere o novo cliente na base de dados.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para criar clientes.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Pedido POST com ação 'salvar' → processar criação do cliente
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados do formulário
            nome     = request.form.get("nome", "").strip()
            telefone = request.form.get("telefone", "").strip()
            email    = request.form.get("email", "").strip()
            morada   = request.form.get("morada", "").strip()

            # Validação: o nome é obrigatório
            if not nome:
                flash("O nome é obrigatório.")
                return render_template("criar_cliente.html")

            # Insere o novo cliente na tabela 'clientes'
            cursor.execute("""
                INSERT INTO clientes (nome, telefone, email, morada)
                VALUES (%s, %s, %s, %s)
            """, (nome, telefone, email, morada))

            conexao.commit()   # Confirma a transação
            flash("Cliente criado com sucesso!")
            return redirect(url_for("clientes_listar"))   # Redireciona para a lista de clientes

        # Pedido GET → mostra o formulário de criação
        return render_template("criar_cliente.html")

    except Exception:
        # Em caso de erro, regista no log, desfaz a transação e mostra mensagem
        app.logger.exception("ERRO AO CRIAR CLIENTE")
        conexao.rollback()   # Reverte alterações em caso de erro
        flash("Erro ao criar cliente.")
        return redirect(url_for("clientes_listar"))

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA CRIAR ANIMAL — /criar_animal (admin e staff)
# =============================================================================

@app.route("/criar_animal", methods=["GET", "POST"])
def criar_animal():
    """
    Permite criar um novo animal no sistema associado a um cliente.
    Acessível por administradores e staff.
    - GET  → mostra o formulário de criação.
    - POST → valida e insere o novo animal na base de dados.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para criar animais.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Carrega a lista de clientes para o dropdown do formulário
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        # Pedido POST com ação 'salvar' → processar criação do animal
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados do formulário
            nome             = request.form.get("nome", "").strip()
            especie          = request.form.get("especie", "").strip()
            raca             = request.form.get("raca", "").strip()
            data_nascimento  = request.form.get("data_nascimento", "").strip()

            # Trata o cliente_id — deve ser um número inteiro válido
            cliente_id_raw   = request.form.get("cliente_id", "").strip()
            cliente_id       = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Validação: nome, espécie e cliente são obrigatórios
            if not nome or not especie or not cliente_id:
                flash("Nome, espécie e cliente são obrigatórios.")
                return render_template("criar_animal.html", clientes=clientes)

            # Insere o novo animal na tabela 'animais'
            # Se a data de nascimento estiver vazia, guarda NULL na BD
            cursor.execute("""
                INSERT INTO animais (cliente_id, nome, especie, raca, data_nascimento)
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, nome, especie, raca, data_nascimento or None))

            conexao.commit()   # Confirma a transação
            flash("Animal criado com sucesso!")
            return redirect(url_for("animais_listar"))   # Redireciona para a lista de animais

        # Pedido GET → mostra o formulário de criação
        return render_template("criar_animal.html", clientes=clientes)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA CRIAR CONSULTA — /criar_consulta (admin e staff)
# =============================================================================

@app.route("/criar_consulta", methods=["GET", "POST"])
def criar_consulta():
    """
    Permite agendar uma nova consulta para um animal.
    Acessível por administradores e staff.
    - GET  → mostra o formulário de criação.
    - POST → valida e insere a nova consulta na base de dados.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para criar consultas.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Carrega a lista de animais com o nome do cliente dono
    # (para exibir no dropdown do formulário)
    cursor.execute("""
        SELECT animais.id, animais.nome, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome
    """)
    animais = cursor.fetchall()

    try:
        # Pedido POST com ação 'salvar' → processar criação da consulta
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Trata o animal_id — deve ser um número inteiro válido
            animal_id_raw = request.form.get("animal_id", "").strip()
            animal_id     = int(animal_id_raw) if animal_id_raw.isdigit() else None

            # Recolhe os restantes dados do formulário
            data_hora = request.form.get("data_hora", "").strip()
            motivo    = request.form.get("motivo", "").strip()
            notas     = request.form.get("notas", "").strip()

            # Validação: animal e data/hora são obrigatórios
            if not animal_id or not data_hora:
                flash("Animal e data/hora são obrigatórios.")
                return render_template("criar_consulta.html", animais=animais)

            # Insere a nova consulta na tabela 'consultas'
            cursor.execute("""
                INSERT INTO consultas (animal_id, data_hora, motivo, notas)
                VALUES (%s, %s, %s, %s)
            """, (animal_id, data_hora, motivo, notas))

            conexao.commit()   # Confirma a transação
            flash("Consulta criada com sucesso!")
            return redirect(url_for("consultas_listar"))   # Redireciona para a lista de consultas

        # Pedido GET → mostra o formulário de criação
        return render_template("criar_consulta.html", animais=animais)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()

    # Nota: Esta linha nunca é alcançada após o bloco try/finally,
    # mas foi mantida por compatibilidade com o código original.
    return render_template("criar_consulta.html", clientes=clientes, animais=animais)


# =============================================================================
# ROTA EDITAR CLIENTE — /editar_cliente/<id> (admin e staff)
# =============================================================================

@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    """
    Permite editar os dados de um cliente existente.
    O parâmetro 'id' é o identificador único do cliente na base de dados.
    - GET  → carrega e mostra os dados atuais do cliente no formulário.
    - POST → valida e atualiza os dados do cliente.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para editar clientes.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca o cliente pelo ID passado na URL
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()

    # Se o cliente não existir, mostra mensagem e redireciona
    if not cliente:
        flash("Cliente não encontrado.")
        return redirect(url_for("clientes_listar"))

    try:
        # Pedido POST com ação 'salvar' → processar atualização do cliente
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os novos dados do formulário
            nome     = request.form.get("nome", "").strip()
            telefone = request.form.get("telefone", "").strip()
            email    = request.form.get("email", "").strip()
            morada   = request.form.get("morada", "").strip()

            # Validação: o nome é obrigatório
            if not nome:
                flash("O nome é obrigatório.")
                return render_template("editar_cliente.html", cliente=request.form)

            # Atualiza os dados do cliente na base de dados
            cursor.execute("""
                UPDATE clientes
                SET nome=%s, telefone=%s, email=%s, morada=%s
                WHERE id=%s
            """, (nome, telefone, email, morada, id))

            conexao.commit()   # Confirma a transação
            flash("Cliente atualizado com sucesso!")
            return redirect(url_for("clientes_listar"))

        # Pedido GET → mostra formulário com os dados atuais do cliente
        return render_template("editar_cliente.html", cliente=cliente)

    except Exception:
        # Em caso de erro, regista no log, desfaz a transação e mostra mensagem
        app.logger.exception("ERRO AO EDITAR CLIENTE")
        conexao.rollback()   # Reverte alterações em caso de erro
        flash("Erro ao atualizar cliente.")
        return redirect(url_for("clientes_listar"))

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA EDITAR CONSULTA — /editar_consulta/<id> (admin e staff)
# =============================================================================

@app.route("/editar_consulta/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):
    """
    Permite editar os dados de uma consulta existente.
    O parâmetro 'id' é o identificador único da consulta na base de dados.
    - GET  → carrega e mostra os dados atuais da consulta no formulário.
    - POST → valida e atualiza os dados da consulta.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para editar consultas.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca a consulta pelo ID passado na URL
    cursor.execute("SELECT * FROM consultas WHERE id = %s", (id,))
    consulta = cursor.fetchone()

    # Se a consulta não existir, mostra mensagem e redireciona
    if not consulta:
        flash("Consulta não encontrada.")
        return redirect(url_for("consultas_listar"))

    # Carrega a lista de animais com o nome do cliente dono
    # (para o dropdown no formulário de edição)
    cursor.execute("""
        SELECT animais.id, animais.nome, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome
    """)
    animais = cursor.fetchall()

    try:
        # Pedido POST com ação 'salvar' → processar atualização da consulta
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Trata o animal_id — deve ser um número inteiro válido
            animal_id_raw = request.form.get("animal_id", "").strip()
            animal_id     = int(animal_id_raw) if animal_id_raw.isdigit() else None

            # Recolhe os restantes dados do formulário
            data_hora = request.form.get("data_hora", "").strip()
            motivo    = request.form.get("motivo", "").strip()
            notas     = request.form.get("notas", "").strip()

            # Validação: animal e data/hora são obrigatórios
            if not animal_id or not data_hora:
                flash("Animal e data/hora são obrigatórios.")
                return render_template("editar_consulta.html",
                                       consulta=request.form,
                                       animais=animais)

            # Atualiza os dados da consulta na base de dados
            cursor.execute("""
                UPDATE consultas
                SET animal_id=%s, data_hora=%s, motivo=%s, notas=%s
                WHERE id=%s
            """, (animal_id, data_hora, motivo, notas, id))

            conexao.commit()   # Confirma a transação
            flash("Consulta atualizada com sucesso!")
            return redirect(url_for("consultas_listar"))

        # Pedido GET → mostra formulário com os dados atuais da consulta
        return render_template("editar_consulta.html",
                               consulta=consulta,
                               animais=animais)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA EDITAR ANIMAL — /editar_animal/<id> (admin e staff)
# =============================================================================

@app.route("/editar_animal/<int:id>", methods=["GET", "POST"])
def editar_animal(id):
    """
    Permite editar os dados de um animal existente.
    O parâmetro 'id' é o identificador único do animal na base de dados.
    - GET  → carrega e mostra os dados atuais do animal no formulário.
    - POST → valida e atualiza os dados do animal.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para editar animais.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca o animal pelo ID passado na URL
    cursor.execute("SELECT * FROM animais WHERE id = %s", (id,))
    animal = cursor.fetchone()

    # Se o animal não existir, mostra mensagem e redireciona
    if not animal:
        flash("Animal não encontrado.")
        return redirect(url_for("animais_listar"))

    # Carrega a lista de clientes para o dropdown do formulário
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        # Pedido POST com ação 'salvar' → processar atualização do animal
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados do formulário
            nome            = request.form.get("nome", "").strip()
            especie         = request.form.get("especie", "").strip()
            raca            = request.form.get("raca", "").strip()
            data_nascimento = request.form.get("data_nascimento", "").strip()

            # Trata o cliente_id — deve ser um número inteiro válido
            cliente_id_raw  = request.form.get("cliente_id", "").strip()
            cliente_id      = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Validação: nome, espécie e cliente são obrigatórios
            if not nome or not especie or not cliente_id:
                flash("Nome, espécie e cliente são obrigatórios.")
                return render_template("editar_animal.html",
                                       animal=request.form,
                                       clientes=clientes)

            # Atualiza os dados do animal na base de dados
            # Se a data de nascimento estiver vazia, guarda NULL na BD
            cursor.execute("""
                UPDATE animais
                SET cliente_id=%s, nome=%s, especie=%s, raca=%s, data_nascimento=%s
                WHERE id=%s
            """, (cliente_id, nome, especie, raca, data_nascimento or None, id))

            conexao.commit()   # Confirma a transação
            flash("Animal atualizado com sucesso!")
            return redirect(url_for("animais_listar"))

        # Pedido GET → mostra formulário com os dados atuais do animal
        return render_template("editar_animal.html",
                               animal=animal,
                               clientes=clientes)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA EDITAR UTILIZADOR — /editar_user/<id> (apenas admin)
# =============================================================================

@app.route("/editar_user/<int:id>", methods=["GET", "POST"])
def editar_user(id):
    """
    Permite editar os dados de um utilizador existente.
    O parâmetro 'id' é o identificador único do utilizador na base de dados.
    Apenas admin e staff têm acesso. Só o admin pode alterar passwords.
    - GET  → carrega e mostra os dados atuais do utilizador.
    - POST → valida e atualiza os dados do utilizador.
    """
    # Controlo de acesso: apenas admin e staff têm permissão
    if not (admin() or staff()):
        flash("Não tem permissão para editar utilizadores.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca o utilizador pelo ID passado na URL
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()

    # Se o utilizador não existir, mostra mensagem e redireciona
    if not user:
        flash("Utilizador não encontrado.")
        return redirect(url_for("users_listar"))

    # Carrega lista de clientes para o dropdown (associar utilizador a cliente)
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    try:
        # Pedido POST com ação 'salvar' → processar atualização do utilizador
        if request.method == "POST" and request.form.get("acao") == "salvar":

            # Recolhe os dados do formulário
            username   = request.form.get("username", "").strip()
            role_form  = request.form.get("role", "").strip()

            # Trata o cliente_id — pode ser vazio para admin/staff
            cliente_id_raw = request.form.get("cliente_id", "").strip()
            cliente_id     = int(cliente_id_raw) if cliente_id_raw.isdigit() else None

            # Apenas o admin pode alterar passwords de outros utilizadores
            nova_password = None
            if admin():
                nova_password_raw = request.form.get("password", "").strip()
                if nova_password_raw:
                    # ATENÇÃO: Em produção, deve-se usar hashing (ex: generate_password_hash)
                    nova_password = generate_password_hash(nova_password_raw)   # type: ignore

            # Validação: username é obrigatório
            if not username:
                flash("Username é obrigatório.")
                return render_template("editar_user.html",
                                       user=request.form,
                                       clientes=clientes)

            # Atualiza o utilizador — com ou sem nova password
            if nova_password:
                # Atualiza incluindo a nova password
                cursor.execute("""
                    UPDATE users
                    SET username=%s, role=%s, cliente_id=%s, password=%s
                    WHERE id=%s
                """, (username, role_form, cliente_id, nova_password, id))
            else:
                # Atualiza sem alterar a password existente
                cursor.execute("""
                    UPDATE users
                    SET username=%s, role=%s, cliente_id=%s
                    WHERE id=%s
                """, (username, role_form, cliente_id, id))

            conexao.commit()   # Confirma a transação
            flash("Utilizador atualizado com sucesso!")
            return redirect(url_for("users_listar"))

        # Pedido GET → mostra formulário com os dados atuais do utilizador
        return render_template("editar_user.html",
                               user=user,
                               clientes=clientes)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA APAGAR CLIENTE — /apagar_cliente/<id> (apenas admin)
# =============================================================================

@app.route("/apagar_cliente/<int:id>", methods=["POST"])
def apagar_cliente(id):
    """
    Apaga um cliente da base de dados pelo seu ID.
    Apenas aceita pedidos POST (por segurança — evita apagamentos acidentais por GET).
    Apenas administradores têm permissão.
    """
    # Controlo de acesso: apenas administradores podem apagar clientes
    if not admin():
        flash("Apenas administradores podem apagar clientes.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor()

    # Executa o DELETE na tabela 'clientes' pelo ID
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conexao.commit()   # Confirma a transação

    # Fecha ligação e redireciona
    cursor.close()
    conexao.close()

    flash("Cliente apagado com sucesso!")
    return redirect(url_for("clientes_listar"))


# =============================================================================
# ROTA APAGAR ANIMAL — /apagar_animal/<id> (apenas admin)
# =============================================================================

@app.route("/apagar_animal/<int:id>", methods=["POST"])
def apagar_animal(id):
    """
    Apaga um animal da base de dados pelo seu ID.
    Apenas aceita pedidos POST (por segurança).
    Apenas administradores têm permissão.
    """
    # Controlo de acesso: apenas administradores podem apagar animais
    if not admin():
        flash("Apenas administradores podem apagar animais.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor()

    # Executa o DELETE na tabela 'animais' pelo ID
    cursor.execute("DELETE FROM animais WHERE id = %s", (id,))
    conexao.commit()   # Confirma a transação

    # Fecha ligação e redireciona
    cursor.close()
    conexao.close()

    flash("Animal apagado com sucesso!")
    return redirect(url_for("animais_listar"))


# =============================================================================
# ROTA APAGAR CONSULTA — /apagar_consulta/<id> (apenas admin)
# =============================================================================

@app.route("/apagar_consulta/<int:id>", methods=["POST"])
def apagar_consulta(id):
    """
    Apaga uma consulta da base de dados pelo seu ID.
    Apenas aceita pedidos POST (por segurança).
    Apenas administradores têm permissão.
    """
    # Proteção: verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Controlo de acesso: apenas administradores podem apagar consultas
    if not admin():
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Executa o DELETE na tabela 'consultas' pelo ID
        cursor.execute("DELETE FROM consultas WHERE id = %s", (id,))
        conexao.commit()   # Confirma a transação
        flash("Consulta apagada com sucesso!")

    except Exception as erro:
        # Em caso de erro (ex: chave estrangeira), regista no log e desfaz a transação
        app.logger.exception("ERRO AO APAGAR CONSULTA")
        conexao.rollback()   # Reverte alterações em caso de erro
        flash("Erro ao apagar consulta. Verifique dependências ou tente novamente.")

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()

    # Redireciona para a lista de consultas após tentativa de apagar
    return redirect(url_for("consultas_listar"))


# =============================================================================
# ROTA APAGAR UTILIZADOR — /apagar_user/<id> (apenas admin)
# =============================================================================

@app.route("/apagar_user/<int:id>", methods=["POST"])
def apagar_user(id):
    """
    Apaga um utilizador da base de dados pelo seu ID.
    Apenas aceita pedidos POST (por segurança).
    Apenas administradores têm permissão.
    """
    # Controlo de acesso: apenas administradores podem apagar utilizadores
    if not admin():
        flash("Apenas administradores podem apagar utilizadores.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor()

    # Executa o DELETE na tabela 'users' pelo ID
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conexao.commit()   # Confirma a transação

    # Fecha ligação e redireciona
    cursor.close()
    conexao.close()

    flash("Utilizador apagado com sucesso!")
    return redirect(url_for("users_listar"))


# =============================================================================
# ROTA LISTAR CLIENTES — /clientes (admin e staff)
# =============================================================================

@app.route("/clientes")
def clientes_listar():
    """
    Mostra a lista completa de todos os clientes registados.
    Acessível apenas por administradores e staff.
    """
    # Controlo de acesso: apenas admin e staff podem ver a lista de clientes
    if not (admin() or staff()):
        flash("Não tem permissão para ver clientes.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os clientes da base de dados, ordenados por nome (A-Z)
    cursor.execute("SELECT * FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    # Fecha ligação
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de clientes
    return render_template("clientes_listar.html", clientes=clientes)


# =============================================================================
# ROTA LISTAR UTILIZADORES — /users (admin e staff)
# =============================================================================

@app.route("/users")
def users_listar():
    """
    Mostra a lista completa de todos os utilizadores do sistema.
    Inclui o nome do cliente associado (se existir), via LEFT JOIN.
    Acessível por administradores e staff.
    """
    # Controlo de acesso: apenas admin e staff podem ver a lista de utilizadores
    if not (admin() or staff()):
        flash("Não tem permissão para ver utilizadores.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os utilizadores e, se existir, o nome do cliente associado
    # LEFT JOIN → inclui utilizadores mesmo sem cliente associado (admin/staff)
    cursor.execute("""
        SELECT users.*, clientes.nome AS cliente_nome
        FROM users
        LEFT JOIN clientes ON clientes.id = users.cliente_id
        ORDER BY users.username
    """)
    users = cursor.fetchall()

    # Fecha ligação
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de utilizadores
    return render_template("users_listar.html", users=users)


# =============================================================================
# ROTA LISTAR ANIMAIS — /animais (admin e staff)
# =============================================================================

@app.route("/animais")
def animais_listar():
    """
    Mostra a lista completa de todos os animais registados.
    Inclui o nome do cliente dono de cada animal.
    Acessível apenas por administradores e staff.
    """
    # Controlo de acesso: apenas admin e staff podem ver todos os animais
    if not (admin() or staff()):
        flash("Não tem permissão para ver animais.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todos os animais com o nome do cliente dono (via INNER JOIN)
    # INNER JOIN → apenas animais que tenham cliente associado são mostrados
    cursor.execute("""
        SELECT animais.*, clientes.nome AS cliente_nome
        FROM animais
        INNER JOIN clientes ON clientes.id = animais.cliente_id
        ORDER BY animais.nome
    """)
    animais = cursor.fetchall()

    # Fecha ligação
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de animais
    return render_template("animais_listar.html", animais=animais)


# =============================================================================
# ROTA LISTAR CONSULTAS — /consultas (admin e staff)
# =============================================================================

@app.route("/consultas")
def consultas_listar():
    """
    Mostra a lista completa de todas as consultas agendadas/realizadas.
    Inclui o nome do animal e do cliente associado.
    Acessível apenas por administradores e staff.
    """
    # Controlo de acesso: apenas admin e staff podem ver todas as consultas
    if not (admin() or staff()):
        flash("Não tem permissão para ver consultas.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca todas as consultas com nome do animal e nome do cliente
    # Ordenadas da mais recente para a mais antiga (DESC)
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

    # Renderiza o template com a lista de consultas
    return render_template("consultas_listar.html", consultas=consultas)


# =============================================================================
# ROTA MINHA CONTA — /minha_conta (apenas cliente)
# =============================================================================

@app.route("/minha_conta")
def minha_conta():
    """
    Página pessoal do cliente autenticado.
    Mostra os dados do próprio cliente (nome, contactos, morada, etc.).
    Apenas utilizadores com papel 'cliente' têm acesso.
    """
    # Proteção: verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Controlo de acesso: apenas clientes podem ver esta página
    if session.get("role") != "cliente":
        flash("Acesso negado. Apenas clientes podem ver esta página.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Busca os dados do cliente correspondente ao ID guardado na sessão
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (session.get("cliente_id"),))
        cliente = cursor.fetchone()

        # Renderiza a página com os dados do cliente autenticado
        return render_template("minha_conta.html", cliente=cliente)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA MEUS ANIMAIS — /meus_animais (apenas cliente)
# =============================================================================

@app.route("/meus_animais")
def meus_animais():
    """
    Página que mostra ao cliente os seus próprios animais registados.
    Filtra os animais usando o cliente_id guardado na sessão.
    Apenas utilizadores com papel 'cliente' têm acesso.
    """
    # Proteção: verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Controlo de acesso: apenas clientes podem ver os seus próprios animais
    if session.get("role") != "cliente":
        flash("Apenas clientes podem ver os seus próprios animais.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Busca apenas os animais pertencentes ao cliente autenticado
        # Filtra pelo cliente_id guardado na sessão no momento do login
        cursor.execute("""
            SELECT id, nome, especie, raca, data_nascimento
            FROM animais
            WHERE cliente_id = %s
            ORDER BY nome
        """, (session.get("cliente_id"),))

        animais = cursor.fetchall()

        # Renderiza a página com a lista de animais do cliente
        return render_template("meus_animais.html", animais=animais)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA MINHAS CONSULTAS — /minhas_consultas (apenas cliente)
# =============================================================================

@app.route("/minhas_consultas")
def minhas_consultas():
    """
    Página que mostra ao cliente o histórico das suas consultas veterinárias.
    Filtra as consultas pelos animais pertencentes ao cliente autenticado.
    Apenas utilizadores com papel 'cliente' têm acesso.
    """
    # Proteção: verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Controlo de acesso: apenas clientes podem ver as suas consultas
    if session.get("role") != "cliente":
        flash("Apenas clientes podem ver as suas consultas.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Busca todas as consultas dos animais pertencentes ao cliente autenticado
        # Usa subquery via WHERE para filtrar pelo cliente_id da sessão
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

        # Renderiza a página com a lista de consultas do cliente
        return render_template("minhas_consultas.html", consultas=consultas)

    finally:
        # Fecha sempre o cursor e a ligação
        cursor.close()
        conexao.close()


# =============================================================================
# ROTA TROCAR PASSWORD — /trocar_password/<id>
# =============================================================================

@app.route("/trocar_password/<int:id>", methods=["GET", "POST"])
def trocar_password(id):
    """
    Permite a um utilizador alterar a sua própria password.
    Um administrador também pode alterar a password de qualquer utilizador.
    O parâmetro 'id' é o identificador único do utilizador.
    - GET  → mostra o formulário de troca de password.
    - POST → valida e atualiza a password na base de dados.
    """
    # Proteção: verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Controlo de acesso: apenas o próprio utilizador ou um admin podem alterar a password
    if session["user_id"] != id and not admin():
        flash("Não tem permissão para alterar esta password.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Busca os dados do utilizador pelo ID
    cursor.execute("SELECT id, username FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()

    # Se o utilizador não existir, mostra mensagem e redireciona
    if not user:
        flash("Utilizador não encontrado.")
        return redirect(url_for("dashboard"))

    # Pedido POST → processar a troca de password
    if request.method == "POST":
        nova      = request.form.get("nova_password", "").strip()      # Nova password
        confirmar = request.form.get("confirmar_password", "").strip()  # Confirmação da nova password

        # Validação: ambos os campos são obrigatórios
        if not nova or not confirmar:
            flash("Preencha todos os campos.")
            return render_template("users/trocar_password.html", user=user)

        # Validação: as duas passwords devem ser iguais
        if nova != confirmar:
            flash("As passwords não coincidem.")
            return render_template("users/trocar_password.html", user=user)

        # Atualiza a password na base de dados
        cursor.execute("""
            UPDATE users SET password=%s WHERE id=%s
        """, (nova, id))

        conexao.commit()   # Confirma a transação

        # Fecha ligação e redireciona
        cursor.close()
        conexao.close()

        flash("Password alterada com sucesso!")
        return redirect(url_for("dashboard"))

    # Pedido GET → fecha ligação e mostra o formulário
    cursor.close()
    conexao.close()

    return render_template("users/trocar_password.html", user=user)


# =============================================================================
# ROTA LOGOUT — /logout
# =============================================================================

@app.route("/logout")
def logout():
    """
    Termina a sessão do utilizador autenticado.
    Limpa todos os dados de sessão e redireciona para a página de login.
    """
    # Limpa todos os dados da sessão (equivale a "fazer logout")
    session.clear()

    # Redireciona para a página de login após terminar sessão
    return redirect(url_for("login"))


# =============================================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# =============================================================================

# Este bloco apenas é executado quando o ficheiro é corrido diretamente
# (ex: python app.py). Não é executado quando importado como módulo.
if __name__ == "__main__":
    # Inicia o servidor Flask em modo debug.
    # debug=True → reinicia automaticamente ao detetar alterações no código
    #             → mostra erros detalhados no browser (NÃO usar em produção!)
    app.run(debug=True)