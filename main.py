from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os
import json
import random

app = Flask(__name__)
CORS(app)

# OpenAI API-Key aus Umgebungsvariable
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/api/generate', methods=['GET'])
def generate_aufgabe():
    klasse = request.args.get('klasse')
    thema = request.args.get('thema')
    schwierig = request.args.get('schwierig')

    random_seed = random.randint(1, 1000)

    prompt = (
        f"Du bist ein Mathematiklehrer. Erstelle eine abwechslungsreiche und einzigartige Mathematik-Aufgabe "
        f"für Klasse {klasse}, Thema {thema}, Schwierigkeitsgrad {schwierig}. "
        f"Die Aufgabe soll klar formuliert sein und den Schüler genau anweisen, wie die Lösung formatiert werden soll "
        f"(z.B. als Bruch, gerundet auf 2 Nachkommastellen, ganze Zahl). "
        f"Variiere die Zahlen, den Kontext und die Art der Fragestellung. "
        f"Nutze die Zufallszahl {random_seed} um Variation zu gewährleisten. "
        f"Antworte nur mit einem JSON-Objekt mit den Schlüsseln 'frage' und 'loesung', ohne weitere Erklärungen. "
        f"Beispiel: {{\"frage\": \"Berechne 3 + 4. Gib eine ganze Zahl an.\", \"loesung\": 7}}."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=300
        )

        raw_content = response.choices[0].message.content
        aufgabe = json.loads(raw_content)
        return jsonify(aufgabe)

    except json.JSONDecodeError:
        return jsonify({"error": "Antwort konnte nicht als JSON interpretiert werden.", "rohdaten": raw_content}), 500
    except Exception as e:
        return jsonify({"error": "Allgemeiner Fehler", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
