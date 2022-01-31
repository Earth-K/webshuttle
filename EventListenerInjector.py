class EventListenerInjector:

    def __init__(self, web_crawler):
        self._web_crawler = web_crawler

    def add_mouseover(self):
        jsFile = open("js/add_mouseover.js", "r")
        self._web_crawler.execute_js(jsFile.read())
        jsFile.close()

    def add_mouseleave(self):
        jsFile = open("js/add_mouseleave.js", "r")
        self._web_crawler.execute_js(jsFile.read())
        jsFile.close()

    def add_tooltip(self):
        jsFile = open("js/add_tooltip.js", "r")
        self._web_crawler.execute_js(jsFile.read())
        jsFile.close()

    def add_mousedown_right(self):
        jsFile = open("js/add_mousedown_right.js", "r")
        self._web_crawler.execute_js(jsFile.read())
        jsFile.close()
