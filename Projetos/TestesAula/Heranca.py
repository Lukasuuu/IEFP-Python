#Importa a classe Aluno do módulo Aluno
import Aluno

class AlunoBolseiro(Aluno.Aluno):
    def __init__(self, nome, nota, bolsa):
        #Chama o contrutor da classe pai (Aluno) para inicializar os atributos nome e nota
        super().__init__(nome, nota)
        #Inicializa o atributo específico da classe AlunoBolseiro (bolsa - opcional)
        if bolsa < 0:
            raise ValueError("O valor da bolsa não pode ser negativo.")
        self.bolsa = bolsa
    
    def resumo(self):
        #sobrescreve o método resumo da classe Aluno para incluir informações sobre a bolsa
        #reaproveita o texto original do pai com super{} e adiciona a informação da bolsa
        return f"{super().resumo()} - Bolsa:{self.bolsa}€)"
    
    def aumentar_bolsa(self, valor):
        if valor < 0:
            raise ValueError("O valor para aumentar a bolsa não pode ser negativo.")
        self.bolsa += valor
        return self.bolsa
    

    

