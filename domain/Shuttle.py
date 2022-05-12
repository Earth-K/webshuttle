import threading

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
    def __init__(self, shuttles, shuttle_seq, shuttle_widget_group, chrome_service, mixer_sound, time=DefaultTime()):
        self.shuttles = shuttles
        self.id = shuttle_seq
        self.shuttle_widget_group = shuttle_widget_group
        self.chrome_service = chrome_service
        self.time = time
        self.sound = mixer_sound

    def start(self):
        self._create_thread().start()

    def stop(self):
        self.shuttles[self.id] = None

    def _create_thread(self):
        return threading.Thread(target=self._start_scrap_thread, daemon=False, args=(
            self.id, self.shuttle_widget_group))

    def _start_scrap_thread(self, id, shuttle_widget_group):
        threading.Thread(target=self._run_scrap, daemon=False, args=(
            id, shuttle_widget_group)).start()

    def _run_scrap(self, id, shuttle_widget_group):
        pre_shuttle_thread = self.shuttles[id]
        text_list = []
        while True:
            if pre_shuttle_thread != self.shuttles[id]:
                break
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument("--start-maximized")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            tmp_web_crawler = WebScraper(shuttle_widget_group.url_widget.text(), options, self.chrome_service)
            self.time.sleep(1)
            elements = tmp_web_crawler.get_elements_by_classnames(shuttle_widget_group.target_classes_widget.text())
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
                shuttle_widget_group.update_list_widget.append(log_text.updated_shuttle_name(shuttle_widget_group.shuttle_name_widget.text()))
                shuttle_widget_group.update_list_widget.append(f"{no_newline_text}\n")
                self.sound.play()

            tmp_web_crawler.close_driver()
            self.time.sleep(int(shuttle_widget_group.period_widget.text()))
