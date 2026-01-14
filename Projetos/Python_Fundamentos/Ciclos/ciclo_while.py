import random

'''
while condição:
    instrução1
    instrução2
    instrução3
    break
else:
    instrução5
instrução4
'''
#ciclo infinito
'''
n = 1
while n <= 5:
    print(n)
print('Fim do programa')
'''
n = 1
while n <= 5: # 
    print(n)
    n += 1
    if n == 4:
        break # quando o if for verdadeiro, vai parar o programa e vai para o ultimo print
else:
    print('Fim de ciclo')
print('Fim do programa')

valor = random.randint(1, 10)
print(valor)

# Desafio 5
'''
Colocar o computador a gerar um numero aleatório entre 1 e 6.
Pedir ao utilizador para tentar adivinhar o número.
Dar ao utilizador 3 tentativas para conseguir.
Dar os prabéns caso acerte, caso contrário, desejar boa sorte para a proxima.
'''
import random

numero_aleatorio = random.randint(1,6)
tentativas = 3
while tentativas > 0:
    palpite = int(input('Adivinhe o número entre 1 e 6: '))
    if palpite == numero_aleatorio:
        print('Parabéns! Você acertou!')
        break
    else:
        tentativas -= 1
        print(f'Errado! Você tem {tentativas} tentativas restantes.')
        if tentativas == 0:
            print(f'Boa sorte na próxima! O número era {numero_aleatorio}.')
print('Fim do programa')
print(' ')

#ciclo while com else

contador = 1
while contador <= 5:
    print(contador)
    contador += 1
else:
    print('Fim do ciclo while')
print(' ')

#ciclo while com continue
contador = 0
while contador < 5:
    contador += 1
    if contador == 3:
        continue
    print(contador) 
print('Fim do ciclo while')
print(' ')

#ciclo while com break
contador = 0
while contador < 5:
    contador += 1
    if contador == 3:
        break
    print(contador)
print('Fim do ciclo while')
print(' ')

#ciclo while com pass
contador = 0
while contador < 5:
    contador += 1
    if contador == 3:
        pass
    print(contador)
print('Fim do ciclo while')
print(' ')
