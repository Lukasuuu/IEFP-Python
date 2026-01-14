# Desafio 1
# Pedir nome e cor, depois mostrar frase

nome = input("Digite o seu nome: ")
cor = input("Digite a sua cor favorita: ")

print(f"O {nome} gosta da cor {cor}")



#===============================================================================

# Desafio 2
# Pedir ano de nascimento e mostrar idade

ano = int(input("Ano de nascimento: "))
idade = 2026 - ano

print(f"A tua idade é {idade}")

#===============================================================================

# Desafio 3
# Pedir dois números e mostrar a soma, subtração, multiplicação e divisão 

num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

soma = num1 + num2
subtracao = num1 - num2
multiplicacao = num1 * num2
divisao = num1 / num2

print(f"Soma: {soma}")
print(f"Subtração: {subtracao}")
print(f"Multiplicação: {multiplicacao}")
print(f"Divisão: {divisao}")

#===============================================================================

# Desafio 4
# Classificar nota

nota = int(input("Digite a nota: "))

if nota < 50:
    print("Insuficiente")
elif nota > 90:
    print("Muito Bom")
elif nota > 70:
    print("Bom")
elif nota > 50:
    print("Suficiente")

#===============================================================================

# Desafio 4.1
# Validar password entre 6 e 15 caracteres

pw = input("Digite a password: ")

if 6 <= len(pw) <= 15:
    print("Password válida")
else:
    print("Password inválida")

#===============================================================================

# Desafio 5
# Jogo do dado com 3 tentativas

import random

numero = random.randint(1, 6)
tentativas = 3

for i in range(tentativas):
    palpite = int(input("Adivinhe o número (1 a 6): "))
    if palpite == numero:
        print("Parabéns! Acertou!")
        break
else:
    print(f"Boa sorte para a próxima! O número era {numero}")

#===============================================================================

# Desafio 6
# Mostrar o maior número da lista

lista = [3, 9, 2, 7, 5]
print("O maior número é:", max(lista))

#===============================================================================

# Desafio 7
# Remover duplicados de uma lista

lista = [1, 2, 2, 3, 4, 4, 5]
lista_sem_duplicados = list(set(lista))

print(lista_sem_duplicados)

#===============================================================================

# Desafio 8
# Converter sequência numérica em texto

numeros = input("Digite uma sequência de números: ")

mapa = {
    "0": "zero", "1": "um", "2": "dois", "3": "três",
    "4": "quatro", "5": "cinco", "6": "seis",
    "7": "sete", "8": "oito", "9": "nove"
}

resultado = ""

for n in numeros:
    resultado += mapa[n] + " "

print(resultado.strip())

#===============================================================================

# Desafio 9
# Pedir dois números e mostrar a soma

a = int(input("Digite um número: "))
b = int(input("Digite outro número: "))
print("Soma =", a + b)

#===============================================================================

# Desafio 10
# Pedir idade e dizer se é maior de idade

idade = int(input("Idade: "))
if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")
    
#===============================================================================

# Desafio 11
# Pedir um número e dizer se é par ou ímpar

n = int(input("Número: "))
if n % 2 == 0:
    print("Par")
else:
    print("Ímpar")

#===============================================================================

# Desafio 12
# Criar uma função que retorna o dobro de um número

def dobro(x):
    return x * 2

print(dobro(5))

#===============================================================================

# Desafio 13
# Contar de 1 a 10 com um ciclo

for i in range(1, 11):
    print(i)
    
#===============================================================================

# Desafio 14
# Somar todos os números de uma lista

lista = [1, 2, 3, 4, 5]
print(sum(lista))

#===============================================================================

# Desafio 15
# Pedir um nome e mostrar quantas letras tem

nome = input("Nome: ")
print("Número de letras:", len(nome))

#===============================================================================

# Desafio 16
# Criar lista com 5 nomes e mostrar o primeiro e o último

nomes = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]
print(nomes[0], nomes[-1])

#===============================================================================

# Desafio 17
# Verificar se um número está na lista

lista = [3, 7, 10, 15]
n = int(input("Número: "))

if n in lista:
    print("Está na lista")
else:
    print("Não está na lista")

#===============================================================================

# Desafio 18
# Criar função que diz "Olá" com nome

def ola(nome):
    print(f"Olá, {nome}!")

ola("Lucas")

#===============================================================================

# Desafio 19
# Contar quantos números maiores que 10 existem na lista

lista = [5, 12, 3, 18, 20]
contador = 0

for n in lista:
    if n > 10:
        contador += 1

print("Maiores que 10:", contador)

#===============================================================================

# Desafio 20
# Criar lista de 1 a 20 usando ciclo

lista = []
for i in range(1, 20+1):
    lista.append(i)

print(lista)

#===============================================================================

# Desafio 21
# Mostrar apenas números pares de uma lista

lista = [1, 2, 3, 4, 5, 6]
pares = []

for n in lista:
    if n % 2 == 0:
        pares.append(n)

print(pares)

#===============================================================================

# Desafio 22
# Pedir frase e mostrar em maiúsculas

frase = input("Digite uma frase: ")
print(frase.upper())

#===============================================================================

# Desafio 23
# Criar função que retorna a média de 3 números

def media(a, b, c):
    return (a + b + c) / 3

print(media(10, 15, 20))

#===============================================================================

# Desafio 24
# Verificar se password contém "@" (simples validação)

pw = input("Password: ")

if "@" in pw:
    print("Password válida")
else:
    print("Password inválida")

#===============================================================================

# Desafio 25
# Criar lista e adicionar elemento pedido ao utilizador

lista = ["a", "b", "c"]
novo = input("Adicionar elemento: ")
lista.append(novo)
print(lista)

#===============================================================================

# Desafio 26
# Mostrar números de 10 até 1

for i in range(10, 0, -1):
    print(i)

#===============================================================================

# Desafio 27
# Pedir número e mostrar tabuada

n = int(input("Número: "))

for i in range(1, 11):
    print(f"{n} x {i} = {n*i}")

#===============================================================================

# Desafio 28
# Criar lista e remover elemento escolhido

lista = [1, 2, 3, 4, 5]
remover = int(input("Número a remover: "))

if remover in lista:
    lista.remove(remover)

print(lista)

#===============================================================================

# Desafio 29
# Contar vogais numa palavra

palavra = input("Palavra: ").lower()
vogais = "aeiou"
contador = 0

for letra in palavra:
    if letra in vogais:
        contador += 1

print("Vogais:", contador)

#===============================================================================

# Desafio 30
# Criar função que retorna o maior de 3 números

def maior(a, b, c):
    return max(a, b, c)

print(maior(10, 3, 7))

#===============================================================================

# Desafio 31
# Pedir lista de números e mostrar em ordem crescente

numeros = input("Digite números separados por espaço: ")
lista = [int(n) for n in numeros.split()]
lista.sort()
print("Ordem crescente:", lista)

#===============================================================================

# Desafio 31.1
# Verificar se uma palavra começa com letra maiúscula

palavra = input("Palavra: ")

if palavra[0].isupper():
    print("Começa com maiúscula")
else:
    print("Não começa com maiúscula")

#===============================================================================

# Desafio 32
# Criar lista com números de 2 em 2 até 20

lista = list(range(0, 21, 2))
print(lista)

#===============================================================================

# Desafio 33
# Pedir 5 números e guardar numa lista

lista = []

for i in range(5):
    n = int(input("Número: "))
    lista.append(n)

print(lista)

#===============================================================================

# Desafio 34
# Somar apenas números ímpares de uma lista

lista = [1, 2, 3, 4, 5, 6]
soma = 0

for n in lista:
    if n % 2 != 0:
        soma += n

print("Soma dos ímpares:", soma)

#===============================================================================

# Desafio 35
# Criar função que inverte uma string

def inverter(texto):
    return texto[::-1]

print(inverter("python"))

#===============================================================================

# Desafio 36
# Pedir nome e idade, mostrar mensagem personalizada

nome = input("Nome: ")
idade = input("Idade: ")
print(f"Olá {nome}, você tem {idade} anos.")

#===============================================================================

# Desafio 37
# Verificar se número é primo ou não Exibir mensagem

n = int(input("Número: "))
if n > 1:
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            print("Não é primo")
            break
    else:
        print("É primo")
else:
    print("Não é primo")

#===============================================================================

# Desafio 38
# Criar dicionário com 3 países e suas capitais, mostrar capital pedida
paises = {
    "Portugal": "Lisboa",
    "Espanha": "Madrid",
    "França": "Paris"
}
pais = input("Digite o nome de um país: ")
capital = paises.get(pais, "País não encontrado")
print("Capital:", capital)

#===============================================================================

# Desafio 39
# Pedir número e mostrar Dobro, Triplo e Raiz Quadrada

n = float(input("Número: "))
dobro = n * 2 # type: ignore
triplo = n * 3
raiz_quadrada = n ** 0.5
print(f"Dobro: {dobro}, Triplo: {triplo}, Raiz Quadrada: {raiz_quadrada}")
#===============================================================================

# Desafio 40
# Pedir 3 notas e calcular a média final

notas = []
for i in range(3):
    nota = float(input(f"Nota {i+1}: "))
    notas.append(nota)
media = sum(notas) / 3   # type: ignore
print(f"Média final: {media}")

#===============================================================================

# Desafio 41
# Verificar se ano é bissexto

ano = int(input("Ano: "))
if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
    print("Ano bissexto")
else:
    print("Ano não é bissexto")

#===============================================================================

# Desafio 42
# Criar lista com 10 números aleatórios entre 1 e 100

import random
lista = [random.randint(1, 100) for _ in range(10)]
print(lista)

#===============================================================================

# Desafio 43
# Pedir frase e contar palavras

frase = input("Digite uma frase: ")
palavras = frase.split()
print("Número de palavras:", len(palavras))

#===============================================================================

# Desafio 44
# Criar função que verifica se número é positivo, negativo ou zero

def verificar_numero(n):
    if n > 0:
        return "Positivo"
    elif n < 0:
        return "Negativo"
    else:
        return "Zero"
print(verificar_numero(-5))

#===============================================================================

# Desafio 45
# Pedir lista de nomes e mostrar em ordem alfabética

nomes = input("Digite nomes separados por vírgula: ")
lista_nomes = [nome.strip() for nome in nomes.split(",")]
lista_nomes.sort()
print("Nomes em ordem alfabética:", lista_nomes)

#===============================================================================

# Desafio 46
# Calcular fatorial de um número

n = int(input("Número: "))
fatorial = 1
for i in range(1, n + 1):
    fatorial *= i
print(f"Fatorial de {n} é {fatorial}")

#===============================================================================

# Desafio 47
# Pedir número e mostrar sequência de Fibonacci até esse número

n = int(input("Número: "))
a, b = 0, 1
while a <= n:
    print(a, end=' ')
    a, b = b, a + b
print()

#===============================================================================

# Desafio 48
# Criar dicionário com 3 frutas e seus preços, mostrar preço pedido de cada fruta

frutas = {
    "maçã": 2.5,
    "banana": 1.8,
    "laranja": 3.0
}

fruta = input("Digite o nome de uma fruta: ")
preco = frutas.get(fruta, "Fruta não encontrada")
print("Preço:", preco)

#===============================================================================

# Desafio 49
# Pedir número e mostrar se é múltiplo de 3 ou 5

n = int(input("Número: "))
if n % 3 == 0 or n % 5 == 0:
    print(f"{n} é múltiplo de 3 ou 5")
else:
    print(f"{n} não é múltiplo de 3 ou 5")

#===============================================================================

# Desafio 50
# Criar função que converte Celsius para Fahrenheit

def celsius_para_fahrenheit(c):
    return (c * 9/5) + 32
print(celsius_para_fahrenheit(25))

#===============================================================================

# Desafio 51
#função que verifica se uma string é um palíndromo

def eh_palindromo(texto):
    texto = texto.replace(" ", "").lower()
    return texto == texto[::-1]
print(eh_palindromo("Ana"))

#===============================================================================

# Desafio 52
# Pedir lista de números e mostrar o menor número   

numeros = input("Digite números separados por espaço: ")
lista = [int(n) for n in numeros.split()]
print("O menor número é:", min(lista))
#===============================================================================

# Desafio 53
# Pedir número e mostrar se é positivo, negativo ou zero

n = float(input("Número: "))
if n > 0:
    print("Positivo")
elif n < 0:
    print("Negativo")
else:
    print("Zero")
#===============================================================================

# Desafio 54
# Criar lista com 5 cidades e mostrar a que tem o nome mais longo

cidades = ["Lisboa", "Porto", "Faro", "Coimbra", "Braga"]
cidade_mais_longa = max(cidades, key=len)
print("Cidade com nome mais longo:", cidade_mais_longa)

#===============================================================================

# Desafio 55
# Pedir número e mostrar se é par ou ímpar usando função

def par_ou_impar(n):
    return "Par" if n % 2 == 0 else "Ímpar"
n = int(input("Número: "))
print(par_ou_impar(n))

#===============================================================================

# Desafio 56
# Pedir lista de números e mostrar a soma dos números pares

numeros = input("Digite números separados por espaço: ")
lista = [int(n) for n in numeros.split()]
soma_pares = sum(n for n in lista if n % 2 == 0)
print("Soma dos números pares:", soma_pares)

#===============================================================================

# Desafio 57
# Criar função que retorna o quadrado de um número

def quadrado(n):
    return n ** 2
print(quadrado(4))

#===============================================================================

# Desafio 58
# Pedir frase e mostrar número de caracteres

frase = input("Digite uma frase: ")
print("Número de caracteres:", len(frase))

#===============================================================================

# Desafio 59
# Criar lista com 10 números e mostrar apenas os maiores que 5

numeros = [1, 6, 3, 8, 5, 10, 2, 7, 4, 9]
maiores_que_cinco = [n for n in numeros if n > 5]
print("Números maiores que 5:", maiores_que_cinco)

#===============================================================================

# Desafio 60
# Pedir número e mostrar a tabuada usando função

def tabuada(n):
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")
n = int(input("Número: "))
tabuada(n)

#===============================================================================

# Desafio 61
# Verificar se uma string é um anagrama de outra

def eh_anagrama(str1, str2):
    return sorted(str1.replace(" ", "").lower()) == sorted(str2.replace(" ", "").lower())
print(eh_anagrama("amor", "roma"))

#===============================================================================

# Desafio 62
# Pedir lista de números e mostrar o segundo maior número

numeros = input("Digite números separados por espaço: ")
lista = [int(n) for n in numeros.split()]
lista_sem_duplicados = list(set(lista))
lista_sem_duplicados.sort()
if len(lista_sem_duplicados) >= 2:
    print("O segundo maior número é:", lista_sem_duplicados[-2])
else:
    print("Não há segundo maior número.")
    
#===============================================================================

# Desafio 63
# Criar função que retorna a soma dos dígitos de um número

def soma_digitos(n):
    return sum(int(digito) for digito in str(n))
print(soma_digitos(1234))

#===============================================================================

# Desafio 64
#função que verifica se uma lista está ordenada em ordem crescente

def esta_ordenada(lista):
    return lista == sorted(lista)
print(esta_ordenada([1, 2, 3, 4, 5]))

#===============================================================================

# Desafio 65
# Pedir número e mostrar se é positivo, negativo ou zero usando função

def verificar_numero(n):
    if n > 0:
        return "Positivo"
    elif n < 0:
        return "Negativo"
    else:
        return "Zero"
n = float(input("Número: "))
print(verificar_numero(n))

#===============================================================================

# Desafio 66
# Criar lista com 10 números aleatórios e mostrar a média

import random
lista = [random.randint(1, 100) for _ in range(10)]
media = sum(lista) / len(lista) # type: ignore
print("Média dos números:", media)

#===============================================================================

# Desafio 67
# Pedir frase e mostrar número de palavras usando função

def contar_palavras(frase):
    palavras = frase.split()
    return len(palavras)
frase = input("Digite uma frase: ")
print("Número de palavras:", contar_palavras(frase))

#===============================================================================

# Desafio 68
# Criar função que retorna o fatorial de um número

def fatorial(n):
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado
print(fatorial(5))

#===============================================================================

# Desafio 69
# Pedir lista de números e mostrar apenas os ímpares usando função

def filtrar_impares(lista):
    return [n for n in lista if n % 2 != 0]

numeros = input("Digite números separados por espaço: ")
lista = [int(n) for n in numeros.split()]
impares = filtrar_impares(lista)

print("Números ímpares:", impares)

#===============================================================================

# Desafio 70
# Criar função que converte Fahrenheit para Celsius

def fahrenheit_para_celsius(f):
    return (f - 32) * 5/9

print(fahrenheit_para_celsius(77))

#===============================================================================

# Desafio 71
#função que verifica se um número é perfeito

def eh_perfeito(n):
    soma_divisores = sum(i for i in range(1, n) if n % i == 0)
    return soma_divisores == n
print(eh_perfeito(28))

#===============================================================================

# Desafio 72
# Pedir número e mostrar se é múltiplo de 4 e 6 usando função

def multiplo_de_4_e_6(n):
    return n % 4 == 0 and n % 6 == 0

n = int(input("Número: "))
if multiplo_de_4_e_6(n):
    print(f"{n} é múltiplo de 4 e 6")
else:
    print(f"{n} não é múltiplo de 4 e 6")
    
#===============================================================================

# Desafio 73
# Criar lista com 5 nomes e mostrar em ordem inversa usando função

def inverter_lista(lista):
    return lista[::-1]
nomes = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]
print(inverter_lista(nomes))

#===============================================================================

# Desafio 74
# Pedir número e mostrar se é primo usando função

def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
n = int(input("Número: "))
if eh_primo(n):
    print(f"{n} é primo")
else:
    print(f"{n} não é primo")

#===============================================================================

# Desafio 75
# Criar função que retorna a soma dos quadrados de uma lista

def soma_dos_quadrados(lista):
    return sum(n ** 2 for n in lista)
numeros = [1, 2, 3, 4, 5]
print(soma_dos_quadrados(numeros))

#===============================================================================

# Desafio 76
# Pedir frase e mostrar se é palíndromo usando função

def eh_palindromo(frase):
    frase = frase.replace(" ", "").lower()
    return frase == frase[::-1]
frase = input("Digite uma frase: ")
if eh_palindromo(frase):
    print("É palíndromo")
else:
    print("Não é palíndromo")

#===============================================================================

# Desafio 77
# Criar função que retorna o menor número de uma lista

def menor_numero(lista):
    return min(lista)
numeros = [5, 2, 9, 1, 7]
print(menor_numero(numeros))

#===============================================================================

# Desafio 78
# função que normaliza uma string (remove espaços extras e coloca em minúsculas)

def normalizar_string(texto):
    return ' '.join(texto.split()).lower()
texto = "   Olá   Mundo   "
print(normalizar_string(texto))

#===============================================================================

# Desafio 79
# Pedir função que retorna a soma dos números pares de uma lista

def soma_numeros_pares(lista):
    return sum(n for n in lista if n % 2 == 0)
numeros = [1, 2, 3, 4, 5, 6]
print(soma_numeros_pares(numeros))

#===============================================================================

# Desafio 80
# Criar função que verifica se uma lista contém um elemento específico

def contem_elemento(lista, elemento):
    return elemento in lista
numeros = [1, 2, 3, 4, 5]
elemento = int(input("Elemento para verificar: "))
if contem_elemento(numeros, elemento):
    print(f"{elemento} está na lista")
else:
    print(f"{elemento} não está na lista")

#===============================================================================    