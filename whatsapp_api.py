import requests
from config import WHATSAPP_TOKEN, PHONE_NUMBER_ID

def send_message(phone_number, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

def send_mood_prompt(phone_number):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "How are you feeling today?"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "happy", "title": "😊 Happy"}},
                    {"type": "reply", "reply": {"id": "sad", "title": "😢 Sad"}},
                    {"type": "reply", "reply": {"id": "angry", "title": "😠 Angry"}},
                    {"type": "reply", "reply": {"id": "anxious", "title": "😟 Anxious"}},
                ]
            }
        }
    }
    requests.post(url, headers=headers, json=payload)