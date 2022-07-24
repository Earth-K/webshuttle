from webshuttle.adapter.incoming.ui import ShuttlesWidget
from webshuttle.adapter.incoming.ui import StateWidget


class ImportShuttlesCommand:
    def __init__(self, shuttles_widget: ShuttlesWidget, state_widget: StateWidget):
        self.shuttles_widget = shuttles_widget
        self.state_widget = state_widget

        if shuttles_widget is None or type(shuttles_widget) is not ShuttlesWidget:
            raise ValueError
        if state_widget is None or type(state_widget) is not StateWidget:
            raise ValueError
