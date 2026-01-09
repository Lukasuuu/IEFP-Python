idade = [10,15,8,9,17]
nome = ["Maria","Joana",'Pedro','Paulo' ,'Ana' ,'Rita']
print(f'\n {nome} \ n')
print(f'\n: {idade} \n') 

print(nome[1])   # Vai buscar a Joana
print(nome[-1])  # Vai buscar a Rita
print(nome[1:3]) # Mostra a Joana e  o Pedro
print(nome[2][0]) #Busca o P do Pedro

nome[2] = 'Maria'
print(nome) #Trocou Pedro por Maria e Repetiu a Maria