#import converter

# print(converter.euro_dollar(100))
# print(converter.dollar_euro(100))


#outra forma de importar funções específicas dos módulos monetario euro e dollar
from converter_monetario import euro_dollar,dollar_euro

print(euro_dollar(100))
print(dollar_euro(100))

#outra forma de importar o módulo todo
import converter_monetario

print(converter_monetario.euro_dollar(100))
print(converter_monetario.dollar_euro(100))


'''DESAFIOOO DENOVOO'''
# Desafio 11

#criar duas funcões que façam a conversão de graus Celsius para graus
#fahrenheit e vice-versa
#Importar o módulo e experimentar converter 32ºC para fahrenheit.

#importando funções específicas dos módulos celsius e fahrenheit
from converter_temperatura import celsius, fahrenheit

valor= float(input('Me de um valor numerico de temperatura:'))

print(f'Em celsius:{celsius(valor)}')
print(f'Em fahrenheit: {fahrenheit(valor)}')

#outra forma de importar o módulo todo
import converter_temperatura

print(f'Em celsius:{converter_temperatura.celsius(valor)}')
print(f'Em fahrenheit: {converter_temperatura.fahrenheit(valor)}')
