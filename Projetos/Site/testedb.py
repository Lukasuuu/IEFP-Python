from flask import Flask
import mysql.connector
from flask import render_template, request, redirect, url_for,session,flash
import json
import requests
import datetime

def ligar_db():
       return mysql.connector.connect(
                  host="127.0.0.1",
                  port="3306",
                  user="root",
                  password="123.Abc",
                  database="efa0125_08_vet_clinic"
)

def testar_db():
    try:
        conn = ligar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * from animais")
        resultado = cursor.fetchall()

        print("Conexão bem-sucedida! Resultado:", resultado)

        cursor.close()
        conn.close()
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)

if __name__ == "__main__":
    testar_db()
