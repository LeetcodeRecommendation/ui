import reflex as rx
import reflex_chakra as rc
from ui.components.state.user_leetcode_preferences import LCUserPreferences


def company_badge(company: str):
    return rx.badge(
        company,
        rx.icon(
            "x",
            cursor="pointer",
            on_click=lambda: LCUserPreferences.toggle_company(company),
        ),
        variant="soft",
        color_scheme="gray",
    )


def cookie_settings():
    return rx.card(
        rx.vstack(
            rx.heading("Cookie Settings", size="6"),
            rx.text("Configure your custom cookie settings.", color="gray"),
            rx.vstack(
                rx.text("Cookie value", font_weight="bold"),
                rx.input(
                    placeholder="Enter cookie value",
                    value=LCUserPreferences.cookie_value,
                    on_change=LCUserPreferences.set_cookie_name,
                ),
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.text("CSRF value", font_weight="bold"),
                rx.input(
                    placeholder="Enter CSRF value",
                    value=LCUserPreferences.csrf_value,
                    on_change=LCUserPreferences.set_csrf_value(),
                ),
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.text("Expiration Date", font_weight="bold"),
                rc.date_picker(
                    value=LCUserPreferences.expiration_date,
                    on_change=LCUserPreferences.set_expiration_date,
                ),
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.text("Relevant Companies", font_weight="bold"),
                rc.menu(
                    rc.menu_button(" --- Select Companies --- "),
                    rc.menu_list(
                        rx.foreach(
                            LCUserPreferences.COMPANIES,
                            lambda company: rc.menu_item(
                                company,
                                on_click=lambda: LCUserPreferences.toggle_company(
                                    company
                                ),
                            ),
                        )
                    ),
                ),
                rx.flex(
                    rx.foreach(
                        LCUserPreferences.selected_companies,
                        company_badge,
                    ),
                    spacing="2",
                ),
                align_items="start",
                width="100%",
            ),
            rx.button(
                "Save preferences",
                on_click=LCUserPreferences.save_preferences,
                width="100%",
            ),
            spacing="4",
            align_items="stretch",
        ),
        width="100%",
        max_width="400px",
        justify="end",
    )
