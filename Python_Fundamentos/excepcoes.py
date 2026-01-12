'''
try:
    idade = int(input('Idade: '))
    print(f'a idade é: {idade} anos')
    salario = 1600
    risco = salario/idade
except ValueError:
    print('A idade não pode ser uma string')
except ZeroDivisionError:
    print('Não a idade igual a zero tente outro número')

'''
'''DESAFIO DE EXCEPÇÕES'''
#Desafio 10
# Pedir ao utilizador o preço de um produto e a respectiva percentagem de desconto
# O programa devera calcular e mostrar o valor a pagar apos o desconto
# Caso a informação introduzida não seja válida
# O programa indica qual foi o erro!
while True:
    try:
        preco= float(input('Me de um valor: '))
        if preco <= 0:
            print ('o valor do preco não pode ser negativo e nem Zero tente outra vez')
        else:
            break   
    except ValueError:
            print ('o valor nao é valido pois usou uma string')
    
while True:
    try:
        desconto=float(input('me de a porcentagem de desconto: '))
        if desconto < 0:
            print ('o valor do desconto não pode ser negativo tente outra vez')
        else:
            break
    except ValueError:
        print ('o valor nao é valido pois usou uma string')

try:
    valorPagar= preco - preco * (desconto/100)
    print(f'Valor a pagar é: {valorPagar}')
except NameError:
    print('O PROGRAMA NÃO CONSEGUE CALCULAR POR FALTA DE INFORMACAO')