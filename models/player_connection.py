from socket import socket

from models.hangman_player import HangmanPlayer


class PlayerConnection:
    def __init__(self, _socket: socket, player: HangmanPlayer = None):
        self._socket = _socket
        self.player = player
