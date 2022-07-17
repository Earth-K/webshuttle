from PyQt5.QtWidgets import QMessageBox

from webshuttle.application.port.incoming.ParseTargetElementsUseCase import ParseTargetElementsUseCase
from webshuttle.domain.DefaultTime import DefaultTime
from webshuttle.domain.LogText import LogText


class ParseTargetElementsService(ParseTargetElementsUseCase):
    def __init__(self, shuttle_add_widget, web_scraper, elements_report_widget):
        self._web_scraper = web_scraper
        self._shuttle_add_widget = shuttle_add_widget
        self._elements_report_widget = elements_report_widget

    def parse(self):
        if self._web_scraper is None or self._web_scraper.is_selected_elements() is False:
            QMessageBox.information(self._shuttle_add_widget, 'Error',
                                    '먼저 선택 영역을 선택하고 데이터를 불러오세요.\n'
                                    '1. 스크랩 하고 싶은 데이터가 있는 웹 페이지의 URL을 입력하세요.\n'
                                    "2. '영역 선택하러 가기' 버튼을 클릭하세요.\n"
                                    "3. 새로 열린 브라우저에서 마우스 우클릭으로 영역을 선택하세요.\n"
                                    "4. 웹셔틀의 '선택 영역 데이터 불러오기' 버튼을 클릭하세요.\n",
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return

        element_class_names = self._web_scraper.get_element_class_names_of_target()
        self._elements_report_widget.setText(
            '{0} - get target element data.\n'.format(LogText('New Shuttle', DefaultTime().localtime()).localtime()))
        self._elements_report_widget.append('class names : {0}'.format(element_class_names))
        self._elements_report_widget.append('id : {0}'.format(self._web_scraper.get_element_id()))
        elements = self._web_scraper.get_elements_by_classnames(element_class_names)
        self._elements_report_widget.append('--- elements with same class ---\n')
        for e in elements:
            self._elements_report_widget.append('{0}\n'.format(e.text))
        pass
