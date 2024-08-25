import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_cache(key: str):
    return await redis_client.get(key)

async def set_cache(key: str, value: str):
    await redis_client.set(key, value, ex=settings.REDIS_CACHE_EXPIRE_IN_SECONDS)