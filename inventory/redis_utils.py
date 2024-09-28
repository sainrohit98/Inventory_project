from django.core.cache import cache
import json

def cache_item(item_id, item_data):
    cache_key = f'item_{item_id}'
    cache.set(cache_key, json.dumps(item_data), timeout=3600)  # Cache for 1 hour

def get_cached_item(item_id):
    cache_key = f'item_{item_id}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    return None

def delete_cached_item(item_id):
    cache_key = f'item_{item_id}'
    cache.delete(cache_key)