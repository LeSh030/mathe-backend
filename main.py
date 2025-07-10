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

    # Neuer, klarer Prompt
    prompt = (
        f"Erstelle eine Mathematik-Aufgabe für die Klasse {klasse}, Thema {thema}, Schwierigkeitsgrad {schwierig}. "
        f"Die Aufgabe muss in deutscher Sprache formuliert sein. "
        f"Formuliere die Aufgabenstellung so, dass immer klar ist, in welchem Format die Lösung erwartet wird. "
        f"Zum Beispiel: "
        f"'Gib die Wahrscheinlichkeit als Bruch an.', "
        f"'Runde das Ergebnis auf zwei Nachkommastellen.', "
        f"'Gib die Antwort als gekürzten Bruch an.', "
        f"oder 'Antworte mit einer ganzen Zahl.' "
        f"Liefere als Antwort nur ein JSON-Objekt im folgenden Format: "
        f"{{ \"frage\": \"...\", \"loesung\": \"...\" }}. "
        f"Keinen Fließtext, keine Erklärungen, nur die Frage und die Lösung. "
        f"Beispiel: {{ \"frage\": \"Berechne 2 + 3. Gib eine ganze Zahl an.\", \"loesung\": 5 }}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_content = response.choices[0].message.content

        # Antwort als JSON parsen
        aufgabe = json.loads(raw_content)

        return jsonify(aufgabe)

    except json.JSONDecodeError:
        return jsonify({"error": "Antwort konnte nicht als JSON interpretiert werden.", "rohdaten": raw_content}), 500
    except Exception as e:
        return jsonify({"error": "Allgemeiner Fehler", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
