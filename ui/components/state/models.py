import reflex as rx


class LeetCodeQuestion(rx.Base):
    title: str
    url: str
    difficulty: str
    companies: list[str]
    completed: bool
    manually_marked_by_user: bool


class YoutubeVideo(rx.Base):
    title: str
    url: str
    completed: bool
