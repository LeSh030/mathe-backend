from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# OpenAI API-Key aus Environment-Variable holen
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/api/generate', methods=['GET'])
def generate_aufgabe():
    klasse = request.args.get('klasse')
    thema = request.args.get('thema')
    schwierig = request.args.get('schwierig')

    prompt = (
        f"Erstelle eine Mathematik-Aufgabe für Klasse {klasse}, "
        f"Thema: {thema}, Schwierigkeitsgrad: {schwierig}. "
        f"Gib die Aufgabe und die Lösung im JSON-Format zurück. "
        f"Beispiel: {{\"frage\": \"Berechne 2 + 3.\", \"loesung\": 5}}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        antwort = response.choices[0].message.content

        # Rückgabe als JSON
        return jsonify(eval(antwort))  # Achtung: eval() nur zum Testen!

    except Exception as e:
        return jsonify({"error": "OpenAI-Fehler", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
