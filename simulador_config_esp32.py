import requests
import json

url = 'http://127.0.0.1:5000/config-esp32'

data = {
    'isSalvar': 0,
    'tempo': 36,
    'delay': 1000
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print("Configurações enviadas com sucesso:", response.json())
else:
    print("Erro ao enviar configurações:", response.status_code, response.text)
