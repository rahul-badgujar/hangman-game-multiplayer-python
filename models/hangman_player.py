class HangmanPlayer:
    def __init__(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name
        self.guesses_so_far = set()

    def get_word_guessed_so_far(self, word):
        guesses = []
        for c in word.upper():
            if c in self.guesses_so_far:
                guesses.append(c)
            else:
                guesses.append('_')
        return ' '.join(guesses)

    def consider_guess(self, guessed_char: str):
        self.guesses_so_far.add(guessed_char.upper())

    def has_guessed_all(self, word) -> bool:
        return self.get_word_guessed_so_far(word).count('_') <= 0
