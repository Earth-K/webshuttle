from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebCrawler:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, chrome_options=self.options())

    def options(self):
        result = webdriver.ChromeOptions()
        return result

    def openWindow(self):
        self.driver.maximize_window(self)
