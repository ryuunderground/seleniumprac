from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import time

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir):
        self.browser = webdriver.Chrome(options=chrome_options)
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir

    def search_and_screen_capture(self):
        # 구글 접속
        self.browser.get("https://google.com")
        # 검색바 찾고 입력, 엔터
        search_bar = self.browser.find_element(By.CLASS_NAME, "gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)
        #파지네이션 찾기
        try:
            pagination = self.browser.find_element(By.CLASS_NAME, "AaVjTc")
            page = pagination.find_elements(By.TAG_NAME, "td")
            max_page = int(page[-2].text)

        except Exception:
            max_page = 1
        
        for j in range(max_page):
            now_page = j + 1
            # 예외 처리
            try:
                search_result_exceptions = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "TzHB6b.Hwkikb.WY0eLb")))
                self.browser.execute_script("""
                const exception = arguments[0];
                for(let i = 0; i<exception.length; i++){
                    parent = exception[i].parentElement
                    if (parent !== null){            
                        while(parent.firstChild !== null){
                            parent.removeChild(parent.firstChild)
                        }
                    }
                }                
                """,
                    search_result_exceptions,
                )

                search_result_exceptions_second_case = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "TQc1id k5T88b")))
                self.browser.execute_script("""
                const exception = arguments[0];
                for(let i = 0; i<exception.length; i++){
                    parent = exception[i].parentElement
                    if (parent !== null){            
                        while(parent.firstChild !== null){
                            parent.removeChild(parent.firstChild)
                        }
                    }
                }                
                """,
                    search_result_exceptions_second_case,
                )
            except Exception:
                pass

            #결과 모으기
            if now_page == 1:
                search_results = self.browser.find_elements(By.CLASS_NAME, "TzHB6b.cLjAic")
            else:
                search_results = self.browser.find_elements(By.CLASS_NAME, "MjjYud")
            
            search_results.pop()
            
            #결과 추려내기, 제목만
            os.mkdir(f"{self.screenshots_dir}/{self.keyword}{now_page}")
            for index, search_result in enumerate(search_results):
                search_result.screenshot(f"{self.screenshots_dir}/{self.keyword}{now_page}/{self.keyword} x {index}.png")
            #다음 페이지로 넘어가기
            next_page = self.browser.find_element(By.ID, "pnnext")
            next_page.send_keys(Keys.ENTER)

            
    def execute(self):
        #브라우저 끄기
        self.browser.quit()

spatula = GoogleKeywordScreenshooter("Auro Kronii", "screenshots")
spatula.search_and_screen_capture()
spatula.execute()
