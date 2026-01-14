# ProducaoFundamentos.py
# Produção (CLI) — Fundamentos de Python
# Autor: (Marcos Alvarães)
# Execução: python 

from __future__ import annotations
import json 
 

CRITERIOS_SITUACAO = ("Reprovado", "Aprovado")  


def ler_int(mensagem: str, minimo: int | None = None, maximo: int | None = None) -> int:
    idade=int(input("Diga me a sua idade: "))
    while idade <= 0:
        idade=int(input("Não e possivel essa idade tente outra vez: "))
        if idade > 0:
            return idade
            break
    

def ler_string(mensagem: str) -> str:
    nome=input("Diz me um nome: ")
    return nome

def ler_float(mensagem: str, minimo: float | None = None, maximo: float | None = None) -> float:
    idade=float(input("Diz-me a tua altura:"))
    while (minimo is not None and idade < 0.3) or (maximo is not None and idade > 2.5):
        idade = int(input("Não é possivel essa idade, tente outra vez: "))
    
    return idade


def ler_nota(mensagem: str) -> float:
    nota=float(input("Diga me a sua nota: "))
    while nota < 0 and nota > 20:
        nota=float(input("Nao invalida tente outra vez: "))
    return nota      

def calcular_media(notas: list[float]) -> float:
    soma=0
    for i in notas:
        soma = soma + i
    media=soma / len(notas)
    return media
    
def obter_situacao(media: float) -> str:
    if media < 10:
        return CRITERIOS_SITUACAO[0]# Aprovado
    else:
        return CRITERIOS_SITUACAO[1]# Reprovado

def obter_aproveitamento(media: float) -> str:
    if media >= 14:
        return "Bom"
    elif media >= 10 and media < 14:
        return "Regular"
    elif media < 10:
       return "Insuficiente"
   
def gravar_dict_to_json(alunos: list[dict]) -> None:
    with open('lucas.json','w', encoding='utf-8') as f:
        json.dump(alunos,f)
        
##########################################################################################    

def criar_aluno() -> dict:
    """Recolhe dados, valida e devolve um dicionário com o aluno."""
    print("\n--- Adicionar Aluno ---")
    nome = ler_string("Nome do aluno: ")
    idade = ler_int("Idade: ", minimo=0)
    altura = ler_float("Altura (ex.: 1.65): ", minimo=0.3, maximo=2.5)

    notas: list[float] = []
    print("Introduza 3 notas (0 a 20).")
    for i in range(1, 4):
        nota = ler_nota(f"Nota {i}: ")
        notas.append(nota)

    media = calcular_media(notas)
    situacao = obter_situacao(media)
    aproveitamento = obter_aproveitamento(media)

    aluno = {
        "nome": nome,
        "idade": idade,
        "altura": altura,
        "notas": notas,
        "media": media,
        "situacao": situacao,
        "aproveitamento": aproveitamento,
    }
    print("Aluno registado com sucesso.\n")
    return aluno


def listar_alunos(alunos: list[dict]) -> None:
    """Lista alunos com informação resumida."""
    print("\n--- Lista de Alunos ---")
    if not alunos:
        print("Sem alunos registados.")
        return

    for idx, a in enumerate(alunos, start=1):
        print(f"{idx:>2}. {a['nome']} | Média: {a['media']:.2f} | {a['situacao']} | {a['aproveitamento']}")


def estatisticas(alunos: list[dict]) -> None:
    """Mostra estatísticas globais da turma."""
    print("\n--- Estatísticas da Turma ---")
    if not alunos:
        print("Sem alunos registados.")
        return

    medias = [a["media"] for a in alunos]
    media_turma = calcular_media(medias)
    melhor_media = max(medias)
    pior_media = min(medias)

    aprovados = sum(1 for a in alunos if a["situacao"] == "Aprovado")
    reprovados = len(alunos) - aprovados

    dist = {"Bom": 0, "Regular": 0, "Insuficiente": 0}
    for a in alunos:
        dist[a["aproveitamento"]] += 1

    # Nomes dos melhores/piores (pode haver empate)
    melhores = [a["nome"] for a in alunos if a["media"] == melhor_media]
    piores = [a["nome"] for a in alunos if a["media"] == pior_media]

    print(f"Total de alunos: {len(alunos)}")
    print(f"Média da turma: {media_turma:.2f}")
    print(f"Melhor média: {melhor_media:.2f} ({', '.join(melhores)})")
    print(f"Pior média: {pior_media:.2f} ({', '.join(piores)})")
    print(f"Aprovados: {aprovados} | Reprovados: {reprovados}")
    print("Distribuição por aproveitamento:")
    print(f"  Bom: {dist['Bom']}")
    print(f"  Regular: {dist['Regular']}")
    print(f"  Insuficiente: {dist['Insuficiente']}")


def menu() -> None:
    alunos: list[dict] = []

    while True:
        print("\n===== Gestor de Alunos =====")
        print("1) Adicionar aluno")
        print("2) Listar alunos")
        print("3) Estatisticas da turma")
        print("4) Gravar o Dict para json")
        print("5) Sair")

#       opcao = ler_int("Escolha uma opção: ", minimo=1, maximo=5)
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            aluno = criar_aluno()
            alunos.append(aluno)
            
        elif opcao == 2:
            listar_alunos(alunos)
            
        elif opcao == 3:
            estatisticas(alunos)
            

        elif opcao == 4:
            if not alunos:
                print("\nSem alunos registados para gravar.")
            else:
                gravar_dict_to_json(alunos)

        elif opcao == 5:
            print("\nA terminar. Obrigado.")
            break


if __name__ == "__main__":
    menu()
