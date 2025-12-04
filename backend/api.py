from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from main import ask_chatbot

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# 🔹 Embeddings
DATA_FOLDER = "data"
EMBEDDINGS_FILE = f"{DATA_FOLDER}/embeddings.json"

with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    embeddings = json.load(f)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    answer = ask_chatbot(question, embeddings)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
