class Aluno:
    def __init__(self, nome,nota):
        self.nome = nome
        self.nota= nota
        
        
    def situacao(self):
        if self.nota >= 10:
            return 'Aprovado'     
        else:
            return 'Reprovado'
    
    def dados(self):
        print(f'Nome:{self.nome}, Nota: {self.nota}',self.situacao())
                 