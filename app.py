from flask import Flask, request, jsonify
from intent_classifier import IntentClassifier
from entity_extractor import extract_crop
from responder import build_response
import traceback

app = Flask(__name__)

print("Loading intent classifier...")
classifier = IntentClassifier()
print("Classifier loaded successfully!")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
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
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
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
            
            h1 {
                color: #2c5f2d;
                margin-bottom: 10px;
            }
            
            .subtitle {
                color: #666;
                margin-bottom: 20px;
                font-size: 14px;
            }
            
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
            
            .input-area {
                display: flex;
                gap: 10px;
            }
            
            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #4CAF50;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
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
            
            button:hover {
                background-color: #45a049;
            }
            
            button:active {
                background-color: #3d8b40;
            }
            
            button:disabled {
                background-color: #ccc;
                cursor: not-allowed;
            }
            
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
                <input 
                    type="text" 
                    id="queryInput" 
                    placeholder="Type your farming question here..."
                    autocomplete="off"
                >
                <button id="sendBtn" type="button">Send</button>
            </div>
        </div>

        <script>
            const chatBox = document.getElementById('chatBox');
            const queryInput = document.getElementById('queryInput');
            const sendBtn = document.getElementById('sendBtn');
            const loadingMsg = document.getElementById('loadingMsg');

            // Add initial message
            function addMessage(text, isUser) {
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message ' + (isUser ? 'user-msg' : 'bot-msg');
                msgDiv.textContent = text;
                chatBox.appendChild(msgDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function sendQuery() {
                const query = queryInput.value.trim();
                
                if (!query) {
                    alert('Please enter a question');
                    return;
                }

                // Disable input while processing
                queryInput.disabled = true;
                sendBtn.disabled = true;
                loadingMsg.style.display = 'block';

                // Show user message
                addMessage(query, true);
                queryInput.value = '';

                console.log('Sending:', query);

                // Send to API
                fetch('/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                })
                .then(response => {
                    console.log('Response status:', response.status);
                    if (!response.ok) {
                        throw new Error('Server error: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Response data:', data);
                    if (data.advice) {
                        addMessage(data.advice, false);
                    } else {
                        addMessage('Error: No advice returned', false);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('Error: ' + error.message, false);
                })
                .finally(() => {
                    // Re-enable input
                    queryInput.disabled = false;
                    sendBtn.disabled = false;
                    loadingMsg.style.display = 'none';
                    queryInput.focus();
                });
            }

            // Event listeners
            sendBtn.addEventListener('click', sendQuery);
            queryInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendQuery();
                }
            });

            // Add welcome message and focus
            window.addEventListener('load', function() {
                addMessage('Hello! I\\'m here to help with your farming questions. What would you like to know?', false);
                queryInput.focus();
            });
        </script>
    </body>
    </html>
    """

# ✅ CHATBOT API ROUTE
@app.route("/query", methods=["POST"])
def query():
    try:
        print("Received query request")
        
        data = request.get_json(force=True)
        text = data.get("query") or data.get("text") or ""

        if not text:
            return jsonify({"error": "No query text provided"}), 400

        print(f"Processing query: {text}")

        # Intent prediction
        intent_res = classifier.predict(text)
        intent = intent_res.get("intent")
        score = intent_res.get("score")
        print(f"Intent prediction: {intent} ({score:.3f})")

        # Entity extraction
        crop = extract_crop(text)
        print(f"Crop extracted: {crop}")

        # Response generation
        advice = build_response(intent, crop, text)
        print(f"Response generated")

        response = {
            "query": text,
            "intent": intent,
            "intent_score": score,
            "crop": crop,
            "advice": advice
        }
        print(f"Returning response")
        return jsonify(response), 200

    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        print(f"Error processing query: {error_msg}")
        return jsonify({
            "error": "Internal server error",
            "message": error_msg,
            "advice": "Sorry, there was an error processing your query. Please try again."
        }), 500

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌾 FARMER ADVISORY CHATBOT")
    print("="*50)
    print("API running at http://127.0.0.1:5000")
    print("Health check: http://127.0.0.1:5000/health")
    print("Web interface: http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    # Run Flask app
    # use_reloader=False to prevent model from loading twice
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,  # Prevent reloading from loading classifier twice
        threaded=True  # Enable thread support for concurrent requests
    )
