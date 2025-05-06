from apscheduler.schedulers.background import BackgroundScheduler
from db import get_weekly_moods
from whatsapp_api import send_message, send_mood_prompt
from gemini_api import get_tip_for_mood
from redis_client import cache_nudge

scheduler = BackgroundScheduler()

# Replace this with user lookup in DB
USER_PHONE_LIST = []  # Update dynamically from DB

def daily_check_in():
    for phone in USER_PHONE_LIST:
        send_mood_prompt(phone)

def send_nudges():
    for phone in USER_PHONE_LIST:
        # For demo: let's assume we pull latest mood
        mood_data = get_weekly_moods(phone)
        if mood_data:
            top_mood = sorted(mood_data, key=lambda x: x[1], reverse=True)[0][0]
            tip = get_tip_for_mood(top_mood)
            cache_nudge(phone, tip)
            send_message(phone, tip)

def weekly_summary():
    for phone in USER_PHONE_LIST:
        moods = get_weekly_moods(phone)
        summary = "Your mood summary for this week:\n"
        summary += "\n".join(f"{mood}: {count}" for mood, count in moods)
        send_message(phone, summary)

def start():
    scheduler.add_job(daily_check_in, 'cron', hour=8)
    scheduler.add_job(send_nudges, 'interval', hours=4)
    scheduler.add_job(weekly_summary, 'cron', day_of_week='sun', hour=18)
    scheduler.start()