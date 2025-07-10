from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# JSON-Datei mit Aufgaben laden
def lade_aufgaben():
    with open('aufgaben.json', encoding='utf-8') as f:
        return json.load(f)

# API-Endpunkt
@app.route('/api/aufgaben', methods=['GET'])
def get_aufgaben():
    klasse = request.args.get('klasse')
    bundesland = request.args.get('bundesland')
    thema = request.args.get('thema')
    schwierig = request.args.get('schwierigkeit')

    daten = lade_aufgaben()

    # Filter nach Parametern
    gefiltert = [
        a for a in daten
        if a['klasse'] == klasse
        and a['bundesland'] == bundesland
        and a['thema'] == thema
        and a['schwierig'] == schwierig
    ]

    return jsonify(gefiltert)

# Startet den Server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render setzt $PORT automatisch
    app.run(host='0.0.0.0', port=port, debug=True)
