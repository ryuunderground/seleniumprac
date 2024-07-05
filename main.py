from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

KEYWORD = "Ouro Kronii"

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
    
# 예외 처리
search_result_exceptions = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "TzHB6b.Hwkikb.WY0eLb")))
browser.execute_script("""
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

#대기 후 모으기, 바로 검색하니까 차마 결과가 나오기 전에 결과를 모아버림
time.sleep(5)
#결과 모으기
search_results = browser.find_elements(By.CLASS_NAME, "TzHB6b")
search_results.pop()
#결과 추려내기, 제목만
for index, search_result in enumerate(search_results):
    search_result.screenshot(f"screenshots/{KEYWORD} x {index}.png")
    #제외하고 싶은 결과가 있을 경우
    #class_name = search_result.get_attribute("class")
    """
    if "exception class name" not in class_name:
        search_result.screenshot(f"screenshots/{KEYWORD} x {index}.png")
    """
#브라우저 끄기
#browser.quit()