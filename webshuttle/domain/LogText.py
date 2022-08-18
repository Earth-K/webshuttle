from webshuttle.domain.DefaultTime import DefaultTime


class LogText:

    def __init__(self, shuttle_name, default_time: DefaultTime):
        self.default_time = default_time
        self.shuttle_name = shuttle_name

    def localtime(self):
        now = self.default_time.localtime()
        return "%04d/%02d/%02d %02d:%02d:%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    def updated_shuttle_name(self):
        return f"[{self.shuttle_name}] {self.localtime()}"

    def started_shuttle(self):
        return f"[{self.shuttle_name}] 셔틀이 스크랩을 시작합니다. {self.localtime()}\n"

    def stopped_shuttle(self):
        return f"[{self.shuttle_name}] 셔틀이 스크랩을 멈춥니다. {self.localtime()}\n"

    def removed_shuttle(self):
        return f"[{self.shuttle_name}] 셔틀이 삭제되었습니다. {self.localtime()}\n"
