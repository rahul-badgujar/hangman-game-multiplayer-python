from game_config import MAX_INCORRECT_GUESSES


class HangmanPlayer:
    def __init__(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name
        self.guesses_so_far = list()
        self.incorrect_guesses_left = MAX_INCORRECT_GUESSES

    def can_play_chance(self):
        return self.incorrect_guesses_left > 1
