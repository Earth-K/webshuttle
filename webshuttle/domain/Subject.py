from webshuttle.domain import Observer


class Subject:
    def register_observer(self, observer: Observer):
        pass

    def remove_observer(self, observer: Observer):
        pass

    def notify_update(self):
        pass
