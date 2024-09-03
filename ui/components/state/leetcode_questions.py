import asyncio
import logging

import httpx
import reflex as rx

from ui import LOGGER_NAME
from ui.backend.cache import RedisCache
from ui.backend.database import CassandraDB
from ui.backend.utils.environment import Environment
from ui.components.state.models import LeetCodeQuestion
from ui.components.state.username import UsernameState


class LeetCodeQuestionsState(rx.State):
    all_questions: list[LeetCodeQuestion] = list()
    questions: list[LeetCodeQuestion] = list()
    DIFFICULTY_OPTIONS: list[str] = ["Easy", "Medium", "Hard"]
    accepted_difficulties: set[str] = {"Easy", "Medium", "Hard"}
    background_running: bool = False
    title_to_question_mapping: dict[str, LeetCodeQuestion] = dict()

    @rx.background
    async def fetch_leetcode(self):
        cache = RedisCache()
        db = CassandraDB()
        while True:
            async with self:
                user_name = await self.get_state(UsernameState)
                current_user = user_name.username
            user_data = await cache.get_leet_code_cache_data(current_user)
            if user_data is None:
                db_data = await db.get_leetcode_user_questions(current_user)
                if len(db_data) > 0:
                    await cache.set_user_leetcode_data(current_user, db_data)
                    async with self:
                        self.title_to_question_mapping.clear()
                        for question in db_data:
                            self.title_to_question_mapping[question.title] = question
                        self.all_questions = db_data
                        self.toggle_question_recompute()
            elif len(self.questions) == 0:
                async with self:
                    self.title_to_question_mapping.clear()
                    for question in user_data:
                        self.title_to_question_mapping[question.title] = question
                    self.all_questions = user_data
                    self.toggle_question_recompute()

            await asyncio.sleep(1)

    @rx.background
    async def toggle_question_completion(self, title: str, checked: bool):
        async with self:
            self.title_to_question_mapping[title].manually_marked_by_user = checked
            self.toggle_question_recompute()

        log = logging.getLogger(LOGGER_NAME)

        uri = f"http://{Environment.get_user_request_uri()}/api/v1/update_leetcode_question"
        async with self:
            user_name = (await self.get_state(UsernameState)).username

        async with httpx.AsyncClient() as client:
            resp = await client.put(
                uri,
                json={
                    "user_name": user_name,
                    "question_name": title,
                    "user_marked": checked,
                },
            )
        cache = RedisCache()
        async with self:
            await cache.set_user_leetcode_data(user_name, self.all_questions)
        log.info(f"Sent leetcode marking request with status: {resp.status_code}")

    def toggle_question_recompute(self):
        selected_questions = []
        logging.getLogger(LOGGER_NAME).info(
            f"all_questions_len : {len(self.all_questions)}"
        )
        for question in self.all_questions:
            if question.difficulty in self.accepted_difficulties:
                selected_questions.append(question)
            if len(selected_questions) >= 20:
                break
        logging.getLogger(LOGGER_NAME).info(f"questions_len : {len(self.questions)}")
        self.questions = selected_questions

    def toggle_difficulty(self, difficulty: str, checked: bool):
        if checked:
            self.accepted_difficulties.add(difficulty)
        else:
            self.accepted_difficulties.remove(difficulty)
        self.toggle_question_recompute()
