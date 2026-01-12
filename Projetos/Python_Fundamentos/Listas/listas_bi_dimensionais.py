print(' ')
matriz = [[1,2,3],
          [4,5,6],
          [7,8,9]]

print(matriz) # mostra toda a matriz
print(matriz[0]) #mostra so o primeiro indice da matriz
print(matriz[1]) #mostra so o segundo indice da matriz
print(matriz[2]) #mostra so o terceiro indice da matriz
print(' ')

print(matriz[1][0])     
print(' ')              #Mostra o primeiro elemento do meu segundo indice

for j in range(3):
    for k in range(3):
        print(matriz[j][k])
print(' ')              #Mostra os elementos do indice em sequencia

for linha in matriz:
    for num in linha:
        print(num)
print(' ')              #Mostra os elementos do indice em sequencia tipo Python