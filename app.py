import os
from flask import Flask, request, jsonify
from intent_classifier import IntentClassifier
from entity_extractor import extract_crop
from responder import build_response
import traceback

app = Flask(__name__)


classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        print("Loading intent classifier...")
        classifier = IntentClassifier()
        print("Classifier loaded successfully!")
    return classifier



@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "message": "Chatbot is running"}), 200



@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Farmer Query Chatbot</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
            }
            h1 { color: #2c5f2d; margin-bottom: 10px; }
            .subtitle { color: #666; margin-bottom: 20px; font-size: 14px; }
            .chat-box {
                border: 1px solid #ddd;
                border-radius: 4px;
                height: 400px;
                overflow-y: auto;
                padding: 15px;
                margin-bottom: 15px;
                background: #fafafa;
            }
            .message {
                margin: 10px 0;
                padding: 12px;
                border-radius: 4px;
                line-height: 1.5;
                word-wrap: break-word;
            }
            .user-msg {
                background-color: #d3e3fd;
                border-left: 4px solid #2196F3;
                text-align: right;
                margin-left: 20%;
            }
            .bot-msg {
                background-color: #e8f5e9;
                border-left: 4px solid #4CAF50;
                margin-right: 20%;
            }
            .input-area { display: flex; gap: 10px; }
            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
            }
            button {
                padding: 12px 24px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }
            button:hover { background-color: #45a049; }
            .loading {
                text-align: center;
                padding: 10px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 Farmer Advisory Chatbot</h1>
            <p class="subtitle">Ask questions about crops, fertilizers, pests, irrigation, planting, harvesting, diseases, soil, seeds, markets, subsidies, or equipment.</p>
            <div class="chat-box" id="chatBox"></div>
            <div id="loadingMsg" class="loading" style="display:none;">Processing...</div>
            <div class="input-area">
                <input type="text" id="queryInput" placeholder="Type your farming question here..." autocomplete="off">
                <button id="sendBtn">Send</button>
            </div>
        </div>

        <script>
            const chatBox = document.getElementById('chatBox');
            const queryInput = document.getElementById('queryInput');
            const sendBtn = document.getElementById('sendBtn');
            const loadingMsg = document.getElementById('loadingMsg');

            function addMessage(text, isUser) {
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message ' + (isUser ? 'user-msg' : 'bot-msg');
                msgDiv.textContent = text;
                chatBox.appendChild(msgDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function sendQuery() {
                const query = queryInput.value.trim();
                if (!query) return alert('Please enter a question');

                queryInput.disabled = true;
                sendBtn.disabled = true;
                loadingMsg.style.display = 'block';

                addMessage(query, true);
                queryInput.value = '';

                fetch('/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query })
                })
                .then(res => res.json())
                .then(data => addMessage(data.advice || 'No response', false))
                .catch(err => addMessage('Error: ' + err.message, false))
                .finally(() => {
                    queryInput.disabled = false;
                    sendBtn.disabled = false;
                    loadingMsg.style.display = 'none';
                });
            }

            sendBtn.onclick = sendQuery;
            queryInput.onkeypress = e => { if (e.key === 'Enter') sendQuery(); };

            window.onload = () => {
                addMessage("Hello! I'm here to help with your farming questions 🌱", false);
                queryInput.focus();
            };
        </script>
    </body>
    </html>
    """


@app.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json(force=True)
        text = data.get("query") or data.get("text") or ""

        if not text:
            return jsonify({"error": "No query text provided"}), 400

        clf = get_classifier()
        intent_res = clf.predict(text)

        intent = intent_res.get("intent")
        score = intent_res.get("score")

        crop = extract_crop(text)
        advice = build_response(intent, crop, text)

        return jsonify({
            "query": text,
            "intent": intent,
            "intent_score": score,
            "crop": crop,
            "advice": advice
        }), 200

    except Exception:
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "advice": "Sorry, there was an error processing your query."
        }), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Running locally on http://localhost:{port}")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
