import pandas as pd

# dataframe = pd.DataFrame()

'''Examples
#Constructing DataFrame from a dictionary.

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
print(df) 

# col  col1  col2
# 0     1     3
# 1     2     4

'''
'''Dicionario
venda = { 'data':['15/02/2021', '16/02/2021'],
            'valor': [500, 300],
            'produto': ['feijao','arroz'],
            'qtde':[50, 70]
            }

print(venda)
print('')
'''

'''Uma tabela'''
# venda_df = pd.DataFrame(venda)
# print(venda_df)

'''TABELA DE UM FICHEIRO EXCEL'''
vendas_df = pd.read_excel('Vendass.xlsx')
print(vendas_df)
print('_______________________________________________________________________________________________________')

'''HEAD'''
print(vendas_df.head(10))
print('_______________________________________________________________________________________________________')

'''SHAPE'''
print(vendas_df.shape)
print('_______________________________________________________________________________________________________')

'''DESCRIBE'''
print(vendas_df.describe())
print('_______________________________________________________________________________________________________')

produto = vendas_df[['Produto', 'ID Loja']]
print(produto)
print('_______________________________________________________________________________________________________')

print(vendas_df.loc[1])
print(vendas_df.loc[10:15]) #Descreve o inicio da primeira e a ultima linha no comando