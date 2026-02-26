from dataclasses import dataclass, field

@dataclass
class Funcionario:
    _nome: str
    _salario: float = 0.00

    def __post_init__(self):
        # Validações para salário e prêmio
        self.salario = self._salario  # Chama o setter para validar o salário
        
    @property
    def nome(self):
        return self._nome
    
    @property
    def salario(self):
        #Garantir que o salário seja sempre um número válido
        return self._salario
    
    @salario.setter
    def salario(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("O salário deve ser um número.")
        if valor < 0:
            raise ValueError("O salário não pode ser negativo.")
        self._salario = valor


    def salario_total(self):
        return self._salario

    def resumo(self):
        print(f"Funcionário: {self._nome}| Salário: {self._salario:.2f}€")
    def __repr__(self):
        return f"Funcionario(nome='{self._nome}', salario={self._salario:.2f})"
    def __str__(self):
        return f"Funcionário: {self._nome}| Salário: {self._salario:.2f}"
    def __eq__(self, other):
        if not isinstance(other, Funcionario):
            return NotImplemented
        return self._nome == other._nome and self._salario == other._salario

@dataclass
class FuncionarioPremium(Funcionario):
    _premio: float = 0.00

    def __post_init__(self):
        super().__post_init__()  # Valida o salário na superclasse
        self._premio = self._premio  # Chama o setter para validar o prêmio

    @property
    def premio(self):
        return self._premio
    
    @premio.setter
    def premio(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("O prêmio deve ser um número.")
        if valor < 0:
            raise ValueError("O prêmio não pode ser negativo.")
        self._premio = valor

    def salario_total(self):
        return self._salario + self._premio

    def resumo(self):
        print(f"Funcionário Premium: {self._nome}| Salário: {self._salario:.2f}€| Prêmio: {self._premio:.2f}€| Salário Total: {self.salario_total():.2f}€")
    
    def __repr__(self):
        return f"FuncionarioPremium(nome='{self._nome}', salario={self._salario:.2f}, premio={self._premio:.2f})"
    def __str__(self):
        return f"Funcionário Premium: {self._nome}| Salário: {self._salario:.2f}€| Prêmio: {self._premio:.2f}€| Salário Total: {self.salario_total():.2f}€"
    def __eq__(self, other):
        if not isinstance(other, FuncionarioPremium):
            return NotImplemented
        return (self._nome == other._nome and 
                self._salario == other._salario and 
                self._premio == other._premio)
    
# Isso vai levantar um ValueError que é capturado no raise do setter do salário
try:
    f = Funcionario("Lucas Goncalves", -2500.00) 
except ValueError as e:
    print(f"Erro ao criar funcionário: {e}") 

f = Funcionario("Lucas Goncalves", 2500.00)

f2 = Funcionario("Wander", 2500.00)

print(f.nome == f2.nome)        # True, pois os nomes são iguais
print(f.salario == f2.salario)  # True, pois os salários são iguais
print(f == f2)                  # True, pois ambos os atributos são iguais

f2.resumo()
print(f2.nome)
print(f2.salario)
print(f2.salario_total())

f1 = FuncionarioPremium("Maria Silva", 3000.00, 500.00)
f1.resumo()
print(f1.nome)
print(f1.salario)
print(f1.salario_total())

