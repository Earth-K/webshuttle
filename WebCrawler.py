from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebCrawler:
    def __init__(self, startUrl):
        if startUrl == '':
            startUrl = 'http://google.com'
        if not startUrl.startswith('http://'):
            startUrl = 'http://'+startUrl
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(startUrl)

