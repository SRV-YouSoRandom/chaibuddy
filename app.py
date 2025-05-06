import os
import logging
from flask import Flask, request
from whatsapp_api import send_message
from db import add_user, log_mood
from gemini_api import get_tip_for_mood
from redis_client import cache_nudge
import scheduler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MoodBot")

# Environment variables
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "my_moodbot_token_123")

# Start background scheduler tasks
scheduler.start()

@app.route('/', methods=['GET'])
def home():
    return "MoodBot is running.", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("Webhook verified successfully.")
            return challenge, 200
        else:
            logger.warning("Webhook verification failed.")
            return "Invalid verification token", 403

    elif request.method == 'POST':
        # Incoming message handler
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
            logger.exception("Error processing webhook POST")

        return "ok", 200

if __name__ == '__main__':
    logger.info("Starting MoodBot Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)