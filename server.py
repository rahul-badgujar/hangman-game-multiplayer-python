import socket
import random

from events.event_base import Event
from events.event_utils import decode_event, encode_event
from events.player_invitation_acceptance_event import PlayerInvitationAcceptanceEvent
from events.player_invitation_event import PlayerInvitationEvent
from game_config import words, NO_OF_PLAYERS
from models.hangman_player import HangmanPlayer
from models.player_connection import PlayerConnection


def get_word():
    return random.choice(words)


def main():
    server_socket = socket.socket()
    host = socket.gethostname()
    port = 10001
    server_socket.bind((host, port))
    print(f"New Hangman Game started at {host}:{port}")
    # Listen for incoming connections
    server_socket.listen(NO_OF_PLAYERS)

    def send_client_event(client_socket: socket, event: Event):
        client_socket.sendall(encode_event(event))

    def poll_client_event(client_socket: socket):
        received_data = client_socket.recv(1024).decode('utf-8')
        return decode_event(received_data)

    print("Waiting for players to join...")

    # Accept connections from players
    connected_players = dict()
    next_player_id_to_propose = 0
    while len(connected_players.values()) < NO_OF_PLAYERS:
        player_socket, player_address = server_socket.accept()
        print("Received a game join request.")
        print("Sending game invitation...")
        player_socket.sendall(PlayerInvitationEvent(proposed_player_id=next_player_id_to_propose))
        next_player_id_to_propose += 1
        print("Waiting for invitation to get accepted...")
        polled_event = poll_client_event(player_socket)
        if isinstance(polled_event, PlayerInvitationAcceptanceEvent):
            print(f"Player accepted the game invitation. Player name is {polled_event.player_name}")
            # register player for game
            connected_players[polled_event.invitation_event.proposed_player_id] = PlayerConnection(player_socket,
                                                                                                   HangmanPlayer(
                                                                                                       polled_event.invitation_event.proposed_player_id,
                                                                                                       polled_event.player_name))
            # send game lobby update event to all the players
        else:
            print(f"Unexpected event received, was expecting {PlayerInvitationEvent.__name__}")

    # Generate the word for the game
    word = get_word()

    # send game started event to all players

    # Create a list of underscores to represent the unknown letters in the word
    word_display = ["_"] * len(word)

    # # Keep track of the number of incorrect guesses
    # incorrect_guesses = 0
    #
    # # Keep playing until the word is guessed or the maximum number of incorrect guesses is reached
    # while "_" in word_display and incorrect_guesses < MAX_INCORRECT_GUESSES:
    #     # Send the current state of the game to all players
    #     for player_socket in player_sockets:
    #         player_socket.sendall(str.encode(" ".join(word_display)))
    #
    #     # Get the guess from the player
    #     guess = player_sockets[0].recv(1024).decode()
    #     print("Player 1 guesses:", guess)
    #
    #     # Check if the guess is correct
    #     if guess in word:
    #         # Update the display with the guessed letter
    #         for i in range(len(word)):
    #             if word[i] == guess:
    #                 word_display[i] = guess
    #     else:
    #         # Increment the number of incorrect guesses
    #         incorrect_guesses += 1
    #         print("Incorrect guess. You have", MAX_INCORRECT_GUESSES - incorrect_guesses, "guesses left.")
    #
    #     # Rotate the player sockets list so that the next player gets to guess
    #     player_sockets.append(player_sockets.pop(0))
    #
    #     # Check if the game is over
    #     if "_" not in word_display:
    #         # Notify all players that the game has ended and who won
    #         for player_socket in player_sockets:
    #             player_socket.sendall(str.encode("Game over! Player 1 wins! The word was " + word))
    #     elif incorrect_guesses == MAX_INCORRECT_GUESSES:
    #         # Notify all players that the game has ended and who won
    #         for player_socket in player_sockets:
    #             player_socket.sendall(
    #                 str.encode("Game over! Player " + str(len(player_sockets)) + " wins! The word was " + word))
    #
    # # Close the sockets
    # for player_socket in player_sockets:
    #     player_socket.close()
    # server_socket.close()


if __name__ == '__main__':
    main()
