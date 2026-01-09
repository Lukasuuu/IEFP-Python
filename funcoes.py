# Função About mostra tudo que esta dentro dele
'''
    def about():
    print('Bem-vindos ao Programa de Funções')
    print('=' * 83)
    print('Autor: Lucas Goncalves')
    print('versão: 1.03')
    print('=' * 83)
    
    print('')
    about()
    print('')
'''

# Função About mostra tudo que esta dentro dele com argumentos
'''

    def about(autor,versao, weather):
    print('Bem-vindos ao Programa de Funções')
    print('=' * 83)
    print('Autor:', autor)
    print('versão:', versao)
    print('=' * 83)

    print('')
    about('Gabriel',' 1.05')
    print('')

'''

#Funcao de Return ao Cubo de um numero
'''o cubo de qualquer numero'''
print('')
numero = int(input('numero: '))  
print('')
def cubo1(numero):
    return numero ** 3

print(f'o valor é {cubo1(numero)}')
print('')


#Funcao de Return ao Cubo de tres argumentos
def cubo(num1,num2,num3):
   return num1 ** 3,num2 ** 3,num3 ** 3
numero = cubo (2,3,4)

print(numero)
print('')

''' DESAFIO DE FUNCOES'''
# Desafio 9

'''Criar uma função que receba dois numeros e retorne o maior dos dois'''

def maior(n1,n2):
    if n1 > n2:
        return n1
    elif n2 > n1:
        return n2
    else:
        return 'sao iguais 🤟🏼'

n1 = int(input('Me de um numero:''🤔'))
n2 = int(input('Me de um numero:''🤔'))

if n1 != n2:
    print(f'O numero maior é: {maior(n1,n2)}')
else: 
    print(maior(n1,n2))


