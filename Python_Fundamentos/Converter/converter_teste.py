#import converter

# print(converter.euro_dollar(100))
# print(converter.dollar_euro(100))

from converter import euro_dollar,dollar_euro

print(euro_dollar(100))
print(dollar_euro(100))

'''DESAFIOOO DENOVOO'''
# Desafio 11

#criar duas funcões que façam a conversão de graus Celsius para graus
#fahrenheit e vice-versa
#Importar o módulo e experimentar converter 32ºC para fahrenheit.

import converter_temperatura

valor= float(input('Me de um valor numerico de temperatura:'))

print(f'Em celsius:{converter_temperatura.celsius(valor)}')
print(f'Em fahrenheit: {converter_temperatura.fahrenheit(valor)}')