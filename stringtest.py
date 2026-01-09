nome = "Filipa"
apelido = 'Silva'
idade = 17
altura = 1.65

# Quero a frase "Filipa Silva tem 17 anos e 1.65 de altura"
frase = f"{nome} {apelido} tem {idade} anos e {altura} de altura"
print(frase)

# Quero a frase "Filipa Silva nasceu em 2006"
ano_atual = 2024
ano_nascimento = ano_atual - idade
frase_nascimento = f"{nome} {apelido} nasceu em {ano_nascimento}"
print(frase_nascimento)

# Quero a frase "O nome completo de Filipa Silva tem 12 caracteres"
nome_completo = f"{nome} {apelido}"
num_caracteres = len(nome_completo)
frase_caracteres = f"O nome completo de {nome_completo} tem {num_caracteres} caracteres"
print(frase_caracteres) 

# Quero a frase "A altura de Filipa Silva em centímetros é 165 cm"
altura_cm = altura * 100
frase_altura_cm = f"A altura de {nome_completo} em centímetros é {altura_cm:.0f} cm"
print(frase_altura_cm)

# Quero a frase "Filipa Silva tem 17 anos, o que é maior de idade."
maior_idade = "maior de idade" if idade >= 18 else "menor de idade"
frase_maior_idade = f"{nome_completo} tem {idade} anos, o que é {maior_idade}."
print(frase_maior_idade)

nome_digitado = input("Digite seu nome: ")      #pega o nome digitado pelo usuario
