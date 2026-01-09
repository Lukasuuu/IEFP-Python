import pandas as pd

tabela = pd.read_excel('Produtos.xlsx')
print(tabela)

'''Atualizar o mutiplicador de impostos
# .loc para localizar
# tabela.loc[linha,coluna] = 1,5  // Qual a linha e coluna que quero editar?
# tabela.loc[linha,multiplicador imposto]  // Qual a coluna que quero editar?
# tabela.loc[tabela[tipo]==Servico,coluna] // As linhas que quero editar?'''



tabela.loc[tabela['Tipo'] == 'Servico','Multiplicador Imposto'] = 1.5

'''FAZER O RESULTADO FINAL'''

tabela['Preço Base Final'] = tabela['Multiplicador Imposto'] * tabela['Preço Base Final']

'''GRAVAR EM UM NOVO FICHEIRO'''
tabela.to_excel('ProdutoPandas.xlsx', index=False)

'''
# Se quiser atraves da ABA Produtos podesse escolher um produto e mudar multiplicar de imposto
'''
tabela.loc[tabela['Produtos'] == 'Tablet','Multiplicador Imposto'] = 2.1
tabela['Preço Base Final'] = tabela['Multiplicador Imposto'] * tabela['Preço Base Original']
tabela.to_excel('ProdutoPandas1.xlsx', index=False)



'''
# Criando todos os campos para atribuir o PREÇO BASE FINAL EM UM EXCEL
'''

tabela.loc[tabela['Produtos'] == 'Tablet','Preço Base Original'] = 1000
tabela.loc[tabela['Produtos'] == 'Pós Graduação','Preço Base Original'] = 3500
tabela.loc[tabela['Produtos'] == 'Telemovel','Preço Base Original'] = 799.95
tabela.loc[tabela['Produtos'] == 'Passagem Aérea','Preço Base Original'] = 359.55
tabela.loc[tabela['Produtos'] == 'Computador','Preço Base Original'] = 1249.99
tabela.loc[tabela['Produtos'] == 'SPA','Preço Base Original'] = 400.50
tabela.loc[tabela['Produtos'] == 'Corte Cabelo','Preço Base Original'] = 25


tabela.loc[tabela['Produtos'] == 'Pós Graduação','Multiplicador Imposto'] = 2.1
tabela.loc[tabela['Produtos'] == 'Telemovel','Multiplicador Imposto'] = 1.2
tabela.loc[tabela['Produtos'] == 'Passagem Aérea','Multiplicador Imposto'] = 1.5
tabela.loc[tabela['Produtos'] == 'Computador','Multiplicador Imposto'] = 1.4
tabela.loc[tabela['Produtos'] == 'SPA','Multiplicador Imposto'] = 1.3
tabela.loc[tabela['Produtos'] == 'Corte Cabelo','Multiplicador Imposto'] = 2.5

tabela['Preço Base Final'] = tabela['Multiplicador Imposto'] * tabela['Preço Base Original']
tabela.to_excel('ProdutoPandasTabela.xlsx', index=False)
