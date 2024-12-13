import requests
import json
from flask import Flask, request, jsonify, render_template

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='templates')

def query_gpt4all_api(user_query):
    # URL de base pour le serveur API local GPT4All
    base_url = "http://localhost:4891/v1/chat/completions"

    # Corps de la requête
    payload = {
        "model": "Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": user_query}],
        "max_tokens": 50,
        "temperature": 0.28
    }

    try:
        # Envoi de la requête POST
        response = requests.post(base_url, json=payload)

        # Vérification du statut de la réponse
        if response.status_code == 200:
            # Récupérer uniquement le contenu du message
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Erreur {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Une erreur est survenue lors de la requête: {e}"

# Route Flask pour la page principale
@app.route('/', methods=['GET', 'POST'])
def index():
    response_message = None
    if request.method == 'POST':
        user_query = request.form.get('user_query')
        if user_query:
            response_message = query_gpt4all_api(user_query)
    return render_template('index.html', response_message=response_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
