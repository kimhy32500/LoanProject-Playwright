import os
from playwright.sync_api import Page

BASE_URL = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../app/index.html")
).replace("\\", "/")

class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_btn = page.locator("#btn_login")
        self.logout_btn = page.locator("#btn_logout")
        self.loan_start_btn = page.locator("#btn_loan")

    def navigate(self):
        self.page.goto(f"file:///{BASE_URL}")  # 클래스 밖으로 뺐으므로 그대로 사용 가능

    def click_login(self):
        self.login_btn.wait_for(state="visible")
        self.login_btn.click()

    def click_logout(self):
        self.logout_btn.wait_for(state="visible")
        self.logout_btn.click()

    def click_loan_start(self):
        self.loan_start_btn.wait_for(state="visible")
        self.loan_start_btn.click()