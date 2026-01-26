from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for,session,flash
import json
import requests
import datetime

def ligar_db():
       return mysql.connector.connect(
                host="192.168.64.14",
                user="formando",
                password="123",
                database="clinica_python")
print(input(ligar_db()))
                
################ CRIAÇÃO DA APLICAÇÃO FLASK #################
app = Flask(__name__)

#injetar variáveis ou funções automaticamente em TODOS os templates do Flask
@app.context_processor
def datetime_ano():
        return {"ano":datetime.datetime.now().year}

@app.route("/")
def index():
        
        return render_template("index.html")

if __name__ == "__main__": 
      app.run(debug=True)