from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebCrawler:
    def __init__(self, start_url):
        if start_url == '':
            start_url = 'http://google.com'
        if not start_url.startswith('http://') | start_url.startswith('https://'):
            start_url = 'http://' + start_url
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(start_url)
        self.driver.implicitly_wait(2)

    def execute_js(self, script):
        self.driver.execute_script(script)
