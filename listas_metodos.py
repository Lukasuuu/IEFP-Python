numeros = [1,3,5,4,9,7]

numeros.append(9) #acrescenta o 9 ao final da lista
print(numeros)

numeros.insert(0,6) #acrescenta o 6 na posicao 0
print(numeros)

n2 = numeros.copy() # vai fazer uma copia da lista pra variavel n2
print(n2)

n2.append(8) # acrescenta o 8 ao final da lista de n2
print(n2)

numeros.sort() #ordena a lista por ordem crescente
print(numeros,n2)

numeros.reverse() #ordena a lista por ordem descendente
print(numeros)

print(numeros.count(9)) #Quantas vezes aparece o numero 9 na lista

print(numeros.index(9)) #Mostra a posicao em que esta o primeiro 9 da lista

#print(numeros.pop())   #Vai retirar o ultimo elemento da lista

encontrar = 8 in numeros
print(encontrar)          # verifica se o 8 esta na lista e devolve boolean

encontrar = 4 in numeros
print(encontrar)          # verifica se o 8 esta na lista e devolve boolean

