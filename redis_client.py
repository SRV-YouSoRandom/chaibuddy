import redis
from config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def cache_nudge(phone_number, nudge):
    r.set(f"nudge:{phone_number}", nudge, ex=3600)

def get_cached_nudge(phone_number):
    return r.get(f"nudge:{phone_number}")