from playwright.sync_api import Page

DEFAULT_TIMEOUT = 5000

class LoanPage:
    def __init__(self, page: Page):
        self.page = page
        self.job_dropdown = page.locator("#job")
        self.income_input = page.locator("#income")
        # [수정] 버튼 자체보다 버튼을 감싸는 영역을 타겟팅하기 위해 로케이터 변경
        self.submit_area = page.locator("#submit_area")
        
        self.comp_name = page.locator("#comp_name")
        self.biz_name = page.locator("#biz_name")
        
        self.business_start_date = page.locator("label:has-text('개업일') + input")
        self.join_date_month = page.locator("label:has-text('입사월') + input")
        
        self.health_dropdown = page.locator("#health_type")
        
        
    def enter_work_info(self, company_name, join_date):
        self.comp_name.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        self.comp_name.fill(company_name)
        self.join_date_month.fill(join_date)

    def enter_business_info(self, biz_name, start_date):
        self.biz_name.wait_for(state="visible")
        self.biz_name.fill(biz_name)
        self.business_start_date.fill(start_date)

    def enter_health_info(self, health_val):
        self.health_dropdown.wait_for(state="visible")
        self.health_dropdown.select_option(value=health_val)

    def enter_income(self, income_val):
        self.income_input.wait_for(state="visible")
        self.income_input.click()
        
        # 1. 한 글자씩 타이핑하여 oninput 이벤트 발생 유도
        self.income_input.press_sequentially(str(income_val), delay=30)
        
        # 2. 브라우저 스크립트(showNext)가 확실히 실행되도록 input 이벤트 강제 트리거
        self.income_input.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
        
        # 3. 입력 완료를 알리는 포커스 해제
        self.page.keyboard.press("Tab")

    # [추가] 심사 신청 버튼 클릭 함수
    def submit_application(self):
        self.submit_area.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        # 영역 내의 '심사 신청하기' 버튼 클릭
        self.submit_area.get_by_role("button", name="심사 신청하기").click()