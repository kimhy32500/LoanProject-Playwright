import pytest
import os
from datetime import datetime
from playwright.sync_api import Page
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.loan_page import LoanPage
from pages.result_page import ResultPage

@pytest.fixture
def main_page(page: Page):
    return MainPage(page)

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture
def loan_page(page: Page):
    return LoanPage(page)

@pytest.fixture
def result_page(page: Page):
    return ResultPage(page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 테스트가 실패한 시점만 타겟팅
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # 사용자 지정 경로 설정
            screenshot_dir = os.path.join(os.path.dirname(__file__), "capture")
            
            # 폴더가 없으면 생성
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            # 파일명 생성: 테스트명_시간.png
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = os.path.join(screenshot_dir, file_name)

            # 스크린샷 저장
            page.screenshot(path=file_path)
            # 터미널에 저장 경로 출력 (선택 사항)
            print(f"\n[FAIL] 스크린샷 저장 완료: {file_path}")

def pytest_collection_modifyitems(items):
    last_items = [i for i in items if "test_last_" in i.nodeid]
    other_items = [i for i in items if "test_last_" not in i.nodeid]
    items[:] = other_items + last_items

@pytest.fixture(autouse=True)
def set_timeout(page):
    page.set_default_timeout(5000)