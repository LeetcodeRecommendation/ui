import reflex as rx

from ui.components.state.username import UsernameState


def username_header():
    return rx.flex(
        rx.hstack(
            rx.icon("user"),
            rx.cond(
                UsernameState.is_editing_username,
                rx.input(
                    value=UsernameState.new_username,
                    on_change=UsernameState.set_new_username,
                ),
                rx.heading(f"{UsernameState.username}'s Dashboard", size="6"),
            ),
            rx.button(
                rx.cond(
                    UsernameState.is_editing_username,
                    rx.icon("save"),
                    rx.icon("pencil"),
                ),
                on_click=[UsernameState.handle_username_edit],
                variant="outline",
                size="2",
            ),
            justify="center",
            align="center",
            width="50%",
        ),
        justify="center",
        align="end",
        padding="1",
    )
