class Avatar:
    def __init__(self, n1, e1, d1):
        self.nome = n1
        self.energia = e1
        self.dinheiro = d1
        
    def unidade_monetaria(self):
        self.dinheiro -= 10
    def alimenta(self):
        self.energia += 5   
    def move_direita(self):
        print('move direita...')
    def move_esquerda(self):
        print('move pra esquerda...')
    def dados(self):
        print(f'Nome: {self.nome}, Energia: {self.energia}, Dinheiro: {self.dinheiro}')
        
        
    