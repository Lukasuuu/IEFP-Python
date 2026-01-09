import requests
import json

# Sua chave da API
Key = "3689129ee7af0fa500cad990971aecd6"
cidade = "Faro,PT"

# Link da API
link = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={Key}&lang=pt_br"

# Faz a requisição
requisicao = requests.get(link)

# Converte para JSON
dados = json.loads(requisicao.text)

# Verifica se a requisição foi bem-sucedida
if requisicao.status_code == 200: # 200 significa sucesso de conexão API
    print(f"🌤️ Tempo em {dados['name']}")
    print(f"Temperatura atual: {dados['main']['temp']- 273.15}°C")
    print(f"Humidade: {dados['main']['humidity']}%")
    print(f"Condição: {dados['weather'][0]['description'].capitalize()}")
else:
    print("Erro ao consultar o tempo:", dados)

