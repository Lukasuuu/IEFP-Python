import mysql.connector

# 1) DADOS DA LIGAÇÃO (os mesmos que já tem)
HOST = "62.28.39.135"
USER = "efa0125"
PASSWORD = "123.Abc"
DATABASE = "efa0125_25_formacao_crud"


# 2) FUNÇÃO PARA LIGAR À BASE DE DADOS
def ligar_bd():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )


# 3) CREATE - INSERIR UTILIZADOR
def inserir_utilizador():
    nome = input("Nome: ")
    email = input("Email: ")

    cnx = ligar_bd()
    cursor = cnx.cursor()

    sql = "INSERT INTO utilizadores (nome, email) VALUES (%s, %s)"
    cursor.execute(sql, (nome, email))
    cnx.commit()

    print("Utilizador inserido com sucesso!")

    cursor.close()
    cnx.close()


# 4) READ - LISTAR UTILIZADORES
def listar_utilizadores():
    cnx = ligar_bd()
    cursor = cnx.cursor()

    sql = "SELECT id, nome, email, created_at FROM utilizadores"
    cursor.execute(sql)

    resultados = cursor.fetchall()

    print("\n--- LISTA DE UTILIZADORES ---")
    for linha in resultados:
        # linha = (id, nome, email, created_at)
        print(linha)

    cursor.close()
    cnx.close()


# 5) UPDATE - ATUALIZAR UTILIZADOR
def atualizar_utilizador():
    
    id_utilizador = input('ID do utilizador a atualizar: ')
    novo_nome = input('Diga o nome do utilizador a atualizar: ')
    novo_email = input('Diga o email a atualizar: ')
    
    cnx = ligar_bd()
    cursor = cnx.cursor()

    sql = " UPDATE utilizadores SET nome = %s, email = %s WHERE id = %s "

    cursor.execute(sql, id_utilizador, novo_nome, novo_email)
    cnx.commit()

    print("Utilizador atualizado com sucesso!")

    cursor.close()
    cnx.close()


# 6) DELETE - APAGAR UTILIZADOR

def apagar_utilizador():
    id_utilizador = input('ID do utilizador a apagar: ')
    
    cnx = ligar_bd()
    cursor = cnx.cursor()
    
    sql = "DELETE FROM utilizadores WHERE id = %s"
    cursor.execute(sql,(id_utilizador))
    cnx.commit()
    
    if cursor.rowcount == 0:
        print('Nao existe utilizador com esse ID')
    else:
        print('Utilizador apagado com sucesso!')

    cursor.close()
    cnx.close()
    
# 7) MENU PRINCIPAL

def menu():
    while True:
        print("\n===== MENU CRUD =====")
        print("1 - Inserir utilizador")
        print("2 - Listar utilizadores")
        print("3 - Atualizar utilizador")
        print("4 - Apagar utilizador")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            inserir_utilizador()
        elif opcao == "2":
            listar_utilizadores()
        elif opcao == "3":
            atualizar_utilizador()
        elif opcao == "4":
            apagar_utilizador()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opção inválida!")


# 8) ARRANQUE DO PROGRAMA
menu()
