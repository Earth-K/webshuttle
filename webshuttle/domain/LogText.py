class LogText:

    def __init__(self, local_time):
        self.now = local_time

    def formatted_localtime(self):
        now = self.now
        return "%04d/%02d/%02d %02d:%02d:%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    def updated_shuttle_name(self, shuttle_name):
        return f"[{shuttle_name}] {self.formatted_localtime()}"

    def started_shuttle(self, shuttle_name):
        return f"[{shuttle_name}] 셔틀이 스크랩을 시작합니다. {self.formatted_localtime()}\n"

    def stopped_shuttle(self, shuttle_name):
        return f"[{shuttle_name}] 셔틀이 스크랩을 멈춥니다. {self.formatted_localtime()}\n"

    def removed_shuttle(self, shuttle_name):
        return f"[{shuttle_name}] 셔틀이 삭제되었습니다. {self.formatted_localtime()}\n"
