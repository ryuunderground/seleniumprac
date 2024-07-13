from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

result = []

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome()

search_key = "transcriptome"
browser.get(f"https://www.nature.com/search?q={search_key}&article_type=research%2C+reviews%2C+research-highlights&order=relevance")

articles = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "app-article-list-row__item")))
coockies = browser.find_element(By.CLASS_NAME, "cc-button.cc-button--secondary.cc-button--contrast.cc-banner__button.cc-banner__button-accept")
coockies.click()

for article in articles:
    article_anchor = article.find_element(By.TAG_NAME, "a")
    ActionChains(browser).key_down(Keys.COMMAND).click(article_anchor).perform()


windows = browser.window_handles[1:]
for window in windows:
    browser.switch_to.window(window)
    try:
        article_title = browser.find_element(By.CLASS_NAME, "c-article-title")
        result_title = article_title.text
        print(result_title)
        index_list = browser.find_element(By.CLASS_NAME,"c-article-metrics-bar.u-list-reset")
        indexs = index_list.find_elements(By.TAG_NAME, "li")
        indexs = indexs[:-1]
        index_array = []
        for index in indexs:
            index_array.append(index.text)
            print(index_array)
            
        result_array = [result_title, index_array]
        print("-----result_array----------")
        print(result_array)
        result.append(result_array)
    except:
        print("none")
    
print(result)
time.sleep(550)
