from flask import Flask, request
from whatsapp_api import send_message
from db import add_user, log_mood
from gemini_api import get_tip_for_mood
from redis_client import cache_nudge
import scheduler
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MoodBot")

# Start scheduler background tasks
scheduler.start()

@app.route('/', methods=['GET'])
def home():
    return "MoodBot is running.", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logger.info(f"Received data: {data}")

    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages:
            msg = messages[0]
            phone = msg["from"]
            message_type = msg["type"]

            logger.info(f"Message from {phone}: {message_type}")
            add_user(phone)

            if message_type == "interactive":
                mood_id = msg["interactive"]["button_reply"]["id"]
                logger.info(f"Received mood: {mood_id}")
                log_mood(phone, mood_id)
                tip = get_tip_for_mood(mood_id)
                cache_nudge(phone, tip)
                send_message(phone, f"Got it. Here's something for you:\n{tip}")
        else:
            logger.info("No messages in webhook payload.")

    except Exception as e:
        logger.exception("Error processing webhook")

    return "ok", 200

if __name__ == '__main__':
    logger.info("Starting MoodBot Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)