import socket

from events.game_lost_event import GameLostEvent
from events.game_over_event import GameOverEvent
from events.event_base import Event
from events.event_utils import encode_event, decode_event
from events.game_won_event import GameWonEvent
from events.host_message_event import HostMessageEvent
from events.player_invitation_event import PlayerInvitationEvent
from events.player_invitation_acceptance_event import PlayerInvitationAcceptanceEvent
from events.player_played_turn_event import PlayerPlayedTurnEvent
from events.player_turn_event import PlayerTurnEvent
from game_config import HOST_NAME, HOST_PORT

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_connection:
    print('Connecting to the server...')
    server_connection.connect((HOST_NAME, HOST_PORT))
    print('CONNECTED...')


    def send_event_to_host(event: Event):
        server_connection.sendall(encode_event(event))


    def poll_event_from_host() -> Event:
        received_data = server_connection.recv(1024)
        return decode_event(received_data)


    player_name = input("Enter your name: ")
    print("Requesting to join the active game...")
    this_hangman_player = None
    while True:
        polled_event = poll_event_from_host()
        if isinstance(polled_event, PlayerInvitationEvent):
            # received playing invitation from game
            # accepting the invitation
            send_event_to_host(PlayerInvitationAcceptanceEvent(polled_event, player_name))
            print("Successfully joined the game. Game will start once all the players join.")
        elif isinstance(polled_event, HostMessageEvent):
            print(polled_event.update_message)
        elif isinstance(polled_event, PlayerTurnEvent):
            # ask player for guess
            print(f"You have guessed so far: {polled_event.current_guessed_word}")
            guess = input("Enter your next character guess: ")
            # send guess to server
            send_event_to_host(PlayerPlayedTurnEvent(guess))
        elif isinstance(polled_event, GameWonEvent):
            print("Congratulations, You WON the game!!! Keep it up. ")
        elif isinstance(polled_event, GameLostEvent):
            print("Unfortunately, You LOST the game!!! Better luck next time. ")
        elif isinstance(polled_event, GameOverEvent):
            print("GAME OVER...!!!")
            break
    server_connection.close()
