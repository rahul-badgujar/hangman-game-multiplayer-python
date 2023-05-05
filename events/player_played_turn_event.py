from events.event_base import Event


class PlayerPlayedTurnEvent(Event):
    def __init__(self, guessed_character):
        super().__init__()
        self.guessed_character = guessed_character
