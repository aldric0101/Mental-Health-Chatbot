# Mental-Health-Chatbot
Mental Health Chatbot Prototype

Overview

This project is a Mental Health AI Chatbot built with:

Frontend: React (chat interface, speech-to-text input, sentiment labels).
Backend: Flask (Python) serving APIs.
Models: BlenderBot-3B for dialogue, RoBERTa (CardiffNLP) for sentiment detection.
Custom response filter for greetings, encouragement injection, and crisis overrides.
The goal is to create a chatbot that provides supportive and empathetic responses while ensuring safety in sensitive situations.

Install dependencies:
pip install -r requirements.txt

Install dependencies:
cd frontend
npm install

How to Run
1. Start the Backend

Open a terminal in the backend folder and run:
python app.py

You should see:
 * Running on http://127.0.0.1:5000

2. Start the Frontend

Open another terminal in the frontend folder and run:
npm start

This will launch the React app in your browser at:
http://localhost:3000

