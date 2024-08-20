import reflex as rx


class LeetCodeQuestion(rx.Base):
    title: str
    url: str
    difficulty: str
    companies: list[str]
    completed: bool


class YoutubeVideo(rx.Base):
    title: str
    url: str
    completed: bool
