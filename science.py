from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv 
import time

# cloudflare 해결 못 함

class nature_miner:
    def __init__(self, search_key):
        self.search_key = search_key
        # 브라우저 꺼짐 방지 옵션
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # WebDriver 초기화
        service = Service(executable_path="/opt/homebrew/bin/chromedriver")  # 여기에 chromedriver 경로를 지정하세요.
        self.broswer = webdriver.Chrome(service=service, options=chrome_options)
        #Stealth 설정
        stealth(self.broswer,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)
        self.results = []
        # 자바스크립트로 WebDriver 속성을 제거
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
            """
        })

    # 제목, 지수, 초록 추출
    def data_extractor(self):
        time.sleep(30)
        
    # 제목
        article_title = self.browser.find_element(By.CLASS_NAME, "text-reset.animation-underline")
        result_title = article_title.text
        print(result_title)
        """
        # 지수
        index_list = self.browser.find_element(By.CLASS_NAME,"c-article-metrics-bar.u-list-reset")
        indexs = index_list.find_elements(By.TAG_NAME, "li")
        indexs = indexs[:-1]
        index_array = []
        for index in indexs:
            index_array.append(index.text)
        #초록
        try:
            abstract = self.browser.find_element(By.ID, "Abs1-content")
            result_abs = abstract.find_element(By.TAG_NAME, "p").text
        except:
            print("blocked")
                
        result_array = [result_title, index_array, result_abs]
        self.results.append(result_array)

    def save_file(self):
        file = open(f"{self.search_key}-science_article_review.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["title", "index", "Abstract"])
        for result in self.results:
            writer.writerow(result)
"""
    def article_extractor(self, url):
        self.browser.get(url)
        articles = WebDriverWait(self.browser, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "article-title.sans-serif.text-deep-gray.mb-1")))
        print("allARticlesLoaded")
    # 새 탭 열기
        for article in articles:
            article_anchor = article.find_element(By.TAG_NAME, "a")
            article_url = article_anchor.get_attribute("href")
            
            # 자바스크립트를 사용해 새 탭 열기
            self.browser.execute_script(f"window.open('{article_url}');")
            print(f"Opened new tab: {article_url}")
    # 각 탭 돌면서 추출
        windows = self.browser.window_handles[1:]
        for window in windows:
            self.browser.switch_to.window(window)
            try:
                self.data_extractor()
            except:
                print("none")
        print(self.results)

    def start(self):
        final_search_key = self.search_key.replace(" ","+")
        science = f"https://www.science.org/action/doSearch?AllField={final_search_key}"
        self.article_extractor(science)
        """self.save_file()"""





transcriptome_tester = nature_miner("Proteomics")
transcriptome_tester.start()

