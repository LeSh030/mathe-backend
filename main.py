from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

# OpenAI API-Key aus Umgebungsvariable
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/api/generate', methods=['GET'])
def generate_aufgabe():
    klasse = request.args.get('klasse')
    thema = request.args.get('thema')
    schwierig = request.args.get('schwierig')

    # 💡 Intelligenter, universeller Prompt
    prompt = (
        f"Erstelle eine Mathematik-Aufgabe für Klasse {klasse} im Thema {thema} "
        f"mit dem Schwierigkeitsgrad {schwierig}. "
        f"Gib ausschließlich ein JSON-Objekt mit den Feldern 'frage' und 'loesung' zurück. "
        f"Die Lösung soll eine Zahl (ganzzahlig), ein Bruch (z.B. '1/6') oder eine Dezimalzahl "
        f"mit maximal 2 Nachkommastellen sein. Keine Erklärungen, kein Fließtext."
        f"Beispiel: {{\"frage\": \"Berechne 2 + 3\", \"loesung\": 5}}"
    )

    try:
        # Neue OpenAI-API (ab Version 1.x)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # günstig zum Testen
            messages=[{"role": "user", "content": prompt}]
        )

        raw_content = response.choices[0].message.content

        # 💡 Antwort parsen – JSON auslesen
        aufgabe = json.loads(raw_content)

        return jsonify(aufgabe)

    except json.JSONDecodeError:
        return jsonify({"error": "Antwort konnte nicht als JSON interpretiert werden.", "rohdaten": raw_content}), 500
    except Exception as e:
        return jsonify({"error": "Allgemeiner Fehler", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
