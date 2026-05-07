# 신용대출 심사 자동화 테스트 프로젝트 (Playwright)

Playwright 기반의 웹 대출 시나리오 자동화 테스트 프로젝트입니다.

## 테스트 시연 (Demo)
<!-- 실행 GIF 캡처 후 추가 권장 -->
![Demo](images/Loan_TestAutomation_pw.gif)

---

## 1. 주요 특징

### ✅ Page Object Model (POM) 디자인 패턴 적용
- **역할 분리**: 각 화면(Main, Login, Loan, Result)의 Selector와 Action을 pages/ 폴더로 분리하여 UI 변경 시 해당 파일만 수정하면 되도록 설계했습니다.
- **가독성**: 테스트 시나리오와 UI 조작 코드를 분리하여 비즈니스 로직을 한눈에 파악할 수 있습니다.

### ✅ 데이터 기반 테스트 (Data-Driven Test)
- **상수 분리**: 테스트 데이터(LOAN_DATA, LOGIN_SCENARIO)를 테스트 로직과 동일 파일 내 상수로 분리하여 관리합니다.
- **자동 반복 실행**: `@pytest.mark.parametrize`를 활용해 직업 유형 4종 × 성공/실패 2종 = 8개 케이스를 단일 함수로 자동 실행합니다.

### ✅ 스마트 타임아웃 & 에러 가시성
- **전역 타임아웃**: `set_default_timeout(5000)`으로 모든 대기를 5초로 통일하여 불필요한 30초 대기를 제거했습니다.
- **명확한 실패 원인**: 단순 타임아웃 에러가 아닌 "기대한 화면과 실제 화면의 불일치"를 AssertionError로 명확히 기록합니다.

### ✅ 예외 처리 및 자동 디버깅
- **결과 자동 판단**: 성공/실패 화면을 스스로 판단하여 검증하는 통합 로직을 구현했습니다.
- **Auto-Screenshot**: 테스트 실패 시 `capture/` 폴더에 자동으로 스크린샷을 저장하여 즉각적인 원인 파악이 가능합니다.

---

## 2. 테스트 대상 앱 (루피 뱅크)

테스트 자동화의 대상이 되는 웹앱을 직접 제작했습니다. 로그인부터 대출 심사 결과까지 실제 금융 서비스 흐름을 구현했으며, 직업 유형별로 입력 필드와 심사 로직이 달라지는 복합적인 시나리오를 포함합니다.

- **직업 유형 4종**: 직장인/공무원, 개인사업자, 프리랜서, 무직
- **연소득 기준 심사**: 기준 이상 승인 / 미만 거절
- **유효성 검사**: 직장명·사업장명 입력 시 신청 활성화
- **팝업 처리**: 로그인 실패, 로그아웃 확인, 신청 완료 팝업

![FlowChart](app/대출조회_플로우차트.png)

---

## 3. 프로젝트 구조
LoanProject-Playwright/
├── app/                        # [Target] 테스트 대상 웹앱
├── pages/                      # [POM] 페이지별 Selector & Action
├── tests/                      # [Scenario] 테스트 시나리오
├── capture/                    # [Debug] 실패 시 자동 스크린샷
├── images/                     # [Doc] GIF 파일
├── conftest.py
├── pytest.ini
├── requirements.txt
└── .gitignore

---

## 4. 테스트 케이스 구성

> 💡 TC_03, TC_06은 의도적으로 잘못된 데이터를 주입하여
> 기대 화면 불일치 시 FAIL이 정확히 검출되는지 검증한 케이스입니다.

| Case ID | 직업 유형 | 조회 결과 | 테스트 결과 |
|---------|----------|-----------|------------|
| TC_01 | 직장인 / 공무원 | ❌ 거절 | ✅ PASS |
| TC_02 | 직장인 / 공무원 | ✅ 승인 | ✅ PASS |
| TC_03 | 개인사업자 | ❌ 거절 | ⚠️ FAIL (네거티브 검증) |
| TC_04 | 개인사업자 | ✅ 승인 | ✅ PASS |
| TC_05 | 프리랜서 | ❌ 거절 | ✅ PASS |
| TC_06 | 프리랜서 | ✅ 승인 | ⚠️ FAIL (네거티브 검증) |
| TC_07 | 무직 | ❌ 거절 | ✅ PASS |
| TC_08 | 무직 | ✅ 승인 | ✅ PASS |
---

## 5. 리팩토링 히스토리

| 버전 | 내용 |
|------|------|
| v1 | 직업 유형별 개별 함수로 작성 (test_03~10) |
| v2 | `pytest.mark.parametrize`로 8개 케이스 단일 함수로 통합 |

---

## 6. 사전 준비 (Prerequisites)

- **Python 3.14**
- **Playwright** (Chromium)

---

## 7. 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/kimhy32500/LoanProject-Playwright.git

# 라이브러리 설치
pip install -r requirements.txt
playwright install
```

### pytest 기반 실행 (권장)

```bash
# 기본 실행
pytest tests/test_integration.py

# 상세 에러 로그 출력
pytest --tb=short
```