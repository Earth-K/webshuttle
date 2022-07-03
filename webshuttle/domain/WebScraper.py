from selenium import webdriver
from selenium.webdriver.common.by import By


class WebScraper:
    def __init__(self, start_url, driver):
        self.start_url = start_url
        if start_url == '':
            self.start_url = 'http://google.com'
        if not self.start_url.startswith('http://') | self.start_url.startswith('https://'):
            self.start_url = 'http://' + start_url
        self.driver: webdriver.Chrome = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)
        self.driver.get(self.start_url)

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

    def quit_driver(self):
        self.driver.quit()
