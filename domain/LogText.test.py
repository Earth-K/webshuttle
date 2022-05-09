import time
import unittest

from domain.LogText import LogText


class LogTextTest(unittest.TestCase):
    def setUp(self) -> None:
        self.TIME_20200913_212640 = 1600000000
        self.TEXT_20200913_212640 = '2020/09/13 21:26:40'
        self.SHUTTLE_NAME = "Shuttle Name"

    def test_updated_shuttle_name(self):
        self.assertEqual(LogText(time.localtime(self.TIME_20200913_212640)).updated_shuttle_name(self.SHUTTLE_NAME),
                         f'[{self.SHUTTLE_NAME}] {self.TEXT_20200913_212640}')

    def test_started_shuttle(self):
        self.assertEqual(LogText(time.localtime(self.TIME_20200913_212640)).started_shuttle(self.SHUTTLE_NAME),
                         f'[{self.SHUTTLE_NAME}] 셔틀이 스크랩을 시작합니다. {self.TEXT_20200913_212640}\n')

    def test_stopped_shuttle(self):
        self.assertEqual(LogText(time.localtime(self.TIME_20200913_212640)).stopped_shuttle(self.SHUTTLE_NAME),
                         f'[{self.SHUTTLE_NAME}] 셔틀이 스크랩을 멈춥니다. {self.TEXT_20200913_212640}\n')

    def test_removed_shuttle(self):
        self.assertEqual(LogText(time.localtime(self.TIME_20200913_212640)).removed_shuttle(self.SHUTTLE_NAME),
                         f'[{self.SHUTTLE_NAME}] 셔틀이 삭제되었습니다. {self.TEXT_20200913_212640}\n')


if __name__ == '__main__':
    unittest.main()
