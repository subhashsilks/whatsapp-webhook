from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = "whatsapp_replies.xlsx"

def save_reply(number, message):
    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Mobile": number,
        "Message": message
    }
    if os.path.exists(LOG_FILE):
        df = pd.read_excel(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
    df.to_excel(LOG_FILE, index=False)

@app.route("/", methods=["GET"])
def verify():
    """Meta verification when adding webhook"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == "subhashsilks123":  # your secret verify token
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    """Receive incoming messages"""
    data = request.get_json()
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
            number = msg["from"]
            text = msg.get("text", {}).get("body", "")
            print(f"📩 {number}: {text}")
            save_reply(number, text)
    except Exception as e:
        print("⚠️ Error parsing message:", e)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
