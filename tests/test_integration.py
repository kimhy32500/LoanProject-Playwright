import pytest
from playwright.sync_api import Page, expect

# 테스트 데이터 정의 (따로 분리)
LOAN_DATA = {
    "officer": {"extra": "루피건설", "date": "2024-01", "fail": "2500", "success": "3500"},
    "business": {"extra": "루피식당", "date": "2023-05-20", "fail": "3000", "success": "4000"},
    "freelancer": {"extra": "local", "fail": "2000", "success": "1200"},
    "none": {"extra": "dependent", "fail": "500", "success": "3100"}
}

LOGIN_SCENARIO = [
    {"id": "", "pw": "", "desc": "공란 입력"},
    {"id": "wrong_id", "pw": "1234", "desc": "잘못된 아이디"},
    {"id": "admin", "pw": "wrong_pw", "desc": "잘못된 비밀번호"},
    {"id": "admin", "pw": "1234", "desc": "최종 정상 로그인"}
]

loan_test_cases = [
    ("officer", "success"), ("officer", "fail"),
    ("business", "success"), ("business", "fail"),
    ("freelancer", "success"), ("freelancer", "fail"),
    ("none", "success"), ("none", "fail"),
]

# 공통 로그인 로직
def ensure_logged_in(main_page, login_page):
    main_page.navigate()
    
    # 로그인 버튼이 보이면 로그인 실행
    if main_page.login_btn.is_visible():
        main_page.click_login()
        login_page.login("admin", "1234")

        # 신용대출 조회하기 버튼이 보이면 로그인 완료 확인
        expect(main_page.loan_start_btn).to_be_visible(timeout=5000)

        # 로그인 완료 상태면 다음 단계 실행

# --- 시나리오 시작 ---
def test_login_logout_cycle(main_page, login_page, page: Page):
    # LOGIN_SCENARIO 리스트의 마지막 항목([-1])을 가져와서 'user'라고 부릅니다.
    user = LOGIN_SCENARIO[-1] 
    
    main_page.navigate()
    main_page.click_login()
    
    # 이제 고정된 이름 대신 user["id"]와 user["pw"]를 사용합니다.
    login_page.login(user["id"], user["pw"])
    
    # 로그아웃 시 발생하는 알림창(Dialog) 확인
    page.once("dialog", lambda dialog: dialog.accept())
    main_page.click_logout()

def test_login_failure_and_success(main_page, login_page, page: Page):
    main_page.navigate()
    main_page.click_login()
    
    for data in LOGIN_SCENARIO:
        login_page.clear_fields()
        login_page.login(data["id"], data["pw"])
        
        # 마지막 데이터가 아니면 에러 메시지가 보이는지 확인
        if data["id"] != "admin" or data["pw"] != "1234":
            expect(login_page.error_message).to_be_visible()

    page.once("dialog", lambda dialog: dialog.accept())
    main_page.click_logout()
            
# # 3 & 4. 직장인 (데이터 참조)
# def test_03_officer_fail(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["officer"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="officer")
#     loan_page.enter_work_info(data["extra"], data["date"])
#     loan_page.enter_income(data["fail"])
#     loan_page.submit_application()
#     expect(result_page.fail_view).to_be_visible()
#     result_page.return_to_home_after_fail()

# def test_04_officer_success(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["officer"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="officer")
#     loan_page.enter_work_info(data["extra"], data["date"])
#     loan_page.enter_income(data["success"])
#     loan_page.submit_application()
#     expect(result_page.product_card).to_be_visible()
#     result_page.click_first_product()
#     result_page.apply_loan()
#     result_page.return_to_home_after_apply()

# # 5 & 6. 개인사업자
# def test_05_business_fail(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["business"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="business")
#     loan_page.enter_business_info(data["extra"], data["date"])
#     loan_page.enter_income(data["fail"])
#     loan_page.submit_application()
#     expect(result_page.fail_view).to_be_visible()
#     result_page.return_to_home_after_fail()

# def test_06_business_success(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["business"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="business")
#     loan_page.enter_business_info(data["extra"], data["date"])
#     loan_page.enter_income(data["success"])
#     loan_page.submit_application()
#     expect(result_page.product_card).to_be_visible()
#     result_page.click_first_product()
#     result_page.apply_loan()
#     result_page.return_to_home_after_apply()

# # 7 & 8. 프리랜서
# def test_07_freelancer_fail(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["freelancer"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="freelancer")
#     loan_page.enter_health_info(data["extra"])
#     loan_page.enter_income(data["fail"])
#     loan_page.submit_application()
#     expect(result_page.fail_view).to_be_visible()
#     result_page.return_to_home_after_fail()

# def test_08_freelancer_success(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["freelancer"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="freelancer")
#     loan_page.enter_health_info(data["extra"])
#     loan_page.enter_income(data["success"])
#     loan_page.submit_application()
#     expect(result_page.product_card).to_be_visible()
#     result_page.click_first_product()
#     result_page.apply_loan()
#     result_page.return_to_home_after_apply()

# # 9 & 10. 무직
# def test_09_none_fail(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["none"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="none")
#     loan_page.enter_health_info(data["extra"])
#     loan_page.enter_income(data["fail"])
#     loan_page.submit_application()
#     expect(result_page.fail_view).to_be_visible()
#     result_page.return_to_home_after_fail()

# def test_10_none_success(main_page, login_page, loan_page, result_page):
#     ensure_logged_in(main_page, login_page)
#     data = LOAN_DATA["none"]
#     main_page.click_loan_start()
#     loan_page.job_dropdown.select_option(value="none")
#     loan_page.enter_health_info(data["extra"])
#     loan_page.enter_income(data["success"])
#     loan_page.submit_application()
#     expect(result_page.product_card).to_be_visible()
#     result_page.click_first_product()
#     result_page.apply_loan()
#     result_page.return_to_home_after_apply()

@pytest.mark.parametrize("job_type, status", loan_test_cases)
def test_loan_process_integration(main_page, login_page, loan_page, result_page, job_type, status):
    """
    03번부터 10번까지의 시나리오를 하나로 합친 통합 테스트입니다.
    데이터에 따라 성공/실패 화면을 스스로 판단하여 검증합니다.
    """
    # [1] 로그인 상태 확인
    # ensure_logged_in 내부에서 로그인 여부 상태 체크
    ensure_logged_in(main_page, login_page)
    data = LOAN_DATA[job_type]
    main_page.click_loan_start()

    # [2] 직업 선택 및 정보 입력 (직업에 따라 입력 함수를 다르게 호출)
    loan_page.job_dropdown.select_option(value=job_type)
    
    if job_type == "officer":
        loan_page.enter_work_info(data["extra"], data["date"])
    elif job_type == "business":
        loan_page.enter_business_info(data["extra"], data["date"])
    else: # 프리랜서나 무직
        loan_page.enter_health_info(data["extra"])

    # [3] 연봉 입력 및 심사 신청
    loan_page.enter_income(data[status])
    loan_page.submit_application()

    # [4] 결과 화면 판단 로직 (데이터 주권 기반)
    # 1. '홈으로 이동' 버튼 체크
    result_page.go_home_from_result.wait_for(state="visible", timeout=5000)
        
    # 2. 버튼이 보인다면 데이터와 대조
    if status == "success":
        if result_page.product_card.is_visible():
            print(f"[{job_type}] 성공 확인")
            result_page.click_first_product()
            result_page.apply_loan()
            result_page.return_to_home_after_apply()
        else:
            # 성공이어야 하는데 카드가 없으므로 즉시 실패 처리
            pytest.fail(f"[{job_type}] 데이터 오류: 가능이지만 상품 카드가 없음")

    elif status == "fail":
        if result_page.fail_view.is_visible():
            print(f"[{job_type}] 거절 확인")
            result_page.return_to_home_after_fail()
        else:
            # 실패여야 하는데 거절 문구가 없으므로 즉시 실패 처리
            pytest.fail(f"[{job_type}] 데이터 오류: 거절이지만 상품 카드 노출")

    else:
        # 3. 홈으로 이동 버튼 확인 불가 시 기다리지 않고 바로 실패 처리 (타임아웃 0의 효과)
        pytest.fail(f"[{job_type}] 결과 화면 로딩 실패 또는 처리 지연")

def test_last_final_logout(main_page, login_page, page: Page):
    ensure_logged_in(main_page, login_page)
    page.once("dialog", lambda dialog: dialog.accept())
    main_page.click_logout()