from events.event_base import Event


class GameOverEvent(Event):
    def __init__(self):
        super().__init__()
