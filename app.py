from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ✅ Load variables from .env file (only used locally)
load_dotenv()

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Allow frontend from GitHub Pages to access this backend
CORS(app, origins=["https://fameisyash.github.io"])  # Replace with your GitHub Pages domain

# ✅ Connect to MongoDB using MONGO_URI
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["portfolioDB"]
questions = db["questions"]  # Collection name

# ✅ POST route to accept form data
@app.route('/api/questions', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    email = data.get('email', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    questions.insert_one({
        "question": question,
        "email": email
    })

    return jsonify({"message": "Saved successfully"}), 200

# ✅ Home route to test if backend is running
@app.route('/')
def home():
    return "Backend is running."

# ✅ For Render: use 0.0.0.0 and dynamic PORT
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's provided port
    app.run(host='0.0.0.0', port=port)
