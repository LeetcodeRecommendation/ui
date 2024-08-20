import reflex as rx
from ui.components.front.leetcode_questions import leetcode_section
from ui.components.front.user_leetcode_preferences import cookie_settings
from ui.components.front.username import username_header
from ui.components.front.youtube_questions import youtube_section
from ui.components.state.leetcode_questions import LeetCodeQuestionsState
from ui.components.state.youtube_questions import YoutubeState


@rx.page(on_load=[LeetCodeQuestionsState.fetch_leetcode, YoutubeState.fetch_videos])
def index():
    return rx.box(
        username_header(),
        rx.flex(
            rx.card(leetcode_section(), min_width="40%"),
            rx.flex(
                rx.card(
                    youtube_section(),
                    width="100%",
                    spacing="6",
                ),
                rx.card(
                    cookie_settings(),
                    width="100%",
                    spacing="6",
                ),
                min_width="50%",
                direction="column",
            ),
            justify="center",
            min_width="100%",
            spacing="8",
            width="100%",
        ),
        rx.text(
            "© 2024 InterviewPrep. All rights reserved.",
            font_size="sm",
            color="gray",
            text_align="center",
        ),
        align="start",
        min_width="1200px",
        width="100%",
        padding="1",
        spacing="15",
    )
