idade = 15
altura = 1.75
nome = "Lucas Gabriel"
estudante = True

print("Nome:", nome)                                                                                 #mostra o nome
print("Idade:", idade)                                                                               #mostra a idade
print("Altura:", altura)                                                                             #mostra a altura
print("Tipo de nome:", type(nome))                                                                   #mostra o tipo da variavel
print("Tipo de idade:", type(idade))                                                                 #mostra o tipo da variavel
print("Tipo de altura:", type(altura))                                                               #mostra o tipo da variavel
print("Tipo de estudante:", type(estudante))                                                         #mostra o tipo da variavel

contem1 = 'Lucas' in nome                                                                            #verifica se a string 'Lucas' esta contida na variavel nome
print(contem1)                                                                                       #mostra o resultado da verificacao
contem2 = 'lucas' in nome                                                                            #verifica se a string 'lucas' esta contida na variavel nome
print(contem2)                                                                                       #mostra o resultado da verificacao


print("Nome em maiusculas:", nome.upper())                                                          #mostra o nome em letras maiusculas
print("Nome em minusculas:", nome.lower())                                                          #mostra o nome em letras minusculas
print("Mostra a posicao da primeira ocorrencia da letra 'a':", nome.find('a'))                      #mostra a posicao da primeira ocorrencia da letra 'a' no nome
print("mostrar a posicao das letras:", nome.find('tos'))                                            #mostra a posicao da primeira ocorrencia da string 'tos' no nome
print("Nome com espacos removidos:", nome.strip())                                                  #mostra o nome com os espacos removidos no inicio e no fim
print("Nome com espacos a direita removidos:", nome.rstrip())                                       #mostra o nome com os espacos removidos no fim
print("Nome com espacos a esquerda removidos:", nome.lstrip())                                      #mostra o nome com os espacos removidos no inicio
print("Nome com todas as palavras capitalizadas:", nome.title())                                    #mostra o nome com todas as palavras capitalizadas
print("Nome capitalizado:", nome.capitalize())                                                      #mostra o nome com a primeira letra maiuscula e o resto minusculas

print("Quantidade de letras no nome:", len(nome))                                                   #mostra a quantidade de letras no nome
print("Primeira letra do nome:", nome[0])                                                           #mostra a primeira letra do nome
print("Ultima letra do nome:", nome[-1])                                                            #mostra a ultima letra do nome
print("Idade em 5 anos:", idade + 5)                                                                #mostra a idade mais 5 anos
print("Altura em centimetros:", altura * 100)                                                       #mostra a altura em centimetros
print("Nome formatado: {} tem {} anos e {} metros de altura.".format(nome, idade, altura))          #mostra o nome formatado usando o metodo format
print(f"Nome formatado (f-string): {nome} tem {idade} anos e {altura} metros de altura.")           #mostra o nome formatado usando f-string
print("Verifica se 'Jo' esta no nome:", "Jo" in nome)                                               #verifica se a string 'Jo' esta contida na variavel nome
print("Verifica se 'Maria' esta no nome:", "Maria" in nome)                                         #verifica se a string 'Maria' esta contida na variavel nome
print("Lista de caracteres do nome:", list(nome))                                                   #mostra a lista de caracteres do nome
print("Idade arredondada para cima:", round(idade + 0.7))                                           #mostra a idade arredondada para cima
print("Altura arredondada para baixo:", round(altura - 0.2, 1))                                     #mostra a altura arredondada para baixo com 1 casa decimal
print("Idade como string:", str(idade))                                                             #mostra a idade convertida para string
print("Altura como string:", str(altura))                                                           #mostra a altura convertida para string
print("Concatenacao de nome e idade:", nome + " tem " + str(idade) + " anos.")                      #mostra a concatenacao do nome e idade