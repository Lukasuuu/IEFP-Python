for letras in 'Marcos':
    print(letras)

nomes = ['Marcos', 'Joana', 'Pedro', 'Paulo' , 'Ana' , 'Rita']

for i in nomes:
   
    print(i)
    print('-'*5)

numeros = [4,6,8,1,3]
for num in numeros:
    print(num)
print(' ')

for numeros in '1345':
    print(numeros)
print(' ')

for i in range(5):
    print(i)
print(' ')

for i in range (1,5):
    print(num)
print(' ')

for num in range (2,10,2):
    print(num)
print(' ')

'''
Dada uma lista de numeros, pesquise e mocstre qual deles e o maior

numeros = [5,3,7,19,1,3,4,12,6,7]

'''

numeros = [5,3,7,19,1,3,4,12,6,7]
maior = numeros[0] # compara o maior sendo o primeiro da listagem

for num in numeros:
    if num > maior: #se o numero do meu ciclo for maior que o "maior"
        maior = num #entao o maior toma o valor do numero
print(f'o maior é: {maior}')

maior = max(numeros)            #Outra forma de fazer o maior
print(f'O maior é: {maior}')
