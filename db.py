import psycopg2
from config import DB_PARAMS

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def add_user(phone_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (phone_number) VALUES (%s) ON CONFLICT DO NOTHING", (phone_number,))
    conn.commit()
    cur.close()
    conn.close()

def log_mood(phone_number, mood):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE phone_number=%s", (phone_number,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO mood_logs (user_id, mood) VALUES (%s, %s)", (user_id, mood))
    conn.commit()
    cur.close()
    conn.close()

def get_weekly_moods(phone_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT mood, COUNT(*) FROM mood_logs 
        JOIN users ON mood_logs.user_id = users.id
        WHERE phone_number=%s AND timestamp > NOW() - INTERVAL '7 days'
        GROUP BY mood
    """, (phone_number,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result