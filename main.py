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
         f"Erstelle eine abwechslungsreiche Mathematik-Aufgabe mit der immer richtigen lösung für Klasse {klasse}, Thema {thema}, Schwierigkeitsgrad {schwierig}. "
        f"Variiere Zahlen, Fragestellungen und Formate. "
        f"Die Aufgabe soll immer klar machen, in welchem Format die Lösung erwartet wird (z.B. gerundet auf 2 Nachkommastellen, als Bruch, ganze Zahl). "
        f"Liefere ein JSON-Objekt mit folgenden Feldern: "
        f"\"frage\" (die Aufgabe), "
        f"\"loesung\" (die richtige Antwort, rechne die aufgabe selber sodass du immer die richtige lösung zurück gibst. Es darf niemals die falsche lösung sein), "
        f"und \"hinweis\" (einen Lösungsweg oder Tipp, der erklärt, wie man die Aufgabe lösen kann, ohne die exakte Lösung zu verraten). "
        f"Der Hinweis soll dem Schüler helfen, die Aufgabe zu verstehen und zu bearbeiten, aber nicht die Lösung vorwegnehmen. "
        f"Beispiel-Antwort: {{\"frage\": \"Berechne 2 + 3. Gib eine ganze Zahl an.\", \"loesung\": 5, \"hinweis\": \"Addiere die beiden Zahlen einfach zusammen.\"}}."
        
    )


    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=800
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
