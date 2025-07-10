from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def lade_aufgaben():
    with open('aufgaben.json', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/aufgaben', methods=['GET'])
def get_aufgaben():
    klasse = request.args.get('klasse')
    bundesland = request.args.get('bundesland')
    thema = request.args.get('thema')
    schwierig = request.args.get('schwierigkeit')

    daten = lade_aufgaben()

    gefiltert = [
        a for a in daten
        if a['klasse'] == klasse
        and a['bundesland'] == bundesland
        and a['thema'] == thema
        and a['schwierig'] == schwierig
    ]

    return jsonify(gefiltert)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Render nimmt PORT aus der Umgebung
