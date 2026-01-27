from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for,session,flash
import json
import requests
import datetime

def ligar_db():
       return mysql.connector.connect(
                host="62.28.39.135",
                user="efa0125",
                password="123.Abc",
                database="efa0125_8_vet_clinic")

def testar_db():
    try:
        conn = ligar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()

        print("Conexão bem-sucedida! Resultado:", resultado)

        cursor.close()
        conn.close()
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

testar_db()
        
################ CRIAÇÃO DA APLICAÇÃO FLASK #################
app = Flask(__name__)
# Chave secreta usada para sessões (login)
app.secret_key = "123"

#injetar variáveis ou funções automaticamente em TODOS os templates do Flask
@app.context_processor
def datetime_ano():
        return {"ano":datetime.datetime.now().year}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    # Exemplo simples
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    # Proteção: só entra se estiver logado
    if not session.get("user_id"):
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__": 
      app.run(debug=True)