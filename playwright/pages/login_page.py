from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#input_id")
        self.password_input = page.locator("#input_pw")
        self.login_submit_button = page.get_by_role("button", name="로그인 완료")
        self.back_to_main_button = page.get_by_role("button", name="이전 화면으로")
        self.error_message = page.locator("#login_error")

    def login(self, username, password):
        self.username_input.wait_for(state="visible")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_submit_button.click()

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()