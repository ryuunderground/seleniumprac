from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from math import ceil
import os


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 기본 설정값
BROWSER_HEIGHT = 870 # print(browser.get_window_size()) === 875
SCROLL_HEIGHT = 550

class ResponsiveTester:
    def __init__(self, urls):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [480, 960, 1366, 1920 ]

    def screenshot(self, url):
        self.browser.get(url)
        url_name = url.replace('https://www.', '').split('.')[0]
        os.mkdir(f"screenshots/{url_name}")
        for size in self.sizes:
            os.mkdir(f"screenshots/{url_name}/{size}")
            self.browser.set_window_size(size, BROWSER_HEIGHT)
            self.browser.execute_script("""
                window.scrollTo(0,0);
            """)
            time.sleep(3)
            scroll_size = self.browser.execute_script("""
                return document.body.scrollHeight;
            """)
            total_sections = ceil(scroll_size/SCROLL_HEIGHT)

            for section in range(total_sections + 1):
                self.browser.execute_script(
                    f"window.scrollTo(0,{section}*{SCROLL_HEIGHT})"
                )
                self.browser.save_screenshot(f"screenshots/{url_name}/{size}/{size}x{section}.png")



    def start(self):
        for url in self.urls:
            self.screenshot(url)


tester = ResponsiveTester(["https://www.behance.net/"])
tester.start()



