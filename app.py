from flask import Flask, request, jsonify, make_response, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
socketio = SocketIO(app)

# Constantes
QUANT_DATA = 100  # Quantidade máxima de dados armazenados
MAX_TIME = 300  # Tempo máximo para dados em segundos
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

data_list = []

# Função para verificar e converter a data
def verify_convert_date(date_string):
    try:
        return datetime.strptime(date_string, DATE_FORMAT)
    except ValueError:
        return None

# Função para remover dados antigos
def remove_oldest_data():
    now = datetime.utcnow()
    global data_list
    data_list = [item for item in data_list if (now - item['datetime']).seconds <= MAX_TIME]

# Função para remover excesso de dados
def remove_excess_data():
    global data_list
    if len(data_list) > QUANT_DATA:
        data_list = data_list[-QUANT_DATA:]

@app.route("/data", methods=['GET'])
def get_data():
    return jsonify(data_list)

@app.route("/data", methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if 'datetime' not in data or 'x' not in data or 'y' not in data or 'z' not in data:
            raise ValueError("O JSON deve conter os campos 'datetime', 'x', 'y', e 'z'")

        convert_date = verify_convert_date(data['datetime'])
        if convert_date is None:
            raise ValueError("A data informada não corresponde ao formato esperado")

        data_point = {
            'datetime': convert_date,
            'x': data['x'],
            'y': data['y'],
            'z': data['z']
        }

        data_list.append(data_point)
        remove_oldest_data()
        remove_excess_data()

        socketio.emit('new_data', data_point)
        return jsonify(message="Dados recebidos com sucesso"), 200
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('init_data', data_list)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
