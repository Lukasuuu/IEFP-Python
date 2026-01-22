from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests
from datetime import datetime

# ============================================================
# FUNÇÃO DE CONEXÃO AO BANCO DE DADOS
# ============================================================
# Esta função cria e retorna uma conexão com o MySQL.
# Sempre que precisarmos acessar o banco, chamamos ligar_bd().
def ligar_bd():
    return mysql.connector.connect(
        host="62.28.39.135",
        user="efa0125",
        password="123.Abc",
        database="efa0125_25_formacao_crud"
    )

# Criação da aplicação Flask
app = Flask(__name__)

# Chave secreta usada para sessões (login)
app.secret_key = "123"


# ============================================================
# ROTA PRINCIPAL (LISTA DE UTILIZADORES)
# ============================================================
@app.route("/")
def index():

    # Verifica se o utilizador está logado
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Conecta ao banco
    cnx = ligar_bd()
    cur = cnx.cursor(dictionary=True)  # Retorna resultados como dicionário

    # Busca todos os utilizadores ordenados do mais recente para o mais antigo
    cur.execute("SELECT id, nome, email, created_at FROM utilizadores ORDER BY id DESC")
    utilizadores = cur.fetchall()

    cur.close()
    cnx.close()

    # Verifica se o utilizador logado é admin
    is_admin = session.get("user_role") == "admin"

    # Envia dados para o template index.html
    return render_template("index.html", utilizadores=utilizadores, is_admin=is_admin)


# ============================================================
# ROTA PARA GERIR PERMISSÕES (ROLES)
# ============================================================
@app.route("/roles", methods=["GET","POST"])
def roles():

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas administradores podem acessar esta página
    if session.get("user_role") != "admin":
        flash("Acesso Negado. Apenas administradores podem gerir permissões.")
        return redirect(url_for("index"))

    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    # Se o formulário foi enviado (POST), atualiza o role do utilizador
    if request.method == "POST":
        user_id = request.form["user_id"]
        novo_role = request.form["role"]

        cursor.execute("UPDATE login SET role=%s WHERE id=%s", (novo_role, user_id))
        cnx.commit()
        flash("Role atualizado com sucesso!")

    # Busca todos os utilizadores para exibir na página
    cursor.execute("SELECT id, username, role, created_at FROM login ORDER BY id")
    utilizadores = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template("roles.html", utilizadores=utilizadores)


# ============================================================
# ROTA PARA CRIAR NOVO UTILIZADOR
# ============================================================
@app.route("/novo", methods=["GET","POST"])
def novo():

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Se o formulário foi enviado
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        cnx = ligar_bd()
        cursor = cnx.cursor()

        # Insere novo utilizador
        cursor.execute(
            "INSERT INTO utilizadores(nome,email) VALUES(%s,%s)", (nome, email)
        )

        cnx.commit()
        cursor.close()
        cnx.close()

        return redirect(url_for("index"))

    # Se GET, mostra o formulário vazio
    return render_template("form.html", titulo="Novo Utilizador", utilizador=None)


# ============================================================
# ROTA PARA EDITAR UTILIZADOR
# ============================================================
@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admins podem editar
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("index"))

    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    # Se formulário enviado, atualiza dados
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        cursor.execute(
            "UPDATE utilizadores SET nome=%s,email=%s WHERE id=%s", (nome, email, id)
        )

        cnx.commit()
        cursor.close()
        cnx.close()

        return redirect(url_for("index"))

    # Se GET, busca dados do utilizador para preencher o formulário
    cursor.execute("SELECT * FROM utilizadores WHERE id=%s", (id,))
    utilizador = cursor.fetchone()

    cursor.close()
    cnx.close()

    return render_template("form.html", titulo="Editar Utilizador", utilizador=utilizador)


# ============================================================
# ROTA PARA APAGAR UTILIZADOR
# ============================================================
@app.route("/apagar/<int:id>", methods=["POST"])
def apagar(id):

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admins podem apagar
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("index"))

    cnx = ligar_bd()
    cursor = cnx.cursor()

    cursor.execute("DELETE FROM utilizadores WHERE id=%s", (id,))
    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for("index"))


# ============================================================
# ROTA DE LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    # Se formulário enviado
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cnx = ligar_bd()
        cursor = cnx.cursor(dictionary=True)

        # Busca utilizador pelo username
        cursor.execute("SELECT id, username, password, role FROM login WHERE username = %s", (username,))
        utilizador = cursor.fetchone()

        cursor.close()
        cnx.close()

        print("DEBUG: utilizador from DB ->", utilizador)

        # Verifica senha
        if utilizador and utilizador.get("password") == password:

            # Guarda dados na sessão
            session["user_id"] = utilizador["id"]
            session["username"] = utilizador["username"]
            session["user_role"] = utilizador["role"]

            return redirect(url_for("index"))

        else:
            flash("Login incorreto.")
            return redirect(url_for("login"))

    # Se GET, mostra formulário
    return render_template("login.html")


# ============================================================
# ROTA DE LOGOUT
# ============================================================
@app.route("/logout")
def logout():
    session.clear()  # Remove tudo da sessão
    return redirect(url_for("login"))


# ============================================================
# ROTA DE REGISTO DE NOVO UTILIZADOR
# ============================================================
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cnx = ligar_bd()
        cursor = cnx.cursor()

        # Insere novo utilizador com role padrão "utilizador"
        cursor.execute(
            "INSERT INTO login(username,password,role) VALUES(%s,%s,%s)",
            (username, password, "utilizador")
        )

        cnx.commit()
        cursor.close()
        cnx.close()

        flash("Conta criada! Faça login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# ============================================================
# ROTA PARA DELETAR UTILIZADOR (TABELA LOGIN)
# ============================================================
@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Apenas admins podem apagar
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("index"))

    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    # Busca role do utilizador
    cursor.execute("SELECT role FROM login WHERE id = %s", (id,))
    row = cursor.fetchone()

    if not row:
        flash("Utilizador não encontrado.")
        cursor.close()
        cnx.close()
        return redirect(url_for("roles"))

    role = row["role"]

    # Impede apagar administradores
    if role == "admin":
        flash("Não é permitido deletar administradores.")
        cursor.close()
        cnx.close()
        return redirect(url_for("roles"))

    # Deleta utilizador
    cursor.execute("DELETE FROM login WHERE id = %s", (id,))
    cnx.commit()

    if cursor.rowcount > 0:
        flash("Usuário deletado com sucesso.")
    else:
        flash("Falha ao deletar o usuário.")

    cursor.close()
    cnx.close()

    return redirect(url_for("roles"))


# ============================================================
# ROTA PARA CONSULTAR METEOROLOGIA
# ============================================================
@app.route("/meteorologia", methods=["GET","POST"])
def meteorologia():

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    dados = None

    if request.method == "POST":

        key = "3689129ee7af0fa500cad990971aecd6"  # API KEY
        cidade = request.form["cidade"]

        # URL da API
        link = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={key}&lang=pt_br&units=metric"

        # Faz requisição e obtém JSON
        dados = requests.get(link).json()

        print(dados)

    return render_template("meteorologia.html", dados=dados)


# ============================================================
# ROTA PARA CONSULTAR COTAÇÕES DE MOEDAS
# ============================================================
@app.route("/moedas", methods=["GET","POST"])
def moedas():

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Consulta API de moedas
    cotacoes = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL").json()

    # Converte valores para float
    for k, v in cotacoes.items():
        try:
            v["bid"] = float(v["bid"])
        except:
            v["bid"] = None

    return render_template("cotacoes.html", cotacoes=cotacoes)


# ============================================================
# INJETAR DATA ATUAL NOS TEMPLATES
# ============================================================
@app.context_processor
def inject_now():
    return {'now': datetime.now}


# ============================================================
# EXECUTAR A APLICAÇÃO
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
