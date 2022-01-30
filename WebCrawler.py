from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement


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
        return self.driver.execute_script(script)

    def get_target_element(self):
        return self.driver.find_elements_by_class_name("ws-target-element")[0]
