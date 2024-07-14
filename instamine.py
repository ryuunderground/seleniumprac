from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

# 개인정보
FACEBOOK_ID = ""
FACEBOOK_PW = ""


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome()

main_hashtag = "photography"
browser.get(f"https://www.instagram.com/accounts/login/?next=%2Fexplore%2Ftags%2F{main_hashtag}%2F&source=desktop_nav")

# 로그인
login_form = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "loginForm")))
go_to_facebook_login_btn = login_form.find_element(By.CLASS_NAME, "_acan._acao._acas._aj1-._ap30")
go_to_facebook_login_btn.click()
facebook_login_form = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "login_form")))
id_input = facebook_login_form.find_element(By.ID,"email")
pw_input = facebook_login_form.find_element(By.ID, "pass")
facebook_login_btn = facebook_login_form.find_element(By.ID, "loginbutton")
id_input.send_keys(FACEBOOK_ID)
pw_input.send_keys(input("inset password"))
facebook_login_btn.click()

time.sleep(500)
"""
article = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
imgs = article.find_elements(By.TAG_NAME, "img")

for img in imgs:
    ActionChains(browser).key_down(Keys.COMMAND).click(img).perform()
    time.sleep(3)
    img_description = img.get_attribute("alt")
    print(img_description)
"""
#로그인 보안 문제로 포기
