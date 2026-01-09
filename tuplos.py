# As tuplas sao imutáveis isso significa que não podem ser alteradas
# Usar as tuplas quando tenho a certeza que o seu valor nao vai ser alterado

num1 = [1, 2, 3] # Lista
num2 = (1, 2, 3) # Tupla ou lista constante

num1[0] = 5
num2[0] = 5

print(num1)
print(num2)