class Aluno:
    def __init__(self, nome, nota):
        self.__nome = nome
        self.nota = nota  # passa no setter (validação)

    @property
    def nome(self):
        return self.__nome

    @property
    def nota(self):
        return self.__nota

    def situacao(self):
        return "Aprovado" if self.__nota >= 10 else "Reprovado"

    def resumo(self):
        return f"{self.__nome} tem nota {self.__nota} e está {self.situacao()}"
    
    @nota.setter
    def nota(self, valor):
        try:
            if not isinstance(valor, (int, float)):
                raise ValueError("A nota tem de ser um número (int ou float).")
            if valor < 0 or valor > 20:
                raise ValueError("A nota tem de estar entre 0 e 20.")
            self.__nota = valor
        except ValueError as e:
            print(f"Erro ao definir a nota: {e}")



a = Aluno("Maria", 14)
print(a.resumo())

#a.nota = 18
print(a.resumo())

#a.nota = 100

#a.nota = "dez"

#a.__nota = 999

print(a.resumo())
print(a.__dict__)
