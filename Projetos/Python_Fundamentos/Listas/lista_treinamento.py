def soma_lista(lista):
    soma = 0
    for num in lista:
        soma += num
    return soma

numeros = [3,7, 2, 9, 10]
resultado = soma_lista(numeros)

print(f'A soma dos numeros da lista é: {resultado}')