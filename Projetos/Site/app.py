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
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Preencha todos os campos.")
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, username, password, role, cliente_id
        FROM users
        WHERE username = %s AND password = %s
    """, (username, password))

    user = cursor.fetchone()

    if not user:
        cursor.close()
        conexao.close()
        flash("Credenciais inválidas.")
        return redirect(url_for("login"))

    # LOGIN OK
    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["username"] = user["username"]   # <--- ESSENCIAL

    # Se for cliente, cliente_id DEVE existir
    if user["role"] == "cliente":
        if not user["cliente_id"]:
            flash("Erro: este utilizador cliente não está associado a um cliente.")
            cursor.close()
            conexao.close()
            return redirect(url_for("login"))

        session["cliente_id"] = user["cliente_id"]

    cursor.close()
    conexao.close()

    flash("Login efetuado com sucesso!")
    return redirect(url_for("dashboard"))

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
# ============================================================
# ROTA PARA CRIAR USER (APENAS ADMIN)
# ============================================================
@app.route("/criar_user", methods=["GET", "POST"])                # define a rota e os métodos permitidos
def criar_user():                                                 # função que trata a criação de utilizadores
    if "user_id" not in session:                                  # verifica se existe sessão (utilizador autenticado)
        return redirect(url_for("login"))                         # se não, redireciona para a página de login

    if session.get("role") != "admin":                            # verifica se o utilizador tem role 'admin'
        flash("Acesso restrito.")                                 # mostra mensagem de acesso restrito
        return redirect(url_for("dashboard"))                     # redireciona para o dashboard

    if request.method == "GET":                                   # se o pedido for GET
        return render_template("criar_user.html")                 # renderiza o formulário de criação de user

    # abaixo é o fluxo para POST (formulário submetido)
    username = request.form.get("username")                       # lê o campo username do formulário
    password = request.form.get("password")                       # lê o campo password do formulário
    role = request.form.get("role")                               # lê o campo role do formulário
    nome = request.form.get("nome")                               # lê o campo nome (opcional, para cliente)
    email = request.form.get("email")                             # lê o campo email (opcional, para cliente)

    if not username or not password or not role:                  # validação simples dos campos obrigatórios
        flash("Preencha todos os campos obrigatórios.")           # avisa o utilizador que faltam campos
        return redirect(url_for("criar_user"))                    # volta ao formulário

    conexao = ligar_db()                                          # abre ligação à base de dados
    cursor = conexao.cursor(dictionary=True)                      # cria cursor que devolve dicionários

    try:
        # se o role for 'cliente' e o utilizador forneceu nome/email, cria primeiro o cliente
        if role == "cliente" and (nome or email):                 # verifica se devemos criar um registo cliente
            cursor.execute(                                       # executa a inserção na tabela clientes
                "INSERT INTO clientes (nome, email) VALUES (%s, %s)",
                (nome, email)
            )
            cliente_id = cursor.lastrowid                         # obtém o id do cliente criado
        else:
            cliente_id = None                                     # se não, cliente_id fica None

        # insere o user na tabela users, referenciando cliente_id (pode ser NULL)
        cursor.execute(
            "INSERT INTO users (username, password, role, cliente_id) VALUES (%s, %s, %s, %s)",
            (username, password, role, cliente_id)
        )

        conexao.commit()                                          # confirma a transação no banco
        flash("Utilizador criado com sucesso!")                   # mensagem de sucesso para o utilizador

    except Exception as erro:                                     # captura qualquer erro que ocorra
        app.logger.exception("ERRO AO CRIAR USER")                # regista o erro completo no log do Flask
        print("\nERRO AO CRIAR USER:", type(erro).__name__, erro, "\n")  # imprime o erro no terminal para debug
        conexao.rollback()                                        # desfaz a transação para manter integridade
        flash("Erro ao criar utilizador. Verifique os dados e tente novamente.")  # mensagem genérica ao utilizador

    finally:
        cursor.close()                                            # fecha o cursor
        conexao.close()                                           # fecha a ligação

    return redirect(url_for("users_listar"))                      # redireciona para a lista de utilizadores



# ============================================================
# ROTA PARA CRIAR CLIENTE (ADMIN E STAFF)
# ============================================================
@app.route("/criar_cliente", methods=["GET", "POST"])              # define a rota e os métodos permitidos
def criar_cliente():                                              # função que trata a criação de clientes
    if "user_id" not in session:                                  # verifica se existe sessão (utilizador autenticado)
        return redirect(url_for("login"))                         # se não, redireciona para login

    if session.get("role") not in ["admin", "staff"]:             # verifica se o utilizador é admin ou staff
        flash("Acesso restrito.")                                 # mostra mensagem de acesso restrito
        return redirect(url_for("dashboard"))                     # redireciona para o dashboard

    if request.method == "GET":                                   # se for GET
        return render_template("criar_cliente.html")              # renderiza o formulário de criação de cliente

    # fluxo POST: ler campos do formulário
    nome = request.form.get("nome")                               # lê o nome do cliente (obrigatório)
    email = request.form.get("email")                             # lê o email do cliente (obrigatório)
    telefone = request.form.get("telefone")                       # lê o telefone (opcional)
    morada = request.form.get("morada")                           # lê a morada (opcional)

    criar_login = request.form.get("criar_login") == "on"         # checkbox: True apenas se marcado

    if not nome or not email:                                     # validação simples dos campos obrigatórios
        flash("Nome e email são obrigatórios.")                   # avisa o utilizador
        return redirect(url_for("criar_cliente"))                 # volta ao formulário

    conexao = ligar_db()                                          # abre ligação à base de dados
    cursor = conexao.cursor(dictionary=True)                      # cria cursor em modo dicionário

    try:
        # 1) Inserir o cliente primeiro (respeita o esquema atual)
        cursor.execute(
            "INSERT INTO clientes (nome, telefone, email, morada) VALUES (%s, %s, %s, %s)",
            (nome, telefone, email, morada)
        )
        cliente_id = cursor.lastrowid                             # obtém o id do cliente criado

        # 2) Se for para criar login, inserir user referenciando cliente_id
        if criar_login:                                           # verifica se o admin marcou criar login
            username = request.form.get("username")               # lê username do formulário
            password = request.form.get("password")               # lê password do formulário

            if not username or not password:                      # validação simples para username/password
                conexao.rollback()                                # desfaz a inserção do cliente se faltar dados
                flash("Username e password são obrigatórios para criar login.")  # avisa o utilizador
                return redirect(url_for("criar_cliente"))         # volta ao formulário

            cursor.execute(                                       # insere o user com cliente_id (respeita FK)
                "INSERT INTO users (username, password, role, cliente_id) VALUES (%s, %s, 'cliente', %s)",
                (username, password, cliente_id)
            )

        conexao.commit()                                          # confirma todas as alterações (cliente e user)
        flash("Cliente criado com sucesso!")                      # mensagem de sucesso

    except Exception as erro:                                     # captura qualquer erro que ocorra
        app.logger.exception("ERRO AO CRIAR CLIENTE")             # regista o erro completo no log do Flask
        print("\nERRO AO CRIAR CLIENTE:", type(erro).__name__, erro, "\n")  # imprime o erro no terminal para debug
        conexao.rollback()                                        # desfaz a transação para manter integridade
        flash("Erro ao criar cliente. Verifique os dados (email/username) e tente novamente.")  # mensagem genérica

    finally:
        cursor.close()                                            # fecha o cursor
        conexao.close()                                           # fecha a ligação

    return redirect(url_for("clientes_listar"))                   # redireciona para a lista de clientes


# ============================================================
# ROTA PARA CRIAR ANIMAL (ADMIN, STAFF, CLIENTE)
# ============================================================
@app.route("/criar_animal", methods=["GET", "POST"])              # define a rota e os métodos permitidos
def criar_animal():                                               # função que trata a criação de animais
    if "user_id" not in session:                                  # verifica se o utilizador está autenticado
        return redirect(url_for("login"))                         # redireciona para login se não estiver

    role = session.get("role")                                    # obtém o papel do utilizador da sessão

    conexao = ligar_db()                                          # abre ligação à base de dados
    cursor = conexao.cursor(dictionary=True)                      # cria cursor em modo dicionário

    if role in ["admin", "staff"]:                                # se for admin ou staff
        cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")  # busca lista de clientes
        clientes = cursor.fetchall()                              # guarda a lista de clientes
    else:
        clientes = None                                           # para cliente normal não mostramos lista

    if request.method == "GET":                                   # se for GET
        cursor.close()                                            # fecha o cursor antes de renderizar
        conexao.close()                                           # fecha a ligação
        return render_template("criar_animal.html", clientes=clientes)  # renderiza o formulário com clientes

    # fluxo POST: ler campos do formulário
    nome = request.form.get("nome")                               # nome do animal (obrigatório)
    especie = request.form.get("especie")                         # espécie do animal (obrigatório)
    raca = request.form.get("raca")                               # raça (opcional)
    data_nascimento = request.form.get("data_nascimento")         # data de nascimento (opcional)

    if not nome or not especie:                                   # validação simples
        flash("Nome e espécie são obrigatórios.")                 # avisa o utilizador
        return redirect(url_for("criar_animal"))                  # volta ao formulário

    if role in ["admin", "staff"]:                                # se admin/staff escolhe cliente no formulário
        cliente_id = request.form.get("cliente_id")               # lê cliente_id enviado pelo formulário
    else:
        cliente_id = session.get("cliente_id")                    # cliente normal usa cliente_id da sessão

    try:
        cursor.execute(                                           # insere o animal na tabela animais
            "INSERT INTO animais (nome, especie, raca, data_nascimento, cliente_id) VALUES (%s, %s, %s, %s, %s)",
            (nome, especie, raca, data_nascimento, cliente_id)
        )
        conexao.commit()                                          # confirma a transação
        flash("Animal criado com sucesso!")                       # mensagem de sucesso

    except Exception as erro:                                     # captura erros
        app.logger.exception("ERRO AO CRIAR ANIMAL")              # regista o erro completo no log
        print("\nERRO AO CRIAR ANIMAL:", type(erro).__name__, erro, "\n")  # imprime o erro no terminal
        conexao.rollback()                                        # desfaz a transação
        flash("Erro ao criar animal. Verifique os dados e tente novamente.")  # mensagem genérica

    finally:
        cursor.close()                                            # fecha o cursor
        conexao.close()                                           # fecha a ligação

    return redirect(url_for("animais_listar"))                    # redireciona para o lista de animais



# ============================================================
# ROTA PARA CRIAR CONSULTA (ADMIN, STAFF, CLIENTE)
# ============================================================
@app.route("/criar_consulta", methods=["GET", "POST"])
def criar_consulta():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # ADMIN / STAFF → podem escolher cliente
    if role in ["admin", "staff"]:
        cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
    else:
        clientes = None

    animais = []

    # GET → mostrar formulário
    if request.method == "GET":
        if role == "cliente":
            cursor.execute("""
                SELECT id, nome
                FROM animais
                WHERE cliente_id = %s
                ORDER BY nome
            """, (session.get("cliente_id"),))
            animais = cursor.fetchall()

        cursor.close()
        conexao.close()
        return render_template("criar_consulta.html",
                               clientes=clientes,
                               animais=animais)

    # POST → criar consulta
    cliente_id = None

    if role == "cliente":
        cliente_id = session.get("cliente_id")
    else:
        cliente_id = request.form.get("cliente_id")

    # Carregar animais do cliente selecionado
    cursor.execute("""
        SELECT id, nome
        FROM animais
        WHERE cliente_id = %s
        ORDER BY nome
    """, (cliente_id,))
    animais = cursor.fetchall()

    animal_id = request.form.get("animal_id")
    data_hora = request.form.get("data_hora")
    motivo = request.form.get("motivo")
    notas = request.form.get("notas")

    if not cliente_id or not animal_id or not data_hora:
        flash("Selecione cliente, animal e data.")
        cursor.close()
        conexao.close()
        return render_template("criar_consulta.html",
                               clientes=clientes,
                               animais=animais)

    cursor.execute("""
        INSERT INTO consultas (animal_id, data_hora, motivo, notas)
        VALUES (%s, %s, %s, %s)
    """, (animal_id, data_hora, motivo, notas))

    conexao.commit()
    cursor.close()
    conexao.close()

    flash("Consulta criada com sucesso!")
    return redirect(url_for("consultas_listar"))

# ============================================================
# ROTA PARA EDITAR CLIENTE (ADMIN E STAFF)
# ============================================================
@app.route("/cliente_editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    # Se o utilizador não estiver logado, volta para o login
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
    if "user_id" not in session:
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar consulta + cliente do animal
    cursor.execute("""
        SELECT consultas.*, animais.cliente_id
        FROM consultas
        INNER JOIN animais ON animais.id = consultas.animal_id
        WHERE consultas.id = %s
    """, (id,))
    consulta = cursor.fetchone()

    if not consulta:
        flash("Consulta não encontrada.")
        return redirect(url_for("consultas_listar"))

    # Buscar clientes (admin/staff)
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    # Buscar animais do cliente da consulta
    cursor.execute("""
        SELECT id, nome
        FROM animais
        WHERE cliente_id = %s
        ORDER BY nome
    """, (consulta["cliente_id"],))
    animais = cursor.fetchall()

    if request.method == "POST":
        animal_id = request.form.get("animal_id")
        data_hora = request.form.get("data_hora")
        motivo = request.form.get("motivo")
        notas = request.form.get("notas")

        cursor.execute("""
            UPDATE consultas
            SET animal_id=%s, data_hora=%s, motivo=%s, notas=%s
            WHERE id=%s
        """, (animal_id, data_hora, motivo, notas, id))

        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Consulta atualizada com sucesso!")
        return redirect(url_for("consultas_listar"))  # CORREÇÃO AQUI ✔

    cursor.close()
    conexao.close()

    return render_template("editar_consulta.html",
                           consulta=consulta,
                           clientes=clientes,
                           animais=animais)

# ============================================================
# ROTA PARA EDITAR ANIMAL (ADMIN, STAFF, CLIENTE)
# ============================================================
@app.route("/animal_editar/<int:id>", methods=["GET", "POST"])
def editar_animal(id):
    # 1) Verifica se o utilizador está autenticado; se não, redireciona para login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # 2) Obtém o papel do utilizador (admin, staff ou cliente)
    role = session.get("role")

    # 3) Abre ligação à base de dados e cria cursor que devolve dicionários
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # 4) Busca o registo do animal pelo id (GET inicial)
    cursor.execute("SELECT * FROM animais WHERE id = %s", (id,))
    animal = cursor.fetchone()

    # 5) Se o animal não existir, fecha recursos e redireciona com mensagem
    if not animal:
        cursor.close()
        conexao.close()
        flash("Animal não encontrado.")
        return redirect(url_for("animais_listar"))

    # 6) Se o animal existe e tem campo data_nascimento como date/datetime,
    #    converte para string 'YYYY-MM-DD' para o input type="date"
    #    Isto evita o erro "date object is not subscriptable" no template.
    if animal.get("data_nascimento") is not None:
        # Pode ser datetime.date ou datetime.datetime; usamos isoformat() ou strftime
        try:
            # Se for date/datetime, isoformat() devolve 'YYYY-MM-DD' ou 'YYYY-MM-DDTHH:MM:SS'
            # Para garantir só a parte da data usamos strftime
            animal["data_nascimento"] = animal["data_nascimento"].strftime("%Y-%m-%d")
        except Exception:
            # Se já for string, mantemos como está
            animal["data_nascimento"] = str(animal["data_nascimento"])

    # 7) Se for cliente, garante que só pode editar os seus próprios animais
    if role == "cliente":
        if animal.get("cliente_id") != session.get("cliente_id"):
            cursor.close()
            conexao.close()
            flash("Não tem permissão para editar este animal.")
            return redirect(url_for("dashboard"))

    # 8) Carrega lista de clientes apenas para admin/staff (para reatribuir dono)
    clientes = None
    if role in ["admin", "staff"]:
        cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()

    # 9) PROCESSA O FORMULÁRIO (POST) → atualizar animal
    if request.method == "POST":
        # Recebe os campos enviados pelo formulário (são strings)
        nome = request.form.get("nome")
        especie = request.form.get("especie")
        raca = request.form.get("raca")
        data_nascimento = request.form.get("data_nascimento")  # já em 'YYYY-MM-DD' string

        # Determina cliente_id: admin/staff podem escolher; cliente usa o seu próprio id
        if role in ["admin", "staff"]:
            cliente_id_str = request.form.get("cliente_id")
            try:
                cliente_id = int(cliente_id_str) if cliente_id_str else None
            except ValueError:
                cliente_id = None
        else:
            cliente_id = session.get("cliente_id")

        # Validação simples: nome e cliente_id são obrigatórios
        if not nome or not cliente_id:
            flash("Nome e cliente são obrigatórios.")
            cursor.close()
            conexao.close()
            # Reapresenta o formulário com os valores enviados (request.form é um dict-like)
            # Convertemos request.form para dict simples para o template usar chaves por nome
            return render_template("editar_animal.html", animal=dict(request.form), clientes=clientes)

        try:
            # Atualiza o registo do animal na base de dados
            cursor.execute("""
                UPDATE animais
                SET nome=%s, especie=%s, raca=%s, data_nascimento=%s, cliente_id=%s
                WHERE id=%s
            """, (nome, especie, raca, data_nascimento, cliente_id, id))

            conexao.commit()

            cursor.close()
            conexao.close()

            flash("Animal atualizado com sucesso!")
            return redirect(url_for("animais_listar"))

        except Exception:
            # Em caso de erro, mostra mensagem e reabre o formulário com os dados enviados
            flash("Erro ao atualizar animal. Verifique os dados e tente novamente.")
            cursor.close()
            conexao.close()
            return render_template("editar_animal.html", animal=dict(request.form), clientes=clientes)

    # 10) GET → renderiza o formulário com os dados do animal carregados
    cursor.close()
    conexao.close()
    return render_template("editar_animal.html", animal=animal, clientes=clientes)

# ============================================================
# ROTA PARA EDITAR USER (APENAS ADMIN)
# ============================================================
@app.route("/user_editar/<int:id>", methods=["GET", "POST"])
def editar_user(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if not is_admin():
        flash("Apenas administradores podem editar utilizadores.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # Buscar o utilizador
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conexao.close()
        flash("Utilizador não encontrado.")
        return redirect(url_for("users_listar"))

    # Carregar lista de clientes
    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()

    # POST → atualizar
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        role_form = request.form.get("role", "").strip()

        # Remover espaços e validar cliente_id
        cliente_id_raw = request.form.get("cliente_id", "").strip()

        if cliente_id_raw.isdigit():
            cliente_id = int(cliente_id_raw)
        else:
            cliente_id = None

        # Validação
        if not username or not email:
            flash("Username e email são obrigatórios.")
            cursor.close()
            conexao.close()
            return render_template("editar_user.html", user=request.form, clientes=clientes)

        try:
            cursor.execute("""
                UPDATE users
                SET username=%s, email=%s, role=%s, cliente_id=%s
                WHERE id=%s
            """, (username, email, role_form, cliente_id, id))

            conexao.commit()

            cursor.close()
            conexao.close()

            flash("Utilizador atualizado com sucesso!")
            return redirect(url_for("users_listar"))

        except Exception as erro:
            print("ERRO AO ATUALIZAR USER:", erro)
            flash("Erro ao atualizar utilizador. Verifique os dados e tente novamente.")
            cursor.close()
            conexao.close()
            return render_template("editar_user.html", user=request.form, clientes=clientes)

    # GET → mostrar formulário
    cursor.close()
    conexao.close()
    return render_template("editar_user.html", user=user, clientes=clientes)

# ============================================================
# ROTA PARA APAGAR CLIENTE (APENAS ADMIN)
# ============================================================
@app.route("/apagar_cliente/<int:id>", methods=["GET", "POST"])
def apagar_cliente(id):
    # Verifica se existe um utilizador autenticado na sessão
    if "user_id" not in session:
        # Se não houver, redireciona para a página de login
        return redirect(url_for("login"))

    # Verifica se o utilizador atual tem permissões de administrador
    if not is_admin():
        # Se não for admin, mostra mensagem e redireciona para o dashboard
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    # Cria um cursor que devolve dicionários (facilita leitura de campos se necessário)
    cursor = conexao.cursor(dictionary=True)
    try:
        # Se o pedido for POST, significa que o formulário de apagar foi submetido
        if request.method == "POST":
            try:
                # Executa o DELETE para apagar o cliente com o id fornecido
                cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
                # Confirma as alterações na base de dados
                conexao.commit()
                # Informa o utilizador que o cliente foi apagado com sucesso
                flash("Cliente apagado com sucesso!")
            except Exception:
                # Em caso de erro, desfaz a transação
                conexao.rollback()
                # Mostra mensagem genérica de erro (podes registar o erro no log se quiseres)
                flash("Erro ao apagar cliente. Verifique dependências ou tente novamente.")
            # Após tentativa de apagar, redireciona sempre para a listagem de clientes
            return redirect(url_for("clientes_listar"))

        # Se o método for GET, não processamos apagamento por GET; redirecionamos para a lista
        return redirect(url_for("clientes_listar"))
    finally:
        # Fecha o cursor para libertar recursos
        cursor.close()
        # Fecha a ligação à base de dados
        conexao.close()


# ============================================================
# ROTA PARA APAGAR ANIMAL (APENAS ADMIN)
# ============================================================
@app.route("/apagar_animal/<int:id>", methods=["GET", "POST"])
def apagar_animal(id):
    # Verifica se o utilizador está autenticado
    if "user_id" not in session:
        # Redireciona para login se não estiver autenticado
        return redirect(url_for("login"))

    # Verifica se o utilizador tem permissões de administrador
    if not is_admin():
        # Mostra mensagem e redireciona para o dashboard se não for admin
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    # Cria cursor em modo dicionário para possíveis leituras (mesmo que não sejam usadas)
    cursor = conexao.cursor(dictionary=True)
    try:
        # Se o pedido for POST, procede ao apagamento
        if request.method == "POST":
            try:
                # Executa o DELETE para apagar o animal com o id fornecido
                cursor.execute("DELETE FROM animais WHERE id = %s", (id,))
                # Confirma a transação
                conexao.commit()
                # Mensagem de sucesso para o utilizador
                flash("Animal apagado com sucesso!")
            except Exception:
                # Em caso de erro, desfaz a transação
                conexao.rollback()
                # Mensagem genérica de erro (podes registar detalhes no log)
                flash("Erro ao apagar animal. Verifique dependências ou tente novamente.")
            # Redireciona para a listagem de animais após tentativa de apagar
            return redirect(url_for("animais_listar"))

        # Se for GET, não executamos DELETE por GET; redirecionamos para a listagem
        return redirect(url_for("animais_listar"))
    finally:
        # Fecha o cursor
        cursor.close()
        # Fecha a ligação à base de dados
        conexao.close()


# ============================================================
# ROTA PARA APAGAR CONSULTA (APENAS ADMIN)
# ============================================================
@app.route("/apagar_consulta/<int:id>", methods=["GET", "POST"])
def apagar_consulta(id):
    # Verifica se existe sessão de utilizador
    if "user_id" not in session:
        # Redireciona para login se não estiver autenticado
        return redirect(url_for("login"))

    # Verifica se o utilizador é administrador
    if not is_admin():
        # Mostra mensagem e redireciona para o dashboard se não for admin
        flash("Apenas administradores podem apagar registos.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    # Cria cursor em modo dicionário
    cursor = conexao.cursor(dictionary=True)
    try:
        # Se o pedido for POST, tenta apagar a consulta
        if request.method == "POST":
            try:
                # Executa o DELETE para apagar a consulta com o id fornecido
                cursor.execute("DELETE FROM consultas WHERE id = %s", (id,))
                # Confirma as alterações
                conexao.commit()
                # Mensagem de sucesso
                flash("Consulta apagada com sucesso!")
            except Exception:
                # Em caso de erro, desfaz a transação
                conexao.rollback()
                # Mensagem genérica de erro
                flash("Erro ao apagar consulta. Verifique dependências ou tente novamente.")
            # Redireciona para a listagem de consultas
            return redirect(url_for("consultas_listar"))

        # Se for GET, redireciona para a listagem (não permitimos apagar por GET)
        return redirect(url_for("consultas_listar"))
    finally:
        # Fecha o cursor
        cursor.close()
        # Fecha a ligação
        conexao.close()


# ============================================================
# ROTA PARA APAGAR UTILIZADOR (APENAS ADMIN)
# ============================================================
@app.route("/apagar_user/<int:id>", methods=["GET", "POST"])
def apagar_user(id):
    # Verifica se o utilizador está autenticado na sessão
    if "user_id" not in session:
        # Redireciona para a página de login se não estiver autenticado
        return redirect(url_for("login"))

    # Verifica se o utilizador tem permissões de administrador
    if not is_admin():
        # Mostra mensagem e redireciona para o dashboard se não for admin
        flash("Apenas administradores podem apagar users.")
        return redirect(url_for("dashboard"))

    # Abre ligação à base de dados
    conexao = ligar_db()
    # Cria cursor em modo dicionário
    cursor = conexao.cursor(dictionary=True)
    try:
        # Se o pedido for POST, processa o apagamento
        if request.method == "POST":
            try:
                # Executa o DELETE para apagar o utilizador com o id fornecido
                cursor.execute("DELETE FROM users WHERE id = %s", (id,))
                # Confirma a transação
                conexao.commit()
                # Mensagem de sucesso
                flash("Utilizador apagado com sucesso!")
            except Exception:
                # Em caso de erro, desfaz a transação
                conexao.rollback()
                # Mensagem genérica de erro
                flash("Erro ao apagar utilizador. Verifique dependências ou tente novamente.")
            # Redireciona para a listagem de utilizadores
            return redirect(url_for("users_listar"))

        # Se for GET, redireciona para a listagem (não executa DELETE por GET)
        return redirect(url_for("users_listar"))
    finally:
        # Fecha o cursor para libertar recursos
        cursor.close()
        # Fecha a ligação à base de dados
        conexao.close()


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

@app.route("/meus_animais")
def meus_animais():
    # 1) Verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # 2) Apenas clientes podem ver esta página
    if session.get("role") != "cliente":
        flash("Apenas clientes podem ver os seus próprios animais.")
        return redirect(url_for("dashboard"))

    # 3) Abrir ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # 4) Buscar apenas os animais do cliente logado
    cursor.execute("""
        SELECT id, nome, especie, raca, data_nascimento
        FROM animais
        WHERE cliente_id = %s
        ORDER BY nome
    """, (session.get("cliente_id"),))

    animais = cursor.fetchall()

    # 5) Fechar ligação
    cursor.close()
    conexao.close()

    # 6) Renderizar o template
    return render_template("meus_animais.html", animais=animais)

@app.route("/minhas_consultas")
def minhas_consultas():
    # 1) Verifica se o utilizador está autenticado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # 2) Apenas clientes podem ver as próprias consultas
    if session.get("role") != "cliente":
        flash("Apenas clientes podem ver as suas consultas.")
        return redirect(url_for("dashboard"))

    # 3) Abrir ligação à base de dados
    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # 4) Buscar consultas apenas dos animais do cliente logado
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

    # 5) Fechar ligação
    cursor.close()
    conexao.close()

    # 6) Renderizar o template
    return render_template("minhas_consultas.html", consultas=consultas)

# ============================
# LISTAR CLIENTES
# ============================
@app.route("/clientes_listar")
def clientes_listar():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            clientes.id,
            clientes.nome,
            clientes.telefone,
            clientes.email,
            clientes.morada,
            clientes.created_at,
            users.username AS utilizador
        FROM clientes
        LEFT JOIN users ON users.cliente_id = clientes.id
        ORDER BY clientes.nome
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("clientes_listar.html", clientes=clientes)

# ============================
# LISTAR USERS (APENAS ADMIN)
# ============================
@app.route("/users_listar")
def users_listar():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Apenas administradores podem ver a lista de users.")
        return redirect(url_for("dashboard"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            users.id,
            users.username,
            users.role,
            users.created_at,
            clientes.nome AS cliente_nome
        FROM users
        LEFT JOIN clientes ON clientes.id = users.cliente_id
        ORDER BY users.username
    """)

    users = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("users_listar.html", utilizadores=users)

# ============================
# LISTAR ANIMAIS (por tipo de utilizador)
# ============================
@app.route("/animais_listar")
def animais_listar():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    # ADMIN e STAFF veem todos os animais
    if session.get("role") in ["admin", "staff"]:
        cursor.execute("""
            SELECT 
                animais.id,
                animais.nome,
                animais.especie,
                animais.raca,
                animais.data_nascimento,
                animais.created_at,
                clientes.nome AS cliente_nome
            FROM animais
            LEFT JOIN clientes ON clientes.id = animais.cliente_id
            ORDER BY animais.nome
        """)

    # CLIENTE vê apenas os seus animais
    elif session.get("role") == "cliente":
        cursor.execute("""
            SELECT 
                animais.id,
                animais.nome,
                animais.especie,
                animais.raca,
                animais.data_nascimento,
                animais.created_at
            FROM animais
            WHERE cliente_id = %s
            ORDER BY animais.nome
        """, (session.get("cliente_id"),))

    else:
        flash("Acesso negado.")
        return redirect(url_for("dashboard"))

    animais = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("animais_listar.html", animais=animais)

# ============================
# LISTAR CONSULTAS (por tipo de utilizador)
# ============================
@app.route("/consultas_listar")
def consultas_listar():
    # Verifica autenticação
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admin/staff podem ver todas; clientes podem ver só as suas consultas
    role = session.get("role")

    conexao = ligar_db()
    cursor = conexao.cursor(dictionary=True)

    if role in ["admin", "staff"]:
        # JOIN para trazer nome do cliente e nome do animal
        cursor.execute("""
            SELECT c.id,
                   cl.nome AS cliente,
                   a.nome AS animal,
                   c.data_hora,
                   c.motivo,
                   c.notas,
                   c.created_at
            FROM consultas c
            JOIN animais a ON c.animal_id = a.id
            JOIN clientes cl ON a.cliente_id = cl.id
            ORDER BY c.data_hora DESC
        """)
    else:
        # Cliente vê só as suas consultas (assumindo session['cliente_id'])
        cursor.execute("""
            SELECT c.id,
                   cl.nome AS cliente,
                   a.nome AS animal,
                   c.data_hora,
                   c.motivo,
                   c.notas,
                   c.created_at
            FROM consultas c
            JOIN animais a ON c.animal_id = a.id
            JOIN clientes cl ON a.cliente_id = cl.id
            WHERE cl.id = %s
            ORDER BY c.data_hora DESC
        """, (session.get("cliente_id"),))

    consultas = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Renderiza o template com a lista de consultas
    return render_template("consultas_listar.html", consultas=consultas)

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