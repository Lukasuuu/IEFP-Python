from aluno import Aluno

turma = []

quantidade = int(input('Quantos alunos tem na turma? '))

for i in range(quantidade):
    print(f'\nAluno {i + 1}')
    nome = input('Diz me o nome: ')
    nota = int(input('Diz me a nota: '))
    
    aluno = Aluno(nome, nota)
    turma.append(aluno)

print('\n--- Lista de Alunos ---')
for aluno in turma:
    aluno.dados()