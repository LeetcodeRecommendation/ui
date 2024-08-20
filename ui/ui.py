import reflex as rx
from dotenv import load_dotenv

from ui import LOGGER_NAME
from ui.backend.utils.logging import initialize_logger
from ui.pages.dashboard import index

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="teal",
    )
)
load_dotenv()
initialize_logger(LOGGER_NAME)
app.add_page(index, title="Interview prep.")
