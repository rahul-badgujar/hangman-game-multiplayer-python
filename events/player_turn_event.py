from events.event_base import Event


class PlayerTurnEvent(Event):
    def __init__(self, current_guessed_word: str):
        super().__init__()
        self.current_guessed_word = current_guessed_word
