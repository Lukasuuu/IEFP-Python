'''
# openpyxl - pip install openpyxl
# trabalhamos com workbook
# bva um excel tem o nome de workbook
'''

from openpyxl import workbook, load_workbook
'''
# SE utilizar so o import do workboook, so vou conseguir criar o ficheiro , mas se quiser
# utilizar esse tengo o metodo load workbook
'''
tabela = load_workbook('Produtos.xlsx')

aba_ativa = tabela.active

'''
#Quando abrimos o excel é a aba que esta aberta para nós
# Identificar a coluna e a linha que quero trabalhar
#aba_ativa['A1]
'''

'''
for celula in aba_ativa['C']:
    if celula.value == 'Serviço':
        linha = celula.row
        aba_ativa[f'D{linha}']=1.7
        
tabela.save('ProdutoTeste.xlsx')
'''

for celula in aba_ativa['A']:
    if celula.value == 'SPA':
        for celula in aba_ativa['C']:
            if celula.value == 'Serviço':
                linha = celula.row
                aba_ativa[f'D{linha}']=2.5
    
        
tabela.save('ProdutoTeste1.xlsx')
print('tabela criada e altera com sucesso!!!')


