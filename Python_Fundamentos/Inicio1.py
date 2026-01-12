def main():
    print("Ola Mundo!!!!!")

if __name__ == "__main__":

    main()


    import math
    a = 15.7

    print(math.ceil(a))                                                                     #arredonda para cima
    print(math.floor(a))                                                                    #arredonda para baixo
    print(math.sqrt(a))                                                                     #raiz quadrada
    print(math.factorial(int(a)))                                                           #fatorial
    print(math.pow(a, 2))                                                                   #potencia
    print(math.pi)                                                                          #valor de pi
    print(math.e)                                                                           #valor de euler
    print(math.log(a))                                                                      #logaritmo natural
    print(math.log10(a))                                                                    #logaritmo base 10
    print(math.sin(a))                                                                      #seno
    print(math.cos(a))                                                                      #cosseno
    print(math.tan(a))                                                                      #tangente
    print(math.hypot(3, 4))                                                                 #hipotenusa
    print(math.degrees(a))                                                                  #converte radianos para graus
    print(math.radians(a))                                                                  #converte graus para radianos
    print(math.gcd(48, 18))                                                                 #maior divisor comum
    print(math.lcm(48, 18))                                                                 #menor multiplo comum
    print(math.isqrt(int(a)))                                                               #raiz quadrada inteira
    print(math.comb(5, 2))                                                                  #combinacoes
    print(math.perm(5, 2))                                                                  #permutacoes
    print(math.dist((1, 2), (4, 6)))                                                        #distancia entre dois pontos
    print(math.prod([1, 2, 3, 4]))                                                          #produto dos elementos
    print(math.fsum([1.1, 2.2, 3.3]))                                                       #soma precisa de elementos flutuantes
    print(math.modf(a))                                                                     #parte fracionaria e inteira
    print(math.copysign(3, -2))                                                             #copia o sinal
    print(math.ulp(a))                                                                      #unidade de menor valor representavel

    import random
    print(random.random())                                                                  #numero aleatorio entre 0 e 1
    print(random.randint(1, 10))                                                            #numero aleatorio entre 1 e 10
    print(random.choice(['apple', 'banana', 'cherry']))                                     #escolha aleatoria
    print(random.sample(range(1, 100), 5))                                                  #amostra aleatoria
    
    lista = [1, 2, 3, 4, 5]    #lista de numeros
    random.shuffle(lista)      #embaralha a lista
    print(lista)               #mostra a lista embaralhada  

    import datetime
    agora = datetime.datetime.now() #data e hora atual
    print(agora)                    #data e hora atual
    print(agora.year)               #ano
    print(agora.month)              #mes
    print(agora.day)                #dia
    print(agora.hour)               #hora
    print(agora.minute)             #minuto
    print(agora.second)             #segundo
    print(agora.strftime("%d/%m/%Y %H:%M:%S")) #formata a data e hora
    data_futura = agora + datetime.timedelta(days=10)
    print(data_futura) #data futura
    diferenca = data_futura - agora
    print(diferenca.days) #diferenca em dias
    print(diferenca.seconds) #diferenca em segundos

    