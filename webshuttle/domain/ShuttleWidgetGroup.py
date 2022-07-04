from PyQt5.QtWidgets import QTextEdit, QPushButton

from webshuttle.domain.Observer import Observer
from webshuttle.domain.Subject import Subject


class ShuttleWidgetGroup(Subject):
    def __init__(self, update_list_widget, target_classes_widget, period_widget, url_widget,
                 shuttle_name_widget, parent=None):

        self.update_list_widget: QTextEdit = update_list_widget
        self.update_list_widget.setReadOnly(True)
        self.target_classes_widget = target_classes_widget
        self.period_widget = period_widget
        self.url_widget = url_widget
        self.shuttle_name_widget = shuttle_name_widget
        self.parent = parent
        self._saveButtonWidget: QPushButton = QPushButton("저장")
        self._saveButtonWidget.clicked.connect(self.saveSettings)
        self.observer_list: list = []

    def register_observer(self, observer: Observer):
        self.observer_list.append(observer)

    def remove_observer(self, observer: Observer):
        self.observer_list.remove(observer)

    def notify_update(self):
        for observer in self.observer_list:
            observer.update()

    def updated_list(self):
        return self.update_list_widget

    def saveSettings(self):
        self.notify_update()
