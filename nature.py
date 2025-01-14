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
    def __init__(self, search_key, cycle):
        self.search_key = search_key
        self.cycle = int(cycle)
        self.browser = webdriver.Chrome()
        self.results = []
   
        
    def data_extractor(self):
        # Default values
        article_data = {
            'title': "Value not found",
            'metrics': ["Value not found"],
            'abstract': "Value not found",
            'link': "Value not found",
            'pdf_link': "Value not found"
        }
        
        try:
            # 제목
            try:
                article_title = self.browser.find_element(By.CLASS_NAME, "c-article-title")
                article_data['title'] = article_title.text
            except:
                print("Could not extract title")
            
            # 지수
            try:
                index_list = self.browser.find_element(By.CLASS_NAME,"c-article-metrics-bar.u-list-reset")
                indexs = index_list.find_elements(By.TAG_NAME, "li")
                indexs = indexs[:-1]
                index_array = []
                for index in indexs:
                    index_array.append(index.text)
                if index_array:  # Only update if we found metrics
                    article_data['metrics'] = index_array
            except:
                print("Could not extract metrics")
                
            # 초록
            try:
                abstract = self.browser.find_element(By.ID, "Abs1-content")
                article_data['abstract'] = abstract.find_element(By.TAG_NAME, "p").text
            except:
                print("Could not extract abstract")

            # 링크
            try:
                article_data['link'] = self.browser.current_url
                print(article_data["link"])
            except:
                print("Could not extract link")
            
            # 다운로드
            try:
                download = self.browser.find_element(By.CLASS_NAME, "c-pdf-download.u-clear-both.js-pdf-download")
                article_data['pdf_link'] = download.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                print("Could not extract PDF link")

            self.results.append(article_data)
            return True
            
        except Exception as e:
            print(f"Error in data extraction: {str(e)}")
            self.results.append(article_data)  # Still append the data with default values
            return False

    def get_results(self):
        """Return the collected results"""
        return self.results

    def clear_results(self):
        """Clear the current results"""
        self.results = []

    def article_extractor(self, url):
        try:
            self.browser.get(url)
            articles = WebDriverWait(self.browser, 3).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "app-article-list-row__item"))
            )
            cookies = self.browser.find_element(By.CLASS_NAME, "cc-button.cc-button--secondary.cc-button--contrast.cc-banner__button.cc-banner__button-accept")
            cookies.click()

            cycle = int(self.cycle)
            start_idx = 20 * (cycle - 1)
            end_idx = 20 * cycle
            
            for article in articles[start_idx:end_idx]:
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
        except ValueError:
            print("Error: cycle must be a valid number")
            return []

    def start(self):
        self.clear_results()  # Clear any previous results
        nature = f"https://www.nature.com/search?q={self.search_key}&article_type=reviews&order=relevance"
        self.article_extractor(nature)
        return self.get_results()  # Return results instead of saving to CSV

"""transcriptome_tester = nature_miner("transcriptome")
transcriptome_tester.start()"""

