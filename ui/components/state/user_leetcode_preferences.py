import httpx
import reflex as rx

from ui.backend.utils.environment import Environment
from ui.components.state.username import UsernameState


class LCUserPreferences(rx.State):
    cookie_value: str = ""
    csrf_value: str = ""
    expiration_date: str = ""
    selected_companies: list[str] = []
    COMPANIES: list[str] = [
        "Facebook",
        "Amazon",
        "Google",
        "Microsoft",
        "Apple",
        "Uber",
        "Netflix",
    ]

    def set_cookie_name(self, value: str):
        self.cookie_value = value

    def set_csrf_value(self, value: str):
        self.csrf_value = value

    def set_expiration_date(self, date: str):
        self.expiration_date = date

    def toggle_company(self, company: str):
        if company in self.selected_companies:
            self.selected_companies.remove(company)
        else:
            self.selected_companies.append(company)

    async def save_preferences(self):
        uri = f"http://{Environment.get_user_request_uri()}/api/v1/update_user_token"
        user_name = await self.get_state(UsernameState)
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                uri,
                json={
                    "name": user_name.username,
                    "token": self.cookie_value,
                    "csrfToken": self.csrf_value,
                    "expirationTime": self.expiration_date,
                    "companies": [
                        company.lower() for company in self.selected_companies
                    ],
                },
            )
        print(f"Request sent status: {resp.status_code}, {resp.content}")
