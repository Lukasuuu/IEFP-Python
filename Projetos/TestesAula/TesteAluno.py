import Aluno
import Heranca

def main():
    #METODO Por mecanismo de herança, a classe AlunoBolseiro
    aluno_normal = Aluno.Aluno("Maria", 14)
    aluno_bolseiro = Heranca.AlunoBolseiro("Joao",12, 150)

    aluno1 = Aluno.Aluno("Maria", 15)
    aluno2 = Aluno.Aluno("João", 8)

    print(aluno1.nome, aluno1.nota, aluno1.situacao())
    print(aluno2.nome, aluno2.nota, aluno2.situacao())

    print("\n")

    print(aluno1.dados())
    print(aluno2.dados())


    print(f"Aluno 2 nota original: {aluno2.nota}")
    aluno2.alterar_nota(7)
    print(f"Aluno 2 nota alterada via método: {aluno2.nota}")

    print("\n")

    print(f"{aluno1.nome}: aprovado(a)? \n{aluno1.esta_aprovado()}")
    print(f"{aluno2.nome}:  aprovado(a)? \n{aluno2.esta_aprovado()}")

    print("\n")

    print(aluno1.resumo())
    print(aluno2.resumo())

    print("\n")

    print(aluno2.pontos_extra(2))
    print(f"{aluno2.nome} tem nota extra:{aluno2.pontos_extra(2)} e obteve nota final: {aluno2.nota}")

    print("\n")


    print(aluno_normal.resumo())
    print(aluno_bolseiro.resumo()) 

    print("---------------------------------------------------------------------")  

    print(aluno_normal.situacao())
    print(aluno_bolseiro.situacao())
    print("---------------------------------------------------------------------")  

    print(aluno_bolseiro.bolsa)
    print(aluno_bolseiro.aumentar_bolsa(50))

    print("---------------------------------------------------------------------")

    print(aluno_bolseiro.resumo())    

if __name__ == "__main__":
    main()
