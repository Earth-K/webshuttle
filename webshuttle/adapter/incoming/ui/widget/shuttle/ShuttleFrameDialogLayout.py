from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from webshuttle.adapter.incoming.ui.widget.shuttle import ShuttleFrame


class ShuttleFrameDialogLayout(QVBoxLayout):
    def __init__(self, shuttle_frame: ShuttleFrame, dialog, shuttles_widget):
        super().__init__()
        self.frame_name = shuttle_frame.frame_name.text()
        self.shuttles_widget = shuttles_widget
        self.draft_shuttleWidgets = shuttle_frame.draft_shuttleWidgets
        self.shuttle_widget_group = shuttle_frame.shuttle_widget_group

        name_hBoxLayout = QHBoxLayout()
        name_hBoxLayout.addWidget(QLabel("셔틀 이름 : "))
        name_hBoxLayout.addWidget(self.draft_shuttleWidgets.name_widget)
        self.addLayout(name_hBoxLayout)
        url_hBoxLayout = QHBoxLayout()
        url_hBoxLayout.addWidget(QLabel("URL : "))
        url_hBoxLayout.addWidget(self.draft_shuttleWidgets.url_widget)
        self.addLayout(url_hBoxLayout)
        period_hBoxLayout = QHBoxLayout()
        period_hBoxLayout.addWidget(QLabel("반복 주기(초) : "))
        period_hBoxLayout.addWidget(self.draft_shuttleWidgets.period_widget)
        self.addLayout(period_hBoxLayout)
        classes_hBoxLayout = QHBoxLayout()
        classes_hBoxLayout.addWidget(QLabel("타깃 클래스 : "))
        classes_hBoxLayout.addWidget(self.draft_shuttleWidgets.target_classes_widget)
        self.addLayout(classes_hBoxLayout)
        filtering_keyword_hBoxLayout = QHBoxLayout()
        filtering_keyword_hBoxLayout.addWidget(QLabel("필터링 키워드 : "))
        filtering_keyword_hBoxLayout.addWidget(self.draft_shuttleWidgets.filtering_keyword_widget)
        self.addLayout(filtering_keyword_hBoxLayout)

        confirm_hBoxLayout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.apply_draft(dialog))
        confirm_hBoxLayout.addWidget(ok_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.cancel_draft(dialog))
        confirm_hBoxLayout.addWidget(cancel_button)
        self.addLayout(confirm_hBoxLayout)

    def apply_draft(self, widget):
        self.shuttle_widget_group.notify_update()
        self.shuttles_widget.save_shuttles()
        widget.close()

    def cancel_draft(self, widget):
        self.draft_shuttleWidgets.url_widget.setText(self.shuttle_widget_group.url_widget.text())
        self.draft_shuttleWidgets.name_widget.setText(self.shuttle_widget_group.shuttle_name_widget.text())
        self.draft_shuttleWidgets.target_classes_widget.setText(self.shuttle_widget_group.target_classes_widget.text())
        self.draft_shuttleWidgets.period_widget.setValue(self.shuttle_widget_group.period_widget.value())
        self.draft_shuttleWidgets.filtering_keyword_widget.setText(self.shuttle_widget_group.filtering_keyword_widget.text())
        self.draft_shuttleWidgets.name_widget.setText(self.frame_name)
        widget.close()
