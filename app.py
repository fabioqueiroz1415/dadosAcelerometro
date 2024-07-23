from flask import Flask, request, jsonify, make_response, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
socketio = SocketIO(app)

data_point = []

@app.route("/data", methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if ('x' not in data) or ('y' not in data) or ('z' not in data):
            raise ValueError("O JSON deve conter os campos 'x', 'y', e 'z'")

        data_point = {
            'x': data['x'],
            'y': data['y'],
            'z': data['z']
        }

        socketio.emit('new_data', data_point)
        return jsonify(message="Dados recebidos com sucesso!!!"), 200
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('new_data', data_point)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
