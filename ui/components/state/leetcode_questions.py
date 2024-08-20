import asyncio
import reflex as rx

from ui.backend.cache import RedisCache
from ui.backend.database import CassandraDB
from ui.backend.utils.environment import Environment
from ui.components.state.models import LeetCodeQuestion
from ui.components.state.username import UsernameState


class LeetCodeQuestionsState(rx.State):
    all_questions: list[LeetCodeQuestion] = list()
    questions: list[LeetCodeQuestion] = list()
    DIFFICULTY_OPTIONS: list[str] = ["Easy", "Medium", "Hard"]
    accepted_difficulties: set[str] = set(DIFFICULTY_OPTIONS)
    background_running: bool = False

    @rx.background
    async def fetch_leetcode(self):
        cache = RedisCache()
        db = CassandraDB()
        while True:
            async with self:
                user_name = await self.get_state(UsernameState)
                current_user = user_name.username
            user_data = await cache.get_user_cache_data(current_user)
            if user_data is not None and len(self.questions) == 0:
                async with self:
                    self.all_questions = user_data[1]
                    self.toggle_question_recompute()
            else:
                db_data = await db.get_leetcode_user_questions(current_user)
                if len(db_data) > 0:
                    await cache.set_user_cache_data(current_user, None, db_data)
                    async with self:
                        self.all_questions = db_data
                        self.toggle_question_recompute()
            await asyncio.sleep(1)

    def toggle_question_completion(self, title: str, changed: bool):
        print(f"Question {title} changed")

    def toggle_question_recompute(self):
        selected_questions = []
        for question in self.all_questions:
            if question.difficulty in self.accepted_difficulties:
                selected_questions.append(question)
            if len(selected_questions) > 20:
                break
        self.questions = selected_questions

    def toggle_difficulty(self, difficulty: str, checked: bool):
        if checked:
            self.accepted_difficulties.add(difficulty)
        else:
            self.accepted_difficulties.remove(difficulty)
        self.toggle_question_recompute()
