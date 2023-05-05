import socket

from events.game_over_event import GameOverEvent
from events.event_base import Event
from events.event_utils import encode_event, decode_event
from events.game_started_event import GameStartedEvent
from events.player_invitation_event import PlayerInvitationEvent
from events.player_invitation_acceptance_event import PlayerInvitationAcceptanceEvent

HOST = 'rahul-badgujar'  # The server's hostname or IP address
PORT = 10001  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('Connecting to the server...')
    s.connect((HOST, PORT))
    print('CONNECTED...')


    def send_event_to_host(event: Event):
        s.sendall(encode_event(event))


    def poll_event_from_host() -> Event:
        received_data = s.recv(1024).decode('utf-8')
        return decode_event(received_data)


    player_name = input("Enter your name: ")
    send_event_to_host(PlayerInvitationAcceptanceEvent(player_name))
    print("Requesting to join the active game...")
    this_hangman_player = None
    while True:
        polled_event = poll_event_from_host()
        if isinstance(polled_event, PlayerInvitationEvent):
            # received playing invitation from game
            # accepting the invitation
            send_event_to_host(PlayerInvitationAcceptanceEvent(player_name))
            print("Successfully joined the game. Game will start once all the players join.")
        elif isinstance(polled_event, GameStartedEvent):
            print("GAME STARTED...!!!")
        elif isinstance(polled_event, GameOverEvent):
            print("GAME OVER...!!!")
            if polled_event.did_won:
                print("Congratulations you won game.")
            else:
                print("Unfortunately, You have lost the game.")
                print(f"Say congratulations to {polled_event.winner_player_name} for winning the game.")
            break
