from pickletools import string1


nome=input("Digite seu nome: ") #pega o nome digitado pelo usuario
print("Nome digitado:", nome)   #mostra o nome digitado
cor= input("Digite sua cor favorita: ") #pega a cor favorita digitada pelo usuario
print("Cor favorita digitada:", cor)   #mostra a cor favorita digitada


concat = nome + " gosta da cor " + cor + "."  #concatena o nome e a cor favorita
print(concat)  #mostra a concatenacao


print(nome=="Lucas") # Verifica se o nome digitado é igual a "Lucas" por uma boolean

fstring = f"{nome} gosta da cor {cor}."  #cria uma f-string com o nome e a cor favorita
print(fstring)  #mostra a f-string

print(f'{nome} gosta da cor {cor}.')  #mostra a f-string diretamente no print

'Pedir ao utilizador para digitar o ano de nascimento '
' a saida calcular a idade atual e mostrar:'
'Qual a sua idade? '
'Sua idade é: X anos.'

anoNascimento = int(input("Digite seu ano de nascimento: "))  #pega o ano de nascimento digitado pelo usuario
anoAtual = 2025                             #ano atual

idade = anoAtual - anoNascimento            #calcula a idade
print(f'Sua idade é: {idade} anos.')        #mostra a idade
print('Sua idade é:', idade)                #mostra a idade calculada
print('Sua idade é: ' + str(idade))          #mostra a idade calculada diretamente

print('ano de nascimento:', anoNascimento)  #mostra o ano de nascimento
print('ano atual:', anoAtual)               #mostra o ano atual










print('Nome em minusculas:',nome.lower())  #mostra o nome em letras minusculas
print('Nome em maiusculas:',nome.upper())  #mostra o nome em letras maiusculas
print('primeira letra da cada palavra Maiuscula:',nome.title())  #mostra o nome com a primeira letra de cada palavra em maiuscula
print('quantas letra tem:', len(nome))     #mostra a quantidade de letras do nome
print('primeira letra do nome:',nome[0])      #mostra a primeira letra do nome
print('ultima letra do nome:', nome[-1])     #mostra a ultima letra do nome
print("usa a letra 'a' no nome?", 'a' in nome)  #verifica se a letra 'a' esta no nome
print("usa a letra 'z' no nome?", 'z' in nome)  #verifica se a letra 'z' esta no nome
print(nome.strip())  #mostra o nome sem espacos no inicio e no fim
print(nome.replace('a', '@'))  #mostra o nome substituindo 'a' por '@'