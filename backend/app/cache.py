import redis
import json
from typing import Optional, Any
from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class CacheService:
    def __init__(self, prefix: str = "freelancehub"):
        self.prefix = prefix
        self.client = redis_client

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    def get(self, key: str) -> Optional[Any]:
        try:
            data = self.client.get(self._key(key))
            if data:
                return json.loads(data)
            return None
        except Exception:
            return None

    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        try:
            self.client.setex(
                self._key(key),
                expire,
                json.dumps(value, default=str)
            )
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        try:
            self.client.delete(self._key(key))
            return True
        except Exception:
            return False

    def delete_pattern(self, pattern: str) -> bool:
        try:
            keys = self.client.keys(f"{self.prefix}:{pattern}*")
            if keys:
                self.client.delete(*keys)
            return True
        except Exception:
            return False

cache = CacheService()