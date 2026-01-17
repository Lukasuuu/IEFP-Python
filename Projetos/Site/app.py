from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for,session,flash
import json
import requests

#Fazer a ligação com a Base de dados
def mysql_connector():
    return mysql.connector.connect(
        host="192.168.64.17",
        user="admin",
        password="123",
        database="teste"
        )
        
#Criar a Pagina WEB com os dados da Base de Dados
app = Flask (__name__)
app.secret_key="123"

@app.route("/")

def index():  
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    cnx = mysql_connector() # faz a ligacao com Base Dados
    cursor = cnx.cursor(dictionary=True)
        
    cursor.execute("SELECT id,name,email, created_at FROM users ORDER BY id DESC") #envia a query SQL
    users = cursor.fetchall() #fetchall é um metodo que traz as linhas todas da query executada
    
    cursor.close()
    cnx.close()
    ##render_template envia os dados todos para o ficheiro HTML        
    return render_template("index.html",users=users)
app.run(debug=True)