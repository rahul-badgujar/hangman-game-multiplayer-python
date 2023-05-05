from events.event_base import Event


class GameLostEvent(Event):
    def __init__(self):
        super().__init__()
