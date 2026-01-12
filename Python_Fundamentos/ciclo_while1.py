##################### Ciclo While em Python #####################

import random

# Estrutura do while em Python
'''
while condição:
    # bloco de código a ser executado enquanto a condição for verdadeira
    instruções1
    instruções2
    instruções3
    break  # opcional, para sair do loop
else:
    # bloco de código a ser executado quando a condição for falsa
    instruções4
instruções5
'''
#ciclo infinito
'''
n = 1
while n <= 5:
    print("Número:", n)
print("Fim do loop while.")
'''

# Exemplo básico de uso do while
n = 1
while n <= 5:
    print("Número:", n)
    n += 1 # Incrementa n em 1 a cada iteração
    if n == 4:
        break  # Sai do loop quando n é igual a 3
else: # Este bloco não será executado devido ao break
        print("Fim do loop while.")
print("Loop while encerrado.")

####################### Desafios com While #######################

# Desafio: Jogo de adivinhação

'''Jogo de adivinhação onde o usuário tenta adivinhar o número 
   Gerado aleatoriamente entre 1 e 6. 
   Dar ao utilizador 3 tentativas para adivinhar o número.
   Dar dicas se o palpite é muito alto ou muito baixo.
   Dar os parabéns se o utilizador adivinhar corretamente.'''

valor = random.randint(1,10)
numero_tentativas = 0  # Número máximo de tentativas
while numero_tentativas < 3:  # Enquanto o número de tentativas for menor que 3
    palpite = int(input("Adivinhe o número entre 1 e 10: "))  # Pede ao usuário para adivinhar o número
    if palpite == valor: 
        print("Parabéns! Você adivinhou o número corretamente.")
        break  # Sai do loop se o usuário adivinhar corretamente
    else:  
        numero_tentativas += 1  # Incrementa o número de tentativas restantes
        print("Você tem", numero_tentativas, "tentativas restantes.")
print('Fim de Jogo!!! Jogue denovo se quiser.\n')

####################### Soluções dos Desafios #######################


#desafio 1
contador = 1                     #inicializa o contador
while contador <= 5:             #enquanto o contador for menor ou igual a 5
    print("Contador é:", contador)  #mostra o valor do contador
    contador += 1                  #incrementa o contador em 1
print("Fim do contador\n")

#desafio 2
soma = 0                         #inicializa a soma
numero = 1                       #inicializa o numero
while numero <= 10:              #enquanto o numero for menor ou igual a 10
    soma += numero               #adiciona o numero a soma
    numero += 1                  #incrementa o numero em 1
print("A soma dos numeros de 1 a 10 é:", soma)  #mostra a soma dos numeros de 1 a 10

#desafio 3
n = int(input("Digite um numero para calcular o fatorial: "))  #pega
# o numero digitado pelo usuario
fatorial = 1                     #inicializa o fatorial
contador = 1                     #inicializa o contador
while contador <= n:             #enquanto o contador for menor ou igual a n
    fatorial *= contador         #multiplica o fatorial pelo contador
    contador += 1                #incrementa o contador em 1
print("O fatorial de", n, "é:", fatorial)  #mostra o fatorial de n

#desafio 4
senha_correta = "python123"      #define a senha correta
senha_digitada = ""              #inicializa a senha digitada
while senha_digitada != senha_correta:  #enquanto a senha digitada for
    senha_digitada = input("Digite a senha: ")  #pega a senha digitada pelo usuario
print("Senha correta! Acesso permitido.")  #mostra a mensagem de acesso permitido





