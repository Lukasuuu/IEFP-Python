from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests

# Função para conectar ao banco de dados MySQL
# Retorna o objeto de conexão
# Usada em várias rotas para acessar o banco

def ligar_bd():
    return mysql.connector.connect(
        host="62.28.39.135",
        user="efa0125",
        password="123.Abc",
        database="efa0125_25_formacao_crud"
    )

app = Flask(__name__)
app.secret_key = "123"  # Chave secreta para sessões

# Rota principal da aplicação
@app.route("/")
def index():
    # Verifica se usuário está logado
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redireciona para login se não estiver

    cnx = ligar_bd()  # Conecta ao banco
    cur = cnx.cursor(dictionary=True)  # Cursor que retorna dicionários

    # Executa consulta para buscar usuários ordenados pelo ID decrescente
    cur.execute("SELECT id, nome, email, created_at FROM utilizadores ORDER BY id DESC")
    utilizadores = cur.fetchall()

    cur.close()
    cnx.close()

    # Força o uso de permissões baseadas apenas no admin
    is_admin = session.get("user_role") == "admin"

    return render_template("index.html", utilizadores=utilizadores, is_admin=is_admin)


# Rota para gerenciar roles (permissões)
@app.route("/roles", methods=["GET","POST"])
def roles():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Verifica login
    
    # Apenas admins podem acessar
    if session.get("user_role") != "admin":
        flash("Acesso Negado. Apenas administradores podem gerir permissões.")
        return redirect(url_for("index"))
    
    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    # Se for POST, atualiza role do usuário
    if request.method == "POST":
        user_id = request.form["user_id"]  # ID do usuário a alterar
        novo_role = request.form["role"]  # Novo role

        # Atualiza role no banco
        cursor.execute("UPDATE login SET role=%s WHERE id=%s", (novo_role, user_id))
        cnx.commit()  # Salva alterações
        flash("Role atualizado com sucesso!")

    # Busca todos os usuários para mostrar
    cursor.execute("SELECT id, username, role, created_at FROM login ORDER BY id")
    
    utilizadores = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template("roles.html", utilizadores=utilizadores)


# Rota para criar novo usuário
@app.route("/novo", methods=["GET","POST"])
def novo():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Verifica login
    # Opcional: só admins podem criar usuários
    #if session.get("user_role") != "admin":
        #flash("Acesso negado.")
        #return redirect(url_for("index"))
    
    if request.method == "POST":
        nome = request.form["nome"]  # Nome do novo usuário
        email = request.form["email"]  # Email do novo usuário
        
        cnx = ligar_bd()
        cursor = cnx.cursor()

        # Insere novo usuário no banco
        cursor.execute(
            "INSERT INTO utilizadores(nome,email) VALUES(%s,%s)", (nome, email)
        )
        
        cnx.commit()  # Salva alterações
        cursor.close()
        cnx.close()

        return redirect(url_for("index"))  # Redireciona para página principal
    return render_template("form.html", titulo="Novo Utilizador", utilizador=None)


# Rota para editar usuário existente
@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))  # Verifica login
    # Opcional: só admins podem editar usuários
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("index"))

    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]  # Novo nome
        email = request.form["email"]  # Novo email

        # Atualiza dados do usuário no banco
        cursor.execute(
            "UPDATE utilizadores SET nome=%s,email=%s WHERE id=%s", (nome, email, id)
        )
        
        cnx.commit()  # Salva alterações
        cursor.close()
        cnx.close()

        return redirect(url_for("index"))  # Redireciona para página principal
    
    # Se GET, busca dados do usuário para preencher formulário
    cursor.execute("SELECT * FROM utilizadores WHERE id=%s", (id,))
    
    utilizador = cursor.fetchone()

    cursor.close()
    cnx.close()

    return render_template("form.html", titulo="Editar Utilizador", utilizador=utilizador)


# Rota para apagar usuário
@app.route("/apagar/<int:id>", methods=["POST"])
def apagar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))  # Verifica login
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("index"))
    
    cnx = ligar_bd()
    cursor = cnx.cursor()

    # Deleta usuário pelo ID
    cursor.execute("DELETE FROM utilizadores WHERE id=%s", (id,))
    cnx.commit()  # Salva alterações

    cursor.close()
    cnx.close()

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cnx = ligar_bd()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password, role FROM login WHERE username = %s", (username,))
        utilizador = cursor.fetchone()
        cursor.close()
        cnx.close()

        print("DEBUG: utilizador from DB ->", utilizador)

        if utilizador and utilizador.get("password") == password:
            session["user_id"] = utilizador["id"]
            session["username"] = utilizador["username"]
            session["user_role"] = utilizador["role"]  # 'admin' ou 'user'
            return redirect(url_for("index"))
        else:
            flash("Login incorreto.")
            return redirect(url_for("login"))

    return render_template("login.html")


# Rota para logout
@app.route("/logout")
def logout():
    session.clear()  # Limpa sessão
    return redirect(url_for("login"))  # Redireciona para login


# Rota para registrar novo usuário
@app.route("/register", methods=["GET","POST"])
def register():
    
    if request.method == "POST":

        username = request.form["username"]  # Usuário do formulário
        password = request.form["password"]  # Senha do formulário

        cnx = ligar_bd()
        cursor = cnx.cursor()

        # Insere novo usuário com role padrão "utilizador"
        cursor.execute(
            "INSERT INTO login(username,password,role) VALUES(%s,%s,%s)", (username, password, "utilizador")
        )
        cnx.commit()  # Salva alterações
        cursor.close()
        cnx.close()

        flash("Conta criada! Faça login.")
        return redirect(url_for("login"))
    
    return render_template("register.html")


# Rota para deletar usuário
@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):
    # Verifica sessão
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("user_role") != "admin":
        flash("Acesso negado.")
        return redirect(url_for("index"))

    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    # 1. Buscar o role do usuário
    cursor.execute("SELECT role FROM login WHERE id = %s", (id,))
    row = cursor.fetchone()

    if not row:
        flash("Utilizador não encontrado.")
        cursor.close()
        cnx.close()
        return redirect(url_for("roles"))

    role = ["role"]

    # 2. Impedir apagar admin
    if role == "admin":
        flash("Não é permitido deletar administradores.")
        cursor.close()
        cnx.close()
        return redirect(url_for("roles"))

    # 3. Deletar usuário
    cursor.execute("DELETE FROM login WHERE id = %s", (id,))
    cnx.commit()

    if cursor.rowcount and cursor.rowcount > 0:
        flash("Usuário deletado com sucesso.")
    else:
        flash("Falha ao deletar o usuário. Verifique restrições no BD.")

    cursor.close()
    cnx.close()
    return redirect(url_for("roles"))


# Rota para consultar meteorologia
@app.route("/meteorologia", methods=["GET","POST"])
def meteorologia():

    # Verifica login
    if "user_id" not in session:
        return redirect(url_for("login"))

    dados = None

    if request.method == "POST":
        
        key = "3689129ee7af0fa500cad990971aecd6"  # API key do OpenWeather
        cidade = request.form["cidade"]  # Cidade do formulário
        link = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={key}&lang=pt_br&units=metric"  # URL da API
        
        dados = requests.get(link).json()  # Faz requisição e obtém JSON
        print(dados)  # Debug

    return render_template("meteorologia.html", dados=dados)


# Rota para consultar cotações de moedas
@app.route("/moedas", methods=["GET","POST"])
def moedas():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Consulta API para obter cotações
    cotacoes = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL").json()
    
    # Converte valores para float, trata erros
    for k, v in cotacoes.items():
        try:
            v["bid"] = float(v["bid"])
        except (KeyError, ValueError, TypeError):
            v["bid"] = None
    
    return render_template("cotacoes.html", cotacoes=cotacoes)


if __name__ == "__main__":
    app.run(debug=True)  # Executa app em modo debug