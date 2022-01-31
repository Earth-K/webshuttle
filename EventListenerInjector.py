class EventListenerInjector:

    def __init__(self, web_crawler):
        self._web_crawler = web_crawler

    def add_mouseover(self):
        self._execute_js("js/add_mouseover.js")

    def add_mouseleave(self):
        self._execute_js("js/add_mouseleave.js")

    def add_tooltip(self):
        self._execute_js("js/add_tooltip.js")

    def add_mousedown_right(self):
        self._execute_js("js/add_mousedown_right.js")

    def _execute_js(self, file_path):
        jsFile = open(file_path, "r")
        self._web_crawler.execute_js(jsFile.read())
        jsFile.close()
