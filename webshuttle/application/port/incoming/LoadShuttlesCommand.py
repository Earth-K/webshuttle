from webshuttle.adapter.incoming.ui.widget import StateWidget, ShuttlesWidget


class LoadShuttlesCommand:
    def __init__(self, shuttles_widget: ShuttlesWidget, state_widget: StateWidget):
        self.shuttles_widget = shuttles_widget
        self.state_widget = state_widget

        if shuttles_widget is None:
            raise ValueError
        if state_widget is None:
            raise ValueError
