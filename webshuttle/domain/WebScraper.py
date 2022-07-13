import threading

import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By

from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class WebScraper:
    def __init__(self, shuttle_widget_group: ShuttleWidgetGroup, driver: webdriver.Chrome, shuttle_list: list, shuttle_seq: int):
        pygame.init()
        self.shuttle_widget_group = shuttle_widget_group
        self.url = self._safe_url(shuttle_widget_group.get_url_widget().text())
        self.shuttle_seq = shuttle_seq
        self.shuttle_list = shuttle_list
        self.driver = driver
        self.text_list = []
        self.event = threading.Event()
        self.sound = pygame.mixer.Sound("resource/sounds/sound.wav")

    def _safe_url(self, url):
        result = url
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
        pre_shuttle_thread = self.shuttle_list[self.shuttle_seq]
        while True:
            if pre_shuttle_thread != self.shuttle_list[self.shuttle_seq]:
                break
            self.driver.refresh()
            DefaultTime().sleep(1)
            elements = self.get_elements_by_classnames(
                self.shuttle_widget_group.target_classes_widget.text())
            no_newline_text = ""
            if len(self.text_list) > 0:
                new_text_list = self._get_text_list(elements)
                for new_text in new_text_list:
                    if new_text not in self.text_list:
                        if len(new_text) > 0:
                            # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                            no_newline_text += new_text.replace("\n", " | ") + "\n"
                self.text_list = new_text_list
            else:
                for e in elements:
                    if len(e.text) > 0:
                        self.text_list.append(e.text)
                        # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                        no_newline_text += e.text.replace("\n", " | ") + "\n"
            if len(no_newline_text) > 0:
                log_text = LogText(self.shuttle_widget_group.shuttle_name_widget.text(), DefaultTime().localtime())
                self.shuttle_widget_group.state_widget.append(log_text.updated_shuttle_name())
                self.shuttle_widget_group.state_widget.append(f"{no_newline_text}\n")
                self.sound.play()
            self.event.wait(timeout=int(self.shuttle_widget_group.period_widget.text()))
        self.quit_driver()

    def _get_text_list(self, elements):
        result = []
        for e in elements:
            result.append(e.text)
        return result

    def quit_driver(self):
        self.driver.quit()

    def stop(self):
        self.shuttle_list[self.shuttle_seq] = None
        self.event.set()

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
