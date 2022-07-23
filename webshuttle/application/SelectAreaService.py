import threading

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service

from webshuttle.application.port.incoming.SelectAreaUseCase import SelectAreaUseCase
from webshuttle.domain.EventListenerInjector import EventListenerInjector
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from webshuttle.domain.WebScraper import WebScraper


def init_event_listener(web_scraper):
    injector = EventListenerInjector(web_scraper)
    injector.add_mouseover()
    injector.add_mouseleave()
    injector.add_mousedown_right()
    injector.add_tooltip()
    injector.add_startpopup()


class SelectAreaService(SelectAreaUseCase):
    def __init__(self, url_widget, chrome_driver):
        self._web_scraper = None
        self.url_widget = url_widget
        self.chrome_driver = chrome_driver

    def open_browser(self):
        chrome_service = Service(self.chrome_driver)
        chrome_service.creationflags = 0x08000000
        shuttle_widget_group = ShuttleWidgetGroup(None, None, None, self.url_widget, None, None, self)
        try:
            self._web_scraper = WebScraper(shuttle_widget_group=shuttle_widget_group,
                                           driver=webdriver.Chrome(service=chrome_service),
                                           shuttle_list=[],
                                           shuttle_seq=0,
                                           waiting_event=threading.Event())
            self._web_scraper.get()
            init_event_listener(self._web_scraper)
        except WebDriverException:
            chrome_service.stop()
            self._web_scraper.driver.quit()

    def get_web_scraper(self):
        return self._web_scraper
