from flask import Flask, request, jsonify, make_response, render_template
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

isSalvar = 0
acelerometro = {'x': 0, 'y': 0, 'z': 0}
acelerometros = {}
contador_id = 0

@app.route("/dado", methods=['GET', 'POST'])
def dados():
    global acelerometro, contador_id, isSalvar, acelerometros
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not all(key in data for key in ('x', 'y', 'z')):
                raise ValueError("O JSON deve conter os campos 'x', 'y', 'z'")

            acelerometro = {
                'x': data['x'],
                'y': data['y'],
                'z': data['z']
            }
            if isSalvar == 1:
                acelerometros[f'acelerometro_{contador_id}'] = acelerometro
                contador_id += 1
            return make_response(jsonify({'mensagem': 'recebido.', 'isSalvar': isSalvar, 'dados_recebidos': data}), 200)
        except Exception as e:
            return make_response(jsonify(error=str(e)), 400)
    
    elif request.method == 'GET':
        try:
            return make_response(jsonify(acelerometro), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

@app.route('/dado/armazenar')
def armazenar_dados():
    return render_template('armazenar_dados.html')

@app.route('/dado/armazenados')
def dados_armazenados():
    try:
        response_data = json.dumps(acelerometros, indent=2)
        return make_response(response_data, 200, {'Content-Type': 'application/json'})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route("/isSalvar", methods=['GET', 'POST'])
def isSalvar_handler():
    global isSalvar

    if request.method == 'GET':
        return make_response(jsonify({'isSalvar': isSalvar}), 200)

    elif request.method == 'POST':
        data = request.json 
        if 'isSalvar' in data:
            isSalvar = data['isSalvar'] 
            return make_response(jsonify({'message': 'Recebido.', 'isSalvar': isSalvar}), 200)
        else:
            return make_response(jsonify({'error': 'Chave "isSalvar" não encontrada no JSON'}), 400)

@app.route('/retorna-tudo')
def retorna_tudo():
    global isSalvar, contador_id, acelerometros
    try:
        tudo = {
            'dados': acelerometros,
            'quantidade de dados armazenados': contador_id,
            'isSalvar': isSalvar
        }
        response_data = json.dumps(tudo, indent=2)
        return make_response(response_data, 200, {'Content-Type': 'application/json'})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/')
def tempo_real():
    return render_template('tempo_real.html')

if __name__ == '__main__':
    app.run(debug=True)
