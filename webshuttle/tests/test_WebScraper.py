import sys
from unittest.mock import Mock, MagicMock

import pytest
from PyQt5.QtWidgets import QWidget, QLineEdit, QApplication
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup
from webshuttle.domain.WebScraper import WebScraper


def _create_mock_webdriver():
    mock = Mock(webdriver)
    mock.options = None
    mock.maximize_window = MagicMock(return_value=None)
    mock.implicitly_wait = MagicMock(return_value=None)
    mock.get = MagicMock(return_value=None)
    return mock


def _default_shuttle_widget_group():
    return ShuttleWidgetGroup(QWidget(), QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit())


def _default_web_scraper(mock):
    return WebScraper(shuttle_widget_group=_default_shuttle_widget_group(), driver=mock, shuttle_list=[], shuttle_seq=0)


@pytest.fixture
def qapp():
    return QApplication(sys.argv)


def test_driver_execute_script(qapp):
    script = """
    let body = document.getElementByTag('body');
    return body;
    """
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=script)
    sut = _default_web_scraper(mock)

    sut.execute_script(script)

    mock.execute_script.assert_called_once_with(script)


def test_scroll_to(qapp):
    x, y = 0, 100
    script = "window.scrollBy({0}, {1});".format(x, y)
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = _default_web_scraper(mock)

    sut.scroll_to(x, y)

    mock.execute_script.assert_called_once_with(script)


def test_get_target_element(qapp):
    mock = _create_mock_webdriver()
    mock.find_elements = MagicMock(return_value=[WebElement(None, None)])
    sut = _default_web_scraper(mock)

    result = sut.get_target_element()

    mock.find_elements.assert_called_once_with(By.CSS_SELECTOR, ".ws-target-element")


def test_get_scroll_y(qapp):
    script = "return window.scrollY;"
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = _default_web_scraper(mock)

    result = sut.get_scroll_y()

    mock.execute_script.assert_called_once_with(script)


def test_get_scroll_x(qapp):
    script = "return window.scrollX;"
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = _default_web_scraper(mock)

    result = sut.get_scroll_x()

    mock.execute_script.assert_called_once_with(script)


def test_get_element_pos_x(qapp):
    script = """
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().left-3;
            """
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = _default_web_scraper(mock)

    result = sut.get_element_pos_x()

    mock.execute_script.assert_called_once_with(script)


def test_get_element_pos_y(qapp):
    script = """
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().top-3;
            """
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = _default_web_scraper(mock)

    result = sut.get_element_pos_y()

    mock.execute_script.assert_called_once_with(script)


def test_get_element_class_names_of_target(qapp):
    class_names_of_target = "class1 class2"
    script = '''
            const ws_target_element = document.getElementsByClassName('ws-target-element')[0];
            let className = ws_target_element.className;
            const startIdx = className.indexOf(' ws-target-element');
            return className.substring(0, startIdx); 
            '''
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=class_names_of_target)
    sut = _default_web_scraper(mock)

    result = sut.get_element_class_names_of_target()

    mock.execute_script.assert_called_once_with(script)
    assert (class_names_of_target == result)


def test_get_element_id(qapp):
    script = '''
            const ws_target_element = document.getElementsByClassName('ws-target-element')[0];
            return ws_target_element.id;
            '''
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value="id")
    sut = _default_web_scraper(mock)

    result = sut.get_element_id()

    mock.execute_script.assert_called_once_with(script)
    assert (result == "id")


def test_get_elements_by_classnames(qapp):
    class_names = "class1 class2"
    script = 'return document.getElementsByClassName("' + class_names + '")'
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value="class1 class2")
    sut = _default_web_scraper(mock)

    result = sut.get_elements_by_classnames(class_names)

    mock.execute_script.assert_called_once_with(script)
    assert (class_names == result)


def test_is_selected_elements(qapp):
    script = '''
            const len = document.getElementsByClassName('ws-target-element').length;
            return len > 0 ? true : false;
            '''
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=bool())
    sut = _default_web_scraper(mock)

    result = sut.is_selected_elements()

    mock.execute_script.assert_called_once_with(script)
    assert (type(result) == bool)


def test_quit_driver(qapp):
    mock = _create_mock_webdriver()
    mock.quit = MagicMock(return_value=None)
    sut = _default_web_scraper(mock)

    sut.quit_driver()

    mock.quit.assert_called_once()
