import reflex as rx
from ui.components.state.youtube_questions import YoutubeState, YoutubeVideo


def youtube_video(video: YoutubeVideo):
    return rx.box(
        rx.hstack(
            rx.checkbox(
                checked=video.completed,
                on_change=lambda checked: YoutubeState.toggle_video_completion(
                    video.title, checked
                ),
            ),
            rx.vstack(
                rx.text(video.title, font_weight="bold"),
                align_items="start",
            ),
            rx.icon(
                "youtube",
                color="red",
                on_click=rx.redirect(external=True, path=video.url),
            ),
            width="100%",
            justify="between",
        ),
        py="2",
    )


def youtube_section():
    return rx.box(
        rx.heading("Daily YouTube Videos", size="5"),
        rx.text("Recommended design questions", color="gray", font_size="sm"),
        rx.vstack(
            rx.foreach(YoutubeState.videos, youtube_video),
            width="100%",
            overflow_y="auto",
            max_height="30vh",
            spacing="4",
        ),
        width="100%",
    )
