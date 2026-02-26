class Funcionario:
    def __init__(self, nome, salario=0.00):
        self.__nome = nome
        self.salario = salario  # Chama o setter para validar o salário

    @property
    def nome(self):
        return self.__nome

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("O salário deve ser um número.")
        if valor < 0:
            raise ValueError("O salário não pode ser negativo.")
        self.__salario = valor
    

    def salario_total(self):
        return self.__salario

    def resumo(self):
        print(f"Funcionário: {self.__nome}| Salário: {self.__salario:.2f}€")
    
    
print(12*"---" + "\n------- Funcionario Normal ---------\n" + 12*"---")
# Exemplo de uso
f = Funcionario("Lucas Goncalves", 2500.00)

# Isso vai levantar um ValueError que é capturado no raise do setter do salário
try:
    f1 = Funcionario("Maria Silva", -1000)  
except ValueError as e:
    print(f"Erro ao criar funcionário: {e}")
    
f.resumo()
print(f.nome)
print(f.salario)
print(f.salario_total())

print(12*"---" + "\n------- Funcionario Premium --------\n" + 12*"---")

class FuncionarioPremium(Funcionario):
    def __init__(self, nome, salario=0.00, premio=0.00):
        super().__init__(nome, salario)
        self.premio = premio  # Chama o setter para validar o prêmio

    @property
    def premio(self):
        return self.__premio
    @premio.setter
    def premio(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("O prêmio deve ser um número.")
        if valor < 0:
            raise ValueError("O prêmio não pode ser negativo.")
        self.__premio = valor

    def salario_total(self):
        return super().salario_total() + self.__premio
    def resumo(self):
        super().resumo()
        print(f"Prêmio: {self.__premio:.2f}€ | Total: {self.salario_total():.2f}€")
    
# Exemplo de uso
f_premium = FuncionarioPremium("Carlos", 1500.00, 300.00)

# Isso vai levantar um ValueError que é capturado no raise do setter do prêmio
try:
    f_premium2 = FuncionarioPremium("Maria", 2000.00, -500.00)
except ValueError as e:
    print(f"Erro ao criar funcionário premium: {e}")

f_premium.resumo()

print(f_premium.nome)
print(f_premium.salario)
print(f_premium.premio)
print(f_premium.salario_total())