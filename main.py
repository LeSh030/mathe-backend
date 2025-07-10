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
         f"Du bist ein Mathematiklehrer. Erstelle eine abwechslungsreiche Mathematik-Aufgabe für Klasse {klasse}, Thema {thema}, Schwierigkeitsgrad {schwierig}. "
        f"Formuliere die Aufgabe so, dass die Schüler genau wissen, wie sie die Antwort schreiben müssen. "
        f"Der Hinweis soll nicht nur das Format angeben (z.B. ganze Zahl, Bruch, Dezimalzahl, Koordinaten), sondern auch praktische Tipps enthalten, z.B. wie Leerzeichen zu setzen sind, "
        f"wie Klammern geschrieben werden sollen, oder wie Koordinaten eingegeben werden (z.B. mit Komma getrennt, keine Leerzeichen). "
        f"Der Hinweis soll so verständlich sein, dass Schüler ohne weitere Hilfe wissen, wie sie antworten müssen. "
        f"Liefere als JSON nur die Schlüssel 'frage', 'loesung', 'typ' und 'hinweis'. "
        f"Beispiel: {{\"frage\": \"Berechne die Nullstellen der Funktion f(x) = x^2 - 4.\", \"loesung\": [2, -2], \"typ\": \"koordinaten\", \"hinweis\": \"Gib die Nullstellen als zwei Zahlen getrennt durch Komma ohne Leerzeichen ein, z.B. 2,-2.\"}}"
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
