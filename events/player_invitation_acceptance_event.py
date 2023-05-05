from events.event_base import Event
from events.player_invitation_event import PlayerInvitationEvent


class PlayerInvitationAcceptanceEvent(Event):
    def __init__(self, invitation_event: PlayerInvitationEvent, player_name):
        super().__init__()
        self.invitation_event = invitation_event
        self.player_name = player_name
