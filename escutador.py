import socketio

# Crie uma instância do cliente SocketIO
sio = socketio.Client()

# Defina um manipulador para o evento 'connect'
@sio.event
def connect():
    print("Conectado ao servidor")

# Defina um manipulador para o evento 'new_data'
@sio.on('new_data')
def on_new_data(data):
    print(f"Novo dado recebido: {data}")

# Defina um manipulador para o evento 'disconnect'
@sio.event
def disconnect():
    print("Desconectado do servidor")

# Conecte-se ao servidor Flask SocketIO na Vercel
server_url = 'https://dados-acelerometro.vercel.app:5000'  # Substitua pela URL do seu projeto na Vercel
sio.connect(server_url)

# Mantenha o script em execução
sio.wait()
