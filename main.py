from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# API-Key aus Environment-Variable lesen
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/api/generate', methods=['GET'])
def generate_aufgabe():
    klasse = request.args.get('klasse')
    thema = request.args.get('thema')
    schwierig = request.args.get('schwierig')

    # Prompt zusammenbauen
    prompt = (f"Erstelle eine Mathe-Aufgabe für die Klasse {klasse} "
              f"im Thema {thema}, Schwierigkeitsgrad: {schwierig}. "
              f"Gib die Aufgabe und die richtige Lösung in JSON an. "
              f"Beispiel: {{\"frage\": \"Berechne...\", \"loesung\": 42}}.")

    # Anfrage an OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Antwort auslesen
    antwort = response.choices[0].message.content

    try:
        # JSON-Antwort an Frontend
        return jsonify(eval(antwort))  # Achtung: eval() nur als Beispiel, später json.loads() verwenden
    except Exception as e:
        return jsonify({"error": "Fehler bei der OpenAI-Antwort", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
