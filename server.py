import socket
import random

from events.game_lost_event import GameLostEvent
from events.game_over_event import GameOverEvent
from events.game_won_event import GameWonEvent
from events.player_turn_event import PlayerTurnEvent
from events.event_base import Event
from events.event_utils import decode_event, encode_event
from events.host_message_event import HostMessageEvent
from events.player_invitation_acceptance_event import PlayerInvitationAcceptanceEvent
from events.player_invitation_event import PlayerInvitationEvent
from events.player_played_turn_event import PlayerPlayedTurnEvent
from exceptions.unexpected_event_exception import UnexpectedEventException
from game_config import words, NO_OF_PLAYERS, HOST_PORT
from models.hangman_player import HangmanPlayer
from models.player_connection import PlayerConnection


def get_word():
    return random.choice(words)


def main():
    server_socket = socket.socket()
    host = socket.gethostname()
    port = HOST_PORT
    server_socket.bind((host, port))
    print(f"New Hangman Game started at {host}:{port}")
    # Listen for incoming connections
    server_socket.listen(NO_OF_PLAYERS)

    # To store connections from players
    connected_players = dict()

    def send_client_event(client_socket: socket, event: Event):
        client_socket.sendall(encode_event(event))

    def broadcast_event_to_all_players(event: Event):
        for player_connection in connected_players.values():
            send_client_event(player_connection.socket, event)

    def poll_client_event(client_socket: socket):
        received_data = client_socket.recv(1024)
        return decode_event(received_data)

    def get_connected_players_names():
        return [hangman_player.player.player_name for hangman_player in connected_players.values()]

    print("Waiting for players to join...")

    next_player_id_to_propose = 0
    while len(connected_players.values()) < NO_OF_PLAYERS:
        player_socket, player_address = server_socket.accept()
        print("Received a game join request.")
        print("Sending game invitation...")
        send_client_event(player_socket, PlayerInvitationEvent(proposed_player_id=next_player_id_to_propose))
        next_player_id_to_propose += 1
        print("Waiting for invitation to get accepted...")
        polled_event = poll_client_event(player_socket)
        if not isinstance(polled_event, PlayerInvitationAcceptanceEvent):
            raise UnexpectedEventException(expected_event_type=PlayerInvitationAcceptanceEvent)
        print(f"Player accepted the game invitation. Player name is {polled_event.player_name}")
        # register player for game
        connected_players[polled_event.invitation_event.proposed_player_id] = PlayerConnection(player_socket,
                                                                                               HangmanPlayer(
                                                                                                   polled_event.invitation_event.proposed_player_id,
                                                                                                   polled_event.player_name))
        # send game lobby update event to all the players
        lobby_update_message = f"HOST: In Lobby {', '.join(get_connected_players_names())}."
        players_remaining_to_join = NO_OF_PLAYERS - len(connected_players)
        if players_remaining_to_join <= 0:
            lobby_update_message = f"{lobby_update_message} All players have joined."
        else:
            lobby_update_message = f"{lobby_update_message} Waiting for {players_remaining_to_join} players to join."
        broadcast_event_to_all_players(HostMessageEvent(
            update_message=lobby_update_message))

    # Generate the word for the game
    word = get_word()
    print(f"Selected word for game is {word}")

    game_start_message = f"HOST: Game has started. You have to guess a word of {len(word)} characters."
    broadcast_event_to_all_players(HostMessageEvent(update_message=game_start_message))

    game_completed = False
    # Play turns of each player
    while not game_completed:
        for player_connection in connected_players.values():
            current_player = player_connection.player
            current_player_socket = player_connection.socket
            # tell all the players who is playing the current turn
            player_turn_message = f"HOST: {current_player.player_name} is playing the turn.."
            broadcast_event_to_all_players(HostMessageEvent(player_turn_message))
            # send play turn event to current player
            send_client_event(current_player_socket, PlayerTurnEvent(current_player.get_word_guessed_so_far(word)))
            # wait for player to complete the turn
            player_turn_event = poll_client_event(current_player_socket)
            if not isinstance(player_turn_event, PlayerPlayedTurnEvent):
                raise UnexpectedEventException(expected_event_type=PlayerPlayedTurnEvent)
            # mark player played guess
            current_player.consider_guess(player_turn_event.guessed_character)
            # check if player has won the game
            if current_player.has_guessed_all(word):
                # announce game winner name
                game_winner_announcement_message = f"HOST: {current_player.player_name} has won the game!!!"
                broadcast_event_to_all_players(HostMessageEvent(update_message=game_winner_announcement_message))
                # send game win event to current player
                send_client_event(current_player_socket, GameWonEvent())
                # send game lost event to other players
                for connected_player in connected_players.values():
                    if connected_player.player.player_id != current_player.player_id:
                        send_client_event(connected_player.socket, GameLostEvent())
                # send game over event to all
                broadcast_event_to_all_players(GameOverEvent())
                game_completed = True
                break

    # Close the sockets
    for player_connection in connected_players.values():
        player_connection.socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
