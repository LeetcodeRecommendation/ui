import reflex as rx


class UsernameState(rx.State):
    username: str = rx.LocalStorage("User")
    new_username: str = ""
    is_editing_username: bool = False

    async def handle_username_edit(self):
        if self.is_editing_username:
            if self.new_username.strip():
                self.username = self.new_username.strip()
            self.is_editing_username = False
            self.new_username = ""
        else:
            self.is_editing_username = True
            self.new_username = self.username
