from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class WebCrawler:
    def __init__(self, startUrl):
        if startUrl == '':
            startUrl = 'http://google.com'
        if not startUrl.startswith('http://'):
            startUrl = 'http://' + startUrl
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(startUrl)
        time.sleep(3)

    def executeJs(self, script):
        self.driver.execute_script(script)