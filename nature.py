from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv 

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

class nature_miner:
    def __init__(self, search_key):
        self.search_key = search_key
        self.browser = webdriver.Chrome()
        self.results = []

    # 제목, 지수, 초록 추출
    def data_extractor(self):
    # 제목
        article_title = self.browser.find_element(By.CLASS_NAME, "c-article-title")
        result_title = article_title.text
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
        file = open(f"{self.search_key}-nature_article.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["title", "index", "Abstract"])
        for result in self.results:
            writer.writerow(result)

    def article_extractor(self, url):
        self.browser.get(url)
        articles = WebDriverWait(self.browser, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "app-article-list-row__item")))
        coockies = self.browser.find_element(By.CLASS_NAME, "cc-button.cc-button--secondary.cc-button--contrast.cc-banner__button.cc-banner__button-accept")
        coockies.click()
    # 새 탭 열기
        for article in articles:
            article_anchor = article.find_element(By.TAG_NAME, "a")
            ActionChains(self.browser).key_down(Keys.COMMAND).click(article_anchor).perform()
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
        nature = f"https://www.nature.com/search?q={self.search_key}&article_type=research%2C+reviews%2C+research-highlights&order=relevance"
        self.article_extractor(nature)
        self.save_file()

transcriptome_tester = nature_miner("transcriptome")
transcriptome_tester.start()

