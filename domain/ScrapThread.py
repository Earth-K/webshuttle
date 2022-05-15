from PyQt5.QtCore import QThread
from selenium import webdriver

from domain.LogText import LogText
from domain.WebScraper import WebScraper


def get_text_list(elements):
    result = []
    for e in elements:
        result.append(e.text)
    return result


class ScrapThread(QThread):
    def __init__(self, parent, id, shuttle_widget_group, time, sound, shuttle_list, chrome_service):
        super().__init__(parent)
        self.id = id
        self.shuttle_widget_group = shuttle_widget_group
        self.time = time
        self.sound = sound
        self.shuttle_list = shuttle_list
        self.chrome_service = chrome_service

    def run(self) -> None:
        pre_shuttle_thread = self.shuttle_list[self.id]
        text_list = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--start-maximized")
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        tmp_web_crawler = WebScraper(start_url=self.shuttle_widget_group.url_widget.text(),
                                     driver=webdriver.Chrome(service=self.chrome_service, options=options))
        while True:
            if pre_shuttle_thread != self.shuttle_list[self.id]:
                break
            tmp_web_crawler.driver.refresh()
            self.time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(self.shuttle_widget_group.target_classes_widget.text())
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
                self.shuttle_widget_group.update_list_widget.append(
                    log_text.updated_shuttle_name(self.shuttle_widget_group.shuttle_name_widget.text()))
                self.shuttle_widget_group.update_list_widget.append(f"{no_newline_text}\n")
                self.sound.play()

            self.time.sleep(int(self.shuttle_widget_group.period_widget.text()))
        tmp_web_crawler.quit_driver()
