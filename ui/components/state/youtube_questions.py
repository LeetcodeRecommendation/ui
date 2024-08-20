import asyncio
import logging
import math

import httpx
import reflex as rx

from ui import LOGGER_NAME
from ui.backend.cache import RedisCache
from ui.backend.database import CassandraDB
from ui.backend.utils.environment import Environment
from ui.components.state.models import YoutubeVideo
from ui.components.state.username import UsernameState


class YoutubeState(rx.State):
    videos: list[YoutubeVideo] = list()
    video_mapping: dict[str, YoutubeVideo] = dict()

    background_running: bool = False

    @staticmethod
    def get_video_number(video: YoutubeVideo):
        if ":" not in video.title:
            return math.inf

        try:
            return int(video.title.split(":")[0])
        except ValueError:
            return math.inf

    async def update_videos(self, videos: list[YoutubeVideo]):
        videos.sort(key=lambda x: YoutubeState.get_video_number(x))
        self.video_mapping.clear()
        self.videos.clear()
        for video in videos:
            self.video_mapping[video.title] = video
        self.videos = videos

    @rx.background
    async def fetch_videos(self):
        async with self:
            if not self.background_running:
                self.background_running = True
            else:
                self.videos.clear()
                return
        cache = RedisCache()
        db = CassandraDB()

        while True:
            async with self:
                user_name = await self.get_state(UsernameState)
                current_user = user_name.username
            user_data = await cache.get_user_cache_data(current_user)
            async with self:
                if user_data is not None and len(self.videos) == 0:
                    await self.update_videos(user_data[0])
                else:
                    db_data = await db.get_youtube_video(current_user)
                    if len(db_data) > 0:
                        await cache.set_user_cache_data(current_user, db_data, None)
                        await self.update_videos(db_data)
            await asyncio.sleep(1)

    @rx.background
    async def toggle_video_completion(self, title: str, checked: bool):
        log = logging.getLogger(LOGGER_NAME)

        uri = f"http://{Environment.get_user_request_uri()}/api/v1/youtube_marking"
        async with self:
            user_name = (await self.get_state(UsernameState)).username

        async with httpx.AsyncClient() as client:
            resp = await client.put(
                uri,
                json={
                    "user_name": user_name,
                    "video_name": title,
                    "user_marked": checked,
                },
            )
        async with self:
            self.video_mapping[title].completed = checked
        cache = RedisCache()
        await cache.set_user_cache_data(user_name, self.videos, None)
        log.info(f"Sent youtube marking request with status: {resp.status_code}")
