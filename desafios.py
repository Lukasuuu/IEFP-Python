numeros=[1,3,9,1,5,4,3,9,7,1]

'''
Desafio 1
Dada a lista a acima
Crie um programa que remova os duplicados
'''

duplicado=[]

for num in numeros:
    if num not in duplicado:
        duplicado.append(num)
print(duplicado)

'''
Desafio 2
Pedir ao utilizador para introduzir uma sequencia de numeros
Dada a lista por exemplo: 3 4 2 1
Converte essa sequencia em texto
Crie por exemplo: tres quatro dois um
'''

lista= {'1':'um','2':'dois','3':'tres','4':'quatro'}

numero = input('Por favor , introduza os numeros')
output = '' # minha variavel de saida

for digito in numero: # a variavel digito percorre uma string
    output = output + ' ' + lista.get(digito) + ' '
print(output)


