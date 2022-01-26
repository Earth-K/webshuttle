from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebCrawler:
    def __init__(self, startUrl):
        if startUrl == '':
            startUrl = 'https://google.com'
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(startUrl)

