import asyncio
import json
from typing import Final, Optional
import redis.asyncio as redis

from ui.backend.utils.decorators import Singleton
from ui.backend.utils.environment import Environment
from ui.components.state.models import YoutubeVideo, LeetCodeQuestion


class RedisCache(metaclass=Singleton):
    USER_YOUTUBE_CACHE_PREFIX: Final[str] = r"user-recommendation-cache-youtube-{name}"
    USER_LEETCODE_CACHE_PREFIX: Final[str] = r"user-recommendation-cache-lc-{name}"

    def __init__(self):
        print("initializing cache")
        self._redis_client = redis.from_url(
            f"redis://{Environment.get_redis_ip()}:{Environment.get_redis_port()}"
        )
        self._lock = asyncio.Lock()

    async def get_leet_code_cache_data(
        self, user: str
    ) -> Optional[list[LeetCodeQuestion]]:
        async with self._lock:
            if await self._redis_client.exists(
                RedisCache.USER_LEETCODE_CACHE_PREFIX.format(name=user)
            ):
                leetcode_cache = json.loads(
                    await self._redis_client.get(
                        RedisCache.USER_LEETCODE_CACHE_PREFIX.format(name=user)
                    )
                )
                leetcode = [
                    LeetCodeQuestion(**question) for question in leetcode_cache["data"]
                ]
                return leetcode
            else:
                return None

    async def get_youtube_cache_data(self, user: str) -> Optional[list[YoutubeVideo]]:
        async with self._lock:
            if await self._redis_client.exists(
                RedisCache.USER_YOUTUBE_CACHE_PREFIX.format(name=user)
            ):
                youtube_cache = json.loads(
                    await self._redis_client.get(
                        RedisCache.USER_YOUTUBE_CACHE_PREFIX.format(name=user)
                    )
                )
                youtube = [YoutubeVideo(**video) for video in youtube_cache["data"]]
                return youtube
            else:
                return None

    async def set_user_youtube_cache(
        self,
        user: str,
        yt_videos: list[YoutubeVideo],
    ) -> None:
        async with self._lock:
            yt_videos = {"data": [yt_video.dict() for yt_video in yt_videos]}
            await self._redis_client.set(
                RedisCache.USER_YOUTUBE_CACHE_PREFIX.format(name=user),
                json.dumps(yt_videos),
            )

    async def set_user_leetcode_data(
        self,
        user: str,
        lc_questions: list[LeetCodeQuestion],
    ) -> None:
        async with self._lock:
            lc_data = {"data": [lc_question.dict() for lc_question in lc_questions]}
            await self._redis_client.set(
                RedisCache.USER_LEETCODE_CACHE_PREFIX.format(name=user),
                json.dumps(lc_data),
            )
