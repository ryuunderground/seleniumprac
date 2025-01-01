from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

class cell_miner:
    def __init__(self, search_key, cycle):
        self.search_key = search_key
        self.cycle = int(cycle)
        self.browser = webdriver.Chrome()
        self.results = []

    def cloudflare_bypass(self):
        # Cloudflare 우회
        stealth(self.browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
   
        
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
                article_main = self.browser.find_element(By.CLASS_NAME, "core-container")
                article_title = article_main.find_element(By.TAG_NAME, "h1")
                article_data['title'] = article_title.text
            except:
                print("Could not extract title")
            
            # 지수
            try:
                index_list = self.browser.find_element(By.CLASS_NAME,"plum-x__items")
                indexs = index_list.find_elements(By.TAG_NAME, "div")
          
                index_array = []
                for index in indexs:
                    index_array.append(index.text)
                if index_array:  # Only update if we found metrics
                    article_data['metrics'] = index_array
            except:
                print("Could not extract metrics")
                
            # 초록
            try:
                abstract = self.browser.find_element(By.ID, "author-abstract")
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
                article_header = self.browser.find_element(By.ID, "article_more_menu")
                header_lists = article_header.find_element(By.TAG_NAME, "ul")
                pdf_list = header_lists.find_element(By.CLASS_NAME, "article-tools__item.article-tools__pdf")
                download = pdf_list.find_element(By.TAG_NAME, "a")
                article_data['pdf_link'] = download.get_attribute("href")
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
        self.browser.get(url)
        self.cloudflare_bypass()
        search_input = WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.ID, "searchText"))
            )
        search_input.send_keys(self.search_key)
        search_input.send_keys(Keys.ENTER)
        try:
            search_results = WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rlist.search-result__body.items-results.items-results--articles"))
            )
            articles = search_results.find_elements(By.CLASS_NAME, "search__item.clearfix separator")

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
        cell = "https://www.cell.com/"
        self.article_extractor(cell)
        return self.get_results()  # Return results instead of saving to CSV

transcriptome_tester = cell_miner("transcriptome", 1)
transcriptome_tester.start()

