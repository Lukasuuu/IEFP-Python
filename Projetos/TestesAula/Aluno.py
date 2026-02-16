class Aluno:
    def __init__(self, nome, nota):
        self.nome = nome
        self.nota = nota
        self.definir_nota(nota)
    
    def definir_nota(self, nova_nota):
        try:
            if isinstance(nova_nota, (int, float)):
                self.nota = float(nova_nota)
            else:
                raise ValueError("A nota deve ser um número.")
        except ValueError as NOTA_INVALIDA:
            print(f"Erro ao definir a nota: {NOTA_INVALIDA}")
        finally:
            print(f"Nota atual de {self.nome}: {self.nota}")
            
    def apresentar(self):
        aluno1 = Aluno("Maria",15)
        aluno2 = Aluno("João", 16)

    def situacao(self):
        if self.nota >= 10:
            return "Aprovado"
        else:                
            return "Reprovado"
        
    def dados(self):
        return f"Nome: {self.nome}, Nota: {self.nota}"
    
    def alterar_nota(self, nova_nota):
        self.nota = nova_nota
    
    def esta_aprovado(self):
        if self.nota >= 10:
            return True
        else:
            return False
    
    def resumo(self):
        return f"Aluno: {self.nome}, Nota: {self.nota}, Situação: {self.situacao()}"
    
    def pontos_extra(self, pontos):
        self.nota = pontos + self.nota
        return self.nota
    
    def comparacao_nota(self, outro_aluno):
        if self.nota > outro_aluno.nota:
            return f"{self.nome} tem nota maior que {outro_aluno.nome}"
        elif self.nota < outro_aluno.nota:
            return f"{self.nome} tem nota menor que {outro_aluno.nome}"
        else:
            return f"{self.nome} e {outro_aluno.nome} têm a mesma nota" 