from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


class BigKim:

    def __init__(self, keyword):
        # 기본 브라우저
        # browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # 꺼짐 설정 끈 브라우저
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        # 검색 키워드
        self.keyword = keyword
    # 필요없는 요소 제거
    def useless_element_remover(self, shitty_elements):
        self.browser.execute_script(
            """
            const shitty = arguments[0];
            shitty.parentElement.removeChild(shitty);
            """,
            shitty_elements
        )
    # 논문 리스트 추출
    def get_journal_list(self):
        # 대학원 논문 페이지 접속
        self.browser.get("https://bigkim.cau.ac.kr/논문/")
        # 년도 별 섹션 추출
        journal_list_sections = WebDriverWait(self.browser, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, "section")))
        # 년도 별 섹션 돌면서 논문 리스트 추출
        for section in journal_list_sections:
            lists = section.find_elements(By.TAG_NAME, "li")
            for list in lists:
                journal_info = list.text
                if self.keyword in journal_info:
                    print(journal_info)
                else:
                    self.useless_element_remover(list)

virus_results = BigKim("PRRSV")
virus_results.get_journal_list()
