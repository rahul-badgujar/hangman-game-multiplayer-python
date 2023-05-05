from events.event_base import Event


class GameStartedEvent(Event):
    def __init__(self):
        super().__init__()
