class LogText:

    def __init__(self, local_time):
        self.now = local_time

    def _formatted_localtime(self):
        now = self.now
        return "%04d/%02d/%02d %02d:%02d:%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    def updated_shuttle_name(self, shuttle_name):
        return f"[{shuttle_name}] {self._formatted_localtime()}"

    def stopped_shuttle(self, shuttle_name):
        return f"[{shuttle_name}] 셔틀이 멈췄습니다. {self._formatted_localtime()}\n"
