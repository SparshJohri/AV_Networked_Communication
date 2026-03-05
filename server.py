from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
MESSAGES = []

@app.route("/send", methods=["POST"])
def receive_message():
    """
    Client sends a message here.
    """
    data = request.get_json()
    MESSAGES.append(data)
    print(data) #print(MESSAGES, "\n")
    return jsonify({"status": "ok", "messages_received": len(MESSAGES)})

@app.route("/messages", methods=["GET"])
def get_messages():
    """
    Client asks for all messages.
    """
    return jsonify(MESSAGES)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "server alive"})

if __name__ == "__main__":
    # 0.0.0.0 allows access from other machines on the LAN
    app.run(host="0.0.0.0", port=5000, debug=True)
