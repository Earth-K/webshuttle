from PyQt5.QtWidgets import QLineEdit, QSpinBox

from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup


class DraftShuttleWidgets:
    def __init__(self, shuttle_widget_group: ShuttleWidgetGroup):
        self.name_widget = QLineEdit(shuttle_widget_group.shuttle_name_widget.text())
        self.url_widget = QLineEdit(shuttle_widget_group.url_widget.text())
        self.period_widget = QSpinBox()
        self.period_widget.setMaximum(86400)
        self.period_widget.setValue(shuttle_widget_group.period_widget.value())
        self.target_classes_widget = QLineEdit(shuttle_widget_group.target_classes_widget.text())
        self.filtering_keyword_widget = QLineEdit(shuttle_widget_group.filtering_keyword_widget.text())

