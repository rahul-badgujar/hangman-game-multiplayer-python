from events.event_base import Event


class GameOverEvent(Event):
    def __init__(self, did_won: bool, winner_player_name: str):
        super().__init__()
        self.did_won = did_won
        self.winner_player_name = winner_player_name
