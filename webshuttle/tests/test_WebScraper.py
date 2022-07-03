from unittest.mock import Mock, MagicMock

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from webshuttle.domain.WebScraper import WebScraper


def _create_mock_webdriver():
    mock = Mock(webdriver)
    mock.options = None
    mock.maximize_window = MagicMock(return_value=None)
    mock.implicitly_wait = MagicMock(return_value=None)
    mock.get = MagicMock(return_value=None)
    return mock


def test_driver_execute_script():
    script = """
    let body = document.getElementByTag('body');
    return body;
    """
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=script)
    sut = WebScraper(start_url="", driver=mock)

    result = sut.execute_script(script)

    mock.execute_script.assert_called_once_with(script)


def test_scroll_to():
    x, y = 0, 100
    script = "window.scrollBy({0}, {1});".format(x, y)
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = WebScraper(start_url="", driver=mock)

    sut.scroll_to(x, y)

    mock.execute_script.assert_called_once_with(script)


def test_get_target_element():
    mock = _create_mock_webdriver()
    mock.find_elements = MagicMock(return_value=[WebElement(None, None)])
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_target_element()

    mock.find_elements.assert_called_once_with(By.CSS_SELECTOR, ".ws-target-element")


def test_get_scroll_y():
    script = "return window.scrollY;"
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_scroll_y()

    mock.execute_script.assert_called_once_with(script)


def test_get_scroll_x():
    script = "return window.scrollX;"
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_scroll_x()

    mock.execute_script.assert_called_once_with(script)


def test_get_element_pos_x():
    script = """
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().left-3;
            """
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_element_pos_x()

    mock.execute_script.assert_called_once_with(script)


def test_get_element_pos_y():
    script = """
            let targetElement = document.getElementById('ws-tooltip');
            return targetElement.getBoundingClientRect().top-3;
            """
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=None)
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_element_pos_y()

    mock.execute_script.assert_called_once_with(script)


def test_get_element_class_names_of_target():
    class_names_of_target = "class1 class2"
    script = '''
            const ws_target_element = document.getElementsByClassName('ws-target-element')[0];
            let className = ws_target_element.className;
            const startIdx = className.indexOf(' ws-target-element');
            return className.substring(0, startIdx); 
            '''
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=class_names_of_target)
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_element_class_names_of_target()

    mock.execute_script.assert_called_once_with(script)
    assert (class_names_of_target == result)


def test_get_element_id():
    script = '''
            const ws_target_element = document.getElementsByClassName('ws-target-element')[0];
            return ws_target_element.id;
            '''
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value="id")
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_element_id()

    mock.execute_script.assert_called_once_with(script)
    assert (result == "id")


def test_get_elements_by_classnames():
    class_names = "class1 class2"
    script = 'return document.getElementsByClassName("' + class_names + '")'
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value="class1 class2")
    sut = WebScraper(start_url="", driver=mock)

    result = sut.get_elements_by_classnames(class_names)

    mock.execute_script.assert_called_once_with(script)
    assert (class_names == result)


def test_is_selected_elements():
    script = '''
            const len = document.getElementsByClassName('ws-target-element').length;
            return len > 0 ? true : false;
            '''
    mock = _create_mock_webdriver()
    mock.execute_script = MagicMock(return_value=bool())
    sut = WebScraper(start_url="", driver=mock)

    result = sut.is_selected_elements()

    mock.execute_script.assert_called_once_with(script)
    assert (type(result) == bool)


def test_quit_driver():
    mock = _create_mock_webdriver()
    mock.quit = MagicMock(return_value=None)
    sut = WebScraper(start_url="", driver=mock)

    sut.quit_driver()

    mock.quit.assert_called_once()
