# ============================================================
#   ARQUIVO: simulador_prova_python.py
#   Conteúdo: 8 desafios iniciais + 30 questões do simulador
#   Cada questão contém:
#       - Enunciado
#       - Explicação passo a passo
#       - Código da solução
# ============================================================


# ============================================================
# ===================== DESAFIOS INICIAIS =====================
# ============================================================

# ------------------------------------------------------------
# DESAFIO 1
# ENUNCIADO:
#   Pedir ao utilizador o nome e a cor favorita.
#   Mostrar a frase: "O <nome> gosta da cor <cor>".
#
# PASSO A PASSO:
#   1. Pedimos o nome com input()
#   2. Pedimos a cor com input()
#   3. Usamos f-string para montar a frase final
# ------------------------------------------------------------
nome = input("Digite o seu nome: ")
cor = input("Digite a sua cor favorita: ")
print(f"O {nome} gosta da cor {cor}")


# ------------------------------------------------------------
# DESAFIO 2
# ENUNCIADO:
#   Pedir o ano de nascimento e calcular a idade.
#
# PASSO A PASSO:
#   1. Ler o ano como inteiro
#   2. Subtrair do ano atual (2026)
#   3. Mostrar a idade
# ------------------------------------------------------------
ano = int(input("Ano de nascimento: "))
idade = 2026 - ano
print(f"A tua idade é {idade}")


# ------------------------------------------------------------
# DESAFIO 3
# ENUNCIADO:
#   Classificar nota:
#       < 50 → Insuficiente
#       > 50 → Suficiente
#       > 70 → Bom
#       > 90 → Muito Bom
#
# PASSO A PASSO:
#   1. Ler nota
#   2. Usar condicionais em ordem correta
# ------------------------------------------------------------
nota = int(input("Digite a nota: "))

if nota < 50:
    print("Insuficiente")
elif nota > 90:
    print("Muito Bom")
elif nota > 70:
    print("Bom")
elif nota > 50:
    print("Suficiente")


# ------------------------------------------------------------
# DESAFIO 4
# ENUNCIADO:
#   Validar password entre 6 e 15 caracteres.
#
# PASSO A PASSO:
#   1. Ler password
#   2. Verificar tamanho com len()
# ------------------------------------------------------------
pw = input("Digite a password: ")

if 6 <= len(pw) <= 15:
    print("Password válida")
else:
    print("Password inválida")


# ------------------------------------------------------------
# DESAFIO 5
# ENUNCIADO:
#   Gerar número aleatório entre 1 e 6.
#   Dar 3 tentativas ao utilizador para adivinhar.
#
# PASSO A PASSO:
#   1. Importar random
#   2. Gerar número com randint()
#   3. Criar ciclo for com 3 tentativas
#   4. Comparar palpite com número
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# DESAFIO 6
# ENUNCIADO:
#   Mostrar o maior número de uma lista.
#
# PASSO A PASSO:
#   1. Criar lista
#   2. Usar max()
# ------------------------------------------------------------
lista = [3, 9, 2, 7, 5]
print("O maior número é:", max(lista))


# ------------------------------------------------------------
# DESAFIO 7
# ENUNCIADO:
#   Remover duplicados de uma lista.
#
# PASSO A PASSO:
#   1. Converter lista para set()
#   2. Voltar para lista
# ------------------------------------------------------------
lista = [1, 2, 2, 3, 4, 4, 5]
lista_sem_duplicados = list(set(lista))
print(lista_sem_duplicados)


# ------------------------------------------------------------
# DESAFIO 8
# ENUNCIADO:
#   Converter sequência numérica em texto.
#   Exemplo: 3421 → "três quatro dois um"
#
# PASSO A PASSO:
#   1. Criar dicionário de conversão
#   2. Percorrer cada dígito
#   3. Montar frase final
# ------------------------------------------------------------
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



# ============================================================
# ================== SIMULADOR DE PROVA (30) ==================
# ============================================================

# ------------------------------------------------------------
# QUESTÃO 1
# ENUNCIADO:
#   Criar função que retorna o triplo de um número.
#
# PASSO A PASSO:
#   1. Criar função triplo()
#   2. Retornar n * 3
# ------------------------------------------------------------
def triplo(n):
    return n * 3

print(triplo(4))


# ------------------------------------------------------------
# QUESTÃO 2
# ENUNCIADO:
#   Verificar se número é múltiplo de 5.
# ------------------------------------------------------------
n = int(input("Número: "))
if n % 5 == 0:
    print("É múltiplo de 5")
else:
    print("Não é múltiplo de 5")


# ------------------------------------------------------------
# QUESTÃO 3
# ENUNCIADO:
#   Contar quantas letras "a" existem numa frase.
# ------------------------------------------------------------
frase = input("Frase: ").lower()
print("Quantidade de 'a':", frase.count("a"))


# ------------------------------------------------------------
# QUESTÃO 4
# ENUNCIADO:
#   Criar lista com números pares até 50.
# ------------------------------------------------------------
pares = [i for i in range(0, 51, 2)]
print(pares)


# ------------------------------------------------------------
# QUESTÃO 5
# ENUNCIADO:
#   Função que retorna o maior de 4 números.
# ------------------------------------------------------------
def maior(a, b, c, d):
    return max(a, b, c, d)

print(maior(3, 10, 7, 2))


# ------------------------------------------------------------
# QUESTÃO 6
# ENUNCIADO:
#   Validar email contendo "@" e ".".
# ------------------------------------------------------------
email = input("Email: ")

if "@" in email and "." in email:
    print("Email válido")
else:
    print("Email inválido")


# ------------------------------------------------------------
# QUESTÃO 7
# ENUNCIADO:
#   Somar apenas números negativos de uma lista.
# ------------------------------------------------------------
lista = [-3, 5, -1, 7, -10]
soma = sum([n for n in lista if n < 0])
print(soma)


# ------------------------------------------------------------
# QUESTÃO 8
# ENUNCIADO:
#   Função que conta quantos pares existem numa lista.
# ------------------------------------------------------------
def contar_pares(lista):
    return len([n for n in lista if n % 2 == 0])

print(contar_pares([1, 2, 3, 4, 6, 7]))


# ------------------------------------------------------------
# QUESTÃO 9
# ENUNCIADO:
#   Gerar 10 números aleatórios e guardar numa lista.
# ------------------------------------------------------------
lista = []
for i in range(10):
    lista.append(random.randint(1, 100))

print(lista)


# ------------------------------------------------------------
# QUESTÃO 10
# ENUNCIADO:
#   Verificar se palavra é palíndromo.
# ------------------------------------------------------------
palavra = input("Palavra: ").lower()

if palavra == palavra[::-1]:
    print("É palíndromo")
else:
    print("Não é palíndromo")


# ------------------------------------------------------------
# QUESTÃO 11
# ENUNCIADO:
#   Função que recebe nome e idade e retorna frase formatada.
# ------------------------------------------------------------
def apresentar(nome, idade):
    return f"{nome} tem {idade} anos."

print(apresentar("Lucas", 22))


# ------------------------------------------------------------
# QUESTÃO 12
# ENUNCIADO:
#   Remover todos os zeros de uma lista.
# ------------------------------------------------------------
lista = [0, 3, 0, 5, 7, 0, 9]
lista = [n for n in lista if n != 0]
print(lista)


# ------------------------------------------------------------
# QUESTÃO 13
# ENUNCIADO:
#   Criar lista com quadrados de 1 a 10.
# ------------------------------------------------------------
quadrados = [i*i for i in range(1, 11)]
print(quadrados)


# ------------------------------------------------------------
# QUESTÃO 14
# ENUNCIADO:
#   Função que retorna quantas palavras existem numa frase.
# ------------------------------------------------------------
def contar_palavras(frase):
    return len(frase.split())

print(contar_palavras("Python é muito fixe"))


# ------------------------------------------------------------
# QUESTÃO 15
# ENUNCIADO:
#   Criar menu simples com while.
# ------------------------------------------------------------
op = ""

while op != "3":
    print("1 - Olá")
    print("2 - Adeus")
    print("3 - Sair")
    op = input("Opção: ")

    if op == "1":
        print("Olá!")
    elif op == "2":
        print("Adeus!")


# ------------------------------------------------------------
# QUESTÃO 16
# ENUNCIADO:
#   Converter lista de strings para maiúsculas.
# ------------------------------------------------------------
lista = ["python", "curso", "prova"]
lista = [palavra.upper() for palavra in lista]
print(lista)


# ------------------------------------------------------------
# QUESTÃO 17
# ENUNCIADO:
#   Função que soma todos os números de uma lista.
# ------------------------------------------------------------
def soma_lista(lista):
    return sum(lista)

print(soma_lista([3, 5, 7]))


# ------------------------------------------------------------
# QUESTÃO 18
# ENUNCIADO:
#   Verificar se número está entre 100 e 200.
# ------------------------------------------------------------
n = int(input("Número: "))

if 100 <= n <= 200:
    print("Está no intervalo")
else:
    print("Fora do intervalo")


# ------------------------------------------------------------
# QUESTÃO 19
# ENUNCIADO:
#   Criar lista com números ímpares até 30.
# ------------------------------------------------------------
impares = [i for i in range(1, 31, 2)]
print(impares)


# ------------------------------------------------------------
# QUESTÃO 20
# ENUNCIADO:
#   Função que retorna apenas números maiores que 50.
# ------------------------------------------------------------
def maiores_50(lista):
    return [n for n in lista if n > 50]

print(maiores_50([10, 60, 80, 30]))


# ------------------------------------------------------------
# QUESTÃO 21
# ENUNCIADO:
#   Criar dicionário com nome e idade.
# ------------------------------------------------------------
pessoa = {"nome": "Lucas", "idade": 22}
print(pessoa["nome"], pessoa["idade"])


# ------------------------------------------------------------
# QUESTÃO 22
# ENUNCIADO:
#   Somar apenas números pares de 1 a 100.
# ------------------------------------------------------------
soma = sum([i for i in range(1, 101) if i % 2 == 0])
print(soma)


# ------------------------------------------------------------
# QUESTÃO 23
# ENUNCIADO:
#   Função que retorna o menor número de uma lista.
# ------------------------------------------------------------
def menor(lista):
    return min(lista)

print(menor([5, 2, 9, 1]))


# ------------------------------------------------------------
# QUESTÃO 24
# ENUNCIADO:
#   Ordenar lista de nomes alfabeticamente.
# ------------------------------------------------------------
nomes = ["Carlos", "Ana", "Eduardo", "Beatriz", "Diana"]
nomes.sort()
print(nomes)


# ------------------------------------------------------------
# QUESTÃO 25
# ENUNCIADO:
#   Verificar se frase contém números.
# ------------------------------------------------------------
frase = input("Frase: ")

if any(char.isdigit() for char in frase):
    print("Contém números")
else:
    print("Não contém números")


# ------------------------------------------------------------
# QUESTÃO 26
# ENUNCIADO:
#   Função que calcula o fatorial de um número.
# ------------------------------------------------------------
def fatorial(n):
    resultado = 1
    for i in range(1, n+1):
        resultado *= i
    return resultado

print(fatorial(5))


# ------------------------------------------------------------
# QUESTÃO 27
# ENUNCIADO:
#   Criar matriz 3x3.
# ------------------------------------------------------------
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matriz)


# ------------------------------------------------------------
# QUESTÃO 28
# ENUNCIADO:
#   Somar todos os elementos da matriz.
# ------------------------------------------------------------
soma = 0
for linha in matriz:
    soma += sum(linha)

print(soma)


# ------------------------------------------------------------
# QUESTÃO 29
# ENUNCIADO:
#   Função que retorna apenas consoantes de uma palavra.
# ------------------------------------------------------------
def consoantes(palavra):
    vogais = "aeiou"
    return "".join([l for l in palavra.lower() if l not in vogais])

print(consoantes("Python"))


# ------------------------------------------------------------
# QUESTÃO 30
# ENUNCIADO:
#   Contar quantos números repetidos existem numa lista.
# ------------------------------------------------------------
def contar_repetidos(lista):
    repetidos = 0
    for n in set(lista):
        if lista.count(n) > 1:
            repetidos += 1
    return repetidos

print(contar_repetidos([1, 2, 2, 3, 3, 3]))


# ============================================================
# ======================== FIM DO ARQUIVO =====================
# ============================================================