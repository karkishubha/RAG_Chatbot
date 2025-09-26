import redis.asyncio as redis
import json
from typing import List
from app.config import settings

class RedisChatMemory:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis_url = redis_url
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await redis.from_url(self.redis_url, decode_responses=True)
        return self.redis

    async def get_context(self, conv_id: str, limit: int = 10) -> List[dict]:
        r = await self._get_redis()
        items = await r.lrange(f"conv:{conv_id}", 0, -1)
        return [json.loads(i) for i in items][-limit:]

    async def append_message(self, conv_id: str, message: dict):
        r = await self._get_redis()
        await r.rpush(f"conv:{conv_id}", json.dumps(message))
        await r.expire(f"conv:{conv_id}", 60 * 60 * 24)
