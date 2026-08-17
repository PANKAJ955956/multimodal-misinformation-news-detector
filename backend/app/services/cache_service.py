import json
from typing import Optional, Dict, Any
from app.config import settings
from app.utils.logging import logger

class CacheService:
    def __init__(self):
        self.redis_client = None
        self._try_connect_redis()

    def _try_connect_redis(self):
        try:
            import redis
            logger.info(f"Connecting to Redis cache at {settings.REDIS_URL}...")
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, socket_timeout=2, socket_connect_timeout=2)
            self.redis_client.ping()
            logger.info("Successfully connected to Redis cache.")
        except Exception as e:
            logger.warning(f"Redis cache connection unavailable ({e}). Continuing with in-memory / non-cached fallback.")
            self.redis_client = None

    def get_prediction(self, cache_key: str) -> Optional[Dict[str, Any]]:
        if not self.redis_client:
            return None
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                logger.info(f"Redis cache hit for key: {cache_key}")
                data = json.loads(cached_data.decode("utf-8"))
                data["cached"] = True
                return data
        except Exception as e:
            logger.warning(f"Error reading from Redis cache: {e}")
        return None

    def set_prediction(self, cache_key: str, data: Dict[str, Any], ttl_seconds: int = 3600) -> None:
        if not self.redis_client:
            return
        try:
            # Strip non-serializable fields if any
            clean_data = json.loads(json.dumps(data, default=str))
            self.redis_client.setex(cache_key, ttl_seconds, json.dumps(clean_data))
            logger.info(f"Saved prediction to Redis cache with key: {cache_key}")
        except Exception as e:
            logger.warning(f"Error saving to Redis cache: {e}")

cache_service = CacheService()
