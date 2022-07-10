import time

from webshuttle.domain.LogText import LogText

TIME_20200913_212640 = 1600000000
TEXT_20200913_212640 = '2020/09/13 21:26:40'
SHUTTLE_NAME = "Shuttle Name"


def test_updated_shuttle_name():
    assert (LogText(SHUTTLE_NAME, time.localtime(TIME_20200913_212640)).updated_shuttle_name() ==
            f'[{SHUTTLE_NAME}] {TEXT_20200913_212640}')


def test_started_shuttle():
    assert (LogText(SHUTTLE_NAME, time.localtime(TIME_20200913_212640)).started_shuttle() ==
            f'[{SHUTTLE_NAME}] 셔틀이 스크랩을 시작합니다. {TEXT_20200913_212640}\n')


def test_stopped_shuttle():
    assert (LogText(SHUTTLE_NAME, time.localtime(TIME_20200913_212640)).stopped_shuttle() ==
            f'[{SHUTTLE_NAME}] 셔틀이 스크랩을 멈춥니다. {TEXT_20200913_212640}\n')


def test_removed_shuttle():
    assert (LogText(SHUTTLE_NAME, time.localtime(TIME_20200913_212640)).removed_shuttle() ==
            f'[{SHUTTLE_NAME}] 셔틀이 삭제되었습니다. {TEXT_20200913_212640}\n')
