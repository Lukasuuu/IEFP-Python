def soma_lista(lista): # função para somar os elementos de uma lista
    soma = 0
    for num in lista:  #itera sobre cada número na lista
        soma += num    # adiciona o número à soma total
    return soma        # devolve a soma total

numeros = [3,7, 2, 9, 10]        # lista de números
resultado = soma_lista(numeros)  # chama a função e armazena o resultado

print(f'A soma dos numeros da lista é: {resultado}') # imprime o resultado da soma

lista = ['joana',' maria', 'pedro']
print(f'O primeiro nome da lista é: {lista[0]}') # imprime o primeiro nome da lista
print(f'O segundo nome da lista é: {lista[1]}') # imprime o segundo nome da lista
print(f'O terceiro nome da lista é: {lista[2]}') # imprime o terceiro nome da lista

print(' ')

print('tamanho da lista de numeros é:', len(numeros)) # imprime o tamanho da lista de números
print('tamanho da lista de nomes é:', len(lista))     # imprime o tamanho da lista de nomes 
print(' ')  

# Adicionar elementos a lista
numeros.append(15)  # adiciona o número 15 à lista de números
print('Lista de numeros apos adicionar o 15:', numeros) # imprime a lista de números após adicionar o 15
lista.append('carlos') # adiciona o nome 'carlos' à lista de nomes
print('Lista de nomes apos adicionar carlos:', lista) # imprime a lista de nomes após adicionar 'carlos'
print(' ')

# Remover elementos da lista
numeros.remove(2)  # remove o número 2 da lista de números
print('Lista de numeros apos remover o 2:', numeros) # imprime a lista de números após remover o 2
lista.remove(' maria') # remove o nome ' maria' da lista de nomes
print('Lista de nomes apos remover maria:', lista) # imprime a lista de nomes após remover ' maria'
print(' ')

# Acessar elementos da lista

print('Primeiro numero da lista de numeros:', numeros[0]) # imprime o primeiro número da lista de números
print('Segundo numero da lista de numeros:', numeros[1]) # imprime o segundo número da lista de números
print('Primeiro nome da lista de nomes:', lista[0]) # imprime o primeiro nome da lista de nomes
print('Segundo nome da lista de nomes:', lista[1]) # imprime o segundo nome da lista de nomes
print(' ')

# Iterar sobre a lista
print('Iterando sobre a lista de numeros:')
for num in numeros:  # itera sobre cada número na lista de números
    print(num)       # imprime o número atual
print(' ')

print('Iterando sobre a lista de nomes:')
for nome in lista:  # itera sobre cada nome na lista de nomes
    print(nome)     # imprime o nome atual
print(' ')

# Verificar se um elemento está na lista
if 9 in numeros:  # verifica se o número 9 está na lista de números
    print('O numero 9 está na lista de numeros') # imprime se o número 9 está na lista
else:
    print('O numero 9 nao está na lista de numeros') # imprime se o número 9 não está na lista


if 'pedro' in lista:  # verifica se o nome 'pedro' está na lista de nomes
    print('O nome pedro está na lista de nomes') # imprime se o nome 'pedro' está na lista
else:
    print('O nome pedro nao está na lista de nomes') # imprime se o nome 'pedro' não está na lista
print(' ')
