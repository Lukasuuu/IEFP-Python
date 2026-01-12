from jogo import Avatar


#nome = 'Joana'
#p1 = Avatar() #Variavel do tipo Avatar

#print(type(nome))
#print(type(p1))

#p1.move_direita() #Estou a chamar o metodo que 'move_direita' que pertence a classe Avatar

#p2 = Avatar()
#p2.move_esquerda() #Estou a chamar o metodo que 'move_esquerda' que pertence a classe Avatar

#p1.nome='Joana'
#p2.nome='Rita'

#print(p1.nome)
#print(p2.nome)


p1 = Avatar('Lucas', 33, '')
p2 = Avatar('Carlos', 60, '')

print('')
print('Nome: ', p1.nome)
print('Energia:', p1.energia)
print('')

print(f'Nome: {p2.nome}\nEnergia: {p2.energia} %')

print('')
print(f'Nome:{p1.nome}')

p1.alimenta()
p1.move_direita()
p1.move_esquerda()
p1.move_direita()
p1.move_direita()
p1.move_esquerda()
p1.move_direita()
print(f'Upgrade de 5 a energia: {p1.energia}')


'''Desafio Denovoooooooooooooo'''
#Desafio 12

'''Utilizador a classe Avatar deverá acrescentar
uma propriedade com o nome dinhero
Cada personagem deverá comecçar o jogo com 100 unidades monetarias
Cada vez que o personagem é alimentado deverá perder 
10 unidades monetarias '''

p3 = Avatar( 'Lucas',60,100)
print('Nome:' ,p3.nome)
print('Energia:' ,p3.energia)
print('Dinheiro:',p3.dinheiro)
p3.unidade_monetaria()
print('Dinheiro:' ,p3.dinheiro)
p3.dados()