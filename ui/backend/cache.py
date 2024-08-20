import asyncio
import json
from typing import Final, Optional
import redis.asyncio as redis

from ui.backend.utils.decorators import Singleton
from ui.backend.utils.environment import Environment
from ui.components.state.models import YoutubeVideo, LeetCodeQuestion


class RedisCache(metaclass=Singleton):
    USER_CACHE_PREFIX: Final[str] = r"user-recommendation-cache-{name}"

    def __init__(self):
        print("initializing cache")
        self._redis_client = redis.from_url(
            f"redis://{Environment.get_redis_ip()}:{Environment.get_redis_port()}"
        )
        self._lock = asyncio.Lock()

    async def get_user_cache_data(
        self, user: str
    ) -> Optional[tuple[list[YoutubeVideo], list[LeetCodeQuestion]]]:
        async with self._lock:
            if await self._redis_client.exists(
                RedisCache.USER_CACHE_PREFIX.format(name=user)
            ):
                user_cache = json.loads(
                    await self._redis_client.get(
                        RedisCache.USER_CACHE_PREFIX.format(name=user)
                    )
                )
                youtube_questions = [
                    YoutubeVideo(**video) for video in user_cache["youtube"]
                ]
                leetcode = [
                    LeetCodeQuestion(**question) for question in user_cache["leetcode"]
                ]
                return youtube_questions, leetcode
            else:
                return None

    async def set_user_cache_data(
        self,
        user: str,
        yt_videos: Optional[list[YoutubeVideo]],
        lc_questions: Optional[list[LeetCodeQuestion]],
    ) -> None:
        async with self._lock:
            if await self._redis_client.exists(
                RedisCache.USER_CACHE_PREFIX.format(name=user)
            ):
                user_cache = json.loads(
                    await self._redis_client.get(
                        RedisCache.USER_CACHE_PREFIX.format(name=user)
                    )
                )
                youtube_videos = (
                    [YoutubeVideo(**video) for video in user_cache["youtube"]]
                    if yt_videos is None
                    else yt_videos
                )
                leetcode_questions = (
                    [
                        LeetCodeQuestion(**question)
                        for question in user_cache["leetcode"]
                    ]
                    if lc_questions is None
                    else lc_questions
                )
            else:
                youtube_videos = yt_videos if yt_videos is not None else []
                leetcode_questions = lc_questions if lc_questions is not None else []
            data = {
                "youtube": [video.dict() for video in youtube_videos],
                "leetcode": [question.dict() for question in leetcode_questions],
            }
            await self._redis_client.set(
                RedisCache.USER_CACHE_PREFIX.format(name=user), json.dumps(data)
            )
