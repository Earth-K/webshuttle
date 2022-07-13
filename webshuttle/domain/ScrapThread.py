import threading

from PyQt5.QtCore import QThread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.WebScraper import WebScraper


class ScrapThread(QThread):
    def __init__(self, parent, shuttle_seq, shuttle_widget_group, shuttle_list, chrome_driver):
        super().__init__(parent)
        self.shuttle_seq = shuttle_seq
        self.shuttle_widget_group = shuttle_widget_group
        self.time = DefaultTime()
        self.shuttle_list = shuttle_list
        self.chrome_driver = chrome_driver
        self.web_scraper = None

    def run(self) -> None:
        chrome_service = Service(self.chrome_driver)
        chrome_service.creationflags = 0x08000000
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--start-maximized")
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        self.web_scraper = WebScraper(shuttle_widget_group=self.shuttle_widget_group,
                                      driver=webdriver.Chrome(service=chrome_service, options=options),
                                      shuttle_list=self.shuttle_list, shuttle_seq=self.shuttle_seq)
        self.web_scraper.get()
        self.web_scraper.scrap()
