from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["portfolioDB"]
questions = db["questions"]

# POST route to save form
@app.route('/api/questions', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    email = data.get('email', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    questions.insert_one({"question": question, "email": email})
    return jsonify({"message": "Saved successfully"}), 200

@app.route('/')
def home():
    return "Backend is running."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
