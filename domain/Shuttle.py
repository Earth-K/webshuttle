import threading

import pygame
from selenium import webdriver

from domain.DefaultTime import DefaultTime
from domain.LogText import LogText
from domain.WebScraper import WebScraper


def get_text_list(elements):
    result = []
    for e in elements:
        result.append(e.text)
    return result


class Shuttle:
    def __init__(self, shuttles, shuttle_seq, shuttle_name_widget, url_widget, period_widget, target_classes_widget,
                 log_edittext_widget, start_btn_widget, chrome_service, time=DefaultTime()):
        self.shuttles = shuttles
        self.shuttle_seq = shuttle_seq
        self.start_btn_widget = start_btn_widget
        self.log_edittext_widget = log_edittext_widget
        self.target_classes_widget = target_classes_widget
        self.period_widget = period_widget
        self.url_widget = url_widget
        self.shuttle_name_widget = shuttle_name_widget
        self.id = shuttle_seq
        self.chrome_service = chrome_service
        self.time = time
        self.sound = pygame.mixer.Sound("resource/sounds/sound.wav")

    def start(self):
        self._create_thread().start()

    def stop(self):
        self.shuttles[self.shuttle_seq] = None

    def _create_thread(self):
        return threading.Thread(target=self._start_scrap_thread, daemon=False, args=(
            self.shuttle_seq, self.shuttle_name_widget, self.url_widget, self.period_widget, self.target_classes_widget,
            self.log_edittext_widget))

    def _start_scrap_thread(self, shuttle_seq, shuttle_name, url_widget, period, target_classes, log_edittext_widget):
        threading.Thread(target=self._run_scrap, daemon=False, args=(
            shuttle_seq, shuttle_name.text(), url_widget.text(), int(period.text()), target_classes.text(),
            log_edittext_widget)).start()

    def _run_scrap(self, shuttle_seq, shuttle_name, url, period, target_classes, log_edittext_widget):
        pre_shuttle_thread = self.shuttles[shuttle_seq]
        text_list = []
        while True:
            if pre_shuttle_thread != self.shuttles[shuttle_seq]:
                break
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("--start-maximized")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebScraper(url, options, self.chrome_service)
            self.time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(target_classes)
            no_newline_text = ""
            if len(text_list) > 0:
                new_text_list = get_text_list(elements)
                for new_text in new_text_list:
                    if new_text not in text_list:
                        if len(new_text) > 0:
                            # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                            no_newline_text += new_text.replace("\n", " | ") + "\n"
                text_list = new_text_list
            else:
                for e in elements:
                    if len(e.text) > 0:
                        text_list.append(e.text)
                        # 한 번에 보이는 정보의 양을 늘리기 위해 줄 바꿈 문자를 | 로 변경함
                        no_newline_text += e.text.replace("\n", " | ") + "\n"
            if len(no_newline_text) > 0:
                log_text = LogText(self.time.localtime())
                log_edittext_widget.append(log_text.updated_shuttle_name(shuttle_name))
                log_edittext_widget.append(f"{no_newline_text}\n")
                self.sound.play()

            tmp_web_crawler.close_driver()
            self.time.sleep(period)
