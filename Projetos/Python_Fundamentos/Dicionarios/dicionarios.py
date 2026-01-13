##########Utilizamos chavetas###############

# chave : valor
aluno = {'nome':'Joana','idade':17, 'notas':{9,8,10}, 'inscrito':True}
print(aluno['nome'])
#print(aluno[ano])

print(aluno.get('nome')) # me da o que esta na chave
print(aluno.get('ano'))  # me da o valor nome que signifca que nao tem nada
print(aluno.get('ano',9)) # atribui o valor 9 e mostra ele na tela

aluno['ano'] = 2025.      #cria ano 
print(aluno.get('ano'))   #mostra na lista a chave ano como 2025


aluno ['idade'] = 18          #altera o valor da chave idade
print(aluno.get('idade'))     #mostra o valor alterado da chave idade
print(aluno)                  #mostra o dicionario completo
print(' ')

if aluno.get('inscrito'):    #verifica se o aluno esta inscrito
    print('O aluno está inscrito')   #mostra que o aluno esta inscrito
else:
    print('O aluno não está inscrito') #mostra que o aluno nao esta inscrito
print(' ')

if aluno.get('nota'):       #verifica se o aluno tem nota
    print('O aluno tem nota')      #mostra que o aluno tem nota
else:
    print('O aluno não tem nota')   #mostra que o aluno nao tem nota
print(' ')

if 'notas' in aluno:        #verifica se a chave notas esta no dicionario
    print('A chave notas existe no dicionario') #mostra que a chave notas existe
else:
    print('A chave notas não existe no dicionario') #mostra que a chave notas nao existe
print(' ')

#Calcular a media das notas
media = sum(aluno['notas']) / len(aluno['notas'])  #calcula a media das notas
print(f'A media do aluno é: {media}')  #mostra a media do aluno
print(' ')

if media >= 9:                      #se a media for maior ou igual a 9
    print('Aluno aprovado')         #mostra que o aluno esta aprovado
else:
    print('Aluno reprovado')        #mostra que o aluno esta reprovado

#remover itens do dicionario   
del aluno['inscrito']        #remove a chave inscrito
print(aluno)                 #mostra o dicionario sem a chave inscrito
print(' ')

#Dicionarios aninhados
dados = {aluno['nome']: aluno,  #adiciona o dicionario aluno dentro do dicionario dados
         'Pedro': {'nome':'Pedro','idade':19,'notas':{7,8,6},'inscrito':False},
         'Ana': {'nome':'Ana','idade':18,'notas':{10,9,8},'inscrito':True}
        }
print(dados)                  #mostra o dicionario dados completo
print(' ')

#Aceder a dados em dicionarios aninhados
print(dados['Joana'])         #mostra o dicionario da Joana dentro do dicionario dados
print(' ')
print(dados['Pedro']['notas']) #mostra as notas do Pedro
print(' ')
print(dados['Ana']['inscrito']) #mostra se a Ana esta inscrita
print(' ')