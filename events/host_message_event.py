from events.event_base import Event


class HostMessageEvent(Event):
    def __init__(self, update_message: str):
        super().__init__()
        self.update_message = update_message
