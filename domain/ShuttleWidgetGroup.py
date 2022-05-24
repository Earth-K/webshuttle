from PyQt5.QtWidgets import QTextEdit, QPushButton


class ShuttleWidgetGroup:
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

    def updated_list(self):
        return self.update_list_widget

    def saveSettings(self):
        self.parent.shuttleWidgets.url_widget.setText(self.url_widget.text())
        self.parent.shuttleWidgets.shuttle_name_widget.setText(self.shuttle_name_widget.text())
        self.parent.shuttleWidgets.target_classes_widget.setText(self.target_classes_widget.text())
        self.parent.shuttleWidgets.period_widget.setValue(self.period_widget.value())
