# ...existing code...
import requests
import json
# ...existing

cotacoes = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL')

#print(cotacoes)
#print(type(cotacoes))

cotacoes=cotacoes.json()
#print(cotacoes)
#print(type(cotacoes))

cotacao_dolar = cotacoes['USDBRL']['bid']
cotacao_euro = cotacoes ['EURBRL']['bid']
cotacao_bitcoin = cotacoes['BTCBRL']['bid']

print(f'Cotacao do Bitcoin agora: {cotacao_bitcoin}')
print('')
print(f'Cotacao do Euro agora: {cotacao_euro}')
print('')
print(f'Cotacao do Dolar agora: {cotacao_dolar}')
print('')

