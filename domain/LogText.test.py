import time
import unittest
from unittest.mock import Mock

from domain.LogText import LogText

TIME_20200913_212640 = 1600000000
TEXT_20200913_212640 = '2020/09/13 21:26:40'
SHUTTLE_NAME = "Shuttle Name"

default_time = Mock()
default_time.localtime.return_value = time.localtime(TIME_20200913_212640)


class LogTextTest(unittest.TestCase):

    def test_updated_shuttle_name(self):
        self.assertEqual(LogText(default_time.localtime()).updated_shuttle_name(SHUTTLE_NAME),
                         f'[{SHUTTLE_NAME}] {TEXT_20200913_212640}')

    def test_stopped_shuttle(self):
        self.assertEqual(LogText(default_time.localtime()).stopped_shuttle(SHUTTLE_NAME),
                         f'[{SHUTTLE_NAME}] 셔틀이 멈췄습니다. {TEXT_20200913_212640}\n')


if __name__ == '__main__':
    unittest.main()
