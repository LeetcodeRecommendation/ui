import reflex as rx
import reflex_chakra as rc


from ui.components.state.leetcode_questions import (
    LeetCodeQuestion,
    LeetCodeQuestionsState,
)


def leetcode_question(question: LeetCodeQuestion):
    return rx.box(
        rx.hstack(
            rx.checkbox(
                is_checked=question.completed,
                on_change=lambda changed: LeetCodeQuestionsState.toggle_question_completion(
                    question.title, changed
                ),
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(question.title, font_weight="bold", font_size="smaller"),
                    rx.text(
                        f"{question.difficulty}", font_size="x-small", color="gray"
                    ),
                    align="center",
                ),
                rx.flex(
                    rx.foreach(
                        question.companies,
                        lambda company: rx.badge(
                            company, variant="soft", color_scheme="gray", size="1"
                        ),
                    ),
                    spacing="1",
                ),
                align_items="start",
                on_click=rx.redirect(external=True, path=question.url),
            ),
            rx.cond(
                question.completed,
                rx.icon("circle_check_big", color="green"),
                rx.text(""),
            ),
            width="100%",
            justify="between",
        ),
        py="2",
    )


def leetcode_section():
    return rx.box(
        rx.hstack(
            rx.heading("LeetCode Questions", size="5"),
            rc.menu(
                rc.menu_button(" -- Select Difficulties -- ", size="5"),
                rc.menu_list(
                    rx.foreach(
                        LeetCodeQuestionsState.DIFFICULTY_OPTIONS,
                        lambda company: rx.checkbox(
                            company,
                            default_checked=True,
                            on_change=lambda changed: LeetCodeQuestionsState.toggle_difficulty(
                                company, changed
                            ),
                        ),
                    )
                ),
            ),
        ),
        rx.text(
            "Your personalized list of 20 LeetCode questions",
            color="gray",
            font_size="sm",
        ),
        rx.vstack(
            rx.foreach(LeetCodeQuestionsState.questions, leetcode_question),
            width="100%",
            overflow_y="auto",
            max_height="60vh",
            spacing="4",
        ),
        width="100%",
    )
