
################### fim do dicionário 'dados' #######################

dados = {  # cria o dicionário principal 'dados'
    'Joao': {                 # chave 'Joao' -> dicionário com idade e cidade
        'idade': 25,          # idade do Joao (int)
        'cidade': 'Lisboa'    # cidade do Joao (string)
    },  # fim da entrada Joao
    'Maria': {                # chave 'Maria' -> dicionário com idade e cidade
        'idade': 30,          # idade da Maria (int)
        'cidade': 'Porto'     # cidade da Maria (string)
    },  # fim da entrada Maria
    'Ana': {                  # chave 'Ana' -> dicionário com idade e cidade
        'idade': 22,          # idade da Ana (int)
        'cidade': 'Coimbra'   # cidade da Ana (string)
    },  # fim da entrada Ana
}  # fim do dicionário 'dados'  # dicionário pronto com 3 entradas

print(dados)  # imprime o dicionário completo 'dados'

print('\n') 

print(dados['Joao'])  # imprime o dicionário associado à chave 'Joao' (idade e cidade)
print('\n') 

print(dados['Ana']['idade'])  # imprime apenas a idade da 'Ana' acessando o dicionário interno
print('\n') 

cidade_Maria = dados['Maria']['cidade']  # obtém a cidade da 'Maria' e guarda em 'cidade_Maria'
print(cidade_Maria)  # imprime o valor de 'cidade_Maria'
print('\n')  

idade_Ana = dados['Ana']['idade']  # obtém a idade da 'Ana' e guarda em 'idade_Ana'
print(idade_Ana)  # imprime o valor de 'idade_Ana'
print('\n')  

print('A idade da Ana é ', idade_Ana)  # imprime uma frase concatenando texto e o valor de 'idade_Ana'
print('\n')  

if 'idade' in dados['Ana']:  # verifica se a chave 'idade' existe no dicionário de 'Ana'
    print('A idade da Ana é ', idade_Ana)  # se existir, imprime a idade da Ana
    print('')  
else:
    print('A idade da Ana não esta disponivel.')  # se não existir, avisa que não está disponível
    print('')  
    
if 'Pedro' in dados and dados['Pedro']:  # verifica se 'Pedro' é chave em 'dados' e se o valor não é vazio/False
    print('A idade do Pedro é ',dados['Pedro']['idade']['cidade'])  # tenta acessar informação aninhada de 'Pedro' (pode causar erro se estrutura diferente)
    print('')  
else:
    print('Dados do Pedro nao estao disponivel')  # informa que os dados de 'Pedro' não estão disponíveis
    print('')  
    
    for nome, informacoes in dados.items():     # itera sobre pares (nome, informacoes) no dicionário 'dados'
        idade = informacoes.get('idade', 'N/A')  # obtém 'idade' com valor padrão 'N/A' se não existir
        cidade = informacoes.get('cidade', 'N/A')  # obtém 'cidade' com valor padrão 'N/A' se não existir
        if idade and cidade and nome is not None:  # verifica se existem valores válidos antes de imprimir
            print(f"{nome}: idade = {idade}, cidade = {cidade}")  # imprime nome, idade e cidade formatados
print('\n')

for nome in dados:
    print(nome)
print('\n')

for nome in dados.keys(): #Mais segura para mostrar as chaves da lista
    print(nome)
print('\n')

nome = 'Maria'
if nome in dados:   
    for chave, valor in dados[nome].items():     # itera sobre pares (nome, informacoes) no dicionário 'dados'
        chave = dados[nome].get('idade', 'N/A')  # obtém 'idade' com valor padrão 'N/A' se não existir
        valor = dados[nome].get('cidade', 'N/A') # obtém 'cidade' com valor padrão 'N/A' se não existir
        if idade and cidade and nome is not None:  # verifica se existem valores válidos antes de imprimir
            print(f"{nome}: idade = {chave}, cidade = {valor}")
            break
print('')

if nome in dados:
    print(f'Informação do nome {nome}')
    for chave,valor in dados[nome].items():
        print(f'{chave}:{valor}')
else:
    print(f'{nome} não encontrado no dicionario')
print('')

if nome in dados:
    print(f'Informação do nome {nome}')
    idade = dados[nome].get('idade', 'Idade nao encontrada')
    print(f'A idade de {nome} :{idade}')
else:
    print(f'{nome} não encontrado no dicionario')
print('')


#Transformar dicionario em listas 
#Converter o dicionario em uma lista

chave = list(dados.keys())
print(chave)
print('')

if len(chave) > 2:
    chave_posicao_2 = chave[2]                  #Acender a terceira posicao
    dados_chave = dados[chave[2]]        #Acender o valor associado a essa chave
  
# Mostrar a chave e os dados correspondentes
    print(f'Chave na terceira posicao da lista: {chave_posicao_2}')
    print(f'Dados: ',dados_chave)
else:
    print('Nao ha dados na chave no dicionário')
print('')

