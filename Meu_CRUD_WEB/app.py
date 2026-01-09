from flask import Flask
import mysql.connector
from flask import render_template, request, redirect 

#Fazer a ligação com a Base de dados
def ligar_bd():
    return mysql.connector.connect(
        host="62.28.39.135",
        user="efa0125",
        password="123.Abc",
        database="efa0125_25_formacao_crud"
        )
        
#Criar a Pagina WEB com os dados da Base de Dados
app = Flask (__name__)

@app.route("/")

def index():
    cnx = ligar_bd() # faz a ligacao com Base Dados
    cursor = cnx.cursor(dictionary=True)
        
    cursor.execute("SELECT id,nome,email, created_at FROM utilizadores ORDER BY id DESC") #envia a query SQL
    utilizadores = cursor.fetchall() #fetchall é um metodo que traz as linhas todas da query executada
    
##render_template envia os dados todos para o ficheiro HTML        
    return render_template("index.html",utilizadores=utilizadores)

@app.route("/novo", methods=["GET","POST"])

def novo():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        
        cnx = ligar_bd()
        cursor = cnx.cursor()
        
        cursor.execute(
            "INSERT INTO utilizadores(nome,email) VALUES (%s,%s)",(nome,email)
        )
        
        cnx.commit()
        
        cursor.close()
        cnx.close()
        
        return redirect("/")
    return render_template("form.html", titulo="Novo Utilizador", utilizador=None)

@app.route("/editar/<int:id>", methods=["GET","POST"])

def editar(id):
    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)
    
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        
   
        cursor2 = cnx.cursor()
        
        cursor2.execute(
            "UPDATE utilizadores SET nome=%s, email=%s WHERE id=%s", (nome,email,id)
        )
        
        cnx.commit()
        cursor2.close()
        
        cursor.close()
        cnx.close()
        
        return redirect("/")
    
    cursor.execute("SELECT id,nome,email FROM utilizadores WHERE id=%s", (id,))
    utilizador = cursor.fetchone()
    
    cursor.close()
    cnx.close()
    
    
    return render_template("form.html", titulo="Editar Utilizador", utilizador=utilizador)

@app.route("/apagar/<int:id>", methods=["GET","POST"])

def apagar(id):
    cnx = ligar_bd()
    cursor = cnx.cursor(dictionary=True)
    
    cursor = cnx.cursor()
        
    cursor.execute(
            "DELETE FROM utilizadores WHERE id=%s", (id,)
    )
    
    utilizador = cursor.fetchone()
        
    cnx.commit()
    cursor.close()
        
    cnx.close()
        
    return redirect("/")
    
    return render_template("form.html", titulo="Apagar Utilizador", utilizador=utilizador)

app.run(debug=True)