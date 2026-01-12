import math

a =5
b=3

print("Soma:", a + b)                #mostra a soma
print("Subtracao:", a - b)           #mostra a subtracao
print("Multiplicacao:", a * b)       #mostra a multiplicacao
print("Divisao:", a / b)             #mostra a divisao
print("Divisao inteira:", a // b)    #mostra a divisao inteira
print("Resto da divisao:", a % b)    #mostra o resto da divisao
print("Exponenciacao:", a ** b)      #mostra a potencia



a += 2
print("Apos a += 2, a =", a)        #mostra o valor de a apos a operacao

a = a + 2
print("Apos a += 2, a =", a)         #mostra o valor de a apos a operacao

a -= 2
print("Apos a -= 2, a =", a)        #mostra o valor de a apos a operacao

a = a - 2
print("Apos a -= 2, a =", a)         #mostra o valor de a apos a operacao

a *= 2
print("Apos a *= 2, a =", a)        #mostra o valor de a apos a operacao

a = a * 2
print("Apos a *= 2, a =", a)         #mostra o valor de a apos a operacao

a /= 2
print("Apos a /= 2, a =", a)        #mostra o valor de a apos a operacao

a = a / 2
print("Apos a /= 2, a =", a)         #mostra o valor de a apos a operacao

a //= 2
print("Apos a //= 2, a =", a)        #mostra o valor de a apos a operacao

a = a // 2
print("Apos a //= 2, a =", a)        #mostra o valor de a apos a operacao

a %= 2
print("Apos a %= 2, a =", a)        #mostra o valor de a apos a operacao

a = a % 2
print("Apos a %= 2, a =", a)         #mostra o valor de a apos a operacao


a **= 2
print("Apos a **= 2, a =", a)        #mostra o valor de a apos a operacao

a = a ** 2
print("Apos a **= 2, a =", a)        #mostra o valor de a apos a operacao   

c = 10 + (3 * 2) ** 2
print("Resultado de 10 + (3 * 2) ** 2 =", c)   #mostra o resultado da expressao com precedencia de operadores

d = 7.3
print("Arredondamento de 7.3 para cima:", round(d))    #mostra o arredondamento de d para baixo
e = 7.6
print("Arredondamento de 7.6 para cima:", round(e))    #mostra o arredondamento de e para cima
f= -7.6
print("Arredondamento de -7.6 para cima:", abs(f))     #mostra o valor absoluto - é o modulo do numero

print("arredonda pra cima:", math.ceil(d))                                    #arredonda para cima
print("arredonda pra baixo:",math.floor(e))                                   #arredonda para baixo
print("valor de pi:",math.pi)                                         #valor de pi








print("raiz quadrada:",math.sqrt(49))                #raiz quadrada
print("fatorial:",math.factorial(5))                 #fatorial
print("potencia:",math.pow(3, 4))                    #potencia

print(math.e)                                        #valor de euler
print(math.log(10))                                  #logaritmo natural
print(math.log10(100))                               #logaritmo base 10

print("seno: ",math.sin(math.radians(30)))           #seno
print("coseno:",math.cos(math.radians(60)))          #cosseno
print("tangente:",math.tan(math.radians(45)))        #tangente
print("hipotenusa:", math.hypot(3, 4))               #hipotenusa

print(math.degrees(math.pi/2))                       #converte radianos para graus
print(math.radians(180))                             #converte graus para radianos
print(math.gcd(48, 18))                              #maior divisor comum
print(math.lcm(48, 18))                              #menor multiplo comum
print(math.isqrt(49))                                #raiz quadrada inteira
print(math.comb(5, 2))                               #combinacoes
print(math.perm(5, 2))                               #permutacoes
print(math.dist((1, 2), (4, 6)))                     #distancia