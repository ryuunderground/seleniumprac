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

class science_miner:
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
                article_header = self.browser.find_element(By.TAG_NAME, "header")
                article_title = article_header.find_element(By.TAG_NAME, "h1")
                article_data['title'] = article_title.text
            except:
                print("Could not extract title")
            
            # 지수
            try:
                index_container = self.browser.find_element(By.CLASS_NAME,"toolbar-metric-container.data-source")
                index_menu = index_container.find_element(By.CLASS_NAME, "metrics-menu.toolbar-metric")
                indexs_anchor = index_menu.find_element(By.TAG_NAME, "a")
                index = indexs_anchor.text
                index_array = []
                index_array.append(index)
                if index_array:  # Only update if we found metrics
                    article_data['metrics'] = index_array
            except:
                print("Could not extract metrics")
                
            # 초록
            try:
                abstract = self.browser.find_element(By.ID, "abstract")
                article_data['abstract'] = abstract.find_element(By.TAG_NAME, "div").text
            except:
                print("Could not extract abstract")

            # 링크
            try:
                article_data['link'] = self.browser.current_url
            except:
                print("Could not extract link")
            
            # 다운로드
            try:
                download = self.browser.find_element(By.CLASS_NAME, "info-panel__formats info-panel__item")
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
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card.pb-3.mb-4.border-bottom"))
            )

            cycle = int(self.cycle)
            start_idx = 20 * (cycle - 1)
            end_idx = 20 * cycle

            for article in articles[start_idx:end_idx]:
                article_anchor = article.find_element(By.TAG_NAME, "a")
                article_url = article_anchor.get_attribute("href")
                self.browser.execute_script(f'window.open("{article_url}", "_blank");')

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
        science = f"https://www.science.org/action/doSearch?AllField={self.search_key}"
        self.article_extractor(science)
        return self.get_results()  # Return results instead of saving to CSV

transcriptome_tester = science_miner("transcriptome", 1)
transcriptome_tester.start()

