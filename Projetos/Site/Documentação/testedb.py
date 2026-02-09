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
                database="efa0125_08_vet_clinic"
)

def testar_db():
    try:
        conexao = ligar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * from animais")
        resultado = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        print("Conexão bem-sucedida! Resultado:", resultado)
        
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
  
     

if __name__ == "__main__":
    testar_db()
