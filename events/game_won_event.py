from events.event_base import Event


class GameWonEvent(Event):
    def __init__(self):
        super().__init__()
