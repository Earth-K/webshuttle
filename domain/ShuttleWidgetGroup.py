from PyQt5.QtWidgets import QTextEdit


class ShuttleWidgetGroup:
    def __init__(self, start_btn_widget, update_list_widget, target_classes_widget, period_widget, url_widget,
                 shuttle_name_widget):
        self.start_btn_widget = start_btn_widget
        self.update_list_widget: QTextEdit = update_list_widget
        self.update_list_widget.setReadOnly(True)
        self.target_classes_widget = target_classes_widget
        self.period_widget = period_widget
        self.url_widget = url_widget
        self.shuttle_name_widget = shuttle_name_widget

    def updated_list(self):
        return self.update_list_widget
