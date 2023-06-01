from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

""" Wipo_Connection class is used to connect to WIPO website and search for patents related to a keyword.
    It also extracts the title, date and abstract of the patents.
    Also navigates to the next page and extracts the data from the next page.
    Stops when it reaches the last page."""

class Wipo_Connection():
    def __init__(self):
        self.page_num ='0'
    def connect(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://patentscope.wipo.int/search/en/search.jsf")
        return self.driver
    def search(self,keyword):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "simpleSearchForm:fpSearch:input")))
        search = self.driver.find_element(By.ID,"simpleSearchForm:fpSearch:input")
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)

    def get_patent(self):
        per_page = Select(self.driver.find_element(By.ID,"resultListCommandsForm:perPage:input"))
        per_page.select_by_index(3)
        WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='resultListCommandsForm:perPage:input']/option[4]")))
        time.sleep(10)
        page_num = self.driver.find_element(By.CLASS_NAME,"ps-paginator--page")
        print(page_num.text.split(" ")[-1])
        self.page_num = int(page_num.text.split(" ")[-1])

        title_list = self.driver.find_elements(By.CLASS_NAME,"ps-patent-result--title")
        date_list =self.driver.find_elements(By.CLASS_NAME,"ps-patent-result--title--ctr-pubdate")
        abstract_list= self.driver.find_elements(By.CLASS_NAME,"ps-patent-result--abstract")
        print("title:",len(title_list))
        print("date:",len(date_list))
        print("abstract:",len(abstract_list))
        for title in title_list:
            print(title.text)
        time.sleep(60)
    def execute(self,keyword):
        try:
            self.connect()
        except:
            print("Connection Error")
        try:
            self.search(keyword)
            self.get_patent()
            for i in range(2,self.page_num+1):
                try:
                    print("Navigating to next page....")
                    next_page = self.driver.find_element(By.CLASS_NAME,'ps-paginator--page')
                    next_page.click()
                    next_page_input = self.driver.find_element(By.CLASS_NAME,'ps-paginator-modal--input')
                    next_page_input.clear()
                    next_page_input.send_keys(i)
                    time.sleep(5)
                    next_page_input.send_keys(Keys.RETURN)
                    time.sleep(10)
                    self.get_patent()
                except Exception as e:
                    print(e)
                    break
        except Exception as e:
            print("Search Error: ",e)
        finally:
            print("Closing Connection")
            time.sleep(10)
            self.stop_connection()

    def stop_connection(self):
        self.driver.close()

conn = Wipo_Connection()
conn.execute("digital twin")






