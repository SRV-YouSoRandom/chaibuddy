import requests
from config import GEMINI_API_KEY

def get_tip_for_mood(mood):
    prompt = f"Give a short practical tip or motivation for someone feeling '{mood}'. Keep it under 200 characters."
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    data = response.json()
    return data['candidates'][0]['content']['parts'][0]['text']