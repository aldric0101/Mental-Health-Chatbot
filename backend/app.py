from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import generate_reply
from emotion import detect_emotion
from response_filter import build_final_reply

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        payload = request.get_json(force=True, silent=False) or {}
        user_input = (payload.get("message") or "").strip()
        if not user_input:
            return jsonify({"error": "Empty message"}), 400

        raw_reply = generate_reply(user_input)          # BlenderBot-3B
        emo = detect_emotion(user_input)                # CardiffNLP
        final = build_final_reply(user_input, raw_reply, emo)
        return jsonify({"reply": final, "emotion": emo})
    except Exception:
        return jsonify({"error": "Server error processing message"}), 500

@app.route("/emotion", methods=["POST"])
def emotion_route():
    try:
        payload = request.get_json(force=True, silent=False) or {}
        user_input = (payload.get("message") or "").strip()
        if not user_input:
            return jsonify({"error": "Empty message"}), 400
        emo = detect_emotion(user_input)
        return jsonify({"emotion": emo})
    except Exception:
        return jsonify({"error": "Server error processing emotion"}), 500

if __name__ == "__main__":
    app.run(debug=True)
