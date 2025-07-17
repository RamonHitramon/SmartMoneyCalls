import os
import re
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_500 = "@three_wallets_500"
CHAT_1000 = "@three_wallets_1000"

def clean_message(text):
    lines = text.splitlines()
    lines = [line for line in lines if not line.startswith(("Alert Count", "#", "Time", "Transactions within"))]
    result = "\n".join(lines).replace("[chainEDGE]", "").strip()
    return result

@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.json
    message = data.get("message", {}).get("text", "")
    if not message:
        return "no message", 200

    if '"3w500s1h"' in message:
        chat_id = CHAT_500
    elif '"3w1000s2h"' in message:
        chat_id = CHAT_1000
    else:
        return "unknown tag", 200

    final_message = clean_message(message)

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": final_message}
    )

    return "ok", 200
