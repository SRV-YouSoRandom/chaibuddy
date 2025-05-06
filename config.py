import os
from dotenv import load_dotenv

load_dotenv()

# WhatsApp Cloud
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Redis
REDIS_URL = os.getenv("REDIS_URL")

# PostgreSQL
DB_PARAMS = {
    "dbname": "moodbot",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": 5432
}