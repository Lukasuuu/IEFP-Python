"""
UF23-10793 - FUNDAMENTOS DE PYTHON
Guia de Consulta para Teste (IEFP Braga)
"""
import json  # Importação necessária para manipular JSON
import random

# =============================================================================
# 1. LISTAS, TUPLAS E MATRIZES
# =============================================================================

# LISTAS (Mutáveis)
nomes = ['Marcos', 'Joana', 'Pedro']
nomes[2] = 'Maria'        # Alterar elemento
print(nomes[0])          # Primeiro elemento
print(nomes[-1])         # Último elemento
print(nomes[1:3])        # Slicing (do índice 1 ao 2)

# MÉTODOS DE LISTAS
numeros = [1, 3, 5, 4, 9, 7]
numeros.append(9)        # Adiciona ao fim
numeros.insert(0, 6)     # Adiciona no índice 0
n_copia = numeros.copy() # Copia a lista
numeros.sort()           # Ordena crescente
numeros.reverse()        # Inverte a ordem
print(numeros.count(9))  # Conta quantas vezes aparece o 9
print(numeros.index(9))  # Posição da primeira ocorrência de 9
print(8 in numeros)      # Verifica se existe (True/False)

# TUPLAS (Imutáveis - Não podem ser alteradas após criadas)
num_tupla = (1, 2, 3)    # Usa parênteses

# MATRIZES (Listas Bidimensionais)
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matriz[1][0])      # Acede ao número 4 (Linha 1, Coluna 0)

# =============================================================================
# 2. DICIONÁRIOS (Chave: Valor)
# =============================================================================

aluno = {'nome': 'Joana', 'idade': 17, 'inscrito': True} #

# Aceder a dados
print(aluno['nome']) #
print(aluno.get('ano', 'Não existe')) # .get evita erro se a chave não existir

# Adicionar/Atualizar
aluno['ano'] = 2025 #

# Dicionários Aninhados (Nested)
dados = {
    'Joao': {'idade': 25, 'cidade': 'Lisboa'},
    'Maria': {'idade': 30, 'cidade': 'Porto'}
}
print(dados['Maria']['idade']) # Acede à idade da Maria

# Iterar em Dicionários
for nome, info in dados.items():
    print(f"{nome} vive em {info.get('cidade')}")

# Converter chaves para lista
chaves_lista = list(dados.keys())

# =============================================================================
# 3. CONTROLO DE FLUXO (IF, WHILE, FOR)
# =============================================================================

# IF / ELIF / ELSE e Operadores Lógicos (and, or, not, ==, !=, <, >)
nota = int(input('Qual foi a tua nota? ')) #
if nota < 50:
    print('Insuficiente') #
elif 50 <= nota < 70:
    print('Suficiente') #
else:
    print('Bom/Muito Bom') #

# CICLO WHILE (Executa enquanto a condição for verdadeira)
tentativas = 0
while tentativas < 3:
    tentativas += 1
    if tentativas == 2: break # Interrompe o ciclo

# CICLO FOR
for i in range(5):          # 0 a 4
    print(i)

for i in range(2, 10, 2):   # De 2 a 9, de 2 em 2
    print(i)

# Desafio Comum: Remover duplicados de uma lista
lista_dups = [1, 2, 2, 3, 4, 4]
sem_dups = []
for n in lista_dups:
    if n not in sem_dups:
        sem_dups.append(n) #

# =============================================================================
# 4. JSON (CONVERSÃO E FICHEIROS)
# =============================================================================

# A) Converter Dicionário para String JSON (Serialization)
pessoa_dict = {"nome": "Carlos", "idade": 30, "cidade": "Braga"}
json_string = json.dumps(pessoa_dict, indent=4, ensure_ascii=False)

# B) Converter String JSON para Dicionário (Deserialization)
dicionario_lido = json.loads(json_string)

# C) Gravar Ficheiro JSON
with open('dados.json', 'w', encoding='utf-8') as f:
    json.dump(pessoa_dict, f, indent=4)

# D) Ler Ficheiro JSON
# with open('dados.json', 'r', encoding='utf-8') as f:
#     dados_do_ficheiro = json.load(f)

# =============================================================================
# 5. FUNÇÕES
# =============================================================================

# Função simples
def about():
    print('Autor: Carlos Fontes') #

# Função com múltiplos argumentos e return
def cubo(n1, n2):
    return n1 ** 3, n2 ** 3 #

# Função para encontrar o maior número
def maior(n1, n2):
    return n1 if n1 > n2 else n2 #

# =============================================================================
# 6. DICAS ÚTEIS
# =============================================================================
# input() sempre retorna STRING. Usa int() ou float() para converter.
# len(variavel) serve para ver tamanho de strings ou listas.
# random.randint(1, 10) gera número aleatório.