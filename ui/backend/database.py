import asyncio
import logging
from typing import Final
from cassandra.cluster import Cluster
from cassandra.query import PreparedStatement

from ui import LOGGER_NAME
from ui.backend.utils.decorators import Singleton
from ui.backend.utils.environment import Environment
from ui.components.state.models import LeetCodeQuestion, YoutubeVideo


class CassandraDB(metaclass=Singleton):
    KEYSPACE: Final[str] = "leetcode_rs"
    USER_QUESTIONS_TABLE: Final[str] = "user_questions"
    USER_VIDEOS_TABLE: Final[str] = "user_videos"

    def __init__(self):
        print("initializing db")
        self._log = logging.getLogger(LOGGER_NAME)
        self._log.info("Initializing CassandraDB")
        self._cluster = Cluster(Environment.get_cassandra_uri())
        self._session = self._cluster.connect(CassandraDB.KEYSPACE)
        self._async_lock = asyncio.Lock()
        self._get_user_lc_questions = self._session.prepare(
            f"SELECT question_name, question_url, difficulty, company_names, score FROM {CassandraDB.USER_QUESTIONS_TABLE} WHERE user_name = ? AND solved = false LIMIT 400"
        )
        self._get_youtube_videos = self._session.prepare(
            f"SELECT video_name, video_url, watched FROM {CassandraDB.USER_VIDEOS_TABLE} WHERE user_name = ?"
        )
        self._log.info("Finished initializing CassandraDB")

    async def run_statement(self, query: PreparedStatement):
        return await asyncio.get_running_loop().run_in_executor(
            None, self._session.execute, query
        )

    async def get_leetcode_user_questions(
        self, user_name: str
    ) -> list[LeetCodeQuestion]:
        res = await self.run_statement(self._get_user_lc_questions.bind([user_name]))
        results = {
            question[4]: LeetCodeQuestion(
                title=question[0],
                url=question[1],
                difficulty=question[2],
                companies=question[3],
                completed=False,
            )
            for question in res
        }
        sorted_keys = sorted(results.keys(), reverse=True)
        return [results[key] for key in sorted_keys]

    async def get_youtube_video(self, user_name: str) -> list[YoutubeVideo]:
        res = await self.run_statement(self._get_youtube_videos.bind([user_name]))
        res = [
            YoutubeVideo(title=video[0], url=video[1], completed=video[2])
            for video in res
        ]
        return res
