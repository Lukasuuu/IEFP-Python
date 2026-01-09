##########Utilizamos chavetas###############

# chave : valor
aluno = {'nome':'Joana','idade':17,'inscrito':True}
print(aluno['nome'])
#print(aluno[ano])

print(aluno.get('nome')) # me da o que esta na chave
print(aluno.get('ano'))  # me da o valor nome que signifca que nao tem nada
print(aluno.get('ano',9)) # atribui o valor 9 e mostra ele na tela

aluno['ano'] = 2025.      #cria ano 
print(aluno.get('ano'))   #mostra na lista a chave ano como 2025