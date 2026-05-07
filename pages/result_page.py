from playwright.sync_api import Page

class ResultPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_card = page.locator(".product-card").first
        self.fail_view = page.locator("#fail_view")
        self.detail_view = page.locator("#detail_view")
        self.detail_title = page.locator("#det_title")
        self.apply_btn = page.get_by_role("button", name="지금 신청하기")
        self.go_home_from_result = page.get_by_role("button", name="홈으로 이동")
        self.go_home_from_detail = page.get_by_role("button", name="홈으로")

    def check_loan_result(self):
        """조회 완료 후 화면 상태를 체크하여 결과 타입을 반환합니다."""
        self.page.wait_for_timeout(2000)
        if self.product_card.is_visible():
            return "SUCCESS"
        elif self.fail_view.is_visible():
            return "FAIL"
        else:
            return "ERROR"

    def click_first_product(self):
        self.product_card.wait_for(state="visible")
        self.product_card.click()

    def apply_loan(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.apply_btn.wait_for(state="visible")
        self.apply_btn.click()
        print("[SUCCESS] 알럿 확인 및 최종 신청 완료")

    def return_to_home_after_fail(self):
        self.go_home_from_result.wait_for(state="visible")
        self.go_home_from_result.click()

    def return_to_home_after_apply(self):
        self.go_home_from_detail.wait_for(state="visible")
        self.go_home_from_detail.click()