#desafio 1
# Crie uma função que receba o nome de uma pessoa como parâmetro
# e retorne uma saudação personalizada.

def saudacao(nome):
    return f'Olá, {nome}! Seja bem-vindo(a)!'
print(saudacao('Joana'))

#desafio 2
# Crie uma função que receba dois números como parâmetros
# e retorne a soma desses números.

def soma(num1, num2):
    return num1 + num2  
print(soma(5, 3))

#desafio 3
# Crie uma função que receba uma lista de números como parâmetro
# e retorne o maior número da lista.
def maior_numero(lista_numeros):
    return max(lista_numeros)
print(maior_numero([10, 25, 3, 47, 5]))

#desafio 4
# Crie uma função que receba uma string como parâmetro
# e retorne a string invertida.

def inverter_string(texto):
    return texto[::-1]
print(inverter_string('Python'))

#desafio 5
# Crie uma função que receba uma lista de palavras como parâmetro
# e retorne uma nova lista com as palavras em maiúsculas.

def palavras_maiusculas(lista_palavras):
    return [palavra.upper() for palavra in lista_palavras]
print(palavras_maiusculas(['python', 'funções', 'desafio']))

# Condicionais (if, elif, else)
'''
# Desafio 1
'''
idade = int(input('Qual é a tua idade? '))
if idade >= 18:
    print('És maior de idade.')
else:
    print('És menor de idade.')
'''
# Desafio 2
'''
numero = int(input('Introduz um número: '))
if numero % 2 == 0:
    print('O número é par.')
else:
    print('O número é ímpar.')

# Desafio 3
# Pedir a um aluno para introdzir a nota do teste
# Se a nota for inferior a 50, responder "Insuficiente" 
# Se a nota for maior que 50, responder "Suficiente"    
# Se a nota for maior que 70, responder "Bom"
# Se a nota for maior que 90, responder "Muito Bom"
#usando funções

def avaliar_nota(nota):
    if nota < 50:
        return 'Insuficiente'
    elif nota < 70:
        return 'Suficiente'
    elif nota < 90:
        return 'Bom'
    else:
        return 'Muito Bom.'
nota_teste = int(input('Qual é a tua nota? '))
print(avaliar_nota(nota_teste))

# Desafio 4
# Pedir a idade a uma pessoa e dizer se ela pode tirar a carta de condução
# Se tiver menos de 18 anos, responder "Não podes tirar a carta."
# Se tiver 18 anos ou mais, responder "Podes tirar a carta."
#usando funções

def verificar_idade(idade):
    if idade < 18:
        return 'Não podes tirar a carta.'
    else:
        return 'Podes tirar a carta.'
idade = int(input('Qual é a tua idade? '))
print(verificar_idade(idade))

# Desafio 5
# Pedir ao utilizador se no próximo domingo vai fazer sol
# Pedir ao utilizador se tem boleia
# Se fizer sol e tiver boleia, responder "Vou à praia"
# Caso contrário, responder "Fico em casa"
#usando funções

def decidir_praia(faz_sol, tenho_boleia):
    if faz_sol and tenho_boleia:
        return 'Vou à praia'
    else:
        return 'Fico em casa'
domingo_faz_sol = False
tenho_boleia = False
print(decidir_praia(domingo_faz_sol, tenho_boleia))

# Desafio 6
# Pedir ao utilizador para introduzir uma password
# Se a password for igual a "segredo123", responder "Acesso concedido"
# Caso contrário, responder "Acesso negado"

def verificar_password(password):
    if password == "segredo123":
        return "Acesso concedido"
    else:
        return "Acesso negado"
password_input = input('Introduz a password: ')
print(verificar_password(password_input))

#desafio 7
# Crie uma função que receba um número como parâmetro
# e retorne "Positivo" se o número for maior que zero,
# "Negativo" se for menor que zero, e "Zero" se for igual a zero.

def verificar_numero(numero):
    if numero > 0:
        return "Positivo"
    elif numero < 0:
        return "Negativo"
    else:
        return "Zero"
print(verificar_numero(10))
print(verificar_numero(-5))
print(verificar_numero(0))

# Desafio 8
# Crie uma função que receba a idade de uma pessoa como parâmetro
# e retorne a categoria etária:
# "Criança" (0-12 anos), "Adolescente" (13-19 anos),
# "Adulto" (20-64 anos) ou "Idoso" (65 anos ou mais).

def categoria_etaria(idade):
    if idade <= 12:
        return "Criança"
    elif idade <= 19:
        return "Adolescente"
    elif idade <= 64:
        return "Adulto"
    else:
        return "Idoso"
print(categoria_etaria(10))
print(categoria_etaria(15))
print(categoria_etaria(30))
print(categoria_etaria(70))

# Desafio 9
# Crie uma função que receba três números como parâmetros
# e retorne o maior entre eles.
def maior_entre_tres(num1, num2, num3):
    return max(num1, num2, num3)
print(maior_entre_tres(10, 25, 15))
print(maior_entre_tres(5, 3, 8))
print(maior_entre_tres(12, 12, 12))

# Desafio 10
# Crie uma função que receba um ano como parâmetro
# e retorne True se for um ano bissexto, ou False caso contrário.

def ano_bissexto(ano):
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        return True
    else:
        return False
print(ano_bissexto(2020))
print(ano_bissexto(1900))
print(ano_bissexto(2000))

# Desafio 11
# Crie uma função que receba uma lista de números como parâmetro
# e retorne a soma dos números pares da lista.

def soma_pares(lista_numeros):
    return sum(num for num in lista_numeros if num % 2 == 0)
print(soma_pares([1, 2, 3, 4, 5, 6]))
print(soma_pares([10, 15, 20, 25, 30]))
print(soma_pares([7, 9, 11]))

# Desafio 12
# Crie uma função que receba uma string como parâmetro
# e retorne True se for um palíndromo, ou False caso contrário.
def eh_palindromo(texto):
    texto = texto.replace(" ", "").lower()
    return texto == texto[::-1]
print(eh_palindromo("A  man a plan a canal Panama"))
print(eh_palindromo("Python"))
print(eh_palindromo("racecar"))

# Desafio 13
# Crie uma função que receba dois números como parâmetros
# e retorne a média aritmética entre eles.

def media_aritmetica(num1, num2):
    return (num1 + num2) / 2
print(media_aritmetica(10, 20))
print(media_aritmetica(5, 15))
print(media_aritmetica(7, 3))

# Desafio 14
# Crie uma função que receba uma lista de palavras como parâmetro
# e retorne a palavra mais longa da lista.
def palavra_mais_longa(lista_palavras):
    return max(lista_palavras, key=len)
print(palavra_mais_longa(['python', 'funções', 'desafio', 'programação']))
print(palavra_mais_longa(['casa', 'carro', 'bicicleta', 'avião']))
print(palavra_mais_longa(['sol', 'lua', 'estrela']))

# Desafio 15
# Crie uma função que receba um número como parâmetro
# e retorne a tabuada desse número de 1 a 10.

def tabuada(numero):
    return [numero * i for i in range(1, 11)]
print(tabuada(5))
print(tabuada(8))
print(tabuada(12))

# Desafio 16
# Crie uma função que receba uma lista de números como parâmetro
# e retorne uma nova lista contendo apenas os números positivos.

def numeros_positivos(lista_numeros):
    return [num for num in lista_numeros if num > 0]
print(numeros_positivos([-10, 5, -3, 8, 0, -1, 4]))
print(numeros_positivos([-5, -2, -8]))
print(numeros_positivos([1, 2, 3, 4, 5]))

# Desafio 17
# Crie uma função que receba uma string como parâmetro
# e retorne o número de vogais presentes na string.

def contar_vogais(texto):
    vogais = 'aeiouAEIOU'
    return sum(1 for char in texto if char in vogais)
print(contar_vogais("Olá, como vai você?"))
print(contar_vogais("Python é divertido"))
print(contar_vogais("XYZ"))

#desafio 18
# Crie uma função que receba dois parâmetros: a idade de uma pessoa
# e se ela possui carteira de motorista (True ou False).
# A função deve retornar True se a pessoa puder tirar a carta de condução
# (idade igual ou superior a 18 anos e possuir carteira),
# ou False caso contrário.

def pode_tirar_carta(idade, possui_carteira):
    return idade >= 18 and possui_carteira
print(pode_tirar_carta(20, True))
print(pode_tirar_carta(16, True))
print(pode_tirar_carta(22, False))
print(pode_tirar_carta(18, True))

# Desafio 19
# Crie uma função que receba uma lista de números como parâmetro
# e retorne a média dos números da lista.

def media_lista(lista_numeros):
    return sum(lista_numeros) / len(lista_numeros) if lista_numeros else 0
print(media_lista([10, 20, 30, 40, 50]))
print(media_lista([5, 15, 25]))
print(media_lista([]))

# Desafio 20
# Crie uma função que receba uma string como parâmetro
# e retorne a mesma string com as palavras em ordem inversa.
def inverter_palavras(texto):
    palavras = texto.split()
    palavras_invertidas = palavras[::-1]
    return ' '.join(palavras_invertidas)
print(inverter_palavras("Olá mundo este é um teste"))
print(inverter_palavras("Python funções desafio"))
print(inverter_palavras("Inverter palavras em uma string"))

# Desafio 21
# Crie uma função que receba dois números como parâmetros
# e retorne o maior divisor comum (MDC) entre eles.

def mdc(num1, num2):
    while num2:
        num1, num2 = num2, num1 % num2
    return num1
print(mdc(48, 18))
print(mdc(56, 98))
print(mdc(101, 10))

# Desafio 22
# Crie uma função que receba uma lista de números como parâmetro
# e retorne uma nova lista contendo apenas os números ímpares.
def numeros_impares(lista_numeros):
    return [num for num in lista_numeros if num % 2 != 0]
print(numeros_impares([1, 2, 3, 4, 5, 6]))
print(numeros_impares([10, 15, 20, 25, 30]))
print(numeros_impares([2, 4, 6, 8]))

# Desafio 23
# Crie uma função que receba uma string como parâmetro
# e retorne a mesma string com todas as letras maiúsculas.

def para_maiusculas(texto):
    return texto.upper()
print(para_maiusculas("Olá mundo"))
print(para_maiusculas("Python funções desafio"))
print(para_maiusculas("todas as letras em maiúsculas"))

# Desafio 24
# Crie uma função que receba um número como parâmetro
# e retorne True se o número for primo, ou False caso contrário.

def eh_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    return True
print(eh_primo(11))
print(eh_primo(15))
print(eh_primo(2))
print(eh_primo(1))
print(eh_primo(0))

# Desafio 25
# Crie uma função que receba uma lista de palavras como parâmetro
# e retorne uma nova lista com as palavras ordenadas por tamanho (da menor para a maior).
def ordenar_por_tamanho(lista_palavras):
    return sorted(lista_palavras, key=len)
print(ordenar_por_tamanho(['python', 'funções', 'desafio', 'programação']))
print(ordenar_por_tamanho(['casa', 'carro', 'bicicleta', 'avião']))
print(ordenar_por_tamanho(['sol', 'lua', 'estrela']))

# Desafio 26
# Crie uma função que receba dois parâmetros: a idade de uma pessoa
# e se ela possui carteira de motorista (True ou False).
# A função deve retornar True se a pessoa puder tirar a carta de condução
# (idade igual ou superior a 18 anos e possuir carteira),
# ou False caso contrário.

def pode_tirar_carta(idade, possui_carteira):
    return idade >= 18 and possui_carteira
print(pode_tirar_carta(20, True))
print(pode_tirar_carta(16, True))
print(pode_tirar_carta(22, False))
print(pode_tirar_carta(18, True))

# Desafio 27
# Crie uma função que receba uma lista de números como parâmetro
# e retorne a média dos números da lista.

def media_lista(lista_numeros):
    return sum(lista_numeros) / len(lista_numeros) if lista_numeros else 0
print(media_lista([10, 20, 30, 40, 50]))
print(media_lista([5, 15, 25]))
print(media_lista([]))
# Desafio 28
# Crie uma função que receba uma string como parâmetro  
# e retorne a mesma string com as palavras em ordem inversa.
def inverter_palavras(texto):
    palavras = texto.split()
    palavras_invertidas = palavras[::-1]
    return ' '.join(palavras_invertidas)
print(inverter_palavras("Olá mundo este é um teste"))
print(inverter_palavras("Python funções desafio"))
print(inverter_palavras("Inverter palavras em uma string"))
# Desafio 29
# Crie uma função que receba dois números como parâmetros
# e retorne o maior divisor comum (MDC) entre eles.
def mdc(num1, num2):
    while num2:
        num1, num2 = num2, num1 % num2
    return num1
print(mdc(48, 18))
print(mdc(56, 98))
print(mdc(101, 10))

# Desafio 30
# Crie uma função que receba uma lista de números como parâmetro
# e retorne uma nova lista contendo apenas os números ímpares.
def numeros_impares(lista_numeros):
    return [num for num in lista_numeros if num % 2 != 0]
print(numeros_impares([1, 2, 3, 4, 5, 6]))
print(numeros_impares([10, 15, 20, 25, 30]))
print(numeros_impares([2, 4, 6, 8]))

