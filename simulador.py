import requests
import json
import random
import time

url = 'https://fabioqueiroz1415.pythonanywhere.com/dado'

isSalvar = 0

while True:
    # Gera valores aleatórios para x, y e z
    data = {
        'x': random.randint(0, 10),  # Aleatório entre 0 e 10
        'y': random.randint(0, 10),  # Aleatório entre 0 e 10
        'z': random.randint(0, 10),  # Aleatório entre 0 e 10
        'isSalvar': isSalvar
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        data = response.json()
        isSalvar = data['isSalvar']
        print("Dados enviados com sucesso:", data)
    else:
        print("Erro ao enviar dados:", response.status_code, response.text)

    # Atraso de 2 segundos antes do próximo envio
    time.sleep(2)
