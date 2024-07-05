from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

KEYWORD = "Hololive"

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#브라우저 지정
browser = webdriver.Chrome(options=chrome_options)
# url 지정
browser.get("https://google.com")
# 검색바 찾고 입력, 엔터
search_bar = browser.find_element(By.CLASS_NAME, "gLFyf")
search_bar.send_keys(KEYWORD)
search_bar.send_keys(Keys.ENTER)
#대기, 바로 검색하니까 차마 결과가 나오기 전에 결과를 모아버림
time.sleep(5)
#결과 모으기
search_results = browser.find_elements(By.CLASS_NAME, "MjjYud")
search_results.pop()
#결과 추려내기, 제목만
for index, search_result in enumerate(search_results):
    search_result.screenshot(f"{KEYWORD} x {index}.png")

#브라우저 끄기
#browser.quit()