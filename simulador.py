import requests
import json

# URL do servidor Flask
url = 'https://fabioqueiroz1415.pythonanywhere.com/data'  # Altere para a URL do seu servidor na Vercel quando necessário

# Dados a serem enviados no POST
data = {
    'x': 1,
    'y': 2,
    'z': 3
}

# Cabeçalhos para a requisição
headers = {
    'Content-Type': 'application/json',
    'Origin': 'https://fabioqueiroz1415.pythonanywhere.com'
}

# Enviar a requisição POST
response = requests.post(url, data=json.dumps(data), headers=headers)

# Verificar a resposta
if response.status_code == 200:
    print("Dados enviados com sucesso:", response.json())
else:
    print("Erro ao enviar dados:", response.status_code, response.text)
