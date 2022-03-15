class EventListenerInjector:

    def __init__(self, web_crawler):
        self._web_crawler = web_crawler

    def add_mouseover(self):
        self._execute_js("./resource/js/add_mouseover.js")

    def add_mouseleave(self):
        self._execute_js("./resource/js/add_mouseleave.js")

    def add_tooltip(self):
        self._execute_js("./resource/js/add_tooltip.js")

    def add_mousedown_right(self):
        self._execute_js("./resource/js/add_mousedown.js")

    def add_origin_background_color(self):
        self._execute_js("./resource/js/add_originBackgroundColor.js")

    def _execute_js(self, file_path):
        jsFile = open(file_path, "r", encoding='cp949')
        self._web_crawler.execute_js(jsFile.read())
        jsFile.close()
