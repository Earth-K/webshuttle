import threading

import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By

from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from webshuttle.domain.UpdatedTextParser import UpdatedTextParser


class WebScraper:
    def __init__(self, shuttle_widget_group: ShuttleWidgetGroup, driver: webdriver.Chrome, shuttle_list: list,
                 shuttle_seq: int, waiting_event: threading.Event):
        pygame.init()
        self.shuttle_widget_group = shuttle_widget_group
        self.url = self._safe_url()
        self.shuttle_seq = shuttle_seq
        self.shuttle_list = shuttle_list
        self.driver = driver
        self.stop_event = threading.Event()
        self.waiting_event = waiting_event

    def _safe_url(self):
        result = self.shuttle_widget_group.get_url_widget().text()
        if result == '':
            return 'http://google.com'
        if not result.startswith('http://') | result.startswith('https://'):
            return 'http://' + result
        return result

    def get(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)
        self.driver.get(self.url)

    def scrap(self):
        text_list = []
        sound = pygame.mixer.Sound("resource/sounds/sound.wav")
        pre_shuttle_thread = self.shuttle_list[self.shuttle_seq]
        while True:
            if pre_shuttle_thread != self.shuttle_list[self.shuttle_seq]:
                break
            self.driver.refresh()
            elements = self.get_elements_by_classnames(self.shuttle_widget_group.target_classes_widget.text())
            updated_text_parser = UpdatedTextParser(elements=elements,
                                                    filtering_keyword=self.shuttle_widget_group.filtering_keyword_widget.text(),
                                                    text_list=text_list)
            collected_text = updated_text_parser.parse()
            if len(collected_text) > 0:
                self._print_to_state_widget(collected_text)
                sound.play()
            self.waiting_event.set()
            self.stop_event.wait(timeout=int(self.shuttle_widget_group.period_widget.text()))
        self.driver.quit()

    def _print_to_state_widget(self, collected_text):
        log_text = LogText(self.shuttle_widget_group.shuttle_name_widget.text(), DefaultTime())
        self.shuttle_widget_group.state_widget.append(f"{log_text.updated_shuttle_name()}")
        self.shuttle_widget_group.state_widget.append(f"{self.url}\n")
        self.shuttle_widget_group.state_widget.append(f"{collected_text}\n")

    def stop(self):
        self.shuttle_list[self.shuttle_seq] = None
        self.stop_event.set()

    def execute_script(self, script):
        return self.driver.execute_script(script)

    def scroll_to(self, x, y):
        self.execute_script("window.scrollBy({0}, {1});".format(x, y))

    def get_target_element(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".ws-target-element")[0]

    def get_scroll_y(self):
        return self.execute_script("return window.scrollY;")

    def get_scroll_x(self):
        return self.execute_script("return window.scrollX;")

    def get_element_pos_x(self):
        return self.execute_script(
            '''
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().left-3;
            '''
        )

    def get_element_pos_y(self):
        return self.execute_script(
            '''
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().top-3;
            '''
        )

    def get_element_class_names_of_target(self):
        return self.execute_script(
            '''
            const ws_target_element = document.getElementsByClassName('ws-target-element')[0];
            let className = ws_target_element.className;
            const startIdx = className.indexOf(' ws-target-element');
            return className.substring(0, startIdx); 
            '''
        )

    def get_element_id(self):
        return self.execute_script(
            '''
            const ws_target_element = document.getElementsByClassName('ws-target-element')[0];
            return ws_target_element.id;
            '''
        )

    def get_elements_by_classnames(self, class_names):
        return self.execute_script(
            'return document.getElementsByClassName("' + class_names + '")'
        )

    def is_selected_elements(self):
        return self.execute_script(
            '''
            const len = document.getElementsByClassName('ws-target-element').length;
            return len > 0 ? true : false;
            '''
        )
