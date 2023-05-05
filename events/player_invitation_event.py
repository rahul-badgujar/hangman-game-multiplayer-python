from events.event_base import Event


class PlayerInvitationEvent(Event):
    def __init__(self, proposed_player_id):
        super().__init__()
        self.proposed_player_id = proposed_player_id
