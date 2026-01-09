############### Condicionais em Python ###############

#desafio 1

'''
idade = input("Digite sua idade: ")  #pega a idade digitada pelo usuario

if int(idade) < 18:
    print("Voce é menor de idade e ainda não tem idade pra tirar a carta.")
    print("Espere mais algum tempo.")

else:
    print("Voce é maior de idade." \
    " Pode tirar a carta de motorista.")
'''

#desafio 2

'''
Pedir ao utilizador para digitar uma nota de 0 a 100
Verificar a classificacao da nota e mostrar a mensagem correspondente:
Se a nota for inferio a 50, mostrar "Insuficiente"
Se a nota for superior a 50, mostrar "Suficiente"
Se a nota for superior ou igual a 70, mostrar "Bom"
Se a nota for superior ou igual a 90, mostrar "Excelente"
'''

nota = int(input("Digite sua nota: "))  #pega a nota digitada pelo usuario

if nota < 50:
    print("Insuficiente")
elif nota >= 50 and nota < 70:
    print("Suficiente")
elif nota >= 70 and nota < 90:
    print("Bom")
else:
    print("Excelente")

############ Operadores logicos: (and, or, not) ###############

#desafio 3

domingo_faz_sol = True      #variavel que indica se o domingo faz sol
tenho_boleia = False           #variavel que indica se tenho bola

#and
if domingo_faz_sol and tenho_boleia: #se faz sol e tenho boleia
    print("Vou à praia")
else:
    print("Fico em casa")

#or
if domingo_faz_sol or tenho_boleia: #se faz sol ou tenho boleia
    print("Vou à praia")
else:
    print("Fico em casa")
#not
if domingo_faz_sol or not tenho_boleia: #se nao tenho boleia
    print("vou à praia")
else:
    print("Fico em casa")

########## Operadores de comparacao: (==, !=, >, <, >=, <=) ###############

#desafio 4
'''
Pedir ao utilizador para digitar uma password
Verificar se a password tem pelo menos 6 caracteres e maximo 15 caracteres
Se a password for valida, mostrar "Password valida"
Se a password for invalida, mostrar "Password invalida"
'''

password = input("Digite sua password: ")  #pega a password digitada pelo usuario
if len(password) >= 6 and len(password) <= 15:
    print("Password valida")
else:
    print("Password invalida")
