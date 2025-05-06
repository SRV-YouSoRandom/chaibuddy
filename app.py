from flask import Flask, request
from whatsapp_api import send_message
from db import add_user, log_mood
from gemini_api import get_tip_for_mood
from redis_client import cache_nudge
import scheduler

app = Flask(__name__)
scheduler.start()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    entry = data.get("entry", [])[0]
    changes = entry.get("changes", [])[0]
    value = changes.get("value", {})
    messages = value.get("messages", [])

    if messages:
        msg = messages[0]
        phone = msg["from"]
        message_type = msg["type"]
        add_user(phone)

        if message_type == "interactive":
            mood_id = msg["interactive"]["button_reply"]["id"]
            log_mood(phone, mood_id)
            tip = get_tip_for_mood(mood_id)
            cache_nudge(phone, tip)
            send_message(phone, f"Got it. Here's something for you:\n{tip}")

    return "ok", 200