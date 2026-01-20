from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import requests

def ligar_bd():
    return mysql.connector.connect(
        host="62.28.39.135",
        user="efa0125",
        password="123.Abc",
        database="efa0125_25_formacao_crud"
    )

app = Flask(__name__)
app.secret_key = "123"



@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    cnx = ligar_bd() # faz a ligacao com Base Dados
    cur = cnx.cursor(dictionary=True)

    cur.execute("SELECT id,nome,email,created_at FROM utilizadores ORDER BY id DESC") #envia a query SQL

    utilizadores = cur.fetchall() #fetchall é um metodo que traz as linhas todas da query executada
    
    cur.close()
    cnx.close()

    ##render_template envia os dados todos para o ficheiro HTML  
    return render_template("index.html", utilizadores=utilizadores)




@app.route("/roles", methods=["GET","POST"])
def roles():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Apenas administradores podem aceder
    if session.get("user_role") != "admin":
        flash("Acesso Negado. Apenas administradores podem gerir permissões.")
        return redirect(url_for("index"))
    
    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    # Atualizar role
    if request.method == "POST":
        user_id = request.form["user_id"]
        novo_role = request.form["role"]

        cursor.execute(
            "UPDATE login SET role=%s WHERE id=%s",
            (novo_role, user_id)
        )
        cnx.commit()
        flash("Role atualizado com sucesso!")

    # Buscar utilizadores
    cursor.execute(
        "SELECT id, username, role FROM login ORDER BY id"
        )
    
    utilizadores = cursor.fetchall() #

    cursor.close()
    cnx.close()

    return render_template("roles.html", utilizadores=utilizadores)



@app.route("/novo", methods=["GET","POST"])
def novo():
    if "user_id" not in session: 
        return redirect(url_for("login"))
    
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        
        cnx = ligar_bd()
        cursor = cnx.cursor()

        cursor.execute(
                        "INSERT INTO utilizadores(nome,email) VALUES(%s,%s)",(nome,email)
                       )
        
        cnx.commit()
        cursor.close()
        cnx.close()

        return redirect("/")
    return render_template("form.html", titulo="Novo Utilizador", utilizador=None)

@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):
    if "user_id" not in session: 
        return redirect(url_for("login"))

    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        cursor.execute(
                        "UPDATE utilizadores SET nome=%s,email=%s WHERE id=%s", (nome,email, id))
        
        cnx.commit(); 
        cursor.close(); 
        cnx.close()

        return redirect("/")
    
    cursor.execute(
                        "SELECT * FROM utilizadores WHERE id=%s", (id,)
        )
    
    utilizador = cursor.fetchone()

    cursor.close()
    cnx.close()

    return render_template("form.html", titulo="Editar Utilizador", utilizador=utilizador)

@app.route("/apagar/<int:id>", methods=["GET","POST"])
def apagar(id):
    if "user_id" not in session: 
        return redirect(url_for("login"))
    
    cnx = ligar_bd()
    cursor = cnx.cursor()

    cursor.execute(
                    "DELETE FROM utilizadores WHERE id=%s", (id,)
        )
    utilizador = cursor.fetchone()

    cnx.commit()
    cursor.close()
    cnx.close()

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]

        cnx = ligar_bd()
        cursor = cnx.cursor(dictionary=True)

        #Procurar o utilizador na tabela login:
        
        cursor.execute(
            "SELECT id, username, password,role FROM login WHERE username = %s",(username,)
        )

        utilizador = cursor.fetchone()

        cursor.close()
        cnx.close()

        # Validar password (simple txt)
        if utilizador and utilizador["password"] == password:
            session.update({"user_id":utilizador["id"],
                            "username":utilizador["username"],
                            "user_role":utilizador["role"]}
                            )
            return redirect(url_for("index"))
        else: 
            flash("Login incorreto.")
            return redirect(url_for("login"))
        
    return render_template("login.html")

#Criar um logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username=request.form["username"]
        password=request.form["password"]

        cnx = ligar_bd()
        cursor = cnx.cursor()

        cursor.execute(
                        "INSERT INTO login(username,password,role) VALUES(%s,%s,%s)",(username, password, "user")
                        )
        cnx.commit()
        cursor.close()
        cnx.close()

        flash("Conta criada! Faça login.")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/meteorologia", methods=["GET","POST"])
def meteorologia():

    #Protege para fazer login da sessao pra acessar a pagina
    if "user_id" not in session: 
        return redirect(url_for("login"))

    dados = None

    if request.method == "POST":
        
        key = "3689129ee7af0fa500cad990971aecd6"
        cidade = request.form["cidade"]
        link = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={key}&lang=pt_br&units=metric"
        
        dados = requests.get(link).json()

    return render_template("meteorologia.html", dados=dados)

@app.route("/moedas", methods=["GET",["POST"]])
def moedas():

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    cotacoes = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL").json()
    
    return render_template("cotacoes.html", cotacoes=cotacoes)

if __name__ == "__main__":
    app.run(debug=True)
