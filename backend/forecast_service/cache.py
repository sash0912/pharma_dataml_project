import redis
import json
import hashlib

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def make_cache_key(data: dict):
    raw = json.dumps(data, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()

def get_cached_prediction(data: dict):
    key = make_cache_key(data)
    value = redis_client.get(key)
    if value:
        return float(value)
    return None

def set_cached_prediction(data: dict, prediction: float, ttl=3600):
    key = make_cache_key(data)
    redis_client.setex(key, ttl, prediction)
